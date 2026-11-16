# Templates

If the content repo has `templates/`, copy from there instead. These copies are for working without the repo.

## brief.md

```markdown
---
title: ""
slug: ""
status: "idea"            # idea / script approved / stills / animating / editing / done / published
type: ""                  # ad / social / hero
format: ""                # e.g. 30 s, 9:16
language: ""              # e.g. Levantine Arabic
adflex_account: ""        # prod Adflex / devAdflex
characters: ""            # slugs from characters/
motion_styles: []         # slugs from motion-styles/
cta: ""
production_chat: ""
cost_credits: 0
published: false
---

# <Title>

## Goal
- **Why this video exists:**
- **Audience:**
- **Where it runs:**
- **Success metric:**

## Idea
One or two sentences: what happens, and the message.

## Reference
Link plus what we take from it (structure, pacing, hook). Also add it to `references/<type>/README.md`.

## Motion styles
Which styles from `motion-styles/` this video uses, and any new style copied from the reference.

## Files
- [production.md](production.md): script, shot list, versions, feedback
- [assets.md](assets.md): full links to every asset
- `build/`: editing scripts
```

## production.md

```markdown
# <Title>: production notes

## Script / shot list
| # | Time | Picture | Motion | Line / sound |
|---|---|---|---|---|

## Current cut
File name, length, resolution, loudness, and how it was built (which script in `build/`).

## Versions and feedback
- v1 (date): what changed and why (the team's feedback, quoted).

## Lessons
Anything worth copying into `lessons/`.
```

## assets.md

```markdown
# <Title>: assets

Add the full URL of every asset as soon as it's generated. Mark rejected assets and say why.

## Stills
| Shot | Model / cost | Link | Notes |
|---|---|---|---|

## Clips
| Shot | Model / cost | Link | Notes |
|---|---|---|---|

## Audio
| What | Link |
|---|---|
```

## motion-styles/<slug>.md

```markdown
---
name: ""
slug: ""
type: ""          # camera / transition / edit / graphics / look
fits: []          # ad / social / hero
source: ""        # reference link, or the video it came from
used_in: []       # video slugs
---

# <Name>

## What it looks like
One or two sentences someone can picture without watching the reference.

## Breakdown
- **Camera:** movement, speed, framing, lens feel
- **Cuts and timing:** shot lengths in seconds, beat sync, where the hits land
- **Transitions:** what happens between shots and how long it takes
- **Text and graphics:** what animates in, how, position, font, colors
- **Grade and texture:** colors, contrast, grain, blur, glow
- **Sound cues:** whooshes, hits, risers (not the reference's music)

## How to make it
- **Prompt wording (paste-ready):**
  > …
- **Model:** which one does this well and what it costs
- **Edit recipe:** ffmpeg filters or the script in `tools/` that builds it

## Watch out for
What breaks, and how to fix it.

## Examples
Links to clips in our videos' `assets.md` that show this style.
```

## characters/<slug>.md

```markdown
---
name: ""
role: ""              # e.g. Cartoon cat narrator / mascot
adflex_account: ""    # the account that holds the sheet
used_in: []           # video slugs
---

# <Name>

## Look (keep identical in every prompt)
Clothes, colours, props, expression. Written so it can be pasted into a prompt.

## Reference images
- **Sheet (approved):** full URL
- Rejected versions, with the reason
- Good stills to use as extra references

## Voice direction (paste verbatim)
> timbre, age, energy, accent, and what it is not

## Lessons
Pronunciation hints, what leaks, which model holds the likeness.
```

## references/<type>/<slug>.md

```markdown
# <Reference name>

- **Link:** exact URL or ad ID (or "file from the team")
- **Length / format:**
- **Used in:**

## Shot by shot
| Time | Picture | Camera / motion | Cut | Text / sound |
|---|---|---|---|---|

## Why it works
Hook, structure, pacing.

## What we keep
Idea, structure, pacing, motion style.

## What we change
Story, characters, setting, footage, music, logos.
```

## Rows to add

Repo `README.md`, under the type's table:

```markdown
| [<slug>](videos/<type>/<slug>/brief.md) | One-line description | 30 s, 9:16, Arabic | idea |
```

`references/<type>/README.md`:

```markdown
| Reference name (length) | exact link or ad ID | <slug> | Structure we took, as a chain of beats |
```

`motion-styles/README.md` index:

```markdown
| [<name>](<slug>.md) | camera / transition / edit / graphics / look | ad, social, hero | source | <video slugs> |
```
