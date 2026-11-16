---
version: 0.1.0
name: adflex-reels
description: |
  The AdFlex content team's process for AdFlex's own social reels, ads
  and website hero videos: brief, reference breakdown, motion styles,
  script and shot list, stills, animation, edit, versions and lessons,
  following the AdFlex brand rules (AdFlex first, dialect not MSA,
  approved end-card lines, Arabic captions). Use when: "new AdFlex
  reel", "make an ad for AdFlex", "AdFlex hero video", "adapt this
  viral reel for AdFlex", "next version of the mcp-reel", "write the
  brief", "break down this reference", "add a motion style", "sync the
  captions", "is this cut ready to publish", or work inside the
  adflex-content repo. Chain with adflex-generate,
  adflex-video-edit and adflex-social-publish for each production step.
  NOT for: content for other businesses or AdFlex customers (use
  adflex-generate directly), one-off images or clips with no brief,
  or posting a finished video (use adflex-social-publish).
argument-hint: "[ad | social | hero] [idea or reference link] [slug]"
allowed-tools: Bash, Read, Write, Edit
---

# AdFlex Reels

Make AdFlex's own marketing videos the way the content team does: everything planned in files, every asset linked, every version recorded. Production runs through the AdFlex MCP tools via adflex-generate and adflex-video-edit, with adflex-talking-ad for spoken shots, adflex-video-remix for swaps and recasts, and adflex-brand for lookups when those are installed.

## Step 0: Context

1. **Content repo.** If the working directory is the AdFlex content repo (it has `CLAUDE.md`, `brand/`, `characters/`, `videos/`, `templates/new-video/`), its files win over this skill: read its `CLAUDE.md` and `README.md` first, then the video's `brief.md`, `production.md` and `assets.md`, and `characters/<name>.md` for any recurring character. Without the repo, use this skill's references and keep the same files in a folder the user picks.
2. **Connector.** If no AdFlex tools are available, ask the user to add `https://api.adflex.ai/api/mcp` (Claude Code: `claude mcp add --transport http --scope user adflex https://api.adflex.ai/api/mcp`) and sign in with `/mcp`.
3. **Account.** AdFlex has a prod and a dev account. Each `brief.md` names which one (`adflex_account`); pass that `business_id`. Public versions are recorded on prod. Account IDs live in the content repo's `CLAUDE.md`; otherwise get them from `list_businesses`.
4. **Local tools.** Editing needs `ffmpeg`, Python with Pillow + raqm, and the Cairo font. If the content repo has `tools/check_setup.sh`, run it. When a task needs a missing tool, say what's missing and how to install it before trying.

## Language

The team writes Levantine Arabic mixed with English. Reply the same way, short. Repo docs stay in English. Arabic lines (scripts, captions) are kept exactly as written.

## Hard rules

- **Credits cost money.** Quote the credit cost and get a yes before every paid generation. Reading, searching, importing and editing existing footage are free.
- **Never publish or schedule** unless a person explicitly asks in this session. Drafts are fine; never call a draft live.
- **Say only what is true.** Don't show or say that something was published, scheduled or done by the product when it wasn't. Note dramatized and designed screens in `production.md`.
- From a reference take the **idea, structure and motion style**, never its story, characters, footage, music or logos.
- **AdFlex comes first** in every spoken line, caption and end card. Claude, ChatGPT and MCP appear small and equal weight.
- End cards say AdFlex works with **the AI you already use**. Never «أي موديل» or «أي ذكاء اصطناعي».
- Ad CTA, not comment-bait.
- Real AdFlex UI and real chat recordings, not mockups. Screens recorded on the dev account are placeholders until re-recorded on prod.
- Only invented or logo-free brands in generated footage. Paint out real badges.

Brand details (logo, colors, fonts, captions, end cards, tone) are in `references/brand.md`.

## Stages

