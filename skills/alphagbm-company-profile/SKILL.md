---
name: alphagbm-company-profile
description: >
  Build and maintain company research profiles on AlphaGBM — auto-generated
  from fundamentals, PE/PB Band history, financial red flags, and event radar.
  Each profile is one user+ticker record that the system refreshes on schedule.
  Use when: creating a watchlist of companies to track, pulling up a saved
  research file, refreshing a profile's market data, or checking PE/PB bands.
  Triggers on: "add AAPL to my knowledge base", "show my profile for NVDA",
  "refresh my TSLA profile", "list my tracked companies", "PE band for META",
  "what's in my research brain", "创建公司档案", "我的投研档案".
---

# AlphaGBM Company Profile

Build and manage company research profiles in a user's private knowledge base. Each profile captures fundamentals (PE/PB), 8-year valuation bands, financial red flags, and recent events — auto-refreshed on a schedule.

## When to use

- User wants to track a company in their personal research workspace
- User asks to list / view / delete saved companies
- User asks for PE or PB historical band of a ticker
- User asks to refresh a stale profile
- User mentions "知识库" / "投研档案" / "research brain" / "knowledge base"

## Prerequisites

- **API Key**: stored in env `ALPHAGBM_API_KEY` (format `agbm_xxxx…`).
- **Base URL**: default `https://alphagbm.zeabur.app`. Override with env `ALPHAGBM_BASE_URL`.
- If the user has no key, direct them to register at <https://alphagbm.com> and create one at `/api-keys`.
- **Tier requirement**: Free tier = 1 profile, Plus = 10, Pro = 50. Create endpoint returns 403 with `upgrade_required: true` when the cap is hit.

## API Endpoints

All endpoints require `Authorization: Bearer $ALPHAGBM_API_KEY`.

### 1. List profiles

```
GET /api/research/profiles?page=1&per_page=20
```

**Response:**
```json
{
  "success": true,
  "profiles": [{ "ticker": "AAPL", "company_name": "...", "current_price": 261.0, ... }],
  "total": 3,
  "page": 1,
  "per_page": 20
}
```

### 2. Get profile detail (includes thesis if one exists)

```
GET /api/research/profiles/<TICKER>
```

Returns the full profile + an embedded `thesis` field (null if no thesis yet). See **Response schema** below for field list. Returns 404 if the ticker isn't in the user's knowledge base.

### 3. Create profile

```
POST /api/research/profiles
Content-Type: application/json

{"ticker": "AAPL"}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ticker` | string | yes | Stock ticker (US / HK / A-share), case-insensitive |

**Behavior:** Pulls fundamentals via the data provider, computes red flags and event radar, persists the profile. If a profile already exists for this user+ticker, it's updated in place (idempotent).

**Tier limit response (403):**
```json
{
  "success": false,
  "error": "Profile limit reached. Upgrade to Plus for 10 profiles.",
  "current": 1,
  "max": 1,
  "upgrade_required": true
}
```

### 4. Delete (archive) profile

```
DELETE /api/research/profiles/<TICKER>
```

Soft-deletes by flipping `status` to `archived`. Returns 404 if not found.

### 5. Refresh profile data

```
POST /api/research/profiles/<TICKER>/refresh
```

Pulls fresh market data, recomputes red flags and events. Use when the user says "refresh my profile" or the `last_updated_at` is stale (> 7d old).

### 6. PE/PB Band data (cached 24h)

```
GET /api/research/profiles/<TICKER>/band
```

Returns 8-year PE/PB history for building the band chart. Can be called **without** the ticker being in the user's knowledge base — it's a read-only market data endpoint.

**Response:**
```json
{
  "success": true,
  "ticker": "AAPL",
  "pe_history": [{"date": "2017-04", "pe": 16.2}, ...],
  "pb_history": [...],
  "current_pe_percentile": 0.82,
  "current_pb_percentile": 0.75
}
```

## Response schema — full profile

```
{
  id, ticker, company_name, market,          // market = US | HK | CN
  current_price, pe_ratio, pb_ratio,
  pe_band_data,                              // 8yr history, same shape as /band endpoint
  financial_red_flags,                       // [{rule_id, severity: "high|med|low", message}]
  event_radar,                               // [{event_type, timestamp, headline}]
  ai_profile_summary,                        // markdown, ~500 chars
  status,                                    // "active" | "archived"
  last_viewed_at, last_updated_at, created_at
}
```

## Typical Workflow

```
1. User: "Add NVDA to my research brain"
   → POST /api/research/profiles {"ticker": "NVDA"}
   → Present: "Added NVDA. Current PE 45, 2 red flags, PE at 85th percentile of 8yr range."

2. User: "What's in my knowledge base?"
   → GET /api/research/profiles
   → Present table: ticker · company · PE · last_updated · red flag count

3. User: "Show me my AAPL profile"
   → GET /api/research/profiles/AAPL
   → Present: summary, PE/PB bands, red flags list, event radar, linked thesis (if any)

4. User: "Refresh my TSLA profile"
   → POST /api/research/profiles/TSLA/refresh
```

## Tier Limits

| Tier | Max profiles |
|------|-------------|
| Free | 1 |
| Plus | 10 |
| Pro  | 50 |

When a create hits the limit, the API returns `upgrade_required: true`. Surface this to the user with a prompt to upgrade at `/pricing`.

## Output Formatting Tips

When presenting a profile to the user, highlight:
1. **Ticker + company name** and market flag (US / HK / CN)
2. **Current price + PE / PB** with percentile context ("PE 32, 85th percentile of 8yr range → rich")
3. **Red flags** — group by severity, show top 3
4. **Event radar** — most recent 3-5 events with dates
5. **Linked thesis** — if present, one-line buy reason + exit trigger summary
6. **Staleness** — if `last_updated_at` > 7d old, suggest a refresh

## Related Skills

- **alphagbm-investment-thesis** — Attach buy thesis + exit triggers to a profile
- **alphagbm-health-check** — Detect stale / drifted profiles across the user's workspace
- **alphagbm-stock-analysis** — One-off deep analysis (not persisted to the knowledge base)
- **alphagbm-theme-research** — Group profiles into themes (AI infra, HK dividend, etc.)

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence for traders and AI agents. 10K+ users.*
