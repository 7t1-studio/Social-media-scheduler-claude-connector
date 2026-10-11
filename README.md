# Social media studio for Claude

Plan, publish, and schedule social media posts from Claude. Social media studio, powered by [So-me Studio](https://so-me.studio), lets Claude draft posts, attach your images and videos, check media against each platform's rules, build thread chains, add an automatic first comment, and publish now or on a schedule to the social accounts connected to your So-me Studio workspace. It works in Claude chat, Cowork, and Claude Code.

This repository is the Claude plugin: one skill that teaches Claude the posting workflow, plus a connector entry for So-me Studio's hosted MCP server.

## What you need

- A So-me Studio account with API/MCP access. Your workspace plan and credits decide what you can do.
- Social accounts already connected in So-me Studio.
- Python 3, only if you want Claude to upload local files for you. You can always pick media that is already in your So-me Studio library instead.

## Use it

1. Add the plugin from the Claude directory (**Customize > Plugins** on claude.ai, or `/plugin` in Claude Code).
2. Connect the **Social media studio** connector. On claude.ai and in Cowork, open the plugin's **Connectors** tab and select **Connect**. In Claude Code, run `/mcp` and sign in. You sign in to So-me Studio in your browser with OAuth; you never paste an API key into Claude.
3. Ask Claude for what you want. Every tool that changes data is marked as such, so Claude asks for your approval before it runs unless you chose to allow it in advance.

Example prompts:

- "Schedule this post on my Mastodon account and my LinkedIn page for next Monday at 9:00 AM UTC: 'New on our blog: 5 ways to plan a week of social posts.' Then show me next week's calendar."
- "Write a three-post X thread with tips for batching a week of social posts, add 'Plan your week at so-me.studio' as the first comment, and save it as a draft. Do not publish it."
- "Check if my video spring-launch.mp4 (MP4, 1080x1920, 2 minutes, 120 MB, H.264, 30 fps) can go out as an Instagram Reel, a TikTok video, and a Bluesky video, and tell me what to change for each one that fails."
- "Find calendar-month.webp in my media library and publish it to Bluesky now with the caption 'Plan a whole month of posts in one calendar.'"
- "Move my Mastodon post next week to Tuesday at 3:00 PM UTC and take the LinkedIn post off the schedule."

## What it can do

The connector exposes 28 tools. The full list and every posting option are in [docs/tools.md](docs/tools.md).

- **Posts and scheduling**: create, edit, schedule, reschedule, unschedule, retry, and delete posts; review the posting calendar and publication status.
- **Drafts**: save, edit, and convert drafts into posts.
- **Media**: search and pick files in your media library, upload new images and videos, and check them against each destination's size, type, duration, dimension, aspect-ratio, codec, and frame-rate rules before anything publishes.
- **Thread chains**: multi-post threads on X, Threads, Bluesky, and Mastodon.
- **First comment**: one automatic comment under the post on Facebook, Instagram, X, LinkedIn, LinkedIn Page, Threads, and YouTube.
- **Platform options**: TikTok privacy and interaction settings chosen by the creator, YouTube visibility, Pinterest boards, and Discord and Slack channels.

It does not cover analytics, inbox replies, team or billing settings, webhooks, Reddit, Google Business Profile, or AI image and video generation.

## What runs and where your data goes

- **The connector** sends Claude's tool calls to So-me Studio's MCP server at `https://api.so-me.studio/mcp/claude` over HTTPS. Each call carries only the arguments Claude passes to the tool, such as post text, schedule times, account IDs, and media file IDs. The server acts as your signed-in user in your own workspace.
- **The upload helper** (`skills/social-posting/scripts/upload_media.py`) runs only when Claude uploads a local file for you. It reads the file you chose and sends its bytes with an HTTP `PUT` to the short-lived presigned URL that So-me Studio returned for its own Cloudflare R2 storage account (`8ceee95d15684ff4afd5e8f0d84e4913.r2.cloudflarestorage.com`). It refuses any other destination, including other R2 accounts, and any port other than 443, and it refuses any file whose leading bytes are not an image or video of the declared kind, so it cannot send documents, keys, or other files. It sends no So-me Studio credentials, follows no redirects, and uses only the Python standard library. Its tests are in `tests/test_upload_media.py`.
- **Publishing** sends your post to the social platforms you choose, through the accounts you connected in So-me Studio.
- The plugin itself stores nothing. The skill tells Claude to delete the temporary upload plan after use. The plugin reads no Claude conversation history, memory, or files other than the media files you ask it to upload.
- The plugin contains no API keys or secrets. Sign-in uses OAuth 2.0 with PKCE.

## Privacy policy

So-me Studio's privacy policy is at [so-me.studio/privacy-policy](https://so-me.studio/privacy-policy). It covers what data So-me Studio collects, how it uses and stores that data, which third parties receive it, how long it is kept, and how to contact us. See also [PRIVACY.md](PRIVACY.md) for the MCP-specific notes.

## Support

- Documentation: [docs.so-me.studio/mcp/overview](https://docs.so-me.studio/mcp/overview)
- Support: [so-me.studio/contact-us](https://so-me.studio/contact-us) or support@so-me.studio
- Terms: [so-me.studio/terms-and-conditions](https://so-me.studio/terms-and-conditions)

## For developers

The plugin and the Claude directory connector use the posting endpoint `https://api.so-me.studio/mcp/claude` with OAuth. Developers who need the full So-me Studio tool catalog can connect `https://api.so-me.studio/mcp` with an API key instead; see [docs/setup-claude.md](docs/setup-claude.md) and [config/](config/).

| Path | Purpose |
|------|---------|
| `.claude-plugin/plugin.json` | Plugin manifest and directory listing fields |
| `.mcp.json` | Connector entry for the hosted MCP server |
| `skills/social-posting/` | The posting skill and its upload helper |
| `assets/` | Plugin icon |
| `docs/` | Tool reference, setup guides, listing copy, and the submission checklist |

## License

MIT. See [LICENSE](LICENSE). Copyright © 2026 7t1 Studio / So-me Studio.
