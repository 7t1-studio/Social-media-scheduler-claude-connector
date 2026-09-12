# Marketplace tool catalog (summary)

This is a **directory-safe** summary of So-me Studio MCP capabilities for Claude / ChatGPT listings. The live server exposes a larger catalog for API-key clients; **AI image and video generation** (and related UGC media tools) are **excluded** from marketplace/directory surfaces.

Full product reference: https://docs.so-me.studio/mcp/tools

**Auth:** OAuth (directory) or `X-API-Key: sk_live_...` (custom). **Plan:** Team+ for API access. Endpoint: `https://api.so-me.studio/mcp`.

This connector uses the full `/mcp` endpoint, so every tool below is available to it. `validate_post_media`, `get_media_rules` and `get_tiktok_creator_info` are also on the restricted `/mcp/posting` profile that the Grok and ChatGPT plugins use, which carries 31 tools. `threadParts`, `firstComment` and `tiktok` are fields on the existing write tools, so they are available wherever those tools are.

## Excluded from marketplace

These tools are **not** part of the directory submission surface:

- `generate_image`, `list_generated_images`, `get_generated_image`, `delete_generated_image`, `list_ai_image_providers`
- `generate_video`, `list_videos`, `get_video`, `delete_video`, `list_avatars`, `list_sounds`, `get_sound_genres`, `list_ai_video_providers`
- Compound flows that depend on AI media (e.g. image/video legs of `generate_and_schedule` when used for media generation)

Caption / text AI (`generate_caption`, `generate_content`, `generate_hook_suggestions`) remain allowed.

---

## Posts

| Tool | Description |
|------|-------------|
| `list_posts` | List scheduled/published posts |
| `get_post` | Get a post by ID |
| `create_post` | Create a post |
| `update_post` | Update a post |
| `schedule_post` | Schedule a post |
| `unschedule_post` | Unschedule a post |
| `delete_post` | Delete a post |
| `retry_post` | Retry a failed post |
| `resubmit_post` | Resubmit a rejected post |
| `bulk_delete_posts` | Delete multiple posts |
| `get_calendar_posts` | Posts in a date range |

### Posting options on the write tools

`create_post`, `update_post`, `schedule_post`, `create_draft` and `update_draft` take three top-level fields beside `text`, `fileIds` and `scheduledAt`. `convert_draft` takes `tiktok` as well. They are fields, not tools.

| Field | Type | Purpose |
|-------|------|---------|
| `threadParts` | array | The posts that follow the head post, in order |
| `firstComment` | string | One comment posted under the post right after it publishes |
| `tiktok` | object | The publishing options TikTok requires |

**`threadParts` — chains.** `text` is the head post and `threadParts[0]` is the FIRST REPLY, so a three-post chain is `text` plus two thread parts. Each part is `{ text, fileIds }`; a plain string is read as `{ text }`, and a part needs `text`, `fileIds`, or both. Omit the field for a single post; pass `[]` to clear an existing chain.

| Platform | Text per part | Media per part | Parts |
|----------|---------------|----------------|-------|
| `TWITTER` | 280 characters | 4 | 24 |
| `THREADS` | 500 characters | 20 | 24 |
| `BLUESKY` | 300 **graphemes** | 4 | 24 |
| `MASTODON` | 500 characters | 4 | 24 |

Bluesky counts graphemes, so one emoji is one unit. Every other target rejects `threadParts` with a 400 that names the target and the supported list; put the whole message in `text` instead. Publishing past the head is best effort: a failed part leaves the head live, the ids that published stay on `metaData.threadPartIds`, and `metaData.threadPartWarning` says how many published and why the chain stopped. Report that warning; never republish the head.

**`firstComment`.** One string, usually hashtags or a link kept out of the caption. Supported on Facebook, Instagram, X, LinkedIn, LinkedIn Page, Threads and YouTube only. Limits: X 280, Threads 500, LinkedIn and LinkedIn Page 1250, Instagram 2200, Facebook 8000, YouTube 10000 characters. Over the limit is a 400. Omit the field to leave an existing comment untouched; pass `""` to clear it.

An unsupported target is NOT rejected. The post publishes there without the comment and the response carries a warning:

```json
{ "warnings": [ { "code": "FIRST_COMMENT_UNSUPPORTED", "platforms": ["TIKTOK"] } ] }
```

Check support before promising the comment: `list_accounts` and `get_account` return a per-account `capabilities` object — `firstComment`, `firstCommentMaxLength`, `threads` and `threadPartMaxLength`. With a chain the comment goes under the LAST part, not the head; of the four chain platforms only X and Threads also take a first comment. Delivery is a separate job, so read `firstCommentStatus` (`pending`, `posted`, `failed`, `skipped`) on the post before calling the comment live; `firstCommentError` explains a failure. A YouTube account connected before the comment permission was added must reconnect.

**`tiktok`.** TikTok rejects every post that carries no privacy level, and only the creator may choose one, so never guess it. Call `get_tiktok_creator_info` for the target account, show the user ONLY the values it returns in `privacy_level_options` (a private account cannot choose `PUBLIC_TO_EVERYONE`), recommend `PUBLIC_TO_EVERYONE`, ask whether comments are allowed, then send `{ privacyLevel, allowComments, allowDuet, allowStitch }`. `privacyLevel` is one of `PUBLIC_TO_EVERYONE`, `MUTUAL_FOLLOW_FRIENDS`, `FOLLOWER_OF_CREATOR`, `SELF_ONLY`; the three booleans default to `true`. `brandContentToggle` and `brandOrganicToggle` default to `false` — set them only when the user says so.

