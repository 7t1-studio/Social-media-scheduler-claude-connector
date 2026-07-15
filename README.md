# So-me Studio MCP Connector

Remote [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) connector for **[So-me Studio](https://so-me.studio)** — schedule, publish, and manage social media content from Claude, ChatGPT, Cursor, and other MCP clients.

This repository holds **public packaging and docs** for directory listings and custom connectors. The live MCP server is hosted separately; there is no NestJS backend here.

## Endpoint

| | |
|---|---|
| **MCP URL** | `https://api.so-me.studio/mcp` |
| **Transport** | Streamable HTTP (`POST`) |
| **Product docs** | [docs.so-me.studio/mcp/overview](https://docs.so-me.studio/mcp/overview) |
| **Website** | [so-me.studio](https://so-me.studio) |

## Authentication

| Client | Auth |
|--------|------|
| **Cursor / custom connectors** | `X-API-Key` header with a key in the form `sk_live_...` (Settings → API Access in So-me Studio) |
| **Claude Directory** | OAuth (directory users do not paste API keys) |
| **ChatGPT plugin** | OAuth (coming soon — see [docs/setup-openai.md](docs/setup-openai.md)) |

API / MCP access requires a **Team+** plan (or higher) on so-me.studio. Create an account and connect social destinations in the app before using write tools.

## What you can do

Marketplace-facing tools cover posts, drafts, connected accounts, media library, inbox, analytics, and caption/text AI — without AI image or video generation (directory policy). See [docs/tools.md](docs/tools.md).

## Quick setup

- **Claude Desktop** — [docs/setup-claude.md](docs/setup-claude.md) (Connectors UI or `mcp-remote`)
- **Cursor** — [config/cursor.mcp.json.example](config/cursor.mcp.json.example)
- **Claude custom connector notes** — [config/claude.custom-connector.md](config/claude.custom-connector.md)
- **ChatGPT** — [docs/setup-openai.md](docs/setup-openai.md)

## Privacy

See [PRIVACY.md](PRIVACY.md) and the full policy at [so-me.studio/privacy-policy](https://so-me.studio/privacy-policy).

## License

MIT — see [LICENSE](LICENSE). Copyright © 2026 7t1 Studio / So-me Studio.
