# Claude directory listing copy

Copy for the two submissions in the Claude developer portal ([claude.ai/directory/manage](https://claude.ai/directory/manage)). Limits are the portal's limits as of 2026-10-10, and every field below was counted against them. The process is in [claude-submission-checklist.md](claude-submission-checklist.md).

Never put the reviewer password, an API key, or the reviewer e-mail address in this file. They go into the portal only.

## Submission 1 — MCP connector

### Connection

| Field | Value |
|-------|-------|
| Server URL | `https://api.so-me.studio/mcp/claude` |
| URL type | Universal URL |
| Transport | Streamable HTTP |

### Listing

**Server name** (≤ 100)

```
Social media studio
```

**One-liner** (≤ 200)

```
Draft, schedule, and publish posts with images, videos, threads, and first comments to the social accounts in your So-me Studio workspace.
```

**Description** (≤ 2,000)

```
Social media studio is a productivity tool for social media work, powered by So-me Studio. Plan, schedule, and publish a week of posts to all your connected So-me Studio accounts from one Claude conversation, without switching between social apps.

Create multi-post threads on X, Threads, Bluesky, and Mastodon, and add an automatic first comment on Facebook, Instagram, X, LinkedIn, Threads, and YouTube. Choose images and videos from your media library or upload new ones, and check each file against every destination's size, type, duration, dimension, codec, and frame-rate rules before anything publishes. Review your posting calendar, edit or reschedule upcoming posts, save drafts, and track publication status. TikTok posts use the privacy and interaction options that the creator chooses.

For social media managers, creators, and small businesses that already use So-me Studio. Requires a So-me Studio account with API/MCP access and connected social accounts. You sign in with OAuth; no API key is needed. Media, thread, and first-comment support depends on the destination platform. Reddit and Google Business Profile are not supported. The connector does not provide analytics, inbox replies, billing, or AI image and video generation.

Add the Social media studio plugin to give Claude the full posting workflow as a skill.
```

**Categories** (1–5; use the portal's exact labels): Productivity, Marketing, Social media.

| Field | Value |
|-------|-------|
| Documentation URL | https://docs.so-me.studio/mcp/overview |
| Privacy policy URL | https://so-me.studio/privacy-policy |
| Support contact | support@so-me.studio |
| Icon | [../assets/icon.png](../assets/icon.png) (1024 × 1024 PNG) |
| Slug (permanent) | Proposed: `social-media-studio`. Decide before publishing; it can never change |

### Use cases

**Primary use cases**

```
1. Plan and schedule a week of posts across several connected social accounts from one conversation, then review the posting calendar.
2. Write a thread for X, Threads, Bluesky, or Mastodon, with an automatic first comment, and save it as a draft or publish it.
3. Check images and videos against every destination's media rules before uploading, get the exact fix for each failure, and attach library or uploaded media to posts.
4. Find, edit, reschedule, unschedule, retry, or delete upcoming posts and drafts.
```

**What users need before they connect**

```
A So-me Studio account (so-me.studio) on a workspace plan that includes API/MCP access, with the social accounts they want to post to already connected in So-me Studio.
```

**Reads or writes:** both.

### Company

| Field | Value |
|-------|-------|
| Company name | 7t1 Studio / So-me Studio |
| Website | https://so-me.studio |
| Primary contact | Set in the portal |

### Authentication

OAuth. The authorization server advertises both dynamic client registration (`registration_endpoint`) and client ID metadata documents (`client_id_metadata_document_supported: true` with `none` in `token_endpoint_auth_methods_supported`). No Anthropic-held credentials, no custom connection.

### Data handling

- The underlying API is So-me Studio's own first-party API.
- No personal health data.
- No sponsored content.

### Test & launch

Reviewer instructions (paste into the portal, then add the credentials in the credentials field):

```
Reviewer account: the e-mail address and password are in the credentials field. The account is a member of the workspace "Social media studio", which has 12 connected social accounts (including X @hisomestudio, Bluesky hisomestudio.bsky.social, Mastodon @somestudio, and the LinkedIn page so-me-0047), a populated media library, drafts, and scheduled posts. It has no two-factor authentication.

1. In Claude, add the connector (or install the Social media studio plugin and connect it from its Connectors tab).
2. Claude opens the So-me Studio sign-in page. Sign in with the reviewer e-mail address and password.
3. On the consent page, check that it names Claude and claude.ai, then select Approve. Claude shows the connector as Connected.
4. Run the example prompts below. Bluesky and Mastodon posts publish for real to the reviewer accounts; delete them afterwards with "Delete the post I just published" if you want.

Example prompts:
- Find calendar__c00-month.webp in my Social media studio media library and publish it to my Bluesky account now with the caption "Plan a whole month of posts in one calendar." Then send me the link to the live post.
- Schedule this post on my Mastodon account and my LinkedIn page for next Monday at 9:00 AM UTC: "New on our blog: 5 ways to plan a week of social posts in 30 minutes." Then show me my posting calendar for next week.
- In my posting calendar for next week, move the Mastodon post to Tuesday at 3:00 PM UTC and add #SocialMediaTips to the end of its text. Then take the LinkedIn post off the schedule.
- Write a three-post X thread with practical tips for batching a week of social posts. Add "Plan your week at so-me.studio" as an automatic first comment, and save it as a draft in Social media studio. Do not publish or schedule it.
- Before I upload it, check if my video spring-launch.mp4 can be posted as an Instagram Reel, a TikTok video, a Facebook Reel and a Bluesky video. It is an MP4, 1080x1920, 2 minutes long, 120 MB, H.264, 30 fps. Tell me what to change for each platform that fails.

All 28 tools were run against this account as a custom connector in Claude before submission.
```

### Compliance

Select all seven acknowledgments. The connector calls only So-me Studio's own API, moves no money, generates no images, video, or audio, collects no conversation data beyond each tool's arguments, and has public documentation at https://docs.so-me.studio/mcp/overview.

## Submission 2 — Plugin bundle

### Source

| Field | Value |
|-------|-------|
| Repository | `7t1-studio/Social-media-scheduler-claude-connector` |
| Plugin path | Empty (the plugin is the repository root) |
| Branch or tag | `main` |

### Listing details

The portal reads these from the repository, so edit the files and validate again to change them:

- Name, display name, version, description, author, and links: [`.claude-plugin/plugin.json`](../.claude-plugin/plugin.json)
- Listing description: [`README.md`](../README.md)
- Icon: [`assets/icon.png`](../assets/icon.png)

### Data handling answers

| Question | Answer |
|----------|--------|
| Does the plugin read or store personal data? | It stores nothing itself. Through its connector it reads and changes data in the user's own So-me Studio workspace: posts, drafts, media files, and the names of connected social accounts. |
| Does it send data to services other than its declared connectors? | Only media bytes: when the user asks Claude to upload a local image or video, the bundled helper sends that file with an HTTP PUT to the presigned upload URL that the So-me Studio connector returned (So-me Studio's Cloudflare R2 storage). Nothing else leaves through the plugin. |
| How long does it keep data? | The plugin keeps no data. The temporary upload plan is deleted after use. So-me Studio's retention is described at https://so-me.studio/privacy-policy. |
| Is it intended for people under 18? | No. |

### Compliance

Check the contact e-mail and select all four acknowledgments. Keep **GitHub push webhook** under **How new versions reach the directory**.

### Pairing

Submit the connector and the plugin from the same Claude organization, then pair the two listings in the portal. Both use `https://api.so-me.studio/mcp/claude`, so a user who has both sees one set of tools.
