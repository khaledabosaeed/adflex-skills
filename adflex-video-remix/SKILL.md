---
version: 0.1.0
name: adflex-video-remix
description: |
  Change an existing video with AI through the AdFlex MCP connector:
  swap a product, object or outfit, recast the person (AdFlex
  Genjutsu), restyle or edit a scene, transfer a performance onto a
  new character, extend a take, or upscale. Keeps the source's motion
  and sound where the operation supports it. Use when: "put our
  product in this reel", "replace the person in this video with our
  character", "recast this", "swap the shoes", "make this clip anime
  style", "continue this video for 5 more seconds", "extend the shot",
  "upscale this clip", "do this trend with my character". Chain with
  adflex-video-edit to import, trim and restore audio, and
  adflex-social-publish to post. NOT for: trims, joins, mutes or
  mixing (use adflex-video-edit, free), new video from text or a still
  (use adflex-generate), or talking ads from a script (use
  adflex-talking-ad).
argument-hint: "[source video url] [what changes] [reference images] [what must stay]"
allowed-tools: Bash
---

# AdFlex Video Remix

A source video goes in, a changed video comes out. Decide what changes and what stays before choosing a tool, because each operation preserves different things.

## Step 0: Connection

1. If no AdFlex tools (such as `list_businesses`) are available, ask the user to add the connector, then stop:
   - Claude Code: `claude mcp add --transport http --scope user adflex https://api.adflex.ai/api/mcp`, then `/mcp` to sign in.
   - Other clients: add the HTTP MCP server `https://api.adflex.ai/api/mcp` and sign in.
2. On an auth or scope error, ask the user to reconnect AdFlex with `/mcp`.
3. With more than one business, call `list_businesses` once and pass `business_id` everywhere. Never guess a brand.

## 1. Own the sources

A web page is not a model input, and an AdFlex gallery link alone is refused.

- Public Reel, YouTube video or direct `.mp4`: `import_web_video` (`purpose=import`), once. Reuse the saved URL.
- Reference stills: `import_web_image`, or the upload tools.
- TikTok links aren't a supported source. Ask for the file.
- If the import can't reach the video, ask for the file or a direct link. Don't recreate it from text and call it an edit.

## 2. Write down what changes and what stays

Character identity, product and label, background, camera, action and timing, sound. This record doesn't change later to fit a model.

## 3. Pick the operation

| User wants | Use | Notes |
|---|---|---|
| Replace a **person** in the clip with a character from stills | `gen_genjutsu`, `mode: recast` | 1–10 `reference_images`, primary first |
| Replace an **object, product or outfit** | `gen_genjutsu`, `mode: swap` | |
| Change a described look, color or style across the clip | `gen_video`, `task_type=video_to_video`, on a model that supports video edit | A source-only edit can't take an exact product photo |
| Put a performance onto a new character | A motion-transfer or video-edit operation the model exposes | Check `get_model_info` |
| Continue the same take | `gen_video`, `video_operation: extend` | `duration` = seconds **added** |
| Higher resolution | `gen_video`, `task_type=video_upscale` | |

Genjutsu is its own tool. Never `gen_video` with a Genjutsu model ID. Read `references/operations.md` for each operation's inputs, limits and prompts.

## 4. Quote, run, review

1. Call without `confirm_credits`. Genjutsu always needs an exact quote and an explicit yes.
2. Show the quote with what changes and what stays. After a yes, repeat the same call with `confirm_credits`.
3. Poll `get_generation_details`. An accepted job is pending, not delivered.
4. Compare source and output for the requested change before praising it: the right subject present, the old one gone, the rest of the scene and action kept, hands and contact credible.

## Credits and approval

1. Call the paid tool with a stable `operation_id` and **without** `confirm_credits`. The server runs a small action automatically or returns a quote.
2. Show the quote once with what will be made. Wait for a yes.
3. Repeat the **exact same call** with `confirm_credits` set to the approved amount. A changed prompt, count or quality needs a new quote.
4. `confirm_credits: 0` is a price-only check. After a timeout, reuse the `operation_id` or poll `get_generation_details`; never start the job again.
5. Prices only in AdFlex credits. Never disclose or guess which providers run AdFlex models.

## Rules

- **Sound:** Genjutsu keeps source audio unless `audio_mode: silent` was asked. For an edit model without native audio preservation, copy the original soundtrack back afterwards with `mux_audio_to_video` (edited video as `video_url`, original as `audio_url`, `duration_mode=source_audio`). That copies audio; it is not lip sync.
- **Framing:** keep the source canvas. Leave `aspect_ratio` unset unless the user asks for another.
- **No pixel-perfect promises.** Motion guidance isn't frame-exact, and reference support doesn't guarantee an identical label.
- **A rejection is not a retry cue.** Read why it failed. Don't resend the same inputs, reword around a media refusal, or start a paid batch.
- **No paid quality retries** without a yes. For a visual defect, change the reference or the blocking that caused it, not the adjectives.
- **Not exposed:** masks, tracked regions, exact logo overlays. Say so; don't invent a control.
- Only clips the user has the right to use, and no real people recast without consent.
- Reply in the user's language, briefly. Describe the result and the model by its display name. No JSON or IDs.

## References

- `references/operations.md`: Genjutsu, video edit, motion transfer, extension and upscale, with inputs, prompts, review and troubleshooting.
