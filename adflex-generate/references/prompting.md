# Prompting

## Images

- Lead with the subject and what it's doing, then setting, light, lens and mood.
- Quote any visible text exactly, and say where it goes. Add "no other writing anywhere".
- For an edit of an existing photo (`task_type: edit_existing`), describe only the change and say "keep everything else identical".
- For brand work, pull colors and fonts from `get_brand_kit` instead of asking the user, and name the hex values in the prompt.
- Ask for invented, logo-free brands for any product that isn't the user's own.
- For a social post image, design for the target crop (Instagram feed 4:5, story/reel 9:16, landscape hero 16:9).

## Keeping a character or product the same

- Write one look block (clothes, colours, props, expression) and paste it unchanged into every prompt. Paraphrasing between shots drifts the look.
- Make a character or product sheet first (one `gen_image`), get it approved, and pass it as the identity reference from then on.
- One reference per role. A second image added "for the place" often brings its whole background along; use a still that already shows the right setting, or crop it.
- For a product, say what must stay readable ("the label text stays sharp and unchanged").

## Things to check in every result

- Writing that wasn't asked for, especially invented Arabic on signs.
- Real logos and badges on cars, shoes, phones and banknotes.
- Hands, props and faces. In video, look at the frames right after a fast move for an extra person or limb.
- Burned-in subtitles on speech clips.

Trim or re-crop before paying for a new take.

## Video

- Write direction in English. Keep spoken and on-screen strings in their original language, verbatim.
- First sentence: the camera move and the main action, because models weight it most. Example: "Slow dolly-in on the perfume bottle as golden-hour light sweeps across it."
- One camera move with a clear endpoint per clip. Several moves blur together.
- Length goes in `duration`, never in the prompt.
- For image-to-video, describe the motion only. The still already fixes the look.
- For multi-shot prompts on models that support them, say the exact count and lengths ("exactly four hard-cut shots, about 2 s each").
- Add "no subtitles, no on-screen text" unless text is wanted.
- Generate a little more than the edit needs: about 3 s for a 1.2 s cut. The spare lets the editor pick the clean part.
- Name the look once and reuse the wording across shots ("faded 1990s 35 mm film, warm colours, visible grain"), so the clips grade together.

## Storyboards and carousels

- State the arc (setup, rising, climax, close) or the slide purpose per frame.
- Use `reference_images` with roles for the product or character, so every frame keeps the same identity.

## Music and effects

- Music: mood, instruments, BPM, an instant start and a clean final hit at a stated second. Example: "instrumental, oud, darbuka and riq, mellow bass, about 92 BPM, starts instantly, clean final hit at 40 s".
- The delivered track's tempo and ending rarely match the request exactly. Cut to what was delivered, not to what was asked.
- Effects: one effect per call, described physically ("a soft paper whoosh, 0.6 s").

## Rough idea from the user

Run `enhance_prompt` (free) and use its output. Don't show the enhanced prompt unless asked.
