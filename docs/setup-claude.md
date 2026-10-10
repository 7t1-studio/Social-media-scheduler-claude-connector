# Connect Claude to Social media studio

Social media studio (powered by So-me Studio) runs as a remote **Streamable HTTP** MCP server.

| Use | URL | Sign-in |
|-----|-----|---------|
| Claude plugin and Claude directory connector | `https://api.so-me.studio/mcp/claude` | OAuth in the browser |
| Developers who need the full tool catalog | `https://api.so-me.studio/mcp` | `X-API-Key` header |

`/mcp/claude` carries the 28 posting tools listed in [tools.md](tools.md). You need a So-me Studio account with API/MCP access and social accounts connected in So-me Studio.

## Option 1: Install from the Claude directory

1. On claude.ai or in the desktop app, open **Customize > Plugins**, find **Social media studio**, and add it. In Claude Code, run `/plugin` and add it from the directory.
2. Connect the plugin's connector: on claude.ai and in Cowork from the plugin's **Connectors** tab, in Claude Code with `/mcp`.
3. Sign in to So-me Studio in the browser window and approve the connection.
4. Ask Claude to list your connected accounts or to draft a post.

On Team and Enterprise plans, an Owner may need to add the connector for the organization first; members then connect with their own So-me Studio account.

## Option 2: Add the connector by URL

Use this before the directory listing is live, or without the plugin's skill.

1. Open **Customize > Connectors** and select **Add custom connector**. You can also open this link, which fills in the form: [add Social media studio](https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Social%20media%20studio&connectorUrl=https%3A%2F%2Fapi.so-me.studio%2Fmcp%2Fclaude).
2. Set the name to `Social media studio` and the URL to `https://api.so-me.studio/mcp/claude`. Leave the OAuth client ID and secret empty.
3. Select **Connect**, sign in to So-me Studio, and approve.
4. In a chat, turn the connector on from **+ > Connectors**.

## Option 3: Claude Code

Load the whole plugin (skill and connector) from a local copy of this repository:

```bash
claude --plugin-dir ./Social-media-scheduler-claude-connector
```

Or add only the connector:

```bash
claude mcp add --transport http so-me-studio https://api.so-me.studio/mcp/claude
```

Then run `/mcp`, select the server, and sign in. Claude Code opens the browser and receives the sign-in on a local `localhost` port.

## Option 4: Developers — full catalog with an API key

The full catalog at `https://api.so-me.studio/mcp` includes tools that the directory does not allow, such as AI image and video generation, so it is not offered through the plugin. It authenticates with an API key (`sk_live_...`) from **Settings > API Access** in So-me Studio.

Claude's **Request headers** option for custom connectors is a beta for a limited set of organizations. Everyone else can bridge the server with [`mcp-remote`](https://www.npmjs.com/package/mcp-remote) in `claude_desktop_config.json` (**Settings > Developer > Edit Config**):

```json
{
  "mcpServers": {
    "so-me-studio-full": {
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

Do not put a space after the colon in the `--header` value. Fully quit and reopen Claude Desktop after you save the file. See also [../config/claude.custom-connector.md](../config/claude.custom-connector.md).

## Troubleshooting

### The connector shows Connect or Reconnect

Sign-in did not finish. Select **Connect** again and complete the So-me Studio sign-in and approval in the browser. Allow pop-ups for claude.ai if the window does not open.

### A tool says the workspace has no API/MCP access or no credits

The So-me Studio workspace plan or credit balance blocks the call. Check the workspace in So-me Studio.

### 401 or "Missing X-API-Key header" on `/mcp`

Only the full-catalog URL uses API keys. The header name must be exactly `X-API-Key`, and the value must be an active key that starts with `sk_live_`.

### 405 Method Not Allowed

The server runs in stateless Streamable HTTP mode and accepts only `POST`. Claude's connectors and `mcp-remote` both use Streamable HTTP; no SSE setup is needed.

## More

- Product docs: https://docs.so-me.studio/mcp/overview
- Claude Desktop guide: https://docs.so-me.studio/mcp/claude-desktop
