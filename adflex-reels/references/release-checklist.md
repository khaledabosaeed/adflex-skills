# Release checklist

Run this before a cut is called final, and again before anyone publishes it. Every item comes from something that went wrong, or nearly did, in a past video. Write the open items in `production.md` so the next person sees them.

Finishing this list is not permission to post. Publishing still needs an explicit request in the session.

## Brand

- [ ] AdFlex is first in the spoken payoff, in the captions and on the end card. Watch the cut once asking "whose ad is this?".
- [ ] The end card uses an approved line and the real AdFlex logo, not a text wordmark or a "Partner × AdFlex" lockup.
- [ ] Partner chips (Claude, ChatGPT, MCP / «+») are small and equal weight. No «أي موديل», no «أي ذكاء اصطناعي».
- [ ] The CTA is an ad CTA. No "comment X and I'll send the link".
- [ ] Spoken lines are dialect, not MSA.

## Honesty

- [ ] Nothing says or shows that a post was published, scheduled or went live unless it really did. A draft is a draft.
- [ ] Dramatized screens (a "published ✓" tile for a fictional brand) are noted as dramatization in `production.md`.
- [ ] Designed cards are told apart from real outputs in `production.md` (for example "cards 01 and 06 are designed; 02–05 are real outputs").
- [ ] Every product claim is true today. If the cut says the agent does six steps from one prompt, or that AdFlex works inside a given assistant, confirm it with the team first.
- [ ] Screen recordings are real AdFlex UI and real chats, not mockups.

## Screens

- [ ] No recording shows the dev business name. Screens recorded on dev are placeholders: re-record on prod before a public release.
- [ ] What the screen shows matches what the line says. If the line says "scheduled", the screen shows a scheduled post, not a draft.
- [ ] Recording a prompt being typed: don't send it unless the output is needed. Clear the text afterwards.
- [ ] Recording a connect or publish flow: stop before the final click, or cancel the dialog.
- [ ] A scheduled-post screen, when truly needed: schedule it, capture the screen, then cancel it before its time. Only with the team's explicit request, like any scheduling.

## Third parties

- [ ] No real brand logos or badges in generated footage: car badges, shoe marks, phone logos, banknotes. Check frame by frame and paint them out.
- [ ] No third-party footage, watermark-cropped clips or licensed music. A borrowed test clip must be replaced before official use.
- [ ] Third-party marks (the OpenAI knot, a model's product name) are checked against that company's brand guidelines before paid use.
- [ ] The story is our own. Only the reference's idea, structure and motion style were reused.

## Picture

- [ ] Hands, props and faces checked frame by frame. Trim past a warp; don't keep it.
- [ ] No extra limbs or people appearing for a few frames after fast motion.
- [ ] No burned-in subtitles left over from a talking model.
- [ ] In a grid or mosaic, every cell is a different asset. A still and the clip made from it count as one.
- [ ] Arabic text is shaped and ordered correctly, including digits and mixed Latin words.
- [ ] Pop-up cards and captions stay clear of faces.

## Sound

- [ ] Every spoken line listened to by a person. Speech-to-text alone isn't enough.
- [ ] Brand names pronounced right; no word clipped by a cut. Let a last line's tail run into the next shot.
- [ ] Captions appear with the speech, not before it.
- [ ] Loudness measured: about -14 LUFS for social, -16 LUFS for voice-led reels, true peak under -1 dBFS.
- [ ] The video ends on the music's final hit, not in silence.

## Records

- [ ] `assets.md` has the full URL of every still, clip and audio file, rejected ones included.
- [ ] `production.md` has the current cut (file, length, resolution, loudness), how it was built, and the version entry with the feedback quoted.
- [ ] `brief.md` has the new `status` and `cost_credits`. `published` stays `false` until it is true.
- [ ] The repo `README.md` row is updated.
- [ ] Build scripts are saved in `build/`, not left in a temporary session. Earlier videos lost theirs.
- [ ] The final render is on the shared Drive and linked in `brief.md`.
