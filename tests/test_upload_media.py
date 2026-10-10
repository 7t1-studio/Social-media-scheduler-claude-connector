import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

spec = importlib.util.spec_from_file_location(
    'upload_media', Path(__file__).parents[1] / 'skills/social-posting/scripts/upload_media.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

PNG = b'\x89PNG\r\n\x1a\n' + b'\x00' * 24
MP4 = b'\x00\x00\x00\x18ftypmp42' + b'\x00' * 24
UPLOAD_URL = 'https://0123abcd.r2.cloudflarestorage.com/bucket/object?X-Amz-Signature=private'


class UploadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.file = self.write('photo.png', PNG)
        self.plan = [{
            'filePath': str(self.file), 'fileId': 'media-1', 'uploadUrl': UPLOAD_URL,
            'mimetype': 'image/png', 'size': self.file.stat().st_size,
        }]

    def write(self, name, data):
        path = Path(self.temp.name) / name
        path.write_bytes(data)
        return path

    def assert_rejected_before_upload(self, plan):
        with patch.object(module.http.client, 'HTTPSConnection') as connection:
            with self.assertRaises(ValueError):
                module.upload(plan)
            connection.assert_not_called()

    def test_puts_real_bytes_with_exact_headers_and_no_oauth(self):
        connection = Mock()
        captured = {}
        def request(method, target, body, headers):
            captured.update(method=method, target=target, body=body.read(), headers=headers)
        connection.request.side_effect = request
        connection.getresponse.return_value.status = 200
        with patch.object(module.http.client, 'HTTPSConnection', return_value=connection) as cls, \
                patch('builtins.print') as output:
            module.upload(self.plan)
        cls.assert_called_once_with('0123abcd.r2.cloudflarestorage.com', 443, timeout=300)
        self.assertEqual(captured['method'], 'PUT')
        self.assertEqual(captured['target'], '/bucket/object?X-Amz-Signature=private')
        self.assertEqual(captured['body'], self.file.read_bytes())
        self.assertEqual(captured['headers'], {'Content-Type': 'image/png', 'Content-Length': str(len(PNG))})
        self.assertNotIn('private', str(output.call_args))
        self.assertTrue(json.loads(output.call_args.args[0])['verificationRequired'])
        connection.close.assert_called_once()

    def test_uploads_a_video(self):
        video = self.write('clip.mp4', MP4)
        self.plan[0].update(filePath=str(video), mimetype='video/mp4', size=len(MP4))
        connection = Mock()
        connection.getresponse.return_value.status = 200
        with patch.object(module.http.client, 'HTTPSConnection', return_value=connection), patch('builtins.print'):
            self.assertEqual(len(module.upload(self.plan)), 1)

    def test_validates_all_file_sizes_before_uploading_anything(self):
        self.plan.append({**self.plan[0], 'size': 999})
        self.assert_rejected_before_upload(self.plan)

    def test_does_not_follow_upload_redirects(self):
        connection = Mock()
        connection.getresponse.return_value.status = 302
        with patch.object(module.http.client, 'HTTPSConnection', return_value=connection):
            with self.assertRaises(RuntimeError):
                module.upload(self.plan)
        connection.request.assert_called_once()
        connection.close.assert_called_once()

    def test_rejects_plaintext_upload_url(self):
        self.plan[0]['uploadUrl'] = UPLOAD_URL.replace('https://', 'http://')
        self.assert_rejected_before_upload(self.plan)

    def test_rejects_a_host_that_is_not_so_me_studio_storage(self):
        for url in ('https://attacker.example/upload',
                    'https://r2.cloudflarestorage.com.attacker.example/x',
                    'https://evilr2.cloudflarestorage.com/x'):
            with self.subTest(url=url):
                self.plan[0]['uploadUrl'] = url
                self.assert_rejected_before_upload(self.plan)

    def test_rejects_a_port_other_than_443(self):
        self.plan[0]['uploadUrl'] = UPLOAD_URL.replace('.com/', '.com:8443/')
        self.assert_rejected_before_upload(self.plan)

    def test_rejects_a_file_that_is_not_media(self):
        secret = self.write('id_ed25519', b'-----BEGIN OPENSSH PRIVATE KEY-----\n')
        self.plan[0].update(filePath=str(secret), size=secret.stat().st_size)
        self.assert_rejected_before_upload(self.plan)

    def test_rejects_content_that_does_not_match_the_declared_type(self):
        video = self.write('clip.mp4', MP4)
        self.plan[0].update(filePath=str(video), mimetype='image/png', size=len(MP4))
        self.assert_rejected_before_upload(self.plan)


if __name__ == '__main__':
    unittest.main()
