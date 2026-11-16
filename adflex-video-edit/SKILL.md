---
version: 0.1.0
name: adflex-video-edit
description: |
  Import, inspect, cut, join, mute, mix and mux video on the user's
  AdFlex account with the zero-credit AdFlex finishing tools. Use when:
  "import this reel", "download this Instagram/YouTube video", "trim
  this clip", "cut from 0:03 to 0:09", "join these clips", "remove the
  sound", "add this voiceover/music to the video", "put this song on
  it", "grab the last frame", "what happens in this video", "what does
  she say in this clip". Chain with adflex-generate to create missing
  voiceover, music or shots, and adflex-social-publish to post the
  result. NOT for: generating new footage (use adflex-generate), AI
  changes to a clip such as product or character swaps, style edits or
  extension (use adflex-video-remix), saved multi-step Workflows (use
  adflex-workflows), or posting (use adflex-social-publish).
argument-hint: "[video url or file] [what to do: trim | join | mute | mix | frame | inspect]"
allowed-tools: Bash
---

# AdFlex Video Edit

Deterministic edits of existing media through the AdFlex MCP tools. These tools cost **zero user credits** and need no quote or extra chat approval. They never generate new shots.

## Step 0: Connection

1. If no AdFlex tools (such as `list_businesses`) are available, ask the user to add the connector, then stop:
   - Claude Code: `claude mcp add --transport http --scope user adflex https://api.adflex.ai/api/mcp`, then `/mcp` to sign in.
   - Other clients: add the HTTP MCP server `https://api.adflex.ai/api/mcp` and sign in.
2. On an auth or scope error, ask the user to reconnect AdFlex with `/mcp`.
3. With more than one business, call `list_businesses` once and pass `business_id` everywhere.

## Rules for every edit

1. **One stable `operation_id` per requested edit.** After a timeout, call again with the same `operation_id`, or look up the saved `tool_call_id`. Never import or render the same thing twice.
2. **Owned sources only.** A source must be media delivered in this MCP conversation (generated, imported, uploaded, or an earlier edit) or a ready file from the business's upload library. An AdFlex gallery or CDN URL on its own is refused. Import or upload it first.
3. **Reuse saved URLs.** Each edit returns a new URL; feed that into the next step.
4. Reply in the user's language, briefly, with the final URL. No JSON or tool names in chat.

## Pick the tool

| User wants | Tool | Must set |
|---|---|---|
| Bring in a public Reel, YouTube video or direct video | `import_web_video` | `purpose`: `import` to edit, `inspect` to answer a question about it |
| Bring in a web image as a reference | `import_web_image` | `operation_id` |
| Trim one clip | `assemble_video_clips` | one `video_urls` item, one `clip_trims` entry, `audio_mode=preserve` (unless silence was asked) |
| Join several clips | `assemble_video_clips` | `video_urls` in order (1–6), optional `clip_trims` per clip, `audio_mode` **always** (a join without it is silent); `resolution: "1080p"` to avoid the 720p default |
| Remove the sound | `remove_video_audio` | `video_url` |
| Add voiceover, music or effects (1–8 tracks) | `mix_audio_to_video` | `source_audio_mode`: `preserve` (keep original under) or `replace` |
| Put one soundtrack on unchanged | `mux_audio_to_video` | `duration_mode`: `source_audio` or `shortest` |
| Save a frame as PNG | `extract_video_frame` | `source_url`, `position`: first / last / time (+ `time_seconds`) |
| Describe what's on screen | `inspect_video` (video) / `inspect_media` (images) | |
| What is said or heard | `inspect_audio` | only when the user asks about sound |

Read `references/finishing-recipes.md` for the exact parameters and common recipes.

## Decision rules

- **A single trim keeps the canvas** when `aspect_ratio` and `resolution` are omitted. A multi-clip join is re-encoded at 720p and 30 fps unless `resolution: "1080p"` is set. Cutting re-encodes; it isn't lossless.
- **Mix vs mux.** Mix keeps the whole picture and layers timed tracks with gains in dB (peak-limited, no loudness normalization). Mux copies one soundtrack; `shortest` can cut the picture or the sound, so use it only for an intentional shorter ending.
- **Already silent** video: `remove_video_audio` returns the original URL with no new file. That's success, not an error.
- **Missing audio** (narration, music, effects): create it first with `gen_voiceover`, `gen_music` or `gen_sound_effect` in adflex-generate, under their own quotes. Then mix.
- **Shot continuity:** `extract_video_frame` the last frame, then use its `imageUrl` as `gen_video` `source_url` with `task_type=image_to_video`.
- **Fix before regenerating.** A warp, an extra figure, dead air or a clipped ending is a trim, and trims are free. Offer the trim before a paid retake. Never end a trim inside a spoken word.
- **Out of scope here:** burned-in captions, overlays, speed changes, grading and loudness normalization. Say so and offer the alternatives in `references/finishing-recipes.md`; never report an edit that didn't happen.
- **Import only what's needed.** For a cut or mute of a public Reel: import once with `purpose=import` and edit the saved URL. Don't inspect, transcribe or regenerate it.
- **Inspection is evidence about what was sampled.** Frames don't prove spoken words, continuous motion or sound. Call `inspect_audio` only when the question is about speech or sound. See `references/inspection.md`.
- Never substitute a "similar" Reel for the one the user linked.

## References

- `references/finishing-recipes.md`: parameters, audio levels and step-by-step recipes.
- `references/inspection.md`: how to inspect footage and report what you can and can't tell.
