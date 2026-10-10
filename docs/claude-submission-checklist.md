# Claude directory — submission checklist

Rules checked against Anthropic's docs on **2026-10-10**. Re-read the sources before each submission; the portal changes.

Sources: [Publish to the directory](https://claude.com/docs/directory/publish) · [Submit a connector](https://claude.com/docs/connectors/building/submission) · [Connector pre-submission checklist](https://claude.com/docs/connectors/building/review-criteria) · [Authentication](https://claude.com/docs/connectors/building/authentication) · [Lazy authentication](https://claude.com/docs/connectors/building/lazy-authentication) · [Submit a plugin](https://claude.com/docs/plugins/submit) · [Plugin pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist) · [Plugin structure](https://claude.com/docs/plugins/build) · [Software Directory Policy](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy)

## What changed since the first draft (July–September 2026)

| Topic | Old draft | Rule now |
|-------|-----------|----------|
| Where to submit | Claude.ai → Admin settings → Directory | Developer portal at [claude.ai/directory/manage](https://claude.ai/directory/manage) → **Submit new** |
| Who can submit | Team/Enterprise Owner only | Any paid plan. Pro and Max submit from their own account; on Team and Enterprise an Owner (or an Enterprise custom role with the **Directory** permission) submits. The listing belongs to the organization you submit from |
| What to submit | One connector listing | Two submissions: the server as an **MCP connector** and this repo as a **Plugin bundle**, then pair them. Skills cannot be submitted on their own |
| Connector short text | Tagline ≤ 55 characters | One-liner ≤ 200 characters |
| Connector review | Manual review | Automatic policy scan, then listed as **Community** by default. Anthropic may escalate to **Verified** review on its own; there is no application |
| Plugin review | — | Validation on every commit, a security scan, and a human review before the first version goes live |
| Example prompts | Not required | The policy requires at least three working example prompts or use cases |
| Local servers | MCPB desktop extensions accepted | MCPB listings are deprecated; local servers ship only inside a plugin |
| OAuth client registration | DCR | DCR and CIMD both work. Anthropic recommends CIMD (or Anthropic-held credentials) over DCR for high-traffic servers, because DCR registers a new client on every fresh connection |
| Claude Code sign-in | Not covered | The authorization server must accept loopback redirects `http://localhost:<any port>/callback` and `http://127.0.0.1:<any port>/callback` |
| Sign-in trigger | Not covered | Claude starts sign-in only on an HTTP `401` with `WWW-Authenticate: Bearer resource_metadata=…`. A `200` with `isError: true` never starts sign-in |

## Scope decision (2026-10-10)

The Claude listing uses the **posting** tool set: the same 28 tools as the ChatGPT and Grok plugins, served at `https://api.so-me.studio/mcp/claude`. `/mcp/posting` cannot be used for Claude, because it answers unauthenticated requests with HTTP `200` (OpenAI's per-tool auth pattern) and Claude starts sign-in only on `401`. `/mcp/directory` (193 tools) was not chosen: it carries workspace-admin, API-key, webhook, and billing tools and 55 write tools without `destructiveHint`. Display name: **Social media studio**. Reviewer account: the same account as the ChatGPT review.

## Submission 1 — MCP connector

Portal path: **Submit new → MCP connector**.

| Portal step | Value |
|-------------|-------|
| Connection | `https://api.so-me.studio/mcp/claude` · Universal URL · Streamable HTTP |
| Tools | Auto-synced. Fix every tool the portal flags for a missing `title` or `readOnlyHint`/`destructiveHint` on the server, then re-sync |
| Listing | Name ≤ 100, one-liner ≤ 200, description ≤ 2,000, 1–5 categories, docs URL, privacy URL, support contact, icon, slug. Copy: [listing-copy.md](listing-copy.md). **The slug is permanent** |
| Use cases | Primary use cases, prerequisites (So-me Studio account with API/MCP access and connected social accounts), reads and writes. Text in [listing-copy.md](listing-copy.md) |
| Company | 7t1 Studio / So-me Studio · https://so-me.studio · primary contact for review mail |
| Authentication | OAuth with DCR and CIMD (both advertised by `https://api.so-me.studio/.well-known/oauth-authorization-server`) |
| Data handling | First-party So-me Studio API. No personal health data. No sponsored content |
| Test & launch | Reviewer account and step-by-step OAuth instructions. Confirm every tool was run as a custom connector in Claude or with MCP Inspector |
| Compliance | All seven acknowledgments: directory guidelines, first-party API, financial transactions, AI media generation, prompt injection, conversation data collection, public documentation |

### Server requirements

- [ ] Every tool on `/mcp/claude` has a `title` and the right hint: `readOnlyHint: true` for reads, `destructiveHint: true` for anything that changes or deletes data
- [ ] Tool names ≤ 64 characters; no catch-all tool that mixes reads and writes
- [ ] Descriptions say what the tool does and when to use it. No instructions that tell Claude to call tools the user did not ask for, to fetch instructions from elsewhere, or to override system instructions
- [ ] No AI image, video or audio generation on the listed URL; no money or asset transfers
- [ ] Errors carry an actionable message, never a bare "Internal Server Error" or "Bad Request"
- [ ] Results stay proportional to the request (claude.ai cap ≈ 150,000 characters; Claude Code 25,000 tokens; 240 s per call)
- [ ] Unauthenticated MCP requests that need the user's account fail at the HTTP level with `401` and `WWW-Authenticate: Bearer resource_metadata="…"`
- [ ] Protected resource metadata `resource` equals the listed URL exactly, including `/mcp/claude`
- [ ] Redirect URIs: `https://claude.ai/api/mcp/auth_callback`, plus loopback `localhost` and `127.0.0.1` with the port ignored (Claude Code)
- [ ] Token endpoint accepts `application/x-www-form-urlencoded`, answers in under 10 s, returns `invalid_grant` for a dead refresh token, and rotates refresh tokens for public clients
- [ ] Anthropic's egress range `160.79.104.0/21` is not blocked by the CDN or WAF on the API and the authorization server
- [ ] Tested end to end as a custom connector in claude.ai and in Claude Code

## Submission 2 — Plugin bundle

Portal path: **Submit new → Plugin bundle**. Repository `7t1-studio/Social-media-scheduler-claude-connector`, plugin path empty (the plugin is the repo root), tracked branch `main`.

- [ ] `.claude-plugin/plugin.json` with `name` (permanent, lowercase-hyphen, not a reserved word), `displayName`, `version`, `description`, `author`, `license`, and the listing fields `icon`, `documentationUrl`, `supportUrl`, `privacyPolicyUrl`, `termsOfServiceUrl`
- [ ] `.mcp.json` points at the **same URL** as the connector listing, with `"type": "http"`, and holds no credentials
- [ ] Skills in `skills/<name>/SKILL.md`: `name` ≤ 64 characters and equal to the folder name; `description` ≤ 1,024 characters; body under 500 lines
- [ ] `README.md` of at least 40 words outside code blocks, saying what the plugin does, how to use it, and what data it sends where
- [ ] `LICENSE` file present
- [ ] No `.DS_Store`, `Thumbs.db`, `desktop.ini` or `__MACOSX` in the repo; no symlinks, submodules or Git LFS
- [ ] Every non-image file under 256 KiB; only text, PNG/JPEG/GIF/WebP/SVG images and fonts (no `.zip`, `.pdf`, `.ico`)
- [ ] No top-level `bin/` directory (claude.ai and Cowork refuse to install it)
- [ ] `version` raised on every release
- [ ] `claude plugin validate .` passes (Claude Code 2.1.281 or later accepts the listing fields without warnings)
- [ ] Loaded and tested with `claude --plugin-dir .` and as an uploaded zip in claude.ai (**Customize → Plugins → Add → Upload plugin**)
- [ ] Portal **Validate** shows no **Blocking** findings
- [ ] Repository is public before the listing goes live

Portal steps after **Validate**: Listing details (read from `plugin.json` and the README) → Data handling (personal data, other destinations, retention, under-18 use) → Compliance (contact email and four acknowledgments) → Review and submit (keep **GitHub push webhook**).

After both are submitted from the same organization, pair the plugin with the connector listing.

## Steps only a person can do

- Sign in to claude.ai with the account that should own the listing, and connect GitHub for that organization
- Enter the reviewer credentials in the portal (never in this repo)
- Choose the permanent connector slug
- Answer reviewer feedback; connector escalations go to `mcp-review@anthropic.com`, plugin questions to `directory@anthropic.com`
