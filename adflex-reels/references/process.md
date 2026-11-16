# Production process

Paths are relative to the content repo root. Without the repo, create the same structure in a folder the user picks.

## 1. Brief

1. Pick the type: `ad`, `social` or `hero`. The folder is `videos/<type>/<slug>/` and matches `type` in `brief.md`.
2. Copy the templates (`templates/new-video/` in the repo, or `templates.md` here) into the folder.
3. Fill the **goal, audience and channel** first. Ask the team for anything unknown; don't guess.
4. Set `adflex_account` (prod for anything public), `format`, `language`, `characters`, `cta`.
5. Before using a recurring character, read `characters/<name>.md` (look, reference links, voice, prompts) and `characters.md` here.
6. Add the video's row to the repo `README.md`.

## 2. Reference

1. Check the existing lists first: `references/<type>/README.md`, `motion-styles/`, past videos' `production.md`.
2. If the team sent a link: `import_web_video` (`purpose=inspect`), then `inspect_video` for a shot-by-shot breakdown. Free.
3. Add a row to `references/<type>/README.md`. For a strong one, add `references/<type>/<slug>.md` with the breakdown, why it works, and what you'll keep and change.
4. Keep: idea, structure, pacing, motion style. Change: story, characters, footage, music, logos.

## 3. Motion styles

1. Pick styles from `motion-styles/README.md` that fit the type.
2. If the reference has a reusable style, copy `templates/motion-style.md` to `motion-styles/<slug>.md`, fill in the breakdown, paste-ready prompt wording and edit recipe, and add it to the index.
3. List the chosen slugs in `brief.md` `motion_styles`, and add the video to each style's `used_in`.

## 4. Script and shot list

1. Write the shot table in `production.md`: time, picture, motion, line/sound. Use the styles' prompt wording.
2. Spoken lines: dialect, AdFlex first, short. Keep supplied Arabic exactly.
3. End on the brand end card (see `brand.md`).
4. Shape it with `video-types.md`: the structure and shot lengths that worked for this type.
5. Check the story against the reference. If one sentence describes both, change the story now; a remake costs a whole video.
6. Add an estimated credit total, built from the shot list (see the budgeting table in `model-lessons.md`). **Get the team's approval** before any paid generation. Set `status: script approved`.

## 5. Stills

1. Generate stills per shot with adflex-generate (`gen_image`; brand elements or character sheets as references).
2. Quote, get a yes, generate. Review with the team.
3. Log every URL in `assets.md` → Stills, with model and cost. Mark rejected ones and why.
4. Check each still for real logos and badges, invented writing, and a leaked background from a reference.

## 6. Animate

1. Animate approved stills only (`gen_video`, `task_type=image_to_video`). Use a 480p draft when motion is uncertain, then `render_video_draft`.
2. Talking shots: the talking-video recipe in adflex-generate.
3. Check each clip frame by frame for warps, extra people and burned-in subtitles. Listen to every spoken line.
4. Fix in this order: trim past the problem, splice a good word, re-grade, then regenerate. To redo one beat, animate from a frame of the existing clip so it matches its neighbours.
5. Log every clip URL and cost in `assets.md` → Clips. Audio (voiceover, music, SFX) goes under Audio.

## 7. Edit

1. Simple cuts and audio: adflex-video-edit (`assemble_video_clips`, `mix_audio_to_video`).
2. Captions, end cards, picture-in-picture screens and Arabic text: local ffmpeg/Pillow scripts saved in `videos/<type>/<slug>/build/` **as you write them**. Reusable helpers go in `tools/`.
3. This skill's `scripts/` has three helpers: `speech_bursts.py` (caption timing and dead air), `beat_grid.py` (beat-synced cuts, where the music ends) and `arabic_text.py` (Arabic text to PNG).
4. Renders go in `renders/` (git-ignored). Finals go to the shared Drive, linked in `brief.md`.
5. Follow `editing-lessons.md`.

## 8. Versions and feedback

1. In `production.md`, add `vN (date): what changed and why`, quoting the team's feedback.
2. Update `status` in `brief.md` and the video's row in the repo `README.md`.
3. Update `cost_credits` in `brief.md`. Say when a version cost 0.
4. Feedback that changes a brand rule (a rejected end-card line, a banned phrase) also goes into `brand/brand.md`.
5. Before calling a cut final, run `release-checklist.md` and list the open items in `production.md`.

## 9. Lessons

Add anything reusable (a model quirk, a prompt that worked, an ffmpeg fix) to `lessons/models.md` or `lessons/editing.md`. Character lessons go in the character's file, and a reusable look or move becomes a motion style.

## Finding lost assets

`list_assets` on the right account, searching by prompt words. Date-only searches cover recent items only. Write the full URL back into `assets.md`.
