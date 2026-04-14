---
name: alphagbm-theme-research
description: >
  Group related tickers into investment themes — AI infra, HK dividend, EV
  supply chain, biotech catalysts — with theme-level AI summary and news
  keyword monitoring. Each theme is a named bag of tickers plus keywords
  the system watches for you. Use when: creating a themed basket, pulling
  up a theme's aggregated view, adding/removing tickers, monitoring news
  around a topic. Triggers on: "create an AI infra theme", "show my
  themes", "add MSFT to AI theme", "what's happening in HK dividend",
  "主题研究", "AI基建", "港股高息", "投资主题".
---

# AlphaGBM Theme Research

Group related tickers into named investment themes with an AI-generated summary and news keyword watchlist. Each theme is a lightweight basket you can track at the concept level.

## When to use

- User wants to organize tickers by theme (AI infra, HK dividend, EV supply chain, biotech…)
- User asks to view a specific theme's holdings + latest summary
- User wants to add or remove tickers from a theme
- User wants the system to monitor news around a topic
- User mentions "主题" / "theme" / "basket" / "篮子" / "板块"

## Prerequisites

- **API Key**: env `ALPHAGBM_API_KEY` (format `agbm_xxxx…`).
- **Base URL**: default `https://alphagbm.zeabur.app`. Override via `ALPHAGBM_BASE_URL`.
- **Tier limits apply**: Free tier is capped on themes — `check_profile_limit` mirrors the profile limit model. Check `limits.max_themes` via the dashboard endpoint.

## API Endpoints

All endpoints require `Authorization: Bearer $ALPHAGBM_API_KEY`.

### 1. List themes

```
GET /api/research/themes
```

**Response:**
```json
{
  "success": true,
  "themes": [
    {
      "id": 7,
      "theme_name": "AI Infrastructure",
      "description": "Picks & shovels for the AI capex cycle",
      "tickers": ["NVDA", "AVGO", "MSFT", "ORCL"],
      "news_keywords": ["AI capex", "data center", "hyperscaler"],
      "theme_summary": "Capex guidance up across 4 hyperscalers...",
      "last_updated_at": "2026-04-13T09:00:00Z"
    }
  ]
}
```

### 2. Get theme detail (aggregated)

```
GET /api/research/themes/<THEME_ID>
```

Returns the theme + aggregated data across its tickers (average price change, top movers, recent news matching keywords). 404 if not found or not owned.

### 3. Create theme

```
POST /api/research/themes
Content-Type: application/json

{
  "theme_name": "AI Infrastructure",
  "description": "Picks & shovels for AI capex",
  "tickers": ["NVDA", "AVGO", "MSFT"],
  "news_keywords": ["AI capex", "data center"]
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `theme_name` | string | yes | Display name, used to dedupe |
| `description` | string | no | Short blurb |
| `tickers` | array of string | no | Initial tickers; can be edited later |
| `news_keywords` | array of string | no | Phrases monitored for news matches |

### 4. Update theme (by id)

```
PUT /api/research/themes/<THEME_ID>
Content-Type: application/json

{"tickers": ["NVDA", "AVGO", "MSFT", "ORCL"], "news_keywords": [...]}
```

Partial update. Any of the fields from create are accepted.

### 5. Delete theme (by id)

```
DELETE /api/research/themes/<THEME_ID>
```

Hard-delete. Doesn't affect the underlying company profiles.

## Response schema — theme

```
{
  id, theme_name, description,
  tickers,                  // array of ticker strings
  news_keywords,            // array of phrases for news matching
  theme_summary,            // AI-generated narrative (markdown)
  last_updated_at, created_at
}
```

Theme detail endpoint (`GET /themes/<id>`) additionally includes aggregated fields like top movers and recent matched news — the exact shape is service-side and stable for display, not for programmatic parsing.

## Typical Workflow

```
1. User: "Create an AI infra theme with NVDA, AVGO, MSFT"
   → POST /api/research/themes
     {"theme_name": "AI Infrastructure", "tickers": ["NVDA","AVGO","MSFT"],
      "news_keywords": ["AI capex", "data center"]}
   → Confirm theme created; mention it'll start accumulating summary + news

2. User: "What themes do I have?"
   → GET /api/research/themes
   → Table: theme · ticker count · last updated · summary excerpt

3. User: "Add ORCL to my AI theme"
   → GET /api/research/themes (find id)
   → PUT /api/research/themes/<id> {"tickers": [... + "ORCL"]}

4. User: "What's happening in my HK dividend theme?"
   → GET /api/research/themes/<id>
   → Lead with theme_summary + aggregated movers + matched news
```

## Output Formatting Tips

When presenting themes:
1. **List view** — theme name · ticker count · "updated Xd ago" · 1-sentence summary
2. **Detail view** — lead with `theme_summary` (AI narrative), then ticker grid with % change, then recent matched news
3. **Keyword hygiene** — if the user creates a theme with no `news_keywords`, prompt: "Want me to watch for any news phrases? E.g., 'AI capex', 'hyperscaler'"
4. **Ticker overlap** — when creating a new theme, check if tickers already exist in other themes; it's fine (tickers can be in multiple themes) but worth mentioning

## Related Skills

- **alphagbm-company-profile** — Themes reference profiles; creating a theme with untracked tickers still works but they won't have profile data
- **alphagbm-health-check** — Flags orphan tickers that are in themes but no longer in any profile
- **alphagbm-compare** — Side-by-side comparison for tickers within a theme

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence for traders and AI agents. 10K+ users.*
