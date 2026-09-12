# So-me Studio MCP Connector

Remote [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) connector for **[So-me Studio](https://so-me.studio)** — schedule, publish, and manage social media content from Claude, ChatGPT, Cursor, and other MCP clients.

This repository holds **public packaging and docs** for directory listings and custom connectors. The live MCP server is hosted separately; there is no NestJS backend here.

## Endpoint

| | |
|---|---|
| **Directory MCP URL** | `https://api.so-me.studio/mcp/directory` (Claude / ChatGPT marketplace — no AI media tools) |
| **Full MCP URL** | `https://api.so-me.studio/mcp` (developers / Cursor — full catalog) |
| **Transport** | Streamable HTTP (`POST`) |
| **Product docs** | [docs.so-me.studio/mcp/overview](https://docs.so-me.studio/mcp/overview) |
| **Website** | [so-me.studio](https://so-me.studio) |
| **Listing copy** | [docs/listing-copy.md](docs/listing-copy.md) · icon [assets/icon.svg](assets/icon.svg) |

## Authentication

| Client | Auth |
|--------|------|
| **Cursor / custom connectors** | `X-API-Key` header with a key in the form `sk_live_...` (Settings → API Access in So-me Studio) |
| **Claude Directory** | OAuth (directory users do not paste API keys) |
| **ChatGPT plugin** | OAuth (coming soon — see [docs/setup-openai.md](docs/setup-openai.md)) |

API / MCP access requires a **Team+** plan (or higher) on so-me.studio. Create an account and connect social destinations in the app before using write tools.

## What you can do

Marketplace-facing tools cover posts, drafts, connected accounts, media library, inbox, analytics, and caption/text AI — without AI image or video generation (directory policy). See [docs/tools.md](docs/tools.md).

Posting also covers multi-post chains, an automatic first comment, and TikTok's required publishing options:

- **Chains** — put the head post in `text` and the posts that follow it in `threadParts`, on X (280 characters per part), Threads (500), Bluesky (300 graphemes), and Mastodon (500) only, at most 24 parts.
- **First comment** — `firstComment` posts one comment under the post right after it publishes, on Facebook, Instagram, X, LinkedIn, LinkedIn Page, Threads, and YouTube. An unsupported target still publishes and returns a `FIRST_COMMENT_UNSUPPORTED` warning. Read `capabilities.firstComment` from `list_accounts` first.
- **TikTok** — never guess the privacy level. Call `get_tiktok_creator_info`, offer only the options it returns, recommend `PUBLIC_TO_EVERYONE`, ask whether comments are allowed, then send the `tiktok` object. A TikTok post without `tiktok.privacyLevel` is rejected.
- **Media** — `validate_post_media` measures pixel size, aspect ratio, codec, and frame rate and returns a `fix` string for each mismatch; `get_media_rules` returns the per-platform table.

## Quick setup

- **Claude Desktop** — [docs/setup-claude.md](docs/setup-claude.md) (Connectors UI or `mcp-remote`)
- **Cursor** — [config/cursor.mcp.json.example](config/cursor.mcp.json.example)
- **Claude custom connector notes** — [config/claude.custom-connector.md](config/claude.custom-connector.md)
- **ChatGPT** — [docs/setup-openai.md](docs/setup-openai.md)

## Privacy

See [PRIVACY.md](PRIVACY.md) and the full policy at [so-me.studio/privacy-policy](https://so-me.studio/privacy-policy).

## License

MIT — see [LICENSE](LICENSE). Copyright © 2026 7t1 Studio / So-me Studio.
