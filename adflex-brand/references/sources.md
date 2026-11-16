# Lookups and source reads

`tools/list` is authoritative. All tools here cost zero user credits.

## Business and brand

- `get_business_context`: name, industry, description, brand voice, palette, credit balance. Refresh when the user asks for the current balance.
- `get_brand_kit`: colors, typography, voice rules, do-nots, named logos. Put the hex values and font names into prompts instead of describing them.
- `recall_context`: long-term memories for the business. Filter to the topic; `limit` 1–100, default 25.
- None of these edit anything. The MCP connection has no tool to update a brand kit, a business profile or a memory.

## Brand elements

`list_brand_elements` returns saved characters, locations and props with an `@handle`.

- Over MCP the only filters are `search` (name, `@handle` or description, up to 100 characters) and `category` (`character`, `location`, `prop` or `auto`). Products may be stored as `prop` or `auto`; don't narrow when unsure.
- One call returns up to 50 elements. Narrow with `search` to find a specific one.
- A saved AI Influencer also returns a `voice` (`model_id`, `voice_id`). Pass both unchanged to `gen_voiceover` for its lines.
- For a Workflow, copy the returned source selector; an element ID is not an upload ID.
- A business keeps up to 200 elements.
- Pass IDs in `element_ids` (up to 8) to generation tools and name the `@handle` in the prompt. Some video models refuse elements; check `get_model_info` and fall back to the element's image as a reference.

## Asset library

`list_assets`, newest first.

- `query`: words from the prompt or name ("blue product shot", "arabic").
- `kinds`: `image`, `video`, `post`, `photoshoot`, `storyboard`, `audio`. Audio is left out unless asked for.
- `from_iso` / `to_iso`: inclusive ISO dates. State the timezone you assumed for "yesterday" or "last week".
- `limit` 1–25 (default 10), `page` up to 50.
- A storyboard frame is addressed by its parent and scene order, not by the parent alone. Never assume the first scene.
- Each item carries a source selector for Workflows and posting. Copy it exactly; don't build one by hand.

## Generations

- `list_my_generations`: recent jobs.
- `get_generation_details`: one job by `tool_call_id`: status, outputs, cost. Use it to rejoin a job after a timeout or lost context.

## Reading sources

| Tool | Reads | Limits |
|---|---|---|
| `scan_brand_url` | `url` of a public website: business text, language, visual and social candidates for review | Keep the returned URL, scan date and core sources with the facts |
| `read_creative_references` | Product pages and selected references: declarations and product details | `urls`, 1–3 per call |
| `read_document` | One public HTTPS PDF | PDF only, up to 20 MB, about 8,000 characters of output, about 20 reads an hour per connection |

`read_document` takes `document_url` (required), `extract` (`summary`, `products`, `prices`, `brand`, `full_text`, `auto`) and an optional `question`. AdFlex-hosted file URLs and chat attachments are not accepted.

After lost context, `list_source_receipts` returns what this connection already read (kept about 30 days, up to 50 per business). Read again only when current content is needed.

## Reporting a read

1. Say what was read and when.
2. Give the facts found, each tied to its source ("the menu lists …").
3. Say what was missing, unclear or marked as fallback.
4. If output was truncated, say so and offer a narrower read.

Never turn a source read into "your brand is now updated". It isn't.

## Uploads

- With file access: size and SHA-256 → `create_direct_upload` → PUT the bytes as instructed → `complete_direct_upload`.
- Otherwise, or when the direct upload is refused: `create_upload_link` (link valid about 30 minutes, 5 files by default, 10 at most), then `get_uploaded_files`.
- Images, video and audio only. PDF and DOCX are not accepted.