A TikTok post without `tiktok.privacyLevel` is rejected with `TIKTOK_PRIVACY_LEVEL_REQUIRED`, and that payload lists the allowed values in `privacyLevelOptions`. A level the creator cannot use returns `TIKTOK_PRIVACY_LEVEL_NOT_ALLOWED`. A creator who disabled comments, duet or stitch account-wide forces the matching option off, and the result carries a `TIKTOK_SETTING_FORCED` warning to repeat to the user. Any non-TikTok target rejects the field. A draft stores the options unvalidated; `convert_draft` validates them and accepts a `tiktok` object of its own.

## Post comments

| Tool | Description |
|------|-------------|
| `list_post_comments` | List comments on a post |
| `add_post_comment` | Add a comment |
| `update_post_comment` | Update a comment |
| `delete_post_comment` | Delete a comment |
| `mark_comments_as_read` | Mark comments read |

## Drafts

| Tool | Description |
|------|-------------|
| `list_drafts` | List drafts |
| `get_draft` | Get a draft |
| `create_draft` | Create a draft |
| `update_draft` | Update a draft |
| `delete_draft` | Delete a draft |
| `convert_draft` | Convert draft to a post |

## Accounts

| Tool | Description |
|------|-------------|
| `list_accounts` | List connected social accounts |
| `get_account` | Account details |
| `disconnect_account` | Disconnect an account |

## Media library

| Tool | Description |
|------|-------------|
| `list_media` | List media files |
| `search_media` | Search media |
| `get_media_file` | Get a media file |
| `delete_media` | Delete media |
| `bulk_delete_media` | Bulk delete |
| `list_media_folders` | List folders |
| `create_media_folder` | Create folder |
| `delete_media_folder` | Delete folder |
| `move_media_file` / `move_media_folder` | Move items |
| `rename_media_file` / `rename_media_folder` | Rename items |
| `presign_media_upload` | Presigned upload URL |
| `validate_post_media` | Check media against every requested destination |
| `get_media_rules` | The per-platform media rules table |

### Media validation

Call `validate_post_media` before `create_post` or `schedule_post` whenever you generated, edited or picked the media yourself. Pass `targets` (each `{ socialMedia, postType }`) with either library `fileIds` or local `files` metadata, never both. Library files are measured from their own bytes, so the report compares the measured width, height, duration, video codec and frame rate against each destination's rules and returns, per destination, the status, the `measured` values, the configured `limits`, and one issue per mismatch.

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

## Inbox & engagement

| Tool | Description |
|------|-------------|
| `list_conversations` | List inbox conversations |
| `get_messages` | Messages in a conversation |
| `reply_to_conversation` | Reply |
| `update_conversation` | Update conversation |
| `delete_conversation` | Delete conversation |
| `edit_inbox_message` / `delete_inbox_message` / `hide_inbox_message` | Message actions |
| `list_saved_replies` / `create_saved_reply` / `update_saved_reply` / `delete_saved_reply` / `get_saved_reply` | Saved replies |
| `preview_bulk_reply` / `create_bulk_reply` | Bulk reply |
| `subscribe_inbox` / `unsubscribe_inbox` | Inbox subscription |

## Approvals

| Tool | Description |
|------|-------------|
| `list_approvals` | Pending approvals |
| `approve_post` / `reject_post` | Approve or reject |

## Analytics & best time

| Tool | Description |
|------|-------------|
| `get_analytics_summary` | Workspace analytics summary |
| `get_platform_analytics` | Per-platform analytics |
| `get_post_analytics` | Single-post analytics |
| Platform helpers | e.g. `get_facebook_analytics`, `get_instagram_analytics`, `get_linkedin_analytics`, `get_youtube_analytics`, `get_twitter_analytics`, `get_tiktok_analytics`, `get_pinterest_analytics`, and related post/media breakdowns |
| `get_best_time_recommendations` / `get_best_time_recommendation` / `recompute_best_time_recommendation` | Best time to post |

## Destination lookups

| Tool | Description |
|------|-------------|
| `list_pinterest_boards` | Pinterest boards |
| `list_reddit_subreddits` / `list_reddit_flairs` | Reddit communities and flairs |
| `list_gmb_locations` | Google Business locations |
| `list_discord_channels` / `list_slack_channels` | Discord and Slack channels |
| `get_tiktok_creator_info` | TikTok creator limits and allowed privacy levels |

`get_tiktok_creator_info` is mandatory before every TikTok post: its response carries `requiresPrivacyLevel: true`, the normalized `privacyLevelOptions` list, and `comment_disabled`, `duet_disabled` and `stitch_disabled`, which say the creator turned that interaction off for the whole account.

## Captions & text AI

| Tool | Description |
|------|-------------|
| `generate_caption` | Generate a caption |
| `generate_content` | Generate text content |
| `generate_hook_suggestions` | Hook suggestions |
| `get_ai_history` | Recent AI text history |
| `get_ai_credits` | Remaining AI credits |

## Templates, biolinks, WhatsApp, team, webhooks, support

Also available on the hosted MCP (subject to plan and marketplace filter): post templates, biolink CRUD/analytics, WhatsApp templates, team invite/role tools, webhook subscriptions/deliveries, help-desk tickets, notifications, knowledge docs, Canva export helpers, billing/usage reads, API key management, and MCP introspection (`list_mcp_tools`, `get_mcp_usage`).

Exact `tools/list` for a given client may differ between the full `/mcp` surface and a filtered directory URL once marketplace profiles are enabled.
