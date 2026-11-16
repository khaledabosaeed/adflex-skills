# Generation tools

`tools/list` is authoritative. This file lists the parameters that matter and the mistakes that cost credits. Every paid tool follows the quote, then `confirm_credits` flow in `SKILL.md`.

## gen_image

- Required: `prompt`, `task_type`. Read the `task_type` enum from the schema. Current values: `create_from_scratch`, `photorealistic_quality`, `edit_existing` (keep the photo, change one thing), `combine_multiple` (several images, each with a role), `fast_draft`, `logo_or_graphic`, `character_consistency` (a sheet as reference), `social_post` (a designed post image), `social_media_ad`, `product_shot`, `general`.
- `reference_sheet`: `character`, `product` or `storyboard` for ONE multi-panel image at one image's price. It gives no separate frames; use `gen_storyboard` for those.
- `reference_roles`: `identity`, `character`, `product`, `brand_mark`, `style`, `composition`, `first_frame`, `last_frame`, `motion`, `audio`.
- For `edit_existing`, omit `aspect_ratio` unless a format change was asked. `social_post` defaults to 4:5; other tasks to 1:1.
- `reference_images`: up to the schema limit. Each must be a URL the connection owns or a public URL (see `media-inputs.md`).
- `aspect_ratio`, `quality_tier`: values depend on the model (`get_model_info`); the schema has no fixed list. An unsupported value returns `constraint_violation` with `allowedValues`.
- `attach_brand_logo: true` adds the business logo from the brand kit.
- `product_identity` / `product_subject`: lock a product's look across images.
- `output_format: "gif"` with `gif_frame_count` and `gif_frame_duration` for an animated GIF.
- `transparent_background: true` for a cut-out-ready image.
- Omit `model_id` unless the user named one.

Pitfalls:
- Image models invent unreadable text on signs. Say "no writing anywhere except …" and quote the exact text you want.
- Watch for real brand logos or badges in generated scenes (cars, phones). Ask for logo-free, invented brands.
- A second reference image can leak its background. Use one reference per role, or crop it first.

## remove_background

`reference_images` with exactly one image URL. `output_format` PNG (default), WEBP or JPG; JPG loses transparency. Use it before compositing a product onto a new scene.

## gen_storyboard

- `mode`: `storyboard` (narrative arc), `carousel` (`carousel_layout`: `content` for a marketing swipe with typography, `product` for one subject), `moodboard` (same look, different subjects).
- `num_images` 1–9, `resolution`, `aspect_ratio`, `reference_images` with `reference_roles` for identity lock, `style`, `attach_brand_logo`.
- Priced per frame and higher at 2K and 4K, so always quote first.
- Async. Frames are not available in the same turn. Poll `get_generation_details`, or find the finished frames later with `list_assets`. Don't chain `schedule_post` in the same turn.
- One multi-panel sheet (character sheet, product sheet) is a single `gen_image`, not a storyboard.

## edit_storyboard_scene

`storyboard_id`, `scene_order` (1–9), `action` (`edit`, default, needs an `instruction`; or `reroll`, billed at the frame tier). Paid and synchronous. Works only after the storyboard has finished rendering.

## gen_video

- Required: `prompt`, `task_type`. The `task_type` description in the schema is the live routing table (text-to-video, image-to-video, video-to-video, upscale, and their routes).
- Prompt: English production direction. Open with the camera move and the main action. One move with a stated endpoint beats several. Set length with `duration`, not in the prompt.
- `source_url`: required for `image_to_video`, `video_to_video` and `video_upscale`.
- `end_frame_url`: first + last frame pair where the model supports it.
- `reference_images` / `reference_videos` / `reference_audios` with `reference_roles`.
- Brand Elements go in `element_ids` (see `media-inputs.md`). `elements` is a different, model-specific field (up to 4 objects with a frontal image); don't put brand element IDs in it.
- `multi_prompt_segments`: per-shot prompts. Needs an explicit compatible `model_id`, and the segment durations must add up to `duration`.
- `aspect_ratio` defaults to 16:9. Set 9:16 for vertical ads.
- `generate_audio`: only on models whose live info says audio is a toggle. Leave unset on always-audio models.
- `keep_original_sound`: preserve a source clip's audio on source-video modes.
- `video_operation`: `edit` / `reference` / `extend`. For `extend`, `duration` is seconds **added**.
- `quality_tier`: defaults low on fast and image-to-video routes. Set `720p` when the user asks for higher quality, or the tier they name.
- `draft: true`: cheap 480p preview, only for text-to-video and image-to-video, on a model that supports drafts. Upgrade the same take with `render_video_draft`.
- `cost_priority: "lowest"` only when the user asks for the cheapest option.

