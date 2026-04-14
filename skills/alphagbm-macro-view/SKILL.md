---
name: alphagbm-macro-view
description: >
  Track the macro variables that actually move your portfolio — VIX, US10Y,
  DXY, gold, oil, etc. — with auto-computed impact on user's holdings.
  Each tracked indicator returns current value, change, and AI-generated
  impact analysis linked to the user's profiles. Use when: adding a macro
  indicator, pulling current macro dashboard, asking how VIX affects the
  portfolio. Triggers on: "track VIX", "current 10-year yield", "how's
  the dollar doing", "add gold to my macro watch", "remove US10Y",
  "宏观指标", "美债利率", "美元指数", "VIX恐慌指数".
---

# AlphaGBM Macro View

Track key macro indicators — VIX, US10Y, DXY, gold, oil, BTC, etc. — in the user's knowledge base. Each indicator comes with auto-computed impact analysis linked to the user's actual holdings.

## When to use

- User wants to start tracking a macro variable (VIX, yields, USD, gold…)
- User asks for current macro dashboard / snapshot
- User asks how a macro change affects their portfolio
- User wants to stop tracking an indicator
- User mentions "宏观" / "VIX" / "美债" / "美元" / "macro" / "yield"

## Prerequisites

- **API Key**: env `ALPHAGBM_API_KEY` (format `agbm_xxxx…`).
- **Base URL**: default `https://alphagbm.zeabur.app`. Override via `ALPHAGBM_BASE_URL`.
- No profile requirement — macro tracking is independent of the company profile list.

## API Endpoints

All endpoints require `Authorization: Bearer $ALPHAGBM_API_KEY`.

### 1. List tracked indicators (also returns supported catalog)

```
GET /api/research/macro
```

**Response:**
```json
{
  "success": true,
  "indicators": [
    {
      "indicator_key": "VIX",
      "display_name": "CBOE Volatility Index",
      "current_value": 18.2,
      "previous_value": 16.8,
      "change_pct": 8.3,
      "impact_analysis": "Rising VIX — elevated uncertainty. Your NVDA & TSLA positions are high-beta; consider…",
      "last_updated_at": "2026-04-13T10:15:00Z"
    }
  ],
  "supported": {
    "VIX":    {"name": "CBOE Volatility Index",   "category": "volatility"},
    "US10Y":  {"name": "US 10-Year Treasury",     "category": "yields"},
    "DXY":    {"name": "US Dollar Index",         "category": "currency"},
    "GOLD":   {"name": "Gold Spot",               "category": "commodity"},
    ...
  }
}
```

The `supported` field is the catalog of valid `indicator_key` values. Use it to present options when the user asks "what can I track".

### 2. Add indicator

```
POST /api/research/macro
Content-Type: application/json

{"indicator_key": "VIX"}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `indicator_key` | string | yes | Must be in the `supported` catalog |

**400 response for unsupported keys:**
```json
{
  "success": false,
  "error": "Unsupported indicator. Supported: ['VIX', 'US10Y', 'DXY', ...]"
}
```

### 3. Remove indicator

```
DELETE /api/research/macro/<INDICATOR_KEY>
```

Uses the key (`VIX`, not an id). 404 if not tracked.

## Response schema — indicator

```
{
  id, indicator_key,
  display_name,              // human-readable name
  current_value,             // most recent reading
  previous_value,            // for change_pct computation
  change_pct,                // % change
  impact_analysis,           // AI-generated, references user's holdings
  last_updated_at
}
```

## Common indicator keys

| Key | Meaning | Why it matters |
|-----|---------|---------------|
| `VIX` | CBOE Volatility Index | Risk sentiment, option pricing |
| `US10Y` | US 10-Year Treasury Yield | Discount rate, bond-equity rotation |
| `US2Y` | US 2-Year Yield | Rate-hike expectations |
| `DXY` | US Dollar Index | EM / commodity / multinational earnings |
| `GOLD` | Gold spot | Hedge, real-yield inverse |
| `OIL` | WTI crude | Inflation / energy sector |
| `BTC` | Bitcoin | Risk appetite, crypto-adjacent stocks |
| `HKD` | HKD liquidity | HK market liquidity signal |

Always call `GET /api/research/macro` first to fetch the live `supported` catalog — keys may be added/retired.

## Typical Workflow

```
1. User: "Track VIX and the 10-year yield"
   → POST /api/research/macro {"indicator_key": "VIX"}
   → POST /api/research/macro {"indicator_key": "US10Y"}
   → Confirm both added with their current values

2. User: "What's the macro picture?"
   → GET /api/research/macro
   → Present each indicator: value, change, impact on their holdings

3. User: "Stop tracking DXY"
   → DELETE /api/research/macro/DXY

4. User: "Is high VIX hurting my positions?"
   → GET /api/research/macro → read VIX's impact_analysis field
   → The impact_analysis already references the user's specific holdings
```

## Output Formatting Tips

When presenting macro indicators:
1. **Table-first** for multi-indicator views: key · value · change% · one-line impact
2. **Highlight change direction** with arrow/color (↑ red for VIX/yields up, ↓ green etc.)
3. **Lead with impact_analysis** when user asks "how does X affect my portfolio" — it's pre-computed with their holdings in mind
4. **Stale data** — if `last_updated_at` > 1d old, note "data may be stale, refresh coming"
5. When user asks "what can I track", show the `supported` catalog grouped by category

## Related Skills

- **alphagbm-company-profile** — Macro impact analysis references the user's profiles
- **alphagbm-market-sentiment** — Broader cross-asset sentiment read
- **alphagbm-iv-rank** — Options-specific volatility context

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence for traders and AI agents. 10K+ users.*
