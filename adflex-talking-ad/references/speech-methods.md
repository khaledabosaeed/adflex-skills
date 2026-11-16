# Speech methods

Confirm model IDs and limits with `get_model_info` before using any named here. The server's own instructions win if they differ.

## Native dialogue (one line, one clip)

- One `gen_video` on a model with native speech (currently Gemini Omni Flash, `gemini_omni_flash_1_2`).
- Quote the line once, word for word. Name the dialect ("in natural Palestinian Levantine Arabic").
- Up to 15 s, or 10 s when reference images or videos are attached.
- Length: about 0.6 s per word + 2 s. Give a 4 s line 5 s.
- End the direction with: "then a closed-lip smile; no other dialogue, music or subtitles."
- Extension can't add new dialogue to an uploaded talking clip. Don't promise it.

## Supplied speech (several lines, or a chosen voice)

1. `gen_voiceover` per sentence (join lines under 4 words), one fixed `model_id` and `voice_id`.
2. One `gen_video` per line on the model the server names for audio-driven speech (currently `wan_3_0`):
   - the line's `audioUrl` in `reference_audios`, the speaker image in `reference_images`;
   - `duration` = the delivered `durationSeconds` + about 1 s. Audio up to 15 s per clip;
   - prompt: `Starting on the first frame the speaker says, in the voice and timing of Audio 1: "<line>"; then a silent closed-lip smile; no other dialogue, music or subtitles.`
3. Fill extra length with 2–5 s shots without speech.
4. Join with `assemble_video_clips`, `audio_mode=preserve`.

## Lip-sync on existing video

The picture already exists. Check that the exact model accepts both the source video and the speech file for this operation. If no exposed operation does, say so; don't substitute a new generated scene and call it lip sync.

## Narration over footage

One `gen_voiceover` voice for every line, laid over silent shots with `mix_audio_to_video` (`source_audio_mode=replace`). Never narration generated natively per clip: the voice drifts between clips.

## One voice across unscripted clips

When natural speech is generated per clip and the voice must match, use a Workflow (adflex-workflows): each clip feeds a voice changer and the audio is merged back with `replace`. A `voice_id` starting with `fish_` can't enter a voice changer.

## Voice direction

- **Cast** by role, dialect, timbre and existing samples. Popularity and gender alone aren't fit. A voice description is not listening evidence.
- **Keep** the same model and voice when the emotion changes. Emotion is direction, not a new voice.
- `performance_direction`: a few plain auditory words (warm, slower, smiling, urgent), under 80 characters. No brackets or markup. Some voice models ignore it. Never wording, language, dialect or timing; long cues get dropped or read aloud.
- Carry emphasis in the text's punctuation.
- `voice_style` picks an identity, not acting.

## Arabic

- Decide the dialect from the audience, not from the script.
- Cast a matching accent: `search_voices` accent `kuwaiti` for a Kuwaiti audience, otherwise `gulf`; `saudi` is separate; search Levantine for Levantine.
- Write brand names the way they should sound, inside a full sentence. A name at the very start of a phrase can come out wrong.
- Add tashkeel only to words a model could read two ways. Don't diacritize everything, and don't insert IPA or SSML.
- A language code or filter doesn't enforce an accent.
- Keep code-switching the user intended ("AdFlex", "story").

## Shot plan for a product ad

- `gen_video` defaults to 16:9. Set `aspect_ratio: "9:16"` on every clip of a vertical ad.

- One line and one action per talking clip.
- A size or angle change between talking shots.
- One room still with no person as a reference on every talking shot, and a designed first frame for each close-up.
- At most two inserts from a designed still, never silent: a sound effect or a voice-over line.
- Shoot 1.2–1.4× the final length, then tighten tails.
- A reference sheet is for identity. Don't use a whole sheet as a first frame; prepare a single scene image for that.

## References and roles

Give each reference its real role: `identity` or `character` for the speaker, `product` for the product, `style`, `composition`, `first_frame`. A URL written in the prompt is not a bound reference; pass it in the reference fields.

## Review

- Check the delivered clip against the request: the right person, the product present and readable, the line spoken.
- `inspect_audio` gives the words heard. It mishears brand names; listen as well.
- `inspect_video` samples frames. It proves neither continuous motion nor lip sync.
- Report what was delivered and any specific gap. No generic quality disclaimer, and no paid retake without a yes.

## Fixing a take

1. Dead air or a warp at an edge: trim (free).
2. One word wrong: drop the phrase or regenerate that line only.
3. One beat of a scene: `extract_video_frame` just before it, then image-to-video from that frame.
