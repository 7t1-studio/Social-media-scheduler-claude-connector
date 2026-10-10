#!/usr/bin/env python3
"""PUT local image/video bytes to presigned URLs from a temporary JSON plan."""
import argparse
import http.client
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit

# So-me Studio presigns path-style URLs on its Cloudflare R2 S3 endpoint
# (<account>.r2.cloudflarestorage.com). Refuse every other destination, so a
# plan can never send local bytes anywhere else.
UPLOAD_HOST_SUFFIX = '.r2.cloudflarestorage.com'

# ISO base media brands that hold a still image; every other brand is video.
IMAGE_BRANDS = {b'avif', b'heic', b'heix', b'heim', b'heis', b'mif1', b'msf1'}


def sniff_media_family(head):
    """Return 'image' or 'video' from the file's leading bytes, else None."""
    if head.startswith((b'\xff\xd8\xff', b'\x89PNG\r\n\x1a\n', b'GIF87a', b'GIF89a',
                        b'BM', b'II*\x00', b'MM\x00*')):
        return 'image'
    if head[:4] == b'RIFF' and head[8:12] == b'WEBP':
        return 'image'
    if head[:4] == b'RIFF' and head[8:12] == b'AVI ':
        return 'video'
    if head[4:8] == b'ftyp':
        return 'image' if head[8:12] in IMAGE_BRANDS else 'video'
    if head.startswith(b'\x1a\x45\xdf\xa3'):  # WebM and Matroska
        return 'video'
    return None


def upload(plan):
    if not isinstance(plan, list) or not 1 <= len(plan) <= 20:
        raise ValueError('Plan must contain 1 to 20 uploads')
    prepared = []
    for item in plan:
        path = Path(item['filePath']).expanduser().resolve(strict=True)
        size = item['size']
        mime = item['mimetype']
        url = urlsplit(item['uploadUrl'])
        if not path.is_file() or type(size) is not int or size <= 0 or path.stat().st_size != size:
            raise ValueError('Local file size must match the presign request')
        if not isinstance(mime, str) or not mime.startswith(('image/', 'video/')) or '\r' in mime or '\n' in mime:
            raise ValueError('Expected an image or video MIME type')
        # Only real media leaves the machine: the bytes must match the declared kind.
        with path.open('rb') as stream:
            family = sniff_media_family(stream.read(16))
        if family is None or not mime.startswith(family + '/'):
            raise ValueError('File content is not the declared image or video type')
        if url.scheme != 'https' or not url.hostname or url.username or url.password or url.fragment:
            raise ValueError('Expected an HTTPS presigned upload URL without credentials or fragment')
        if not url.hostname.lower().endswith(UPLOAD_HOST_SUFFIX) or url.port not in (None, 443):
            raise ValueError('Upload URL is not a So-me Studio storage URL')
        prepared.append((item['fileId'], path, size, mime, url))
    results = []
    for file_id, path, size, mime, url in prepared:
        connection = http.client.HTTPSConnection(url.hostname, 443, timeout=300)
        try:
            target = url.path or '/'
            if url.query:
                target += '?' + url.query
            with path.open('rb') as stream:
                connection.request('PUT', target, body=stream, headers={
                    'Content-Type': mime, 'Content-Length': str(size),
                })
                response = connection.getresponse()
                if not 200 <= response.status < 300:
                    raise RuntimeError(f'Upload failed with HTTP {response.status}; no redirect was followed')
            result = {'fileId': file_id, 'uploaded': True, 'verificationRequired': True}
            results.append(result)
            print(json.dumps(result), flush=True)
        finally:
            connection.close()
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', help='Temporary JSON upload plan; contains signed URLs, keep private')
    args = parser.parse_args()
    try:
        upload(json.loads(Path(args.plan).read_text(encoding='utf-8-sig')))
    except Exception as error:
        # Do not print exception messages that may include signed URLs or local paths.
        # The ValueError and RuntimeError messages above are fixed text, so they are safe.
        reason = f': {error}' if isinstance(error, (ValueError, RuntimeError)) else ''
        print(f'Upload stopped ({type(error).__name__}{reason}). Check file sizes and URL expiry; verify completed file IDs before retrying.', file=sys.stderr)
        sys.exit(1)
