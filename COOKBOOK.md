# Cookbook

End-to-end recipes that chain the skills. Each paid step is quoted and approved first.

## 1. Product photo to posted reel

1. **adflex-generate:** `gen_image` (`task_type=edit_existing`) to place the product in a clean scene. Approve.
2. **adflex-generate:** `gen_video` (`task_type=image_to_video`, `source_url` = the still, `draft: true`). Approve the motion, then `render_video_draft`.
3. **adflex-generate:** `gen_music` for a 10 s bed.
4. **adflex-video-edit:** `mix_audio_to_video` with the music at -6 dB, `source_audio_mode=replace`.
5. **adflex-social-publish:** `list_social_accounts` → `draft_post` (`post_type=reel`) → `schedule_post` preview → `confirm: true`.

## 2. Arabic talking product ad (scripted)

1. **adflex-generate:** `read_creative_references` on the product page for facts.
2. Write lines of 8 words or fewer; show them with the quote.
3. `search_voices` (accent to match the audience) → `gen_voiceover` per line, one `voice_id`.
4. `gen_image` for the speaker and a room still.
5. `gen_video` per line with the line's `audioUrl` in `reference_audios` (see `adflex-generate/references/talking-video.md`).
6. **adflex-video-edit:** `assemble_video_clips` with `audio_mode=preserve`, then `mix_audio_to_video` with a music bed at -20 dB and ducking.

## 3. Adapt a viral reel

1. **adflex-video-edit:** `import_web_video` (`purpose=inspect`) → `inspect_video` for a shot list.
2. Keep the structure and motion style, change story, characters and music.
3. **adflex-generate:** stills per shot → `gen_video` per shot.
4. **adflex-video-edit:** `assemble_video_clips`.

## 4. Swap our product into a reel

1. **adflex-video-edit:** `import_web_video` (`purpose=import`).
2. **adflex-generate:** `import_web_image` or upload the product photos.
3. **adflex-generate:** `gen_genjutsu` (`mode=swap`, 1–10 `reference_images`). Approve the quote.

## 5. Carousel post

1. **adflex-generate:** `gen_storyboard` (`mode=carousel`, `carousel_layout=content`, 5 frames). Approve.
2. Wait for frames (`get_generation_details`).
3. **adflex-social-publish:** `schedule_post` with `media_urls` in order, `timezone`, preview → `confirm: true`.

## 6. Multi-clip production as one job

1. **adflex-workflows:** `get_workflow_capabilities` → `prepare_workflow_graph` (clips → voice changer → merge audio → assemble).
2. `quote_workflow_run` → show the quote → `run_workflow` with `confirm: true` and `confirm_credits`.
3. Poll `get_workflow_status`; recover failed steps with `prepare_workflow_recovery`.

## 7. Monthly performance check

1. **adflex-social-publish:** `get_post_insights` (`focus=top_posts`, `period_days=30`).
2. Report from the returned sample only, and suggest one test for next month.

## 8. Fix one line in a finished talking ad

1. **adflex-video-edit:** find the flaw (`inspect_video`, or listen). Dead air or a warp at the edge: trim it and stop here.
2. **adflex-video-edit:** `extract_video_frame` (`position=time`) just before the bad beat.
3. **adflex-generate:** `gen_video` (`task_type=image_to_video`) from that frame with the corrected line. Quote, approve.
4. **adflex-video-edit:** `assemble_video_clips`: old clip up to the frame, new clip, then the rest.

## 9. Beat-cut no-dialogue reel

1. **adflex-generate:** stills per gag with one look block and the character sheet as reference. Approve.
2. **adflex-generate:** `gen_music` with the BPM and a final hit at a stated second; `gen_video` about 3 s per shot.
3. Measure the delivered track's real beat grid and ending (adflex-reels `scripts/beat_grid.py` when working locally).
4. **adflex-video-edit:** trim each clip to the cut length, `assemble_video_clips`, then put the music on. End on the last hit.

## 10. Product page to UGC ad

1. **adflex-brand:** `read_creative_references` on the product page.
2. **adflex-product-photo:** a clean product still from the owner's photo (`edit_existing`).
3. **adflex-talking-ad:** script from the facts → `search_voices` → `gen_voiceover` per line → one clip per line driven by its audio.
4. **adflex-video-edit:** `assemble_video_clips`, then music under the voice.
5. **adflex-social-publish:** draft → preview → confirm.

## 11. Put our product into a trending reel

1. **adflex-video-remix:** `import_web_video` → `gen_genjutsu` (`mode=swap`) with the product stills. Approve the quote.
2. **adflex-video-edit:** trim to the best part.
3. Check the rights to the source clip before posting it.

## 12. Old menu to branded PDF and a post

1. **adflex-documents:** `read_document` (`extract: products`) on the old PDF link → confirm the items → `gen_document`.
2. **adflex-carousel:** a 4-slide menu carousel from the same items.
3. **adflex-social-publish:** schedule the carousel.

## 13. New AdFlex reel (content team)

1. **adflex-reels:** create `videos/<type>/<slug>/` from the templates and fill the brief.
2. Break down the reference, pick motion styles, write the script, get approval.
3. Stills → animate → edit, logging every URL in `assets.md`.
4. Record the version and feedback; add lessons.
5. Run `adflex-reels/references/release-checklist.md` before calling it final. Posting is a separate, explicit request.
