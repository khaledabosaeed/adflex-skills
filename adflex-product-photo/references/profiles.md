# Profiles and review

A profile shapes composition. It never forces photography, a ratio, branding, invented copy or a source. Use `none` when the request doesn't name a use.

## Catalog

For a listing, a store page or a packshot.

- **Make:** a clear silhouette, readable details that matter, a controlled background, the product grounded on a surface.
- **Don't:** add props, or switch to a white studio nobody asked for.
- **Review:** silhouette and details readable, nothing covering the product, background fits the listing. A white background or a photographic look is required only when requested.

## Lifestyle

For the product in use, in a named setting.

- **Make:** believable scale, placement and interaction, one coherent light. The product stays identifiable.
- **Don't:** add people, actions, claims or settings that contradict the brief.
- **Review:** the setting or use reads at a glance, scale and contact are credible, the product is still readable. Judge only the people and actions that were asked for.

## Banner

For a product-led banner or hero.

- **Make:** a clear hierarchy between product and supplied copy, with breathing room for the placement. Respect the requested crop.
- **Don't:** force landscape, a fixed text side, extra copy, a CTA or a logo.
- **Review:** hierarchy, breathing room, the crop, and the supplied copy letter for letter.

## Prompt shape

1. What the product is and what stays unchanged.
2. The one change or the scene.
3. Light: source, direction, softness.
4. Surface and material words that are true ("brushed metal", "clear glass", "matte ceramic").
5. Any exact text, quoted, with its place. Otherwise "no writing anywhere".

Edit example: "Keep the bottle exactly as in the reference: shape, proportions, label text and colors unchanged. Replace the background with a warm beige plaster wall and a pale oak shelf. Soft window light from the left. Keep the bottle's own contact shadow. No writing anywhere except the existing label."

## Realism

- Diagnose before changing: is it over-smoothing, shine, or edge artifacts? Fix that one thing.
- Describe one light with a direction and softness, and make shadows and reflections agree with it.
- Camera names, "RAW" and "8K" are style words. They don't set output quality.
- A polished beauty shot can still be realistic. Don't add grit for its own sake.

## Common failures

| Problem | Do this |
|---|---|
| Label text changed or garbled | Re-run as `edit_existing` with the source as `product`; state "label text unchanged" |
| Product shape drifted | Fewer changes per edit; one edit at a time from the original, not from an edited copy |
| Scene reference leaked into the product | Give each image its own role: `product` and `composition` |
| Floating product, no contact shadow | Ask for a grounded placement and a natural contact shadow |
| A real logo appeared on a prop | Ask for unbranded props |
| The user has no photo but wants the exact product | Ask for the photo. Offer a concept only as a clearly labelled approximation |

## Sizes

Feed posts default to 4:5, stories and reels 9:16, website banners 16:9 or wider. An unsupported ratio returns `constraint_violation` with the allowed values; retry with one.
