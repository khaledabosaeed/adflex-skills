# Captions

## Writing

- Write in the user's language and dialect. Pull the brand voice from `get_brand_kit` or `recall_context` only if it isn't known yet.
- The first line must stand on its own before the "more" cut. Lead with the hook: the strongest fact, a question, or the offer.
- Let the idea set the length: one line, a question, a short list or a short story can all be right.
- End with a clear CTA (visit, order, book, DM). Avoid comment-bait such as "comment X and I'll send the link".
- Never invent prices, discounts, dates, ingredients or results. Use what the user gave or what a source read verified.

## Hashtags

- Put them in the `hashtags` field, not as a block at the end of the caption. Caption lines made only of hashtags are moved there automatically.
- Latin script: CamelCase (`#WeekendCoffee`). Arabic: underscores between words (`#قهوة_الصباح`).
- Instagram: at most 5 per post, counting tags inside the caption. Fewer, relevant tags usually do better.
- A tag inside a sentence stays where you wrote it.

## Carousels

- `media_urls` in order, 2–10 items. For a storyboard, pass each scene's `imageUrl` in scene order.
- Storyboard frames render in the background. Schedule them on a follow-up turn once they exist (`list_assets` finds them).

## Post types

- `feed`: image or carousel in the feed. Instagram feed images need 4:5 to 1.91:1.
- `reel`: vertical 9:16 video.
- `story`: vertical 9:16 image or video, no caption shown.

## Per network

| Network | Formats | Feed image | Hashtags that help | Notes |
|---|---|---|---|---|
| Instagram | image, carousel (up to 10), reel, story | 4:5 | up to 5 (enforced) | About 125 characters show before "more" |
| Facebook | image, carousel (up to 10), reel, story | 4:5 | none needed | A few short lines read best |
| TikTok | video first; photo post of up to 10 images | 9:16 | up to 5 | Keep the caption short. No stories |
| LinkedIn | image, several images, video | 4:5 | up to 3 | Professional tone; two lines show before "see more". No stories |
| X | image, video, up to 4 images | 16:9 | none needed | 280 characters including tags; a link counts as 23 |
| YouTube | Shorts only (`post_type: short`, publish now) | 9:16 | | Needs a privacy status. Without a `title` the caption's first line is used |

More rules the server enforces:
- LinkedIn, X and TikTok take `post_type: feed` only (YouTube takes `short`).
- Facebook, TikTok, X and LinkedIn refuse images and video mixed in one post. Facebook takes one video per post.
- Carousels: up to 10 on Instagram, Facebook and TikTok, 4 on X, 20 on LinkedIn.
- `draft_post` captions up to 5,000 characters and 30 hashtags; X's 280 is a warning, not a refusal.
- Scheduling (`schedule_post`) has no platform options, so it can't set a TikTok privacy level or post a YouTube Short.

Write one caption per network when the audiences differ; a LinkedIn post is not an Instagram caption.

## Platform options (publish_post)

Passed in `platform_options`, keyed by account ID. Only these keys are accepted; anything else is refused.

| Network | Keys | Must be set explicitly |
|---|---|---|
| TikTok | `privacyLevel`, `disableComment`, `disableDuet`, `disableStitch`, `brandContentToggle`, `brandOrganicToggle`, `autoAddMusic` | `privacyLevel`: `PUBLIC_TO_EVERYONE`, `MUTUAL_FOLLOW_FRIENDS`, `FOLLOWER_OF_CREATOR` or `SELF_ONLY` |
| YouTube | `title`, `description`, `tags`, `categoryId`, `privacyStatus`, `madeForKids` | `privacyStatus`: `public`, `unlisted` or `private` |
| LinkedIn | `visibility`, `originalUrl`, `articleTitle`, `articleDescription` | `visibility`, if used: `PUBLIC` or `CONNECTIONS` |
| X | `inReplyToTweetId`, `quoteTweetId` | exact post IDs |

Ask the user for privacy and disclosure choices. They are part of what is approved in the preview.

## After publishing

Report each account's outcome separately. Only a status of published is delivery. Queued, processing or unknown is not published: read `get_publication_status` with the returned post ID, and never post again to "make sure". A partial result is not repeated for the accounts that succeeded.

## Before confirming

Show the preview the tool returns: accounts, platforms, time with timezone, caption, hashtags and media. Ask for a yes. If the user edits anything, call the tool again and show the new preview.
