# Layouts and parameters

`tools/list` is authoritative. Prices are from the tool's own description at the time of writing; the quote is the price.

## gen_storyboard

- `mode`: `storyboard`, `carousel`, `moodboard`.
- `text`: storyboard = the story or script; carousel = the subject and concept; moodboard = the vibe. Any language.
- `num_images`: 1–9.
- `resolution`: `1K` (about 60 credits a frame, social-ready, default), `2K` (about 84), `4K` (about 108, print or hero).
- `aspect_ratio`: `1:1`, `3:2`, `2:3`, `4:3`, `3:4`, `4:5`, `5:4`, `9:16`, `16:9`. Always pass it: when omitted it can fall back to 1:1.
- `reference_images`: up to 4, with `reference_roles` (`identity`, `character`, `product`, `brand_mark`, `style`, `composition`, `first_frame`, `last_frame`).
- `carousel_layout` (carousel only): `content` or `product`.
- `generated_master_role` (carousel only): how a generated first slide anchors the rest: `style`, `identity`, `product` or `character`.
- `style`: a few words to two sentences of design direction.
- `attach_brand_logo`.
- Async. The result comes later.

## Slide structures

**Content carousel (5 slides)**
1. Hook: the claim or question, big.
2. The problem, or the first point.
3. The second point.
4. Proof or the offer.
5. CTA.

**Product carousel**
1. Hero shot.
2. Detail or texture.
3. In use.
4. Scale or what's included.
5. Price or CTA, only if supplied.

**Storyboard**
Setup, rising action, climax, close. One beat per frame, with the framing named (wide, medium, close).

**Moodboard**
One aesthetic across different subjects: palette, light, texture, typography feel.

## Keeping the subject the same

- Pass the product or character as a reference with its role. Without one, set `generated_master_role` so slide 1 anchors the rest.
- Keep style references separate from identity references.
- For an exact product, use the owner's photo as `product`.
- Reference support doesn't guarantee an identical label. Check it.

## Text on slides

- Give the exact words for each slide. Short lines survive best.
- Arabic: check joining, order and digits on every frame.
- A slide with wrong text is an `edit_storyboard_scene`, not a new set.

## edit_storyboard_scene

`storyboard_id`, `scene_order` (1–9), and `action`: `edit` (default; needs an `instruction` saying what to change) or `reroll` (a fresh take, billed at the frame tier). Paid and synchronous, and only after the set has finished rendering. Changes one frame only; the others keep their URLs.

## Finding frames later

`list_assets` with `kinds: ["storyboard"]`. Each frame has its own item (parent plus scene order) and its own URL.

## Posting

- adflex-social-publish `schedule_post`: `media_urls` = the frame URLs in scene order, 2–10 for a carousel.
- Instagram feed images must sit between 4:5 and 1.91:1. 9:16 frames are refused for a feed carousel.
- An animated GIF publishes only on X and LinkedIn.

## Turning frames into video

Each approved frame can be a first frame: adflex-generate `gen_video`, `task_type=image_to_video`, `source_url` = the frame. For many frames under one approval, use adflex-workflows.

## Troubleshooting

| Symptom | Do this |
|---|---|
| "Still running" | Poll `get_generation_details`. Never start it again |
| Frames not found | `list_assets` with `kinds: ["storyboard"]` and words from the text |
| Subject changes between slides | Add an identity or product reference, or set `generated_master_role` |
| Wrong or garbled words on one slide | `edit_storyboard_scene` with the exact text |
| Feed refuses the ratio | Regenerate at 4:5, or post as stories |
| User wants one image with several panels | That's one `gen_image` with a reference sheet, not a storyboard |
