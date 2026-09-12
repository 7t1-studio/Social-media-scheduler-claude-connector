# Claude custom connector — auth notes

## Remote URL

```
https://api.so-me.studio/mcp
```

Transport: **Streamable HTTP** (`POST` only).

## Custom connector / developer setup — API key

1. In So-me Studio (Team+): **Settings → API Access** → create a key (`sk_live_...`).
2. In Claude: **Settings → Connectors → Add custom connector**.
3. Set remote MCP URL to `https://api.so-me.studio/mcp`.
4. Add header:

   | Name | Value |
   |------|-------|
   | `X-API-Key` | `sk_live_...` (your key, no quotes) |

5. Save and start a new chat to load tools.

For `mcp-remote` in `claude_desktop_config.json`, pass the same header as:

```text
X-API-Key:sk_live_...
```

(no space after the colon). See [docs/setup-claude.md](../docs/setup-claude.md).

## Claude Directory — OAuth

Directory-listed So-me Studio connectors use **OAuth** so end users never paste API keys. After install:

1. Approve the OAuth consent for your so-me.studio account.
2. Tool calls run as that user/tenant; posting and other writes remain **plan-gated** (Team+ API entitlement).

Custom connectors may continue to use `X-API-Key` for developers and Cursor; directory users should prefer OAuth when offered.

## YouTube first comment needs a reconnect

`firstComment` on YouTube uses `commentThreads.insert`, which needs the `https://www.googleapis.com/auth/youtube.force-ssl` permission. Uploading does not. Every YouTube account connected before that permission was added must reconnect in So-me Studio. Until it does, the post publishes and the comment fails; `firstCommentError` on the post says exactly this. This is a social-account permission in So-me Studio, not an MCP connector setting: the connector's own auth (`X-API-Key` or OAuth) is unchanged.

## Security tips

- Prefer a dedicated API key per client; revoke unused keys promptly.
- Do not commit real `sk_live_` values to git or share them in chat logs.
- 401 usually means a missing/wrong header name or revoked key.
