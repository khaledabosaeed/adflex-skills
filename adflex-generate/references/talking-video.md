# Talking video

Recipes the AdFlex server recommends for people speaking on camera. Confirm current model IDs with `get_model_info` before using them; the server's own instructions win if they differ.

## Approval of the line

Show the exact prepared line together with the production summary and the credit quote, in one confirmation. Keep that line unchanged when confirming. A changed line needs the new line and a new quote approved.

## Writing product speech

- Use the product form and method of use the user gave or a verified source states. A serum is applied, not drunk.
- Subjective marketing is fine. Don't invent facts about use, health, ingredients, dosage or results.
- Keep any line the user supplied word for word.
- A talking product ad is script first: short dialect lines of 8 words or fewer, built only from supplied facts. Order: hook on the strongest fact, name and label, product in use, occasion, price, CTA last. No greeting or filler.

## Case 1: one exact Arabic line, one clip, no specific voice

One `gen_video` on Gemini Omni Flash (currently `gemini_omni_flash_1_2`), with the line quoted word for word once.
- Up to 15 s, or 10 s when reference images or videos are attached.
- Add tashkeel and a romanization hint for tricky words, and give a 4 s line about 5 s.

## Case 2: a script with several lines, or a specific voice

1. `gen_voiceover` per sentence (join lines under 4 words), one fixed `voice_id` per speaker.
2. One `gen_video` per line on the model the server names for audio-driven speech (currently `wan_3_0`):
   - the line's `audioUrl` in `reference_audios`, the speaker image in `reference_images`;
   - `duration` about the delivered `durationSeconds` + 1 s (audio up to 15 s per clip);
   - prompt: `Starting on the first frame the speaker says, in the voice and timing of Audio 1: "<line>"; then a silent closed-lip smile; no other dialogue, music or subtitles.`
3. Fill extra length with 2–5 s shots without speech. Change framing between speaking shots.
4. Join with `assemble_video_clips`, `audio_mode=preserve` (adflex-video-edit).

## Case 3: narration with no visible speaker

One `gen_voiceover` voice for every line, laid over silent `gen_video` shots with `mix_audio_to_video` (adflex-video-edit). Never native narration per clip, because the voice drifts between clips.

## Case 4: unscripted natural Arabic speech

Omni clips of up to 15 s from text or one opening frame (10 s with references, a first+last frame pair, or an extension). To keep one voice across several clips, use a Workflow (adflex-workflows) where each clip feeds a voice changer and audio is merged with `replace`.

## Talking product ad, shot plan

- One line and one action per Omni clip. Length about 0.6 s per word + 2 s.
- A size or angle change between talking shots.
- One room still (no person) as a reference on every talking shot, and a designed first frame for each close-up.
- At most two inserts from a designed still, never silent (a sound effect or a voice-over line).
- Assemble with tightened tails, audio fades and loudness normalization. Clips should add up to 1.2–1.4× the final film.

## Pronunciation and pacing

- Write brand and foreign names in the script's own letters, the way they should sound: AdFlex as «أدفلكس», Claude as «كلود». Add tashkeel to words a model could read two ways, and a romanization hint in the direction ("pronounced ad-fleks").
- A name at the very start of a phrase can pick up an extra vowel. Put a word before it when the line allows.
- Budget about 8 words for a 6 s clip. Give a 4 s line 5 s. A crowded line gets rushed or cut off.
- Describe the voice once (timbre, age, energy, accent, and what it is not) and paste the same wording into every clip of that speaker. Rewording it changes the voice.
- Say the dialect by name ("everyday colloquial Palestinian Levantine Arabic, not MSA").

## When a take is wrong

Fix in the cheapest way that works, and say which you chose:

1. **Dead air or a warp at either end:** trim it (adflex-video-edit, free).
2. **One word wrong:** drop the phrase if the line survives without it, or regenerate only that line. Never the whole video.
3. **One beat of a longer scene:** `extract_video_frame` at the second just before it, then `gen_video` image-to-video from that frame. The set, light and speaker match the shots around it.
4. **Burned-in subtitles:** re-prompt with "no subtitles, no on-screen text".

A retake is a new paid call: new quote, new yes.

## Accents

Cast Gulf speech with a matching accent: `search_voices` accent `kuwaiti` for a Kuwaiti audience, otherwise `gulf`; `saudi` is a separate dialect. For Levantine, search by Levantine accent. A brand or story film can add one `gen_music` bed about -20 dB under speech with ducking.

## Check the result

Speech-to-text is a check, not proof: it hears brand names wrong ("AdFlicks"). Listen to every line before delivering, or ask the user to.
