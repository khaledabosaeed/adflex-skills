# Operations

`tools/list` and `get_model_info` are authoritative. Confirm any model's operations and limits before quoting.

## gen_genjutsu

Replace a character or a subject in a source video using stills.

| Field | Notes |
|---|---|
| `source_url` | An owned video (imported, uploaded or generated in this conversation) |
| `reference_images` | 1–10 owned stills, the primary one first |
| `mode` | `recast` (a person or character, default) or `swap` (object, product, clothing) |
| `prompt` | Optional direction for the replacement |
| `audio_mode` | `source` (default) or `silent` |
| `quality_tier` | Optional, billed |

- At most 11 owned URLs per call: the source plus 10 references.
- Always quoted, always approved explicitly.
- Reuse a saved result; don't start it again. A finishing step waits for the delivered URL.

**References that work**
- Recast: a clear front view first, then full body and three-quarter views, same wardrobe.
- Swap: the product alone, well lit, from the angle it appears at in the clip.
- Drop references that contradict each other. If the stills disagree about the look, prepare one clean reference first (a paid `gen_image`, quoted separately) and check it before the video.

## Video edit (gen_video, video_to_video)

For a described change to the clip: color, material, style, setting.

- `task_type=video_to_video`, `source_url` = the owned clip.
- Use the edit control the model exposes, one only: `video_operation: edit` on models that take it (Gemini Omni Flash), or the model's own video-edit mode. `get_model_info` says which.
- A native edit re-renders the clip. It is not a pixel-level patch.
- To use an exact product photo, the operation must accept both the source video and a reference image. A source-only edit can change a described color or material but can't receive a specific product.
- `keep_original_sound: true` only when the operation exposes it. For silence, set `generate_audio: false` where exposed instead of planning a mute step.
- Don't turn an edit into text-to-video.

## Performance and motion transfer

Put the source's action onto a new character.

- Bind the character image in its character role. Product, style or composition references alone don't say who to animate.
- Compare framing, pose and prop placement between the character image and the motion source. A full-body dance needs a full-body character image.
- Let the source drive the choreography. Use the prompt for identity, scene and look, not a competing sequence of moves.
- The source should show one continuous, unobstructed performer.

## Extension

Continue the same take, action or dialogue past its ending.

- `task_type=video_to_video`, `video_operation: extend`, one `source_url`, `duration` = **additional** seconds.
- Omni-family models cap the total at 30 s and refuse to extend a clip that contains speech. Segment-style models need a 1–15 s source.
- Read the model's contract first: source length limits, how many seconds can be added, the total cap, and whether it returns the **full video** or only the **new segment**.
- A full-video result already contains the source. Don't prepend the source again.
- A new-segment result is joined after the original with `assemble_video_clips`, `audio_mode=preserve`, `resolution` set to keep the source quality, each part once, in order.
- One stage at a time, from a completed output. A pending job has no usable URL.
- Don't promise the same voice or uninterrupted dialogue across the join. Extension can't add new dialogue to an uploaded talking clip on some models.
- Don't substitute an edit, new shots or silent assembly for a real extension.

## Upscale

`task_type=video_upscale` with `source_url`. A larger canvas doesn't restore detail that isn't in the source.

## Prompts

- Say what changes, then what stays: "Replace the white sneakers with the red pair in the reference. Keep the walk, the camera move, the street and the timing unchanged."
- For contact with objects, name the beats: approach, grip, lift, release, rest. Keep the count and order of objects explicit.
- No workflow commands, approvals or retry notes inside the prompt.

## Review

- Compare source and output: requested subject present, old one replaced, unrelated scene and action preserved, hands and occlusion credible.
- Use `inspect_video` with times around the contact moments. Samples are not continuous playback.
- For speech or sound, `inspect_audio` on the delivered clip. A matching transcript is not proof of the same voice or of lip sync.
- State checked defects and limits plainly. Taste alone is not a failed delivery.

## Troubleshooting

| Symptom | Do this |
|---|---|
| Source URL refused as not owned | Import or upload it in this conversation first |
| Instagram or TikTok link | Reels import; TikTok isn't a supported source. Ask for the file |
| Job rejected | Read the failure detail. Don't resend unchanged inputs or switch tools to get around a policy refusal |
| "Still running" | Poll `get_generation_details`; never start again |
| Sound missing after an edit | `mux_audio_to_video` with the original as `audio_url`, `duration_mode=source_audio` |
| Edited clip shorter than the original audio | `source_audio` mode refuses it; trim the audio intentionally with `mix_audio_to_video`, or use `shortest` knowingly |
| Label or face not exact | Use a cleaner single reference; say that exact fidelity isn't guaranteed |
| User wants a mask or a tracked logo | Not exposed over this connection; say so |
| "Genjutsu" asked on another platform's terms | Describe the result with AdFlex's own operation; don't bring up other platforms unless asked |
