# Model lessons

From the team's productions. Costs are what was observed; always use the live quote. If the content repo has `lessons/models.md`, it is newer than this copy. Confirm any model's limits with `get_model_info` before relying on a line here.

## Images

- **Nano Banana 2** (about 60–70 credits): best for character consistency (`task_type: character_consistency`, a character sheet as reference).
  - Invents gibberish Arabic on signs. Say "no writing anywhere except …".
  - Sometimes adds real brand badges (a pickup came out as a Toyota). Check and paint them out.
  - A second reference image can leak its background: a pier photo pulled a modern skyline into an old-town scene. Use the sheet plus a still from the right setting.
- **GPT Image 2.6 Sunburst** (about 70 credits): best for edits that keep the photo and change one thing, such as filling a blank billboard or rebranding a cup (`task_type: edit_existing`, first frame + brand mark). Handles Arabic text well.

## Video

- **Gemini Omni Flash 1.2:** the go-to model.
  - Talking heads with native audio: write lines with tashkeel and romanization hints; give a 4 s line 5 s. 6 s fits about 8 words.
  - Watch for burned-in subtitles; remove them in the edit.
  - Text-to-video with a product sheet as reference keeps labels readable.
  - Handles multi-shot prompts ("exactly four hard-cut shots, ~2 s each").
  - Kept a character's likeness and a banner consistent across clips better than the alternatives tried.
  - Roughly 500 credits for 8 s at 720p, 315 for 5 s at 720p, 630 for 10 s, 360–460 per 1080p plate.
- **Wan 3.0 Prime:** about 110 credits/s at 720p, image-to-video, no audio. 3 s is enough for cuts of about 1.2 s. A render took about 5 minutes.
- **Kling Video O3 Standard** (about 75 credits/s): works with `image_to_video` + one `source_url` + `multi_prompt_segments`. **Fails immediately (and refunds) when character `elements` are passed.**
- **Seedance 2.5:** used for a UGC video (14 s, 480p draft, about 1,260 credits).
- Check hands and props frame by frame. Trimming past a warp is free; regenerating isn't.
- Fast action can add a person or limb for a few frames. Look at the frames right after the big move.

## Redo one shot, not the scene

To change one line or beat in a finished cut, take a frame from the existing clip (`extract_video_frame` at the right second) and run image-to-video from it. A payoff line was replaced this way for the price of one 5 s clip, and the set, light and actor matched the surrounding shots.

## Audio

- **Music:** 25–80 credits per track. Ask for an instant start, a clean final stab at a given second, and the BPM. Then measure where it really goes silent and what the tempo really is.
- **SFX:** about 6 credits each.
- **Voiceover:** the Levantine voice "Laloosh" was used for a UGC reel. Find voices with `search_voices`.

## STT is a check, not proof

STT heard "AdFlicks" and "Cloud" on takes that sounded right. Always listen to the line yourself.

## Budgeting a video

Give the team an estimate with the script, before any generation. Build it from the shot list, then compare it with these totals.

| Video | Type | Length | Credits |
|---|---|---|---|
| Talking presenter reel with chat demo | ad | 45 s | about 10,150 |
| Family mini-drama, many versions | ad | 40 s | about 9,000 |
| Mascot narrator reel | ad | 42 s | 6,311 |
| UGC duet reel | ad | 48 s | about 4,370 |
| Agent demo reel | ad | 24 s | 3,072 |
| No-dialogue character reel | social | 13 s | 3,673 |
| No-dialogue comedy reel | social | 20 s | about 3,400 |
| Website hero, first attempt | hero | 17 s | about 4,700 |
| Website hero, remake | hero | 17 s | about 3,770 |
| Swap-tool promo | hero | 20 s | 1,578 |

What the totals teach:
- Clips are most of the bill. Stills and audio are small.
- Retakes add up: in one reel, retakes and a three-times-repeated scene cost more than a third of the total.
- Every version after the first that only re-cut, re-graded, re-captioned or re-mixed cost 0. Try the edit fix first.
- A remake because the story sat too close to the reference cost a whole second video. Settle the story at the script stage.
