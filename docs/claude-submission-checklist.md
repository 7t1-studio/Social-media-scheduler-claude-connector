# Claude Connectors Directory — submission checklist

**Prepare only.** A human with Anthropic Team/Enterprise **Owner** (directory management) access must submit in Claude.ai → Admin settings → Directory.

Official docs: [Submission](https://claude.com/docs/connectors/building/submission) · [Review criteria](https://claude.com/docs/connectors/building/review-criteria)

## Assets ready

- [ ] Listing copy: [listing-copy.md](listing-copy.md)
- [ ] Icon: [../assets/icon.svg](../assets/icon.svg) (export PNG if portal requires)
- [ ] Server URL: `https://api.so-me.studio/mcp/directory`
- [ ] Transport: Streamable HTTP
- [ ] Auth: OAuth (not API-key paste for directory users)
- [ ] Docs URL: https://docs.so-me.studio/mcp/overview
- [ ] Privacy URL: https://so-me.studio/privacy-policy
- [ ] Support: support@so-me.studio
- [ ] Reviewer demo account (no 2FA, Team+, sample data) — credentials in secrets manager only
- [ ] Confirm `tools/list` on `/mcp/directory` has titles + annotations and **no** AI image/video tools

## Portal fields (quick map)

| Portal step | Fill with |
|-------------|-----------|
| Connection | URL above, Streamable HTTP, universal URL |
| Tools | Auto-sync; fix any missing title/annotation flags |
| Listing | name / tagline / description / categories / docs / privacy / support / icon / slug |
| Use cases | Multi-platform schedule + inbox + analytics; Team+ required; read+write |
| Company | 7t1 Studio / So-me Studio · https://so-me.studio |
| Authentication | OAuth |
| Data handling | First-party So-me Studio API |
| Test & launch | Demo credentials + steps for OAuth login |
| Compliance | All seven acknowledgments (incl. no AI media on this server) |

## Human blockers

- Anthropic Team/Enterprise Owner login
- Pasting demo credentials into the portal
- Choosing permanent URL slug
- Responding to reviewer feedback / `mcp-review@anthropic.com` if needed