Pitfalls:
- Some models burn subtitles into speech clips. Prompt "no subtitles, no on-screen text".
- Check hands and props frame by frame. Trimming past a warp is free (adflex-video-edit); regenerating is not.
- An unsupported `aspect_ratio` returns `constraint_violation` with the allowed values. Retry with one of them.

## render_video_draft

Pass the `tool_call_id` of an approved `gen_video` draft. It renders the same take at 1080p under a new quote. Async.

## gen_genjutsu

- `source_url`: an owned clip (import a public Reel with `import_web_video` first).
- `reference_images`: 1–10 owned images (`import_web_image` or the upload tools).
- `mode`: `recast` for a character, `swap` for objects, products or clothing.
- `audio_mode`: `source` (default, keeps the clip's sound) or `silent`, only when the user asks for silence.
- `prompt` (optional direction) and `quality_tier` (optional, billed).
- Always returns an exact quote and needs an explicit yes, even for small jobs.
- A general style change is `gen_video` on a supported video-to-video model instead.

## gen_voiceover

- `text`: the exact line. Always pass `model_id` (an exact voice model from `get_model_info`) and the `voice_id` from `search_voices`. One fixed `voice_id` per speaker for the whole video.
- `search_voices` requires that `model_id` and filters by `language_code`, accent and gender.
- `performance_direction`: a short delivery cue only (warm, slower, smiling), up to 80 characters on most models and ignored on some. Never put wording, language or timing in it; the voice may read it aloud.
- `language` is `en`, `ar` or `auto`; a regional Arabic needs `language_code`. `speed` (0.7–1.2) is advisory. `voice_style` as the schema allows.
- Returns `audioUrl` and `durationSeconds`. Use those to size the matching video clip.
- A `fish_` voice ID only works with its own model family, and cannot enter a voice changer.

## gen_music

- Prompt mode: `prompt` (mood, instrumentation, tempo, progression) with `duration_seconds`, `instrumental`, `lyrics`, `vocal_language`. Defaults to 30 s instrumental.
- Plan mode: `composition_plan` alone; it excludes all of the above.
- Ask for an instant start and a clean ending stab at a given second. Check where it really goes silent before cutting to it.

## gen_sound_effect

`prompt` describing one effect, `duration_seconds`, `loop`, `prompt_influence`. Cheap; make one per effect. Async: it returns a queued record and the audio appears later, so poll `get_generation_details`.

## enhance_prompt

`rough_prompt`, `target_use` (required: `image` or `video`), `mood`, `brand_voice`. Free prep. Use the output as the `prompt` of the paid call, and show it to the user only if they asked.

## gen_document

A PDF from supplied content (menu, catalog, price list, one-pager). Needs a stable `operation_id`. The link expires in about seven days and the file is not added to My Assets. No DOCX or PPTX.

## Lookups (free)

- `get_model_info`: limits, tiers, aspect ratios and audio support of a model.
- `list_my_generations` / `get_generation_details`: past jobs and their outputs.
- `list_assets`: the business library; search by prompt words. A date-only search covers recent items only.
- `search_voices`, `list_brand_elements`, `get_brand_kit`, `get_business_context`, `recall_context`.
