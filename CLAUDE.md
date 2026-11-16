# CLAUDE.md: AdFlex Skills

## What this is

Agent skills that drive the **AdFlex MCP connector** (`https://api.adflex.ai/api/mcp`): image/video/audio generation, product photos, talking ads, carousels, video remix, zero-credit video finishing, native Workflows, branded PDFs, brand and library lookups, social publishing (Facebook, Instagram, TikTok, LinkedIn, X, YouTube) with Facebook/Instagram insights, plus the AdFlex content team's reel process.

```
adflex-generate        →  gen_* tools, quotes, talking-video recipes (the general maker)
adflex-product-photo   →  product stills: exact product / edit / concept, catalog / lifestyle / banner
adflex-talking-ad      →  spoken ads: speech method → voice → stills → clips sized to audio → cut
adflex-carousel        →  gen_storyboard sets: carousel / storyboard / moodboard, one-frame edits
adflex-video-remix     →  source-video AI: Genjutsu recast/swap, edit, motion transfer, extend, upscale
adflex-video-edit      →  import, trim, join, mute, mix, mux, frames, inspection (zero credits)
adflex-workflows       →  saved multi-step graphs: draft → quote → approve → run → status → recover
adflex-documents       →  gen_document PDFs and read_document (zero credits)
adflex-brand           →  free lookups and source reads: brand kit, context, elements, assets, sites, PDFs
adflex-social-publish  →  draft → preview → confirm for schedule/publish/reschedule/cancel; insights
adflex-reels           →  AdFlex's own reels/ads/heroes: brief → reference → styles → stills → animate → edit
```

## Repository structure

```
adflex-skills/
├── README.md                 public-facing description
├── INSTALL.md                human-facing install (5 options)
├── INSTALL_FOR_AGENTS.md     agent-driven install runbook
├── CONTRIBUTING.md           PR workflow + checklist
├── CLAUDE.md                 this file
├── COOKBOOK.md               end-to-end recipes
├── VERSION                   repo-wide version
├── LICENSE
├── setup                     bash, idempotent install + connector registration
├── .mcp.json                 AdFlex connector for the Claude Code plugin
├── .claude-plugin/{marketplace,plugin}.json
├── .codex-plugin/plugin.json
├── .cursor-plugin/plugin.json
├── .github/                  CI (validate-skills.yml), issue + PR templates
├── evals/                    README.md, scenarios.md
├── adflex-generate/          SKILL.md, references/{tools,talking-video,prompting,media-inputs,troubleshooting}.md
├── adflex-product-photo/     SKILL.md, references/profiles.md
├── adflex-talking-ad/        SKILL.md, references/speech-methods.md
├── adflex-carousel/          SKILL.md, references/layouts.md
├── adflex-video-remix/       SKILL.md, references/operations.md
├── adflex-video-edit/        SKILL.md, references/{finishing-recipes,inspection}.md
├── adflex-workflows/         SKILL.md, references/{lifecycle,recipes}.md
├── adflex-documents/         SKILL.md, references/doc-types.md
├── adflex-brand/             SKILL.md, references/sources.md
├── adflex-social-publish/    SKILL.md, references/{captions,insights}.md
└── adflex-reels/             SKILL.md, references/{brand,process,video-types,characters,templates,model-lessons,editing-lessons,references-and-styles,release-checklist}.md,
                              scripts/{speech_bursts,beat_grid,arabic_text}.py
```

## API conventions

All skills use the AdFlex MCP tools. **Do not call `api.adflex.ai` REST endpoints directly.** The MCP layer handles auth, scopes, credit quotes, confirmation gates, idempotency and ownership checks.

- **Auth:** OAuth through the client's MCP sign-in (`/mcp` in Claude Code). Scopes: `mcp:read`, `mcp:generate`, `mcp:publish`.
- **Business:** with more than one business, `list_businesses` then pass `business_id`. Never guess.
- **Credits:** call with a stable `operation_id` and no `confirm_credits` → AUTO run or a quote → show it → repeat with `confirm_credits` after a yes. `confirm_credits: 0` is a price-only check.
- **Posts:** schedule/publish/reschedule/cancel return a preview → repeat with `confirm: true` after a yes.
- **Workflows:** `run_workflow` with `quoteId` → preview → repeat with `confirm: true` and `confirm_credits`.
- **Async:** poll `get_generation_details` (by `tool_call_id`) or `get_workflow_status` (by `runId`). Never restart a running job.
- **Ownership:** inputs must be delivered in the same MCP conversation or be ready uploads. A bare CDN or gallery URL is not enough.
- **Source of truth:** never invent tool, model, voice, element or node names. `tools/list`, `get_adflex_capabilities`, `get_model_info`, `search_voices`, `list_brand_elements` and `get_workflow_capabilities` are live. References describe intent → tool, not a database.
- **Confidential:** never disclose or guess which providers run AdFlex models or AdFlex's costs. Prices only in AdFlex credits.

