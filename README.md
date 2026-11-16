# AdFlex Skills

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](./VERSION)
[![Skills](https://img.shields.io/badge/skills-11-blueviolet.svg)](#skills)

AI agent skills for [AdFlex](https://adflex.ai), the AI marketing studio. Generate images, videos, voiceovers and music, cut and mix footage, run multi-step Workflows, and publish to Facebook, Instagram, TikTok, LinkedIn, X and YouTube from Claude Code, Cursor, Codex and other agents that load Markdown skills.

Every skill drives the **AdFlex MCP connector** (`https://api.adflex.ai/api/mcp`). It acts on the signed-in user's AdFlex account: businesses, brand kits, assets, generations and social posts. Paid work is always quoted in AdFlex credits and runs only after you approve it.

## Install

Pick one. Each method needs the AdFlex MCP connector; the setup script and the Claude Code plugin add it for you.

### `npx skills` (recommended, cross-agent)

```bash
npx skills add adflex-ai/skills
```

### `gh skill install`

GitHub CLI v2.90+:

```bash
gh skill install adflex-ai/skills
```

### Claude Code marketplace

Inside Claude Code:

```
/plugin marketplace add adflex-ai/skills
/plugin install adflex@adflex
```

The plugin ships the AdFlex MCP connector. Run `/mcp` and sign in.

### Setup script

Universal fallback:

```bash
git clone --depth 1 https://github.com/adflex-ai/skills.git adflex-skills
cd adflex-skills
./setup
```

More options in [INSTALL.md](./INSTALL.md). Agent-driven install (paste into your agent): [INSTALL_FOR_AGENTS.md](./INSTALL_FOR_AGENTS.md).

## Skills

| Skill | Invoke (Claude Code) | Description |
|---|---|---|
| [`adflex-generate`](./adflex-generate) | `/adflex:adflex-generate` | Images, GIFs, videos, storyboards and carousels, voiceovers, music, sound effects, Genjutsu product/character swaps, background removal and PDF documents. Quote first, then generate. Includes the Arabic talking-video recipes. |
| [`adflex-product-photo`](./adflex-product-photo) | `/adflex:adflex-product-photo` | Product stills from the real product photo or as a concept: catalog packshots, lifestyle scenes, banners, background changes, cut-outs and product sheets. |
| [`adflex-talking-ad`](./adflex-talking-ad) | `/adflex:adflex-talking-ad` | Spoken video ads: UGC, presenter and narrated product films. Picks the speech method, casts one voice, sizes clips to the measured audio, and finishes the cut. Strong on Arabic dialects. |
| [`adflex-carousel`](./adflex-carousel) | `/adflex:adflex-carousel` | Sets of 1–9 related images: swipe carousels, product sets, storyboards and moodboards, with single-frame edits, then posted as a carousel. |
| [`adflex-video-remix`](./adflex-video-remix) | `/adflex:adflex-video-remix` | Change an existing video with AI: Genjutsu product swaps and character recasts, scene edits, performance transfer, extension and upscale. |
| [`adflex-video-edit`](./adflex-video-edit) | `/adflex:adflex-video-edit` | Zero-credit finishing: import Reels and YouTube videos, trim, join, mute, mix voiceover/music/effects, mux a soundtrack, grab frames, and inspect footage. |
| [`adflex-workflows`](./adflex-workflows) | `/adflex:adflex-workflows` | Native AdFlex Workflows: dependent multi-step productions saved as a graph, quoted once, run once, monitored and recovered. |
| [`adflex-documents`](./adflex-documents) | `/adflex:adflex-documents` | Branded PDFs (price lists, menus, one-pagers, media kits, flyers) in English or Arabic from real items, and reading existing PDFs. Zero credits. |
| [`adflex-brand`](./adflex-brand) | `/adflex:adflex-brand` | Free lookups and source reads: brand kit, business context and credit balance, saved memories, brand elements, the asset library, past generations, websites, product pages and PDFs. |
| [`adflex-social-publish`](./adflex-social-publish) | `/adflex:adflex-social-publish` | Draft, schedule, publish, reschedule and cancel posts on the connected social accounts with preview-then-confirm, and report real Facebook and Instagram post insights. |
| [`adflex-reels`](./adflex-reels) | `/adflex:adflex-reels` | The AdFlex content team's process for AdFlex's own reels, ads and hero videos: brief, reference, motion styles, stills, animation, edit, versions and lessons, with the AdFlex brand rules, a release checklist and local helpers for caption timing, beat sync and Arabic text. |

The skills chain: `adflex-brand` finds facts and assets, `adflex-generate` and the focused makers (`adflex-product-photo`, `adflex-talking-ad`, `adflex-carousel`, `adflex-video-remix`) create the pieces, `adflex-video-edit` cuts and mixes them, `adflex-workflows` runs dependent steps as one approved job, `adflex-documents` makes PDFs, and `adflex-social-publish` posts the result. `adflex-reels` orchestrates all of them for AdFlex's own marketing videos.

## What you can ask

- "Make a 9:16 ad for my coffee cart with a Levantine voiceover."
- "Animate this product photo into a 6 second slow push-in."
- "Import this Instagram reel, cut 0:03 to 0:11, and put my music under it."
- "Swap the sneaker in this reel for our product."
- "Make a 5-slide carousel about our summer menu and schedule it for Friday 6pm Riyadh time."
- "How did my reels do over the last 30 days?"
- "Put my serum on a marble counter, keep the label exactly as it is."
- "Make a UGC ad for this product page, Saudi dialect, 20 seconds."
- "Turn our price list into a branded Arabic PDF."
- "What's in my brand kit, and how many credits do I have?"

## Safety built in

- **Credits:** paid calls return a quote first. Nothing runs until you say yes. Price questions never spend credits.
- **Posting:** schedule, publish, reschedule and cancel always show a preview and need your confirmation. Drafts are free and private.
- **Facts:** product claims come from what you supply or from pages you link; the skills never invent prices, ingredients or results.

## Repository layout

```
adflex-skills/
├── adflex-generate/          SKILL.md + references/
├── adflex-product-photo/     SKILL.md + references/
├── adflex-talking-ad/        SKILL.md + references/
├── adflex-carousel/          SKILL.md + references/
├── adflex-video-remix/       SKILL.md + references/
├── adflex-video-edit/        SKILL.md + references/
├── adflex-workflows/         SKILL.md + references/
├── adflex-documents/         SKILL.md + references/
├── adflex-brand/             SKILL.md + references/
├── adflex-social-publish/    SKILL.md + references/
├── adflex-reels/             SKILL.md + references/ + scripts/
├── .mcp.json                 AdFlex MCP connector (used by the Claude Code plugin)
├── .claude-plugin/           Claude Code marketplace + plugin manifest
├── .codex-plugin/            Codex plugin manifest
├── .cursor-plugin/           Cursor plugin manifest
├── setup                     idempotent installer
├── evals/                    test scenarios
└── .github/                  CI, issue and PR templates
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Agents working on this repo should read [CLAUDE.md](./CLAUDE.md).

## License

[MIT](./LICENSE)
