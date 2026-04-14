---
name: alphagbm-health-check
description: >
  Weekly diagnostic report on a user's research knowledge base — flags stale
  profiles (not updated in weeks), thesis drift (AI detects original premise
  no longer holds), and orphan pages (profiles with no thesis, themes with
  missing profiles). Returns an overall 0-100 health score with specific
  action recommendations. Use when: auditing knowledge base state,
  triggering a fresh report, reviewing what needs attention. Triggers on:
  "health check my research", "what's stale", "any drift", "generate a
  report", "研究库体检", "过期档案", "论据偏离", "孤立主题".
---

# AlphaGBM Knowledge Base Health Check

Periodic audit of a user's research workspace — stale profiles, drifted theses, orphan pages — with an overall 0-100 score and concrete recommendations.

## When to use

- User asks for an overview of what's broken / out of date in their KB
- User wants to manually trigger a fresh health report
- User asks about stale profiles, thesis drift, or orphan items
- User mentions "健康体检" / "体检" / "audit" / "health check" / "什么需要更新"

## Prerequisites

- **API Key**: env `ALPHAGBM_API_KEY` (format `agbm_xxxx…`).
- **Base URL**: default `https://alphagbm.zeabur.app`. Override via `ALPHAGBM_BASE_URL`.
- **Tier requirement for generate**: `POST /health/generate` is **Pro-only**. Free/Plus users get 403 with `upgrade_required: true`. Free/Plus users can still read the latest auto-generated weekly report via `GET /health`.

## API Endpoints

All endpoints require `Authorization: Bearer $ALPHAGBM_API_KEY`.

### 1. Get latest health report

```
GET /api/research/health
```

**Response when a report exists:**
```json
{
  "success": true,
  "has_report": true,
  "report_date": "2026-04-13",
  "overall_score": 78,
  "stale_profiles": [
    {"ticker": "AAPL", "days_since_update": 21}
  ],
  "thesis_drift": [
    {"ticker": "NVDA", "drift_reason": "Revenue growth now 12% vs 25% when thesis was written"}
  ],
  "orphan_pages": [
    {"ticker": "XYZ", "issue": "Profile has no thesis after 30 days"}
  ],
  "recommendations": [
    {"action": "refresh", "ticker": "AAPL", "reason": "21 days stale"},
    {"action": "review_thesis", "ticker": "NVDA", "reason": "growth decelerated"},
    {"action": "archive", "ticker": "XYZ", "reason": "orphan for 30+ days"}
  ],
  "created_at": "2026-04-13T02:00:00Z"
}
```

**Response when no report yet:**
```json
{
  "success": true,
  "has_report": false
}
```

### 2. Generate fresh report (Pro-only)

```
POST /api/research/health/generate
```

Kicks off immediate audit across the user's profiles + theses + themes. Returns the new report in the same shape as `GET`.

**Tier-blocked response (403):**
```json
{
  "success": false,
  "error": "Health check generation is a Pro feature.",
  "upgrade_required": true
}
```

Free/Plus users still get an auto-generated report weekly (served by `GET`), just can't trigger on-demand.

## Response schema — report

```
{
  id, report_date,
  stale_profiles,          // [{ticker, days_since_update}]
  thesis_drift,            // [{ticker, drift_reason}]
  orphan_pages,            // [{ticker, issue}]
  overall_score,           // 0-100
  recommendations,         // [{action, ticker, reason}]
  created_at
}
```

## Score band interpretation

| Score | Band | Meaning |
|-------|------|---------|
| 90-100 | Excellent | Nothing urgent |
| 75-89  | Good | Minor staleness |
| 60-74  | Fair | Several profiles need refresh, some drift |
| 40-59  | Poor | Significant drift / orphans |
| 0-39   | Critical | KB is mostly out of date |

## Recommendation action types

- `refresh` — call `POST /api/research/profiles/<ticker>/refresh`
- `review_thesis` — surface the thesis + updated fundamentals; user decides to edit/close
- `archive` — `DELETE /api/research/profiles/<ticker>` or delete orphan
- `create_thesis` — profile exists but has no thesis; prompt user to write one

Skills that execute these actions: `alphagbm-company-profile`, `alphagbm-investment-thesis`.

## Typical Workflow

```
1. User: "How's my research brain looking?"
   → GET /api/research/health
   → If has_report=false: "No report yet — your first auto-audit runs on <day>.
      Pro users can trigger one now."
   → If has_report=true: present score + top 3 recommendations

2. User (Pro): "Run a fresh health check now"
   → POST /api/research/health/generate
   → Present the new report

3. User (Free/Plus): "Run a health check"
   → POST /api/research/health/generate returns 403
   → Fall back: show the last weekly auto-report via GET, suggest upgrade

4. User: "Fix the stale ones"
   → For each recommendation with action=refresh:
     POST /api/research/profiles/<ticker>/refresh
   → Re-check: GET /api/research/health → show updated score
```

## Output Formatting Tips

When presenting a health report:
1. **Lead with overall score** + band (color: green ≥ 75, yellow 60-74, red < 60)
2. **Top 3 recommendations** — most actionable first (refresh > review > archive)
3. **Group by category** — "3 stale profiles · 1 drifted thesis · 2 orphans" as a chip row
4. **Each ticker actionable** — pair the reason with a one-click (or one-prompt) action
5. **Report date prominence** — "as of 2026-04-13" so user knows freshness
6. **If no report yet** — explain the weekly cadence, offer Pro upgrade for on-demand

## Related Skills

- **alphagbm-company-profile** — Run refresh on flagged stale profiles
- **alphagbm-investment-thesis** — Review / close drifted theses
- **alphagbm-theme-research** — Address orphan pages inside themes

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence for traders and AI agents. 10K+ users.*
