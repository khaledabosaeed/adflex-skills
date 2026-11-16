---
version: 0.1.0
name: adflex-generate
description: |
  Generate images, videos, storyboards, carousels, voiceovers, music,
  sound effects, Genjutsu recasts/swaps and PDF documents through the
  AdFlex MCP connector. Quote credits, get approval, then deliver the
  AdFlex URL. Use when: "generate an image", "make a video", "animate
  this photo", "image-to-video", "make a talking ad", "Arabic voiceover",
  "make a carousel", "storyboard this ad", "make music for this",
  "add a sound effect", "swap the product in this reel", "recast this
  character", "remove the background". Chain with adflex-video-edit
  to cut and mix, adflex-workflows for dependent multi-step
  productions, and adflex-social-publish to post.
  NOT for: cutting or mixing footage (adflex-video-edit), product
  stills (adflex-product-photo), spoken ads (adflex-talking-ad), image
  sets (adflex-carousel), changing an existing video
  (adflex-video-remix), PDFs (adflex-documents), Workflows
  (adflex-workflows), posting (adflex-social-publish), or AdFlex's own
  reels (adflex-reels).
argument-hint: "[prompt] [--image|--video <url-or-file>] [--model <name>]"
allowed-tools: Bash
---

# AdFlex Generate

Create media on the user's AdFlex account using the AdFlex MCP tools (`gen_image`, `gen_video`, `gen_storyboard`, `gen_voiceover`, `gen_music`, `gen_sound_effect`, `gen_genjutsu`, `remove_background`, `gen_document`, `render_video_draft`, `enhance_prompt`).

## Step 0: Connection

1. If no AdFlex tools (such as `list_businesses`) are available, the connector is missing. Ask the user to add it, then stop:
   - Claude Code: `claude mcp add --transport http --scope user adflex https://api.adflex.ai/api/mcp`, then `/mcp` to sign in.
   - Other clients: add the HTTP MCP server `https://api.adflex.ai/api/mcp` and complete the OAuth sign-in.
2. If a tool fails with an auth or scope error, tell the user to run `/mcp` (or reconnect AdFlex in their client) and sign in again.
3. If the user has more than one business, call `list_businesses` once and pass `business_id` on every call. Never guess a brand.

## Source of truth

- `tools/list` is authoritative for which tools and parameters exist. `get_adflex_capabilities` summarizes them with their approval route.
- Never invent a model ID. Omit `model_id` and let AdFlex route unless the user names a model or asks for something only one model offers. Check a named model with `get_model_info`.
- Voices come from `search_voices`. Brand characters, places and props come from `list_brand_elements`. Never make up a `voice_id` or `element_id`.

## UX rules

1. Reply in the user's language and dialect. Keep prompts to the models in English, but keep every spoken or on-screen line verbatim in its original script.
2. Be short. No raw JSON, IDs or tool names in chat. Show the delivered AdFlex URL (or the inline media resource) unchanged.
3. Ask one missing thing at a time, and only when it changes the result. Do lookups, prompt prep and quotes without asking.
4. Never disclose or guess which providers run AdFlex models or what AdFlex pays. Talk about price only in AdFlex credits as quoted.

## Credits and approval (every paid call)

1. For a requested action, call the tool with a stable `operation_id` and **without** `confirm_credits`.
2. The server either runs a small action automatically (AUTO, within the daily budget) or returns a **quote**.
3. Show the quote once, with what will be made (and the exact spoken line for talking video). Wait for a yes.
4. Repeat the **exact same call** with `confirm_credits` set to the approved amount. Never invent approval, never start replacement work, and never re-run after a timeout: reuse the `operation_id` or the saved `tool_call_id`.
5. For "how much would it cost?", set `confirm_credits: 0`. Nothing runs.
6. A changed prompt, model or length needs a new quote and a new yes.

Video, storyboards, sound effects and anything that answers "still running" continue in the background. Poll `get_generation_details` with the returned `tool_call_id`. Don't promise a completion time.

## Pick the tool

| User wants | Tool | Notes |
|---|---|---|
| One image, edit of an image, ad still, poster, GIF | `gen_image` | `task_type` per intent; `transparent_background`, `output_format` gif |
| Cut-out on transparent background | `remove_background` | |
| A set of 1–9 related images | `gen_storyboard` | `mode`: storyboard / carousel / moodboard; async |
| Change one storyboard frame | `edit_storyboard_scene` | paid, sync |
| Video from text or a first frame | `gen_video` | `task_type` from the schema; `draft: true` for a cheap 480p test |
| The approved draft at 1080p | `render_video_draft` | same take, new quote |
| Swap a product/outfit or recast a character in a real clip | `gen_genjutsu` | not `gen_video model_id=adflex_genjutsu` |
| Voiceover / narration | `gen_voiceover` | `model_id` plus one fixed `voice_id` per speaker |
| Music bed or song | `gen_music` | |
| One sound effect or ambience | `gen_sound_effect` | |
| Better prompt from a rough idea | `enhance_prompt` | free prep |
| Shareable PDF (menu, price list, one-pager) | `gen_document` | link expires in about 7 days, not in My Assets |

Read `references/tools.md` for parameters and pitfalls of each tool.

This is the general maker. When a focused skill is installed and the request matches it, that skill has the fuller procedure: adflex-product-photo (product stills), adflex-talking-ad (spoken ads), adflex-carousel (image sets), adflex-video-remix (changing an existing video), adflex-documents (PDFs), adflex-brand (lookups and source reads). Without them, the tools above still work from here.

## Decision rules

- **Stills first, then motion.** For anything with a product, character or brand, make and approve the still, then use it as `source_url` with `task_type=image_to_video`.
- **Draft before full quality** when testing motion: `gen_video` with `draft: true`, then `render_video_draft` with that `tool_call_id`.
- **Talking video** (a person speaking a script, especially Arabic): follow `references/talking-video.md`. It decides between one Omni clip and the voiceover-per-line recipe.
- **Continuity between clips:** `extract_video_frame` (free, in adflex-video-edit) gives the last frame for the next clip's `source_url`.
- **Brand consistency:** read `get_brand_kit` / `get_business_context` only for missing facts. Pass brand elements by `element_ids` and mention their `@handle` in the prompt.
- **Files from the user:** chat attachments can't be passed to tools. Follow `references/media-inputs.md` (direct upload, else an upload link).
- **Product facts:** read supplied URLs with `read_creative_references` or `scan_brand_url`, PDFs with `read_document`. Never invent claims about use, health, ingredients or results.
- **Consistency across shots:** one unchanged look block in every prompt, an approved sheet as the identity reference, one reference per role. See `references/prompting.md`.
- **A flawed result:** fix it the cheapest way. Trim or splice first (adflex-video-edit, free), then regenerate only the failed line or shot, from a frame of the existing clip when it must match its neighbours. Never redo the whole piece for one flaw.
- **Several dependent steps** that should run as one approved job: hand off to adflex-workflows.
- After delivery, offer the next step once: cut/mix (adflex-video-edit) or post (adflex-social-publish).

## References

- `references/tools.md`: parameters, task types and pitfalls per tool.
- `references/talking-video.md`: speech recipes for scripted and unscripted talking clips and product ads, pronunciation, pacing and fixing a bad take.
- `references/prompting.md`: how to write image and video prompts that hold up, keep a character or product consistent, and what to check in every result.
- `references/media-inputs.md`: uploads, URL ownership rules, brand elements and references.
- `references/troubleshooting.md`: common errors and what to do.
