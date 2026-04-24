---
name: alphagbm-vix-status
description: |
  Current VIX level + 5-tier fear-thermometer classification + option-seller strategy
  hint. Translates the single VIX number into actionable trading guidance (calm /
  normal / seller sweet spot / caution / extreme fear). Includes current percentile
  vs 1-year history and how many days the market spent in each tier.
  Triggers: "what's VIX", "VIX level", "is market calm", "market fear gauge",
  "should I sell premium now", "VIX tier", "VIX strategy", "volatility environment",
  "fear index", "should I buy protection", "is this a good time for BPS".
globs:
  - "mock-data/vix-status/**"
---

# AlphaGBM VIX Status

The single VIX number, translated into the 5-tier framework that options sellers
actually use to size up and down. Use this as the market-wide backdrop before any
per-ticker analysis.

## What This Skill Does

Maps the raw VIX value to one of five strategy zones:

| Tier | VIX Range | Color | Seller's Move |
|------|-----------|-------|---------------|
| Calm | < 15 | 🔵 blue | Premiums thin; **buy protection cheap** (Long Put) |
| Normal | 15–20 | 🟢 green | Daily Sell Put / BPS routine |
| Seller Sweet Spot | 20–25 | 🟡 yellow | BPS premiums juicy — **actively open positions** |
| Caution | 25–35 | 🟠 orange | Can trade but **halve size**; VIX-explosion risk |
| Extreme Fear | ≥ 35 | 🔴 red | Retail sellers most likely to get buried — **only buy the dip in stock** |

Also returns:
- `mean_1y` — 1-year mean VIX for comparison
- `percentile_1y` — where today's VIX sits in last year's distribution
- `distribution_1y_pct` — % of last year spent in each of the 5 tiers

## How to Use

**Input:** No parameters — market-wide indicator.

**Output:**
- `vix` — current close
- `level` — one of `calm / normal / sweet_spot / caution / extreme_fear`
- `color` — one of `blue / green / yellow / orange / red`
- `label` — zh/en short name (e.g. `卖方甜蜜区 / Seller Sweet Spot`)
- `strategy_hint` — zh/en actionable guidance paragraph
- `percentile_1y`, `mean_1y`
- `distribution_1y_pct` — fraction of the past year in each tier

**Example Queries:**
- `what's VIX right now` — Current level + tier + strategy hint
- `is this a good time for BPS` — Check if VIX is in the "sweet spot" (20–25)
- `should I sell premium today` — Seller-view classification
- `market fear gauge` — VIX with contextual interpretation
- `how often has VIX been in extreme fear this year` — 1-year distribution

## Mock Data

Mock data in `mock-data/vix-status/` — sample responses across the 5 tiers.

## API Endpoint

```
GET /api/options/vix-status
```

No parameters. Returns:

```json
{
  "success": true,
  "vix": 22.5,
  "mean_1y": 18.3,
  "percentile_1y": 68.5,
  "level": "sweet_spot",
  "color": "yellow",
  "label": {"zh": "卖方甜蜜区", "en": "Seller Sweet Spot"},
  "strategy_hint": {"zh": "BPS 权利金变肥，积极开仓", "en": "BPS premiums get juicy — actively open positions"},
  "distribution_1y_pct": {"calm": 12.5, "normal": 45.2, "sweet_spot": 28.7, "caution": 11.3, "extreme_fear": 2.3},
  "timestamp": "2026-04-24T08:00:00"
}
```

Pricing: free (no quota deduction). 5-minute server-side cache.

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-fear-score](../alphagbm-fear-score/) | Per-ticker fear score; VIX is one of its 6 inputs |
| [alphagbm-market-sentiment](../alphagbm-market-sentiment/) | Broader sentiment dashboard (VIX + breadth + sector rotation) |
| [alphagbm-options-strategy](../alphagbm-options-strategy/) | Strategy builder that should respect the VIX tier |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence. 10K+ users.*
