# Tool reference — Claude connector and plugin

The Claude directory connector and the Claude plugin both use the posting endpoint:

```
https://api.so-me.studio/mcp/claude
```

It carries the same 28 tools as the `/mcp/posting` endpoint that the ChatGPT and Grok plugins use, and it signs in with OAuth. The server enforces this allowlist for both `tools/list` and `tools/call`. Every tool has a `title`; read tools carry `readOnlyHint: true` and every tool that changes data carries `destructiveHint: true`, so Claude asks for approval before it runs a write.

Not on this endpoint: analytics, inbox, post comments, approvals, team, billing, account administration, webhooks, Reddit, Google Business Profile, and every AI image or video tool. The developer endpoint with the full catalog is described in [setup-claude.md](setup-claude.md). Full product reference: https://docs.so-me.studio/mcp/tools

## Tools

| Group | Tool | Title | Kind |
|-------|------|-------|------|
| Posts | `list_posts` | List Posts | Read |
| Posts | `get_post` | Get Post | Read |
| Posts | `get_calendar_posts` | Get Calendar Posts | Read |
| Posts | `create_post` | Create Post | Write |
| Posts | `update_post` | Update Post | Write |
| Posts | `schedule_post` | Schedule Post | Write |
| Posts | `unschedule_post` | Unschedule Post | Write |
| Posts | `retry_post` | Retry Post | Write |
| Posts | `delete_post` | Delete Post | Write |
| Drafts | `list_drafts` | List Drafts | Read |
| Drafts | `get_draft` | Get Draft | Read |
| Drafts | `create_draft` | Create Draft | Write |
| Drafts | `update_draft` | Update Draft | Write |
| Drafts | `convert_draft` | Convert Draft | Write |
| Drafts | `delete_draft` | Delete Draft | Write |
| Accounts | `list_accounts` | List Accounts | Read |
| Accounts | `get_account` | Get Account | Read |
| Media | `list_media` | List Media | Read |
| Media | `search_media` | Search Media | Read |
| Media | `get_media_file` | Get Media File | Read |
| Media | `list_media_folders` | List Media Folders | Read |
| Media | `presign_media_upload` | Presign Media Upload | Write |
| Media checks | `validate_post_media` | Check Media Compatibility | Read |
| Media checks | `get_media_rules` | Get Media Rules | Read |
| Destinations | `list_pinterest_boards` | List Pinterest Boards | Read |
| Destinations | `list_discord_channels` | List Discord Channels | Read |
| Destinations | `list_slack_channels` | List Slack Channels | Read |
| Destinations | `get_tiktok_creator_info` | Get Tiktok Creator Info | Read |

`list_accounts` and `get_account` return a per-account `capabilities` object (`firstComment`, `firstCommentMaxLength`, `threads`, `threadPartMaxLength`). Read it before you promise a first comment or a chain.

`get_tiktok_creator_info` is mandatory before every TikTok post: its response carries `requiresPrivacyLevel: true`, the normalized `privacyLevelOptions` list, and `comment_disabled`, `duet_disabled` and `stitch_disabled`, which say the creator turned that interaction off for the whole account.

`presign_media_upload` reserves library entries and returns one presigned upload URL per file; the bytes go to that URL with an HTTP `PUT`, and `get_media_file` with `verifyUpload: true` confirms the upload before the file ID is used in a post.

## Posting options on the write tools

`create_post`, `update_post`, `schedule_post`, `create_draft` and `update_draft` take three top-level fields beside `text`, `fileIds` and `scheduledAt`. `convert_draft` takes `tiktok` as well. They are fields, not tools.

| Field | Type | Purpose |
|-------|------|---------|
| `threadParts` | array | The posts that follow the head post, in order |
| `firstComment` | string | One comment posted under the post right after it publishes |
| `tiktok` | object | The publishing options TikTok requires |

**`threadParts` — chains.** `text` is the head post and `threadParts[0]` is the FIRST REPLY, so a three-post chain is `text` plus two thread parts. Each part is `{ text, fileIds }`; a plain string is read as `{ text }`, and a part needs `text`, `fileIds`, or both. Omit the field for a single post; send an empty array (`[]`) to clear an existing chain.

| Platform | Text per part | Media per part | Parts |
|----------|---------------|----------------|-------|
| `TWITTER` | 280 characters | 4 | 24 |
| `THREADS` | 500 characters | 20 | 24 |
| `BLUESKY` | 300 **graphemes** | 4 | 24 |
| `MASTODON` | 500 characters | 4 | 24 |

