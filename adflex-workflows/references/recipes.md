# Workflow recipes

Node type names below are examples the server has used. Confirm each one with `get_workflow_capabilities` before saving a graph.

## One voice across several unscripted talking clips

Use when natural (unscripted) Arabic speech is generated per clip and the voice must match across clips.

1. One video node per clip (Gemini Omni Flash, up to 15 s each, or 10 s with references).
2. Each clip feeds an `audio.voice-changer` node on its video port.
   - The first clip keeps its own track.
   - The others use `voiceRef` = the first clip when the capabilities show voice cloning available; otherwise one house voice for all.
   - A saved AI Influencer keeps its bound `voice_id` in the voice changer of every clip, the first included.
3. `video.merge-audio` with mode `replace` for each clip.
4. Optional `video.assemble` to join them.

A `voice_id` starting with `fish_` can't enter a voice changer. Use the voiceover-per-line recipe in adflex-generate instead.

## Talking product ad

1. Script: dialect lines of 8 words or fewer from supplied facts only (hook, name, product in use, occasion, price, CTA last).
2. One talking clip per line, about 0.6 s per word + 2 s, with a room still (no person) as a reference on every talking shot and a designed first frame per close-up.
3. Up to two inserts from designed stills, each with a sound effect or a converted voice-over line.
4. `video.assemble` with `tightenTails`, `audioFades` and `normalizeLoudness`. Clips should total 1.2–1.4× the final length.

## Template image edit

1. `list_workflow_templates`, pick the image-edit template.
2. `prepare_workflow_draft` with the template, the source image as `sourceAsset` (role `source`, or `product` for a product image), and the instruction.
3. Quote, approve, run, poll.

## Storyboard to clips

1. `image.storyboard` node with storyboard references bound to the product or character.
2. One image-to-video node per frame, fed by the frame output.
3. `video.assemble`, then audio nodes if available.

## When not to use a Workflow

- One clip, one image, one voiceover: adflex-generate.
- A trim, mute or mix of existing media: adflex-video-edit.
- "Every Monday", "keep generating until…", "pause so I can review": not supported. Run separate jobs instead.