| Stage | `status` in brief.md | Do |
|---|---|---|
| 1. Brief | `idea` | Create `videos/<type>/<slug>/` from the templates; fill goal, audience, channel first. Ask the team what's unknown |
| 2. Reference | `idea` | Import and break down the reference (adflex-video-edit `import_web_video` + `inspect_video`); add it to `references/<type>/README.md` |
| 3. Motion styles | `idea` | Pick styles from `motion-styles/`; save a new one from the template if the reference has one worth reusing |
| 4. Script | `script approved` | Script + shot list in `production.md`. **Get approval before generating** |
| 5. Stills | `stills` | Generate stills first (adflex-generate), review, log each URL in `assets.md` |
| 6. Animate | `animating` | Animate approved stills, log each URL and cost |
| 7. Edit | `editing` | Cut with AdFlex finishing tools or local ffmpeg scripts in `build/`; renders go to `renders/` (git-ignored) |
| 8. Version | `done` | Record the version and the feedback behind it in `production.md`; update `brief.md` and `README.md`; run `references/release-checklist.md` |
| 9. Lessons | | Add anything reusable to `lessons/`, the character file or a motion style |

Read `references/process.md` for each stage in detail and `references/templates.md` for the file templates.

A request can enter at any stage. For "next version of X" or "fix the captions", read the video's three files, do that stage, and record the version. Don't restart from the brief.

## Decision rules

- **Type** decides format: `ad` (presenter/narrator demos AdFlex, ad CTA, 9:16), `social` (no-dialogue comedy reel ending on an AdFlex card, 9:16), `hero` (16:9 website hero or product promo, hard cuts). `references/video-types.md` has the structure, shot lengths and typical cost of each.
- **Estimate before approval.** Give a credit estimate with the script, built from the shot list. Past videos cost 1,600–10,000 credits; see the table in `references/model-lessons.md`.
- **Stills before motion, draft before 1080p.** Never animate an unapproved still.
- **Characters:** paste the look block and the voice direction from the character's file unchanged into every prompt. See `references/characters.md`.
- **Cheapest fix first.** Feedback on a cut is usually an edit: re-cut, re-time, re-grade, re-caption, splice a word. Those cost 0. Regenerate only what an edit can't fix, and redo one shot from a frame of the old clip, not the whole scene.
- **Keep the story ours.** If one sentence describes both the script and the reference, change the story before generating.
- **Model choice:** check `references/model-lessons.md` before choosing a model or writing a prompt; then confirm limits with `get_model_info`.
- **Talking lines in Arabic:** follow adflex-generate's talking-video recipe; add tashkeel and romanization hints, and listen to every line (STT mishears "AdFlex").
- **Editing:** follow `references/editing-lessons.md` (Arabic text rendering, caption timing, loudness, ducking). Use the helpers in `scripts/`: `speech_bursts.py` for caption timing, `beat_grid.py` for beat-synced cuts, `arabic_text.py` for Arabic text PNGs. Save build scripts in the video's `build/` as you go.
- **"Is it ready?"** Run `references/release-checklist.md` and report the open items. A clean checklist is not permission to post.
- **Every asset URL goes into `assets.md` immediately**, including rejected ones with the reason. Find lost ones with `list_assets` on the right account.
- When a reference link can't be imported (TikTok, feeds), ask the team for the file or an exact link. See `references/references-and-styles.md`.

## References

- `references/brand.md`: logo, colors, fonts, captions, end cards, tone.
- `references/process.md`: the stage-by-stage production process.
- `references/video-types.md`: structure, shot lengths and reference criteria for ad, social and hero.
- `references/characters.md`: the recurring cast, voice direction, pronunciation, adding a character.
- `references/templates.md`: `brief.md`, `production.md`, `assets.md`, motion-style, character and reference templates.
- `references/model-lessons.md`: what each model is good and bad at, typical costs, and budgeting a video.
- `references/editing-lessons.md`: Arabic text, captions, timing, audio, layout and end-card lessons.
- `references/references-and-styles.md`: finding and breaking down references, and the motion-style library.
- `references/release-checklist.md`: brand, honesty, screens, third-party, picture, sound and record checks before a cut is final.
- `scripts/`: `speech_bursts.py`, `beat_grid.py`, `arabic_text.py` (run with `--help`).