Bluesky counts graphemes, so one emoji is one unit. Every other target rejects `threadParts` with a 400 that names the target and the supported list; put the whole message in `text` instead. Publishing past the head is best effort: a failed part leaves the head live, the ids that published stay on `metaData.threadPartIds`, and `metaData.threadPartWarning` says how many published and why the chain stopped. Report that warning; never republish the head.

**`firstComment`.** One string, usually hashtags or a link kept out of the caption. Supported on Facebook, Instagram, X, LinkedIn, LinkedIn Page, Threads and YouTube only. Limits: X 280, Threads 500, LinkedIn and LinkedIn Page 1250, Instagram 2200, Facebook 8000, YouTube 10000 characters. Over the limit is a 400. Omit the field to leave an existing comment untouched; send an empty string to clear it.

An unsupported target is NOT rejected. The post publishes there without the comment and the response carries a warning:

```json
{ "warnings": [ { "code": "FIRST_COMMENT_UNSUPPORTED", "platforms": ["TIKTOK"] } ] }
```

Check support before promising the comment: `list_accounts` and `get_account` return a per-account `capabilities` object — `firstComment`, `firstCommentMaxLength`, `threads` and `threadPartMaxLength`. With a chain the comment goes under the LAST part, not the head; of the four chain platforms only X and Threads also take a first comment. Delivery is a separate job, so read `firstCommentStatus` (`pending`, `posted`, `failed`, `skipped`) on the post before calling the comment live; `firstCommentError` explains a failure. A YouTube account connected before the comment permission was added must reconnect.

**`tiktok`.** TikTok rejects every post that carries no privacy level, and only the creator may choose one, so never guess it. Call `get_tiktok_creator_info` for the target account, show the user ONLY the values it returns in `privacy_level_options` (a private account cannot choose `PUBLIC_TO_EVERYONE`), recommend `PUBLIC_TO_EVERYONE`, ask whether comments are allowed, then send `{ privacyLevel, allowComments, allowDuet, allowStitch }`. `privacyLevel` is one of `PUBLIC_TO_EVERYONE`, `MUTUAL_FOLLOW_FRIENDS`, `FOLLOWER_OF_CREATOR`, `SELF_ONLY`; the three booleans default to `true`. `brandContentToggle` and `brandOrganicToggle` default to `false` — set them only when the user says so.

A TikTok post without `tiktok.privacyLevel` is rejected with `TIKTOK_PRIVACY_LEVEL_REQUIRED`, and that payload lists the allowed values in `privacyLevelOptions`. A level the creator cannot use returns `TIKTOK_PRIVACY_LEVEL_NOT_ALLOWED`. A creator who disabled comments, duet or stitch account-wide forces the matching option off, and the result carries a `TIKTOK_SETTING_FORCED` warning to repeat to the user. Any non-TikTok target rejects the field. A draft stores the options unvalidated; `convert_draft` validates them and accepts a `tiktok` object of its own.

## Media validation

Call `validate_post_media` before `create_post` or `schedule_post` whenever you generated, edited or picked the media yourself. Send `targets` (each `{ socialMedia, postType }`) with either library `fileIds` or local `files` metadata, never both. Library files are measured from their own bytes, so the report compares the measured width, height, duration, video codec and frame rate against each destination's rules and returns, per destination, the status, the `measured` values, the configured `limits`, and one issue per mismatch.

Four issue codes report measured properties: `DIMENSIONS_INVALID`, `ASPECT_RATIO_INVALID`, `CODEC_UNSUPPORTED` and `FRAME_RATE_INVALID`. Each carries `measured`, `required` and a `fix` string naming the exact change, plus `suggestedDimensions` where a crop applies:

```json
{
  "code": "ASPECT_RATIO_INVALID",
  "fix": "INSTAGRAM image requires an aspect ratio between 4:5 and 1.91:1; file is 2560x1080 (2.37:1). Crop to 2062x1080 (crop the sides) or 1080x1080 (centre square crop).",
  "measured": { "width": 2560, "height": 1080, "aspectRatioLabel": "2.37:1" },
  "required": { "minAspectRatioLabel": "4:5", "maxAspectRatioLabel": "1.91:1" }
}
```

When you produced the media, apply the `fix` (crop or resize) and validate again; continue only after it passes. When the user supplied it, show the `fix` and let the user choose. For a file that is not uploaded yet, send the measured `width`, `height`, `durationSeconds`, `videoCodec` and `frameRate` in `files`; every property you omit becomes a `needs_review` warning instead of a pass. Never guess a measurement. `get_media_rules` returns the whole table — accepted MIME types, byte caps, attachment counts, duration, pixel bounds, aspect-ratio ranges, video codecs and frame-rate caps, per platform and post type — so use it to generate media at the right size in the first place. These are So-me Studio configured limits, not a live mirror of each platform API.
