# Claude connector — auth notes

## Endpoints

| Use | URL | Auth |
|-----|-----|------|
| Claude plugin, Claude directory connector, custom connector by URL | `https://api.so-me.studio/mcp/claude` | OAuth 2.0 with PKCE |
| Developers (full catalog, includes tools the directory does not allow) | `https://api.so-me.studio/mcp` | `X-API-Key` header |

Transport: **Streamable HTTP** (`POST` only).

## OAuth on `/mcp/claude`

- An unauthenticated request gets HTTP `401` with `WWW-Authenticate: Bearer resource_metadata="https://api.so-me.studio/.well-known/oauth-protected-resource/mcp/claude"`. That starts Claude's sign-in.
- The authorization server is `https://api.so-me.studio`. Its metadata advertises dynamic client registration and client ID metadata documents, S256 PKCE, and the `mcp` scope.
- Accepted redirects: `https://claude.ai/api/mcp/auth_callback` for claude.ai, the desktop and mobile apps, and Cowork; loopback `http://localhost:<port>/callback` and `http://127.0.0.1:<port>/callback` on any port for Claude Code.
- Tool calls run as the signed-in user in that user's workspace. Posting and other writes stay gated by the workspace plan, credits, and connected accounts.
- Leave the OAuth client ID and secret fields empty when you add the connector by URL.

## API key on `/mcp` (developers)

1. In So-me Studio: **Settings > API Access** > create a key (`sk_live_...`).
2. Send it as the `X-API-Key` header. Claude's **Request headers** option is a beta for a limited set of organizations; otherwise use `mcp-remote` as shown in [docs/setup-claude.md](../docs/setup-claude.md), with the header written as `X-API-Key:sk_live_...` (no space after the colon).

## YouTube first comment needs a reconnect

`firstComment` on YouTube uses `commentThreads.insert`, which needs the `https://www.googleapis.com/auth/youtube.force-ssl` permission. Uploading does not. Every YouTube account connected before that permission was added must reconnect in So-me Studio. Until it does, the post publishes and the comment fails; `firstCommentError` on the post says exactly this. This is a social-account permission in So-me Studio, not a connector setting: the connector's own sign-in is unchanged.

## Security tips

- Prefer OAuth. Use a dedicated API key per developer client, and revoke unused keys promptly.
- Never commit real `sk_live_` values to git or paste them in a chat.
- Revoke the Claude connection at any time in So-me Studio settings or by disconnecting the connector in Claude.
