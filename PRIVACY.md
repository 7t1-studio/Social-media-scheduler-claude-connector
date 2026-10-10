# Privacy

So-me Studio's full privacy policy is published at:

**https://so-me.studio/privacy-policy**

It describes the personal data So-me Studio collects, how it is used and stored, which third parties receive it, how long it is kept, your rights, and how to contact us (support@so-me.studio).

## Notes for the Claude plugin and connector

When you connect Social media studio in Claude (through the plugin, the directory connector, or a custom connector), Claude sends tool calls that read or change data in your So-me Studio workspace: posts, drafts, schedules, media files and their metadata, and the names and capabilities of your connected social accounts.

- Tool calls go to `https://api.so-me.studio/mcp/claude` over HTTPS and run as your signed-in user (OAuth 2.0 with PKCE). No API key or secret is stored in the plugin.
- A tool call carries only the arguments Claude passes to that tool. The plugin does not read your Claude conversation history, memory, or files, except a local image or video you ask Claude to upload.
- When you ask Claude to upload a local file, the plugin's helper script sends that file's bytes directly to a short-lived presigned upload URL for So-me Studio's Cloudflare R2 storage. It sends no credentials there.
- When you publish, So-me Studio sends the post to the social platforms you choose, through the accounts you connected.
- So-me Studio processes MCP traffic to run the tools, to enforce plan limits, credits, and rate limits, and for security logging.
- So-me Studio does not use your social content from MCP calls to train third-party foundation models.
- The plugin itself stores no data.
- You control access: disconnect the connector in Claude, or revoke the connection or API keys in So-me Studio settings, at any time.

For categories of personal data, retention periods, and your rights, the main [privacy policy](https://so-me.studio/privacy-policy) applies.
