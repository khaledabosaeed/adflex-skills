# Document types and fields

`tools/list` is authoritative.

## gen_document

| Field | Notes |
|---|---|
| `doc_type` | `price_list`, `menu`, `one_pager`, `media_kit`, `flyer`, `custom` |
| `title` | 1–120 characters, shown in the header |
| `language` | `en` or `ar` (right to left) |
| `sections` | Up to 12. Each: `heading` (up to 80 characters), `body` (up to 1,200), `items` (up to 40) |
| `items` | Each: `name` (required), `description` (one line), `price` (display text, up to 24 characters) |
| `footer_note` | Up to 200 characters: contact, validity, disclaimer |
| `apply_brand` | Default true: brand colors, fonts and logo |
| `operation_id` | Stable per document version |

Output: one A4 PDF at a temporary AdFlex link, deleted about seven days after creation, not added to My Assets. Whether it shows inline depends on the client.

## Worked example

Request: "Make an Arabic menu PDF for our café: espresso 9, flat white 14, cardamom latte 16; cheesecake 18."

```json
{
  "operation_id": "menu-cafe-v1",
  "doc_type": "menu",
  "title": "قائمة المشروبات",
  "language": "ar",
  "sections": [
    { "heading": "القهوة", "items": [
      { "name": "إسبريسو", "price": "9 SAR" },
      { "name": "فلات وايت", "price": "14 SAR" },
      { "name": "لاتيه بالهيل", "price": "16 SAR" }
    ]},
    { "heading": "الحلويات", "items": [
      { "name": "تشيز كيك", "price": "18 SAR" }
    ]}
  ]
}
```

The currency came from the business context. If it isn't known, ask; don't guess one.

## Shaping each type

- **Price list:** group by category; one line of description at most; the validity date in the footer if the user gave one.
- **Menu:** sections in serving order; allergens or notes in the description only if supplied.
- **One-pager:** what it is, who it's for, three proof points, contact. Body sections, few items.
- **Media kit:** who we are, audience, formats and rates if supplied. Audience numbers must come from the user or from real insights, never estimated.
- **Flyer:** one offer, one date, one contact. For a visual poster, use an image instead.

## Rebuilding an old PDF

1. `read_document` with `extract: products` (or `prices`).
2. Show the user what was read and ask them to confirm it. Text output is capped at about 8,000 characters; `truncated: true` means items were left out, so read again with a narrower `question`.
3. `gen_document` with the confirmed items.

## read_document

- `document_url` (required): public HTTPS PDF, up to 20 MB.
- `extract`: `summary`, `products`, `prices`, `brand`, `full_text`, `auto`.
- `question`: a specific thing to answer.
- About 20 reads an hour per connection. After lost context, `list_source_receipts` restores earlier reads.

## Troubleshooting

| Symptom | Do this |
|---|---|
| The link stopped working | It expired after about seven days. Render again with a new `operation_id` |
| The same file came back after an edit | The `operation_id` was reused. Use a new one for a new version |
| The user sent the PDF as a chat file | Ask for a public link or the text; uploads don't accept PDFs |
| No logo or colors | The business has no brand kit set, or `apply_brand` was false |
| Wants Word or PowerPoint | Not available; offer the PDF |
| Wants it in My Assets | Not saved there; the user downloads it |
| A photographed menu | It's an image: upload it and use `inspect_media`, then build the document from the confirmed items |
