---
version: 0.1.0
name: adflex-social-publish
description: |
  Draft, schedule, publish, reschedule and cancel social posts on the
  business's connected accounts (Facebook, Instagram, TikTok, LinkedIn,
  X, YouTube) through AdFlex, and report real Facebook and Instagram
  post performance.
  Every externally visible action shows a preview and runs only after
  the user confirms. Use when: "post this", "schedule this for tomorrow
  9am", "make a carousel post", "write a caption", "publish to
  Instagram", "move my post to Friday", "cancel the scheduled post",
  "what's scheduled", "did it go live", "how did my posts do", "which
  reel performed best". Chain with adflex-generate to make the post
  image or video first, and adflex-video-edit to trim it. NOT for:
  generating media (use adflex-generate), editing footage (use
  adflex-video-edit), paid ad campaigns, replying to comments or
  messages, or insights for networks other than Facebook and Instagram.
argument-hint: "[caption or idea] [media url] [when] [accounts]"
allowed-tools: Bash
---

# AdFlex Social Publish

Post to the business's connected social accounts through the AdFlex MCP tools. Which networks are available is whatever `list_social_accounts` returns for this business: Facebook, Instagram, TikTok, LinkedIn, X and YouTube can publish; Snapchat is connect-only. Insights cover Facebook and Instagram.

## Step 0: Connection

1. If no AdFlex tools (such as `list_businesses`) are available, ask the user to add the connector, then stop:
   - Claude Code: `claude mcp add --transport http --scope user adflex https://api.adflex.ai/api/mcp`, then `/mcp` to sign in.
   - Other clients: add the HTTP MCP server `https://api.adflex.ai/api/mcp` and sign in.
2. Posting needs the `mcp:publish` scope. On an auth or scope error, ask the user to reconnect AdFlex and allow publishing.
3. With more than one business, call `list_businesses` once and pass `business_id` everywhere.

## Hard rules

1. **Never publish or schedule unless the user explicitly asked for it in this session.** Drafts are always fine.
2. **Preview, then confirm.** `schedule_post`, `publish_post`, `reschedule_post` and `cancel_scheduled_post` first return a preview of exactly what will happen. Show it. Repeat the same call with `confirm: true` only after the user agrees.
3. **Never repeat a confirmed post.** After a timeout, check `list_scheduled_posts`, `list_published_posts` or `get_publication_status` before doing anything.
4. **Never claim a post is live** unless the status says it published. A draft is a draft.
5. A payment or reconnection is not approval to post. Re-check state and ask again.
6. Reply in the user's language, briefly. No JSON or IDs in chat.

## Flow

1. **Accounts.** `list_social_accounts` first (`purpose: post` before posting, `connect` to show connection buttons; optional `channel`), to get valid `account_ids`, each account's health and the post types it supports. A data-loading failure doesn't mean an account is disconnected. An inactive or expired connection, or missing permissions, blocks posting: show the action link the tool returns. Never invent a sign-in link, and re-read the accounts after the user reconnects.
2. **Media.** A feed post usually needs a visual. If none exists, make it first with adflex-generate (`gen_image` with `task_type=social_post`, or a storyboard carousel). Skip it when the user asks for text only, supplies media, or the post is naturally text-led. Say which you chose.
3. **Draft.** `draft_post` with `caption`, `hashtags`, `media_url`, `account_ids` / `target_platforms` and `post_type` (`feed`, `story`, `reel`). Nothing is saved or published. `attach_media_to_draft` adds media to the latest draft. `target_platforms` takes only `facebook` and `instagram`; omit it for other networks and rely on `account_ids`.
4. **Schedule** with `schedule_post`: `caption`, `hashtags`, `media_urls` (1–10; 2+ is a carousel), `account_ids`, `scheduled_for` and an IANA `timezone` (for example `Asia/Riyadh`) for wall-clock times. Preview, then `confirm: true`. Scheduling takes `post_type` `feed`, `story` or `reel` and no platform options, so YouTube Shorts and TikTok posts that need a privacy choice are published now with `publish_post`, not scheduled.
5. **Publish now** with `publish_post`: `account_ids`, `post_type` (`feed`, `story`, `reel`, `short`), `caption`, `media` (each item an exact `url` and `type`: `image` or `video`) and, where a network needs them, `platform_options` per account. Preview, then `confirm: true`. TikTok needs an explicit `privacyLevel` and YouTube an explicit `privacyStatus`; ask the user, never pick one. See `references/captions.md`.
6. **Change** with `reschedule_post` (`post_id`, new `scheduled_for`, and `timezone` for a wall-clock time) or `cancel_scheduled_post` (`post_id`), both preview-then-confirm. Cancelling works only before the scheduled time.
7. **Check** with `list_scheduled_posts` (`account_id`, `status`, `page`, `limit` up to 50), `list_published_posts` (`account_id`, `since`, `until`, `include_insights`, `limit`), `get_publication_status` (`post_id`).

An already scheduled post can't be published early over MCP. Point the user to the scheduled posts page in AdFlex; never create a duplicate with `publish_post`.

## Captions and media rules

- Instagram allows at most **5 hashtags** per post, counting tags inside the caption. `schedule_post` refuses more.
- Instagram and TikTok need media. A story or reel takes exactly one media item, and a reel must be a video. An animated GIF publishes only on X and LinkedIn; elsewhere use a still or a video.
- `publish_post` media must be delivered in this conversation, or carry the exact source selector `list_assets` returns. A bare library URL is refused.
- X captions fit in 280 characters.
- Hashtags go in `hashtags`: CamelCase for Latin script, underscores between Arabic words.
- An Instagram feed image slightly outside 4:5 to 1.91:1 is center-trimmed; one further out is refused. Reels and stories are 9:16.
- Never invent prices, offers, dates or claims. Use the brand voice from `get_brand_kit` when it isn't already known.

Read `references/captions.md` for caption writing and `references/insights.md` for performance questions.

## Performance

`get_post_insights` (free, Facebook and Instagram only): `platform` (`facebook`, `instagram`, `all`), `period_days` (7, 30 or 90), `focus` (`summary`, `top_posts`, `engagement`, `reach`), optional `account_id`. Ground every claim in the returned data and read `references/insights.md` before reporting numbers.

## References

- `references/captions.md`: how to write captions and hashtags that fit AdFlex's limits.
- `references/insights.md`: how to read and report performance data without overclaiming.
