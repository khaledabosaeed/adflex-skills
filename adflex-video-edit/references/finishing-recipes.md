# Finishing recipes

`tools/list` is authoritative for parameter names and limits. All tools below are zero user credits and take a stable `operation_id`.

## import_web_video

- `url`: the exact Instagram Reel, YouTube video/Short, or direct `.mp4` link.
- `purpose`: `import` when you'll edit it, `inspect` when the user asks a visual or structural question (pass it as `question`).
- Returns an AdFlex-hosted URL, native measurements and a `tool_call_id`. Reuse them; never import the same source again after a timeout.
- TikTok links aren't a supported source (the import takes Instagram Reels, YouTube, direct MP4/MOV/WebM files). Ask the user to download the file and upload it (see adflex-generate media inputs, or `create_upload_link`).
- Feeds and search pages can't be scrolled. Ask the user for the exact link.

## import_web_image

A public image URL in, an owned reference still out. Use before `gen_genjutsu`, `gen_image` references, or `gen_video` references.

## assemble_video_clips

- `video_urls`: exact owned URLs in play order.
- `video_urls`: 1–6 clips. The same URL may appear twice in a normal join (not in `master` mode).
- `clip_trims`: one entry per clip, `start_seconds` (required) and `end_seconds` (optional, end exclusive). A single trim needs exactly one URL, one trim and an explicit `audio_mode`, or it is refused.
- `audio_mode`: `preserve` keeps each clip's sound; `silent` drops it. **A join without `audio_mode` comes out silent**, so always set it.
- Canvas: a single-clip trim keeps the source frame when `aspect_ratio` and `resolution` are omitted. A multi-clip join is re-encoded to 30 fps at **720p by default**, with the first clip's aspect ratio; pass `resolution: "1080p"` to keep full HD.
- Length: up to 180 s for a normal join. `finishing_mode: master` joins 2–6 distinct clips of up to 180 s each into up to 600 s.
- Size: about 100 MiB per clip, 300 MiB in total, 200 MiB output.
- Re-encodes picture and audio. No AI generation, no new shots.

## remove_video_audio

- `video_url`: an owned video.
- Picture packets are copied and verified unchanged.
- An already-silent source returns its original URL with no new file.

## mix_audio_to_video

- `video_url`: an owned video. The full picture is kept.
- `tracks`: 1–8 delivered audio tracks. Each has `audio_url`, `role`, `start_seconds` (cue), `gain_db`, optional `source_start_seconds` / `duration_seconds` to use part of the track, and `fade_in_seconds` / `fade_out_seconds`.
- `duck_music_under_voice`: lowers music tracks while a voice track plays.
- `source_audio_mode`: required. `preserve` keeps the original sound under the tracks (level with `source_audio_gain_db`); `replace` removes it.
- `preserve` fails with `source_audio_unavailable` when the video has no sound; use `replace` then. `source_audio_gain_db` (-60 to 12) works only with `preserve`. Track gains also run -60 to 12.
- Gains are explicit dB values; there is no loudness normalization. The mix is peak-limited, and withheld if clipping remains. Lower gains and retry.

Starting levels that work:
- Voice: 0 dB.
- Music bed under speech: about -20 dB, with ducking on.
- Music alone (no voice): about -6 dB.
- Sound effects: -6 to -10 dB, cued on the cut or hit.

## mux_audio_to_video

- `video_url`, `audio_url`. `audio_url` may also be a video delivered in this conversation, to reuse its soundtrack (for example an imported Reel).
- `duration_mode`: required. The supplied audio always replaces the video's soundtrack; there is no mix here.
- Limits: video (or an audio-bearing video) up to about 100 MiB, an audio file up to about 30 MiB; codecs must copy into MP4.
  - `source_audio` keeps the soundtrack's full length and refuses a picture shorter than it.
  - `shortest` ends at the shorter stream and may cut picture or sound.
- To keep a full picture under shorter narration, use `mix_audio_to_video` instead.

## extract_video_frame

- `source_url`: an owned video, or a video file from the business upload library.
- `position`: `first`, `last`, or `time` with `time_seconds` (up to 180, clamped to the video's length).
- Returns a PNG `imageUrl` at the video's frame size.

## Recipes

**Trim a Reel and post it**
1. `import_web_video` (`purpose=import`).
2. `assemble_video_clips` with that URL, one trim, `audio_mode=preserve`.
3. Hand the result URL to adflex-social-publish.

**Narrated video from silent shots**
1. Shots exist (adflex-generate `gen_video`), voiceover exists (`gen_voiceover`, one voice).
2. `assemble_video_clips` the shots with `audio_mode=preserve` (or silence).
3. `mix_audio_to_video` with each voice line cued at its shot start (0 dB) and a music bed at -20 dB with ducking, `source_audio_mode=replace`.

**Talking clips joined into one ad**
1. Each talking clip delivered with its own speech.
2. `assemble_video_clips` with `audio_mode=preserve`, trimming dead air at both ends of each clip.
3. Optional: `mix_audio_to_video` with a music bed, `source_audio_mode=preserve`, ducking on.

**Replace a song on a clip**
1. `remove_video_audio` is optional: mux always replaces the existing soundtrack with the one supplied.
2. `mux_audio_to_video` with the song, `duration_mode=shortest` if the song is longer and should end with the picture.

**Seamless next shot**
1. `extract_video_frame` with `position=last`.
2. adflex-generate `gen_video` with `source_url` = that `imageUrl`, `task_type=image_to_video`.

**Cut past a flaw**
1. `inspect_video` (or `extract_video_frame` at a few times) to find where the warp, extra person or dead air starts and ends.
2. `assemble_video_clips` with a trim that leaves it out, `audio_mode=preserve`.
3. For a flaw in the middle, pass the same URL twice with two trims (before and after); a repeated source is allowed in a normal join. Check that no word is cut at the join.

**Tighten a talking clip**
1. Trim the silence before the first word and after the last.
2. Don't end a trim inside a word. Leave a short tail after the last word, and let it run into the next shot when joining.

**Redo one beat so it matches**
1. `extract_video_frame` with `position=time` at the second just before the beat.
2. adflex-generate `gen_video`, `task_type=image_to_video`, `source_url` = that frame (quoted and approved).
3. `assemble_video_clips`: the old clip up to that second, then the new clip.

**Clips for a beat-cut reel**
1. One trim per clip, each the length of the cut (for example 1.2 s), taken from the cleanest part of the clip.
2. `assemble_video_clips` in order, without the clips' own sound when the music replaces it, then `mux_audio_to_video` or `mix_audio_to_video` for the music.
3. End the picture on the music's last hit, not after it.

## Outside these tools

Check `tools/list` first; the server may have added it. As documented here, the finishing tools cut, join, mute, mix, mux and grab frames. They don't burn in captions or titles, overlay a picture-in-picture, change speed, grade colour or normalize loudness. For those, say so plainly and offer the options: a Workflow assembly node if `get_workflow_capabilities` lists one that does it, or a local ffmpeg edit when the user has file access and wants it. Don't claim an edit was done that wasn't.

## After lost context

Find earlier outputs with `list_my_generations` / `get_generation_details`. `get_generation_details` includes the finishing context of an owned recorded call.
