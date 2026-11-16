---
version: 0.1.0
name: adflex-talking-ad
description: |
  Plan and produce a spoken video ad through the AdFlex MCP connector:
  a UGC-style product ad, a presenter or spokesperson clip, a narrated
  product film or a short multi-shot film, with one consistent voice,
  matched lips and a clean final cut. Strong on Arabic dialects.
  Use when: "make a UGC ad for this product", "a girl talking about
  our perfume", "talking head ad", "spokesperson video", "narrated
  product video", "ad with a voiceover", "30 second ad with dialogue",
  "make her say this line", "lip sync this audio". Chain with adflex-brand
  for product facts, adflex-product-photo for the product still,
  adflex-video-edit to finish, adflex-social-publish to post. NOT for:
  silent clips or single images (use adflex-generate), swapping a
  person in an existing video (use adflex-video-remix), or AdFlex's
  own team reels (use adflex-reels).
argument-hint: "[product or link] [who speaks] [language/dialect] [length]"
allowed-tools: Bash
---

# AdFlex Talking Ad

Speech decides everything in a talking ad: who says what, in which voice, and for how long. Choose the speech method before spending, then build pictures around the measured audio.

## Step 0: Connection

1. If no AdFlex tools (such as `list_businesses`) are available, ask the user to add the connector, then stop:
   - Claude Code: `claude mcp add --transport http --scope user adflex https://api.adflex.ai/api/mcp`, then `/mcp` to sign in.
   - Other clients: add the HTTP MCP server `https://api.adflex.ai/api/mcp` and sign in.
2. On an auth or scope error, ask the user to reconnect AdFlex with `/mcp`.
3. With more than one business, call `list_businesses` once and pass `business_id` everywhere. Never guess a brand.

## 1. Brief

Get these from context first; ask only for what is missing and changes the result, one at a time:

- **Product facts.** Read the page or PDF (`read_creative_references`, `scan_brand_url`, `read_document`). Never invent use, ingredients, results or prices.
- **Audience and dialect.** The script alone can't tell Gulf from Egyptian from MSA. If the audience is unclear, ask.
- **Speaker.** A supplied photo, a saved brand element, or a new character.
- **Length and format.** Default 9:16.

## 2. Script

- Short lines, 8 words or fewer, built only from supplied facts.
- Order: hook on the strongest fact, name the product, show it in use, the occasion, the price, CTA last. No greeting, no filler.
- Keep any line the user wrote word for word.
- Timed beats, not fixed-length clips: each beat has an action, a line and a reaction.

## 3. Choose the speech method

| Method | Use when | How |
|---|---|---|
| **Native dialogue** | One exact line, one clip, no specific voice needed | One `gen_video` that speaks the line |
| **Supplied speech** | Several lines, or a specific voice | `gen_voiceover` per line, then one `gen_video` per line driven by that audio |
| **Lip-sync on existing video** | The picture exists and must now speak | A source-video operation the model supports; check `get_model_info` |
| **Narration over footage** | No visible speaker | One voice over silent shots, mixed in the edit |

Narration mixing never fixes lips. Voice identity guidance never promises exact words or timing. Read `references/speech-methods.md` for each recipe and the model notes.

## 4. Produce

1. **Voice.** `search_voices` with a voice `model_id`, filtered by `language_code`, accent and gender. One model and `voice_id` per speaker for the whole ad. A saved AI Influencer brings its own voice; reuse it unchanged.
2. **Stills first.** The speaker and the setting, approved before any clip. One shared sheet only when several shots need the same person or product from new angles.
3. **Measure, then shoot.** Use each line's delivered `durationSeconds` to size its clip (about +1 s).
4. **Coverage.** Change framing between speaking shots: wide, medium, close, reaction.
5. **Finish.** `assemble_video_clips` with `audio_mode=preserve`, trimming dead air; then `mix_audio_to_video` for music at about -20 dB with ducking.

Show the script, the plan and the credit quote together, once. For more than a few dependent clips that should run under one approval, use adflex-workflows.

## Credits and approval

1. Call the paid tool with a stable `operation_id` and **without** `confirm_credits`. The server runs a small action automatically or returns a quote.
2. Show the quote once with what will be made. Wait for a yes.
3. Repeat the **exact same call** with `confirm_credits` set to the approved amount. A changed prompt, count or quality needs a new quote.
4. `confirm_credits: 0` is a price-only check. After a timeout, reuse the `operation_id` or poll `get_generation_details`; never start the job again.
5. Prices only in AdFlex credits. Never disclose or guess which providers run AdFlex models.

## Rules

- **Approved words stay approved.** A changed line needs the new line and a new quote approved.
- **No paid auditions.** No automatic extra takes, alternates or quality retries. One intended output, then targeted fixes.
- **Reuse.** An approved voice, still or clip is reused, not regenerated. A change invalidates only the shots it touches.
- **Listen.** A transcript is evidence of words, not of accent, natural delivery or lip sync. Say what was checked and what wasn't.
- **Subtitles** are not burned in by these tools. Prompt "no subtitles, no on-screen text" so a model doesn't add broken ones.
- Reply in the user's language and dialect. Prompts in English; every spoken line verbatim in its own script.

## References

- `references/speech-methods.md`: the four speech methods step by step, voice direction, Arabic pronunciation, shot planning and review.
