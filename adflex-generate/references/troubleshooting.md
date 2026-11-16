# Troubleshooting

| Symptom | Cause | Do this |
|---|---|---|
| No AdFlex tools in the session | Connector not added | Ask the user to add `https://api.adflex.ai/api/mcp` (Claude Code: `claude mcp add --transport http --scope user adflex https://api.adflex.ai/api/mcp`) and sign in with `/mcp` |
| Auth or scope error | Token expired, or the connection lacks `mcp:generate` / `mcp:publish` | Ask the user to reconnect AdFlex and sign in, granting the needed access |
| Refused without `business_id` | The connection has no default business | `list_businesses`, ask which one, pass `business_id` |
| Returns a quote instead of running | Above the AUTO budget or a gated type (video, posts, Workflows) | Show the quote, wait for a yes, repeat the same call with `confirm_credits` |
| Insufficient credits or spending limit | Balance or connection limit reached | Show the action link the tool returns. Billing belongs to the business owner. After a top-up, check state again; it is not approval to generate |
| `constraint_violation` with `allowedValues` | Unsupported aspect ratio, tier or duration for the model | Retry once with an allowed value |
| "Still running" or a timeout | Async job | Poll `get_generation_details` with the `tool_call_id`. Never start the job again |
| Lost context mid-job | Session restarted | `list_my_generations` to find the job, then `get_generation_details` |
| Tool refuses a URL as not owned | Gallery or CDN link not delivered in this conversation | Import it (`import_web_video` / `import_web_image`) or upload it, then use the new URL |
| Video model fails when character elements are passed (seen on some models) | That model doesn't take them | Drop `element_ids`, pass the element image as a reference instead |
| Burned-in subtitles | Model added captions to speech | Re-prompt "no subtitles", or cover them in the edit |
| Wrong pronunciation of one word | Voice or model mispronunciation | Re-generate that line only, or splice a good take of the word in the edit |
| A name is clipped or gets an extra vowel | The name opens the phrase, or the line is too long for the clip | Put a word before the name, shorten the line or lengthen the clip. See `talking-video.md` |
| Gibberish writing on signs or labels | Image model invented text | Re-prompt "no writing anywhere except …" and quote the exact text |
| A real logo or badge appears | Model reproduced a known product | Re-prompt for an invented, logo-free brand, or edit the image to remove it |
| Background from a reference shows up | A second reference leaked its scene | One reference per role; use a still from the right setting or crop the reference |
| The character looks different between shots | Look described differently each time, or no sheet | Paste one unchanged look block and pass the approved sheet as the identity reference |
| An extra person or warped hand for a few frames | Fast motion | Trim past it (free) before considering a retake |
| User asks which provider runs a model | Confidential | Say it's not something you can share; talk in AdFlex credits only |
