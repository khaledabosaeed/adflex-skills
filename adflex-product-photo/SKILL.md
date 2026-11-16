---
version: 0.1.0
name: adflex-product-photo
description: |
  Product still images through the AdFlex MCP connector: catalog
  packshots, lifestyle scenes and product-led banners, from the user's
  real product photo or as a described concept, plus background
  changes, cut-outs and product reference sheets. Use when: "product
  photo", "packshot", "put my product on a marble table", "change the
  background of this product photo", "lifestyle shot of our mug",
  "banner for the new serum", "white background for my store", "make a
  product sheet". Chain with adflex-generate to animate the still,
  adflex-carousel for a product set, and adflex-social-publish to post.
  NOT for: video (use adflex-generate), multi-slide sets (use
  adflex-carousel), swapping a product inside a video (use
  adflex-video-remix), or PDFs (use adflex-documents).
argument-hint: "[what to show] [product photo url or file] [catalog | lifestyle | banner]"
allowed-tools: Bash
---

# AdFlex Product Photo

Make a still of a product with `gen_image`, following the procedure AdFlex itself uses: decide what is being asked, resolve the source photo, pick a composition profile only when the use calls for one, then review the result against it.

## Step 0: Connection

1. If no AdFlex tools (such as `list_businesses`) are available, ask the user to add the connector, then stop:
   - Claude Code: `claude mcp add --transport http --scope user adflex https://api.adflex.ai/api/mcp`, then `/mcp` to sign in.
   - Other clients: add the HTTP MCP server `https://api.adflex.ai/api/mcp` and sign in.
2. On an auth or scope error, ask the user to reconnect AdFlex with `/mcp`.
3. With more than one business, call `list_businesses` once and pass `business_id` everywhere. Never guess a brand.

## 1. What is being asked

| Intent | Meaning | Needs a source photo |
|---|---|---|
| **Exact product** | The user's real product, with its true shape and label | Yes, the owner's own photo |
| **Edit** | Change one thing in an image they pointed to (background, light, crop) | Yes, that image |
| **Concept** | A new described image, fictional packaging, or an accepted approximation | No |

- "Our product" alone does not mean exact. "With its exact label" does.
- A missing photo never changes the intent. Ask for the photo; don't quietly make a lookalike.
- A generated image is not evidence of what the real product looks like. Don't use one as the source for an exact-product shot.
- An unrelated upload (a logo, another product) is not the source just because it is the only file.

## 2. Resolve the source

- Delivered in this conversation: use that URL.
- In the library: `list_assets` (search by words, `kinds: ["image"]`).
- A file on the user's machine: upload it (`create_direct_upload` → PUT → `complete_direct_upload`, or `create_upload_link` when that fails or there is no file access).
- A public web image: `import_web_image`.
- A saved product in Brand Elements: `list_brand_elements` with `category: prop`.

## 3. Generate

| Case | `task_type` | References |
|---|---|---|
| Exact product or edit | `edit_existing` | the source, role `product` |
| Product placed into another image | `combine_multiple` | the product as `product`, the scene as `composition` |
| Concept | `create_from_scratch` (or `product_shot`) | none required |
| One multi-view product sheet | add `reference_sheet: "product"` | the source when there is one |
| Cut-out on transparency | `remove_background` | one image in `reference_images`; PNG or WEBP keeps transparency |

- Set `product_identity` to `exact` or `concept` to match the intent. With `exact`, `product_subject` is `own` (default) or `public` for a publicly known object.
- For an edit, omit `aspect_ratio` unless a new format was asked; the server keeps the source format.
- Say what must not change: shape, proportions, material, color, label text.
- A background-only edit keeps the product's own light and contact shadow. A white background does not mean "remove the shadow".
- Never invent label text, claims, prices, a CTA or a logo. `attach_brand_logo: true` only when the user wants the brand mark.

Read `references/profiles.md` for the three profiles and the review checks.

## Credits and approval

1. Call the paid tool with a stable `operation_id` and **without** `confirm_credits`. The server runs a small action automatically or returns a quote.
2. Show the quote once with what will be made. Wait for a yes.
3. Repeat the **exact same call** with `confirm_credits` set to the approved amount. A changed prompt, count or quality needs a new quote.
4. `confirm_credits: 0` is a price-only check. After a timeout, reuse the `operation_id` or poll `get_generation_details`; never start the job again.
5. Prices only in AdFlex credits. Never disclose or guess which providers run AdFlex models.

## Rules

- Reply in the user's language, briefly. Show the delivered AdFlex URL unchanged. No JSON or IDs.
- One question at a time, only when the answer changes the image (usually: the photo, or which product).
- Explicit instructions on medium, ratio, copy, branding and source always beat the profile.
- After delivery, review against the profile and say plainly what you see. A critique never starts a paid retake on its own.
- Offer the next step once: animate it (adflex-generate), a set (adflex-carousel), or post it (adflex-social-publish).

## References

- `references/profiles.md`: catalog, lifestyle and banner profiles, review checks, realism notes and common failures.
