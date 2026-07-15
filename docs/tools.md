# Marketplace tool catalog (summary)

This is a **directory-safe** summary of So-me Studio MCP capabilities for Claude / ChatGPT listings. The live server exposes a larger catalog for API-key clients; **AI image and video generation** (and related UGC media tools) are **excluded** from marketplace/directory surfaces.

Full product reference: https://docs.so-me.studio/mcp/tools

**Auth:** OAuth (directory) or `X-API-Key: sk_live_...` (custom). **Plan:** Team+ for API access. Endpoint: `https://api.so-me.studio/mcp`.

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
