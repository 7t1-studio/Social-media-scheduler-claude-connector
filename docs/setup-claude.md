# Connect Claude to So-me Studio MCP

So-me Studio’s MCP server is a remote **Streamable HTTP** endpoint at `https://api.so-me.studio/mcp`.

**Claude Directory** listings authenticate with **OAuth** (no pasted API key). For **custom connectors** and local setups, use an API key (`sk_live_...`) from **Settings → API Access** (Team+ plan). See also [config/claude.custom-connector.md](../config/claude.custom-connector.md).

You can connect Claude Desktop through the built-in **Connectors** UI or by bridging with `mcp-remote` in `claude_desktop_config.json`.

## Option 1: Connectors UI (recommended)

1. In Claude Desktop go to **Settings → Connectors → Add custom connector**.
2. Enter the server details:

   | Field | Value |
   |-------|-------|
   | Name | `so-me-studio` |
   | Remote MCP server URL | `https://api.so-me.studio/mcp` |

3. Provide the API key: add an HTTP header named `X-API-Key` with your key (`sk_live_...`) as the value, then save.
4. Open a new conversation. So-me Studio tools appear in the tools menu — ask Claude to list your posts or create a new one.

If you install So-me Studio from the **Claude Connectors Directory**, follow the in-product OAuth flow instead of pasting `X-API-Key`.

## Option 2: mcp-remote bridge

If your build of Claude Desktop edits servers through the config file, bridge the remote HTTP server with [`mcp-remote`](https://www.npmjs.com/package/mcp-remote). Classic `claude_desktop_config.json` only launches local (stdio) commands, so the URL and header are passed to the bridge.

1. Open the config file via **Settings → Developer → Edit Config**, or open it directly:

   | OS | Path |
   |----|------|
   | macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
   | Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

2. Add the MCP server:

```json
{
  "mcpServers": {
    "so-me-studio": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://api.so-me.studio/mcp",
        "--header",
        "X-API-Key:<YOUR_SO_ME_API_KEY>"
      ]
    }
  }
}
```

**Important:** Do not put a space after the colon in the `--header` value. `mcp-remote` splits the header on the first `:` and a leading space in the value will be sent literally.

3. Save the file and fully quit and reopen Claude Desktop.
4. Verify by asking Claude to list your posts or create a new one.

## Troubleshooting

### 401 / Missing X-API-Key header

The header name must be exactly `X-API-Key` and the value must be an active key beginning with `sk_live_`. With the `mcp-remote` bridge, double-check there is no stray space after the colon.

### 405 Method Not Allowed

The So-me Studio server runs in stateless Streamable HTTP mode and only accepts `POST` requests. `mcp-remote` and the Connectors UI both speak Streamable HTTP; no SSE configuration is required.

## More docs

- Product overview: https://docs.so-me.studio/mcp/overview
- Claude Desktop guide: https://docs.so-me.studio/mcp/claude-desktop
