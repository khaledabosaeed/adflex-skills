# Insights

`get_post_insights` returns real provider data for published Facebook and Instagram posts. It's free and read-only.

## Parameters

- `platform`: `facebook`, `instagram` or `all` (default). Other networks have no insights here; say so when asked.
- `period_days`: 7, 30 (default) or 90. Filters by **when posts were published**, not when the activity happened.
- `focus`: `summary` (sampled totals), `top_posts` (ranked by observed interactions), `engagement` (interaction breakdown), `reach` (audience numbers).
- `account_id` (optional, from `list_social_accounts`) for one account. If more than 50 accounts match, ask which one. Never pick one arbitrarily or drop accounts silently.

## Reporting rules

- Never estimate or invent a metric. Every number you state must come from the result.
- Totals and top posts describe the **returned sample**. Check sample size and coverage before making period-wide claims.
- Metrics are cumulative counters fetched now. They are not activity within the period and not a trend versus a previous period.
- The `impressions` field holds provider views/plays. Read `metricSemantics` / `impressionsMetric` for the exact source.
- Reach is summed per post, not unique people across posts.
- Only compute a rate when the numerator and denominator come from matching sources. Don't compare rates built on different metrics.
- Missing metrics are unknown, not zero.
- Posting-time patterns are hypotheses to test, not proven best times.
- An empty result means no connected account or no posts in the period. Say which, and offer to check accounts.

## Good answer shape

1. One line with the headline (top post, or total views of the sample).
2. A short table: post, date, views/plays, reach, likes, comments, shares.
3. One or two observations, labeled as observations, with a suggested next test.
