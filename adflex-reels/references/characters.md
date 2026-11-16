# Characters

Recurring characters keep AdFlex's videos recognizable. The content repo's `characters/<name>.md` files are the source of truth: they hold the reference image links, the account each character lives on, and the newest lessons. Read the file before every use. This page explains how to work with them and what to do without the repo.

## Using a character

1. Read `characters/<name>.md`: look, reference images, voice direction, lessons.
2. Work on the account named in its frontmatter (`adflex_account`). A character sheet saved as a brand element only exists on that business. Find it with `list_brand_elements`.
3. **Paste the look block into every prompt, unchanged.** Don't paraphrase it between shots.
4. Pass the approved character sheet as the identity reference. Add at most one more reference, for the location, and check that it doesn't drag its background into the shot.
5. **Paste the voice direction verbatim** into every talking-clip prompt. Rewording it changes the voice.
6. After the video, add the slug to the character's `used_in` and any new lesson to its Lessons.

## The cast

| Character | Role | Type | Notes |
|---|---|---|---|
| الحجة (Hajja) | Deadpan Gulf grandma influencer | `social` | Purple-magenta abaya with gold geometric stripes, black hijab, gold bangles, sunglasses pushed up, white-and-violet chunky sneakers. Nothing impresses her; that's the joke. Companions: a cheetah on a leather leash, a baby camel with sunglasses and a violet bow. No dialogue. |
| زعتر (Zaatar) | Cartoon tabby cat narrator | `ad` | Olive-green knitted scarf, brown trousers, warm animated-realism look. A photoreal version was rejected. Speaks colloquial Palestinian Levantine. |
| The presenter double | Talking-head tech creator | `ad` | A generated double of a team member, made from their own photo. The photo and good takes live with the team, not in a skill. Handheld selfie framing, Levantine. |

Characters invented for one video (a family, a designer, a caveman) are described in that video's `production.md`, not in `characters/`.

## Voice direction

Write it once per character and reuse it word for word. It names the timbre, age, energy, accent, and what it is **not**.

Mascot example:
> a cartoon-mascot cat voice, light and slightly high-pitched, mischievous and charming with a soft playful rasp and a tiny purr-like warmth on the vowels, quick confident delivery, like an animated film's sidekick cat, not a deep adult narrator. Everyday colloquial Palestinian Levantine Arabic (not MSA).

Presenter example:
> warm, slightly deep male voice, late 20s, Levantine (Palestinian/Jordanian) Arabic accent, energetic, perfectly lip-synced

## Pronunciation

| Word | Write it as | Note |
|---|---|---|
| AdFlex | «أدفلكس» | Said well mid-sentence. At the start of a phrase it picks up an extra vowel, so put a word before it or splice a good take. |
| Claude | «كلود» / «كْلود» | The vowel of "clawed", never "klawd". |
| Hard dialect words | with tashkeel, plus a romanization hint | For example «يْوَلِّد», «المسودة». |

- 6 s of video fits about 8 words. Give a 4 s line 5 s.
- Check every take with speech-to-text, then listen. STT has returned "AdFlicks" and "Cloud" for correct takes, and passed wrong ones.
- A word that keeps coming out wrong is cut from the script or spliced from a good take. That costs nothing; a retake costs a full clip.

## Model notes for characters

- Stills: the character-consistency image route with the sheet as reference holds identity best. Say "no writing anywhere except …" or signs fill with gibberish Arabic.
- Video: Gemini Omni Flash kept a character's likeness and a site banner consistent across clips. Kling O3 Standard failed and refunded when character `elements` were passed; give it one first frame instead.
- Check `get_model_info` before relying on any of this. Models change.

## Adding a character

Use the character template in `templates.md`. A character needs an approved sheet before its first shot: generate the sheet, get it approved, save the URL in the file, and record rejected versions with the reason.