The server's own MCP instructions (sent on connect) win over this repo if they disagree. When the AdFlex backend changes a tool, update the matching `references/` file.

## Where the truth lives

The AdFlex backend defines everything these skills describe. When updating a skill, read it there rather than guessing:

- `src/modules/mcp/mcp.constants.ts`: `MCP_ALFA_TOOLS` is the list of tools exposed over MCP, with scopes. The MCP-only tools (`list_businesses`, `get_adflex_capabilities`, upload tools, `list_source_receipts`, and the MCP version of `list_brand_elements`) are defined in `mcp-tool-bridge.service.ts` (`MCP_NATIVE_TOOL_SCOPES`); their schemas can differ from the ALFA tool of the same name. A tool in neither must not appear in a skill.
- `src/modules/mcp/mcp-capability-policy.ts`: tools deliberately **not** exposed yet and why (inbox, content calendar, text and logo overlays, brand writes, web search, early publish of a scheduled post). Don't write skills for these until they are exposed.
- `src/modules/mcp/mcp-tool-guidance.ts`: how tool descriptions are adapted for MCP clients.
- `src/modules/alfa/tools/**`: each tool's schema, enums and limits.
- `src/modules/alfa/skills/*.definition.ts` and `creative-methods.ts`: AdFlex's own procedures (product photo, film production, video source, social publishing). The focused skills here follow them.

Never copy provider names, provider model strings or internal costs from the backend into a skill.

## The 300-line rule

Each `SKILL.md` aims for under 300 lines; it loads into context every time the skill triggers.

**Test:** if removing a section would not break the agent's ability to decide what to do next, it belongs in `references/`.

- **SKILL.md keeps:** frontmatter, connection step, hard rules, tool-routing table, decision rules, pointers to references.
- **references/ holds:** full parameter notes, recipes, error tables, templates, lessons.

## Self-contained skills

Each skill folder is independent: no `../` references, and every file in `references/` is linked from its `SKILL.md`. Shared facts (the connection step, the credit flow) are repeated per skill on purpose, so each installs standalone. CI checks this.

## Scripts

A skill may ship helpers in `scripts/` for local work the MCP tools don't do (so far only `adflex-reels`: caption timing, beat grid, Arabic text rendering). They must run standalone with `--help`, fail with a plain message when a dependency is missing, never call AdFlex or any network service, and be named in the skill's `SKILL.md`. CI compiles them.

## Content-team lessons

`adflex-reels/references/` mirrors the AdFlex content repo (`brand/`, `lessons/`, `characters/`, `templates/`). The content repo is newer and wins. When syncing lessons across, leave out business IDs, asset URLs, people's names and anything that names a provider.

## Version sync

`VERSION` is the source of truth and must match:

- every `adflex-*/SKILL.md` `version:` frontmatter,
- `.claude-plugin/marketplace.json` → `plugins[0].version`,
- `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.cursor-plugin/plugin.json` → `version`.

CI fails on drift. Don't bump versions by hand on feature branches.

## Skill chaining

Skills hand off through delivered URLs and IDs, not hidden state.

- `adflex-brand` returns facts, element IDs and library URLs. It never writes.
- `adflex-generate` returns media URLs and `tool_call_id`s. It is the general maker; the focused makers below own their intent when it matches.
- `adflex-product-photo`, `adflex-talking-ad`, `adflex-carousel` and `adflex-video-remix` return delivered URLs the same way.
- `adflex-documents` returns a temporary PDF link.
- `adflex-video-edit` consumes delivered URLs and returns new ones.
- `adflex-workflows` returns completed outputs from `get_workflow_status`.
- `adflex-social-publish` consumes media URLs for drafts and posts.
- `adflex-reels` orchestrates the others and records everything in the content repo files.

When one request spans skills ("make a reel and post it"), finish generation and editing first, then start the posting conversation. Don't batch questions across skills.

## Adding a new skill

See [CONTRIBUTING.md](./CONTRIBUTING.md). TL;DR: new top-level `adflex-<name>/SKILL.md`, frontmatter with `Use when` and `NOT for`, add it to `marketplace.json`, `setup` and `README.md`.
