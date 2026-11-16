---
version: 0.1.0
name: adflex-carousel
description: |
  Sets of related images through the AdFlex MCP connector: swipe
  carousels, product sets, storyboards and moodboards (1 to 9 frames),
  with one frame re-rolled or edited at a time, then posted as a
  carousel. Use when: "make a carousel", "5 slides about our new
  menu", "swipe post", "product set from different angles",
  "storyboard this ad", "moodboard for the campaign", "change slide
  3", "post these as a carousel". Chain with adflex-brand for facts,
  adflex-social-publish to schedule the carousel, and adflex-generate
  to animate storyboard frames. NOT for: one image (use
  adflex-generate or adflex-product-photo), one multi-panel sheet in a
  single file (gen_image with a reference sheet, in adflex-generate),
  PDFs (use adflex-documents), or video.
argument-hint: "[topic or story] [carousel | storyboard | moodboard] [slides] [ratio]"
allowed-tools: Bash
---

# AdFlex Carousel

`gen_storyboard` makes 1–9 separate, downloadable frames that belong together. `edit_storyboard_scene` changes one of them. Frames render in the background.

## Step 0: Connection

1. If no AdFlex tools (such as `list_businesses`) are available, ask the user to add the connector, then stop:
   - Claude Code: `claude mcp add --transport http --scope user adflex https://api.adflex.ai/api/mcp`, then `/mcp` to sign in.
   - Other clients: add the HTTP MCP server `https://api.adflex.ai/api/mcp` and sign in.
2. On an auth or scope error, ask the user to reconnect AdFlex with `/mcp`.
3. With more than one business, call `list_businesses` once and pass `business_id` everywhere. Never guess a brand.

## Pick the mode

| User wants | `mode` | Notes |
|---|---|---|
| A swipe post that makes an argument or teaches something | `carousel`, `carousel_layout: content` | The default for marketing carousels; slides carry typography |
| One physical product shown several ways | `carousel`, `carousel_layout: product` | Same subject on every slide |
| A story, an ad's shots, a narrative arc | `storyboard` | The default when unclear |
| A look and feel: same vibe, different subjects | `moodboard` | No branding |

Read `references/layouts.md` for parameters, slide planning and prices.

## Flow

1. **Facts.** Slide copy comes from what the user gave or from a read source (adflex-brand). Never invent prices, dates or claims.
2. **Plan the slides** in chat when the content matters: one line per slide. Slide 1 is the hook; the last is the CTA.
3. **Quote.** Call `gen_storyboard` without `confirm_credits`. Every frame is paid, and 2K and 4K cost more. Show the quote and the slide plan once.
4. **Generate** after a yes. It answers "running": poll `get_generation_details` with the `tool_call_id`, or find the frames later with `list_assets` (`kinds: ["storyboard"]`).
5. **Review** every frame: text spelled right, same subject, nothing invented.
6. **Fix one frame** with `edit_storyboard_scene` (paid, quoted). Don't re-run the set for one slide.
7. **Post** on a later turn, once the frames exist: adflex-social-publish `schedule_post` with each frame URL in `media_urls`, in order.

## Credits and approval

1. Call the paid tool with a stable `operation_id` and **without** `confirm_credits`. The server runs a small action automatically or returns a quote.
2. Show the quote once with what will be made. Wait for a yes.
3. Repeat the **exact same call** with `confirm_credits` set to the approved amount. A changed prompt, count or quality needs a new quote.
4. `confirm_credits: 0` is a price-only check. After a timeout, reuse the `operation_id` or poll `get_generation_details`; never start the job again.
5. Prices only in AdFlex credits. Never disclose or guess which providers run AdFlex models.

## Rules

- **Don't post in the same turn.** The frames aren't ready when the call returns. Never pass a storyboard record or preview as a frame URL.
- **A frame is addressed by its scene order.** Never assume the first scene.
- **Brand logo:** `attach_brand_logo: true` for publish-ready carousels and promos; false for moodboards, drafts and internal storyboards.
- **Ratio:** 4:5 for Instagram and Facebook feed carousels, 9:16 for stories, 1:1 or 16:9 when asked.
- **Count:** the number the story needs; 5 is a sensible carousel. Don't pad.
- Reply in the user's language, briefly. Show the frame links in order. No JSON or IDs.

## References

- `references/layouts.md`: parameters, slide structures, identity locking, editing a frame, posting and troubleshooting.
