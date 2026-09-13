---
name: alphagbm-research-insights
description: >
  Retrieve AlphaGBM's published market insights and research summaries. Use
  when a user asks for recent AlphaGBM research, market news, an article by
  market or tag, or the source-backed explanation behind a published view.
  Triggers on: "latest AlphaGBM research", "show market insights", "find the
  latest semiconductor research", "what did AlphaGBM publish today", "最近的研报",
  "市场热点", "查看研报解读".
---

# AlphaGBM Research Insights

Retrieve published AlphaGBM research and market insight articles. This Skill
is a reading and interpretation workflow: it does not expose editorial draft,
update or delete operations.

## Prerequisites

No API key is required for published articles. Set `ALPHAGBM_BASE_URL` to
override the default `https://alphagbm.zeabur.app`.

## API Endpoints

### List published insights

```http
GET /api/insights?lang=zh&page=1&limit=20
```

Optional filters:

- `lang=zh|en` — selects the display language; English falls back to Chinese
  when an English title or description is not available.
- `market=us|hk|a|commodity` — filters by market.
- `tag=<tag>` — filters the returned articles by tag.
- `page` — one-based page number.
- `limit` — number of items, capped at 50.

The list response contains `articles`, `total`, `page` and `total_pages`.
Each article includes `slug`, `market`, `title`, `description`, `tags`,
`cover_image`, `read_time_min`, `published_at`, `updated_at` and `url`.

### Read one published insight

```http
GET /api/insights/<SLUG>?lang=zh
```

The detail response contains the same metadata plus `content` in Markdown.
Only published articles are returned; draft and archived records are not
publicly readable.

## Agent Workflow

1. List the latest articles with the requested language and market filter.
2. Rank by `published_at` unless the user asks for a specific tag or topic.
3. Open the selected article by `slug` before summarizing its content.
4. Preserve the article's market, publication time, tags and `url`.
5. Summarize the author's view separately from the agent's interpretation.
6. Never present a published viewpoint as a guaranteed forecast or investment
   recommendation.

## Output Rules

When presenting an article, include:

- title and market;
- publication date/time;
- a short neutral summary;
- the main evidence or assumptions stated in the article;
- uncertainties or conditions that would change the view;
- the original article URL.

If the requested market or tag has no result, say so and do not silently
substitute an unrelated article.

## Related Skills

- [alphagbm-company-profile](../alphagbm-company-profile/) — company-level
  profiles and valuation bands.
- [alphagbm-investment-thesis](../alphagbm-investment-thesis/) — private thesis
  tracking and sell triggers.
- [alphagbm-theme-research](../alphagbm-theme-research/) — private theme and
  ticker grouping.

