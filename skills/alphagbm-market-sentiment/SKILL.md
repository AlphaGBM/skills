---
name: alphagbm-market-sentiment
description: |
  Market-wide sentiment dashboard with VIX, Put/Call ratio, Fear & Greed Index, market breadth,
  and sector rotation analysis. Classifies current regime as risk-on, risk-off, or neutral.
  Triggers: "market sentiment", "is the market fearful", "VIX analysis", "put call ratio",
  "market breadth", "fear and greed", "risk on or risk off", "advance decline",
  "new highs new lows", "sector rotation", "market regime"
globs:
  - "mock-data/market-sentiment/**"
---

# AlphaGBM Market Sentiment Dashboard

Aggregates market-wide sentiment indicators into a single dashboard, classifying the current regime to guide your trading stance.

## What This Skill Does

| Indicator | Description |
|-----------|-------------|
| VIX Level + Percentile | Current VIX value and its rank over the past year (e.g., 85th percentile = elevated fear) |
| Put/Call Ratio | Equity and index P/C ratios — high values signal fear, low values signal complacency |
| Fear & Greed Index | Composite score (0-100) combining multiple sentiment inputs |
| Market Breadth | Advance/decline ratio and new highs vs new lows — measures participation |
| Sector Rotation Stage | Which sectors are leading/lagging, mapped to the economic cycle |
| Regime Classification | Overall assessment: risk-on, risk-off, or neutral with confidence level |

## How to Use

**Input:** A market sentiment query (no ticker required, or specify VIX/SPX for focused analysis).

**Output:**
- Sentiment dashboard with all indicators and their current readings
- Historical context: where each indicator sits relative to the past 1 year
- Current regime classification (risk-on / risk-off / neutral) with confidence %
- Sector rotation map: early cycle, mid cycle, late cycle, or recession positioning
- Actionable interpretation: what the current sentiment means for options trading

**Example Queries:**
- `market sentiment` — Full dashboard with all indicators
- `is the market fearful` — Quick fear/greed assessment
- `VIX analysis` — Deep dive on VIX level, term structure, and percentile
- `put call ratio` — Equity and index put/call with historical context
- `market breadth` — Advance/decline, new highs/lows, participation analysis
- `sector rotation` — Which sectors are leading and what cycle stage we are in

## Mock Data

Mock data files are located in `mock-data/market-sentiment/` and include:
- `sentiment-dashboard.json` — Full dashboard snapshot with all indicators
- `vix-history.json` — VIX time series with percentile ranks
- `sector-rotation.json` — Sector performance and cycle classification

## API Endpoint

```
GET /api/analytics/market-sentiment
```

Query parameters:
- `indicators` (string, default "all") — Comma-separated list: "vix", "pcr", "fear_greed", "breadth", "rotation"
- `lookback_days` (int, default 252) — Historical period for percentile calculations

Response fields: `vix`, `put_call_ratio`, `fear_greed_index`, `breadth`, `sector_rotation`, `regime`, `regime_confidence`

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-stock-analysis](../alphagbm-stock-analysis/) | Individual stock analysis informed by market regime |
| [alphagbm-unusual-activity](../alphagbm-unusual-activity/) | Unusual flow patterns that contribute to sentiment signals |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence. 10K+ users.*
