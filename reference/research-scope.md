# What “19,000 Jev calls” counts

This repo is based on experiments run from 24 to 28 September 2026. The private lab logs were counted on 28 September. They contain source texts and work records that cannot be published wholesale, so this page states the counting rule and the limits of the headline.

| Measure | Count | Rule |
|---|---:|---|
| Jev API log rows | 19,562 | Rows whose logged `path` was `/systemone` or `openrouter:/api/v1/systemone` across 147 lab `calls.jsonl` files |
| Successful Jev responses | **19,367** | Those rows with HTTP status 200; retries and reruns count because they were actual provider responses |
| Unique successful experiment tags | 18,909 | Deduplicated by log file and tag; tags identify an item within an experiment, not a universal request ID |
| Metered input tokens | **90,365,054** | Sum of `response.usage.input_tokens` across successful Jev responses; retries and reruns are included |
| Metered output tokens | 13,962,002 | Sum of `response.usage.output_tokens` across the same responses |

The totals include experiments with multiple questions per request. A call is **not** one independently labelled judgment. Some experiments repeated identical items to measure variation. The 19,367 count says how much Jev we exercised; accuracy claims elsewhere use their own specific test sets and denominators.

The experiments covered ads, reviews, keyword intent, source checks, call transcript search and bounded agent decisions. Most used jev-1.13 through LLM API's `jev-latest` or a pinned OpenRouter route. Model, gateway and prices may change. Check [the live TypeSafe docs](https://docs.typesafe.ai/) and validate thresholds on your own labelled cases.

Our Claude Code session also recorded about 1.01B token accesses, but roughly 999M were cached input rereads. We do **not** describe that as 1B unique research tokens or use it as the headline.
