# Editing lessons

If the content repo has `lessons/editing.md`, it is newer than this copy. Scripts named here are in this skill's `scripts/` folder; run them with `--help` for options.

## Before you build

- Save every build script in `videos/<type>/<slug>/build/` as you write it. Scripts left in temporary sessions were lost for every earlier video, and those cuts can't be rebuilt.
- Reusable helpers go in the repo's `tools/`.
- Motion-graphics pieces (titles, cards, end cards) can be built as an HTML page and rendered frame by frame, so one scene can be re-rendered alone.
- Render heavy composites one at a time. Two in parallel ran out of memory.

## Arabic text

- ffmpeg's libass often shapes Arabic badly. Render text to PNG with Pillow + raqm and overlay it: `scripts/arabic_text.py`. ASS with `shaping=complex` and separate RTL lines also works.
- Cairo comes from npm `@fontsource/cairo`. Its Arabic subset has no ASCII digits, Latin letters or punctuation, so times like 8:00 and words like AdFlex need the Latin font (`--latin-font`).
- Wrap mixed Arabic/Latin captions in RTL embedding when a renderer takes one string.
- Read the rendered PNG before using it. Wrong order or unjoined letters are easy to miss in a moving video.

## Captions

- Time each caption to the measured speech in its own clip, not to the whole shot. Captions shown from the start of the shot appeared 1–2.5 s before the line was spoken.
- Measure with `scripts/speech_bursts.py clip.mp4`: it lists the speech bursts (22 dB below the clip's peak) and the dead air at both ends.
- Split a two-part line into phrases, each timed to its own burst. For a payoff, make the second chunk cumulative so the brand name stays on screen.
- Style: white Cairo ExtraBold on a rounded #8738F5 or dark box at the bottom. Over a floating screen box, captions move up (y=762 on a 1920-high frame); with cards around a presenter they sit at the top (y=96).

## Timing

- Trim dead air at both ends of every talking clip. Let a last line's audio tail (about 0.75 s) run into the next shot.
- Don't cut inside a word. Find where the word really ends first: a brand name ran to 6.84 s in an 8 s take, and cutting earlier clipped it.
- A 0.22 s dissolve with an audio crossfade works at narrated joins. Hero videos use hard cuts.
- Beat sync: `scripts/beat_grid.py track.mp3 --every 2` gives the real grid and cut points. It uses `librosa.beat_track`; a raw spectral-flux autocorrelation picked a 3/4-beat subdivision, and a guessed grid (0.453 s against a real 0.605 s) put every cut off the beat.
- End the video just after the track's final hit. The same script reports where the sound really ends.
- Pacing fixes that cost nothing: narration at 1.07×, plates sped up 1.2–1.8× with `setpts`, a poster shot slowed to 0.77×, pauses trimmed.
- A repeated or fluffed word inside a take: cut it and cover the jump with a punch-in.

## Audio

- Targets: about -14 LUFS for social, -16 LUFS for voice-led reels, limiter at 48 kHz. Measure the final file: `ffmpeg -i out.mp4 -af loudnorm=print_format=summary -f null -`.
- Set a fixed gain per clip first (voice at -16 LUFS, montage at -17), then limit. Don't normalize each clip blindly.
- Duck music under voice with `sidechaincompress` (threshold 0.025, ratio 5, attack 25 ms, release 350 ms). Music at -5 dB then sits 10–12 dB under the voice while someone speaks. With AdFlex's `mix_audio_to_video`, use `duck_music_under_voice` and a bed around -20 dB.
- Raise the music on the end card (about ×1.7), with a 0.5 s fade in at the start and a 1.5 s fade out.
- To offset a voice track, **prepend silence** (`anullsrc` concat). `adelay` silently failed on a pre-rendered track, and a narration started at 0 s instead of 8 s. Check each start afterwards.
- Pre-render voice trims into separate WAV files. One huge inline filter graph deadlocked ffmpeg.
- If one word is mispronounced, splice a good take of that word from another clip, or cut the phrase.
- UGC takes: light denoise and a soft gate on the pauses.
- Sound effects land on the cut or the hit, not near it.

## Layout

- Screen demo over a talking head: keep the full original take and float the recording as a rounded box over the chest (720×440 layer at y=770 on 1080×1920, white border, shadow, 0.25 s fade in). Shrink close-up takes to 0.76 on a blurred, darkened copy of themselves.
- Cards popping around a presenter: measure the face box first and keep every card outside it. White rounded frame, shadow, ease-back pop.
- In a mosaic or grid, every cell must be a different asset. A still and the video made from it count as the same asset.
- Protect the product with a box mask when luminance-keying.
- Screen masks come from the real bezel shape, not a rectangle.
- Burned-in subtitles from a talking model: remove with `delogo`, or cover with the caption box.
- Skip a warped stretch by starting the clip after it (a laptop warp was skipped by starting at 1.8 s).

## End card

- Order and timing that worked on a 3.2 s card: logo at +0.25 s, headline at +0.6, partner pills at +0.95 / 1.1 / 1.25, URL at +1.6.
- The logo is the hero. Rebuild it at high resolution; don't upscale the small brand-kit PNG.
- Pills read right to left in Arabic layouts. A round «+» badge says "and more" without a banned phrase.
- Light background #F7F5FC with soft #D9C1FB glows at the top and bottom only.

## Look

- One grade across every shot of a reel. A film look used: warm curves, lifted blacks, saturation 0.88, vignette, grain.
- A re-grade is free. If a new shot looks more real than the rest, try a grade before offering a paid re-shoot.
- Transformation effects are clipped to a solid mask of the object, so the flood of colour doesn't spill.

## Report the cut

Write in `production.md`: file name, length, resolution, frame rate, loudness and peak, and which script built it.
