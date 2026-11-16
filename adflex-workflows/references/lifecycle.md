# Workflow lifecycle

`tools/list` and `get_workflow_capabilities` are authoritative. The quoted graph validation on the server is final.

## Discovery (free, read-only)

### list_workflow_templates
No parameters. Returns supported recipes with their `templateId`. Nothing is created.

### get_workflow_capabilities
- `nodeTypes` (optional): up to 20 node type IDs in `group.name` form, for example `video.assemble`.
- `modelIds` (optional): up to 12 model IDs to get their controls inside nodes.
- Call it once without filters to get the inventory, then filter with IDs you saw there. Invalid filters return `workflow_capabilities_invalid` and nothing is written.

### get_workflow_context
`workflowId`. Reads the current draft, its revision, nodes and inputs. Use it after a timeout instead of saving again.

## Saving drafts (free, no generation)

### prepare_workflow_draft (template)
- `templateId`: from `list_workflow_templates`.
- `outputNodeIds`: 1–2 node IDs whose results the user wants.
- `sourceAsset`: `{ kind: ai_image | business_image | uploaded_image, id, role: source | product }`.
- `instruction`: what to do, up to 4,000 characters.
- `aspectRatio` (optional), `title` (new drafts only, or an explicit rename).
- `workflowId` + `revision` to update an existing draft.

### prepare_workflow_graph (custom)
- `nodes`: each `{ nodeId, type, label, position: {x, y}, params }`. `position` is required. `params` holds only the native keys listed by `get_workflow_capabilities` (at most 32). No source URLs, owner IDs, prices or approval data in params.
- An `image.storyboard` node carries its own `storyboardReferences` (1–4), binding reference edges to the frames that use them.
- `edges`: connect a source node's output port to a target node's input port.
- `sourceBindings`: bind owned inputs (an AI image, a storyboard frame by `sceneOrder`, a photoshoot image by `imageIndex`, a post image by `imageId`) to the nodes that consume them.
- Final results: connect each requested media output to an `output.collect` node. There is no `outputs` argument.
- `filmPlan` / `productionScope`: for saved multi-sequence films (shots, sequence or whole-film scope).
- Required: `nodes`, `edges`, `sourceBindings`, plus `operation_id`.
- Limits: at most 20 nodes, 80 edges and 20 source bindings per graph.
- `sourceBindings` accept image, video, audio and conversation assets (for example `ai_video`, `uploaded_video`). Copy the selector `list_assets` returns; don't build one.
- `title`, `workflowId`, `revision` as for drafts.

## Quote and run

### quote_workflow_run
`workflowId` and `operation_id`. Creates a stored quote and returns a `quoteId` with the credit total. No generation. If the quote call times out, don't repeat it in the same turn.

### run_workflow
- First call with `quoteId` only: returns the approval preview. Show it.
- After the user agrees: the same call with `confirm: true` and `confirm_credits` set to the approved ceiling (at least the quoted total). The run ID is the quote ID.
- An expired or mismatched quote returns `workflow_quote_invalid_or_expired`. Request a fresh quote and approval.
- Acceptance is not completion. Credits are reserved; failed units are refunded.

### get_workflow_status
`runId`. Returns state, per-step status, failed steps and completed outputs. Poll at a sensible pace; don't spin.

### cancel_workflow_run
`runId`. Shows a preview first; confirm with the user. Irreversible.

### prepare_workflow_recovery
`runId` of a settled run with failed steps, plus `operation_id`. Saves a recovery draft that reuses completed outputs at zero charge. Quote its returned `workflowId` and get a fresh approval for the remaining work.

## Common errors

| Code | Meaning | Do this |
|---|---|---|
| `workflow_capabilities_invalid` (or a similar invalid-filter error) | Filter with an unknown node or model | Re-read the inventory, use observed IDs |
| `workflow_confirmation_required` | Run without approval of this exact quote | Show the preview and wait for a yes |
| `workflow_quote_invalid_or_expired` | Quote expired or belongs to another business | Quote again, approve again |
| `workflow_recovery_unmanaged` | Run can't be recovered this way | Tell the user; offer a new draft |
| Save "may already be saved" | Write timed out after reaching the server | `get_workflow_context`, don't save again |
