# Connect ChatGPT to So-me Studio MCP

So-me Studio ships as a **tools-only ChatGPT plugin / MCP app** (no interactive Apps UI widgets). The marketplace endpoint is:

```
https://api.so-me.studio/mcp/directory
```

Developer / full tool catalog (includes AI media tools **not** allowed on marketplace listings):

```
https://api.so-me.studio/mcp
```

## For end users (after listing approval)

1. Install **So-me Studio** from the ChatGPT plugin / apps directory (or enable it for your workspace).
2. Complete **OAuth** to link your so-me.studio account (**Team+** plan required for API / posting entitlement).
3. Use natural-language prompts to list posts, schedule content, check inbox, or pull analytics — without pasting an API key.

Until the public listing is live, use **Claude** ([setup-claude.md](setup-claude.md)) or **Cursor** ([../config/cursor.mcp.json.example](../config/cursor.mcp.json.example)) with `X-API-Key`.

## For OpenAI reviewers / ops (domain challenge)

When the plugin portal shows a domain verification challenge:

1. Set `OPENAI_APPS_CHALLENGE_TOKEN` on the API host to the **exact** portal token.
2. Confirm:

```bash
curl -sS https://api.so-me.studio/.well-known/openai-apps-challenge
```

The response body must be the raw token only (not JSON).

## Submission packet (internal)

Full OpenAI checklist (org verification, Scan Tools, 5+/3− test prompts, demo account) lives in the private monorepo:

`docs/mcp-openai-plugin-submission.md`

**Human required:** verified OpenAI org + portal submit. This public repo cannot complete that step.

## Links

| | |
|---|---|
| Product docs | https://docs.so-me.studio/mcp/overview |
| Privacy | https://so-me.studio/privacy-policy |
| Terms | https://so-me.studio/terms-and-conditions |
| Website | https://so-me.studio |
| Listing copy | [listing-copy.md](listing-copy.md) |
