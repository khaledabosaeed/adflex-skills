---
version: 0.1.0
name: adflex-workflows
description: |
  Build, quote, run, monitor, cancel and recover native AdFlex
  Workflows: saved multi-step productions where several generation and
  finishing nodes feed each other and run as one approved job. Use when:
  "make this a workflow", "run the whole pipeline", "generate all clips
  and merge them in one go", "keep one voice across all these clips",
  "use the image-edit template", "re-run the failed steps", "is my
  workflow done", "cancel the workflow". Chain with adflex-generate for
  standalone pieces and adflex-social-publish to post the outputs.
  NOT for: one image, one clip or one voiceover (use adflex-generate),
  simple trims, mutes or audio mixes of existing footage (use
  adflex-video-edit), loops, recurring schedules or pause-for-review
  pipelines (Workflows run once).
argument-hint: "[what the production should output] [source assets]"
allowed-tools: Bash
---

# AdFlex Workflows

A Workflow is a saved graph of AdFlex nodes (generation, voice changing, merging, assembly) that runs **once** under **one** approved quote. Use it when steps depend on each other's outputs and should run without a manual hand-off at every step.

## Step 0: Connection

1. If no AdFlex tools (such as `list_businesses`) are available, ask the user to add the connector, then stop:
   - Claude Code: `claude mcp add --transport http --scope user adflex https://api.adflex.ai/api/mcp`, then `/mcp` to sign in.
   - Other clients: add the HTTP MCP server `https://api.adflex.ai/api/mcp` and sign in.
2. On an auth or scope error, ask the user to reconnect AdFlex with `/mcp`.
3. With more than one business, call `list_businesses` once and pass `business_id` everywhere.

## When to use a Workflow

- **Yes:** several clips whose outputs feed later nodes (voice changer per clip, merge audio, assemble); a supported template run (for example the image-edit template); a production the user wants approved once as a whole.
- **No:** one standalone generation (adflex-generate), a trim or mix of existing media (adflex-video-edit). Don't wrap simple work in a Workflow.
- Workflows don't loop, repeat on a schedule, or pause for review. Don't promise that.

## Lifecycle

1. **Discover.** `list_workflow_templates` for ready recipes. `get_workflow_capabilities` for the live node types and model controls; filter with `nodeTypes` / `modelIds` you actually observed. Never invent node types, ports or params.
2. **Save a draft** (no generation, no charge):
   - From a template: `prepare_workflow_draft` with `templateId`, `outputNodeIds`, `sourceAsset` and `instruction`.
   - Custom graph: `prepare_workflow_graph` with `nodes`, `edges` and `sourceBindings`, using only param keys from the capabilities. Final results come from wiring nodes into an `output.collect` node; there is no `outputs` argument.
   - Every save and quote takes a stable `operation_id`.
   - To change an existing draft, pass its `workflowId` and current `revision`. Keep its title unless a rename was asked.
3. **Quote.** `quote_workflow_run` with the `workflowId`. Show the exact saved quote once: steps, outputs and credits.
4. **Run after approval only.** First `run_workflow` with the `quoteId` shows the approval preview. After the user agrees, repeat `run_workflow` with the `quoteId`, `confirm: true` and the approved `confirm_credits` ceiling.
5. **Monitor.** Poll `get_workflow_status` with the `runId`. Only completed media outputs are attached. Don't promise a time.
6. **Recover.** For a settled partial failure, `prepare_workflow_recovery` with the `runId`. Completed steps keep their outputs at no new charge; the rest needs a fresh quote and approval.
7. **Cancel** on request with `cancel_workflow_run` (shows a preview; confirm with the user).

Read `references/lifecycle.md` for parameters, retries and error codes, and `references/recipes.md` for common graphs.

## Rules

- One approval of an exact quote covers all its steps and the polling. It does **not** cover changed work or a new attempt.
- Changed requirements mean a revised draft and a new quote.
- After a save or quote timeout, don't repeat the call blindly. Read the draft with `get_workflow_context`, or reuse the `operation_id`.
- Never redo Workflow steps as direct generations.
- Reply in the user's language, briefly. Show final output URLs, not JSON or node IDs.
- Prices only in AdFlex credits. Never discuss providers.

## References

- `references/lifecycle.md`: every Workflow tool with its parameters, retry rules and errors.
- `references/recipes.md`: graphs for common productions (one voice across clips, talking product ad, template edits).
