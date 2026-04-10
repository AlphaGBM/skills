---
name: alphagbm-compare
description: |
  Side-by-side comparison of 2-5 stocks or options across GBM Five Pillars scores,
  options metrics, technicals, and valuations. Identifies the winner by category.
  Triggers: "compare AAPL vs MSFT", "NVDA or AMD", "which is cheaper TSLA or META options",
  "tech stock comparison", "side by side", "versus", "which is better",
  "compare options", "cheapest IV", "best value stock"
globs:
  - "mock-data/compare/**"
---

# AlphaGBM Compare

Side-by-side comparison of 2-5 stocks or options across every AlphaGBM dimension, so you can pick the best opportunity.

## What This Skill Does

| Dimension | What Gets Compared |
|-----------|--------------------|
| GBM Five Pillars | Momentum, Value, Quality, Volatility, Sentiment scores for each ticker |
| Options Metrics | IV rank, IV percentile, VRP, skew, term structure for each ticker |
| Technicals | RSI, MACD, moving averages, support/resistance levels |
| Valuations | P/E, P/S, EV/EBITDA, PEG ratio — who is cheaper? |
| Category Winner | Best ticker in each dimension highlighted |
| Overall Recommendation | Weighted composite ranking across all dimensions |

## How to Use

**Input:** 2-5 ticker symbols with a comparison query.

**Output:**
- Comparison table with all dimensions side by side
- Winner highlighted per category (green badge)
- Overall recommendation with composite score
- Key differentiators: what makes the winner stand out
- Trade idea: if you had to pick one, which and why

**Example Queries:**
- `compare AAPL vs MSFT` — Head-to-head across all dimensions
- `NVDA or AMD` — Which semiconductor name is the better trade?
- `which is cheaper TSLA or META options` — Options cost comparison
- `tech stock comparison AAPL MSFT GOOGL AMZN META` — Full sector comparison
- `compare options AAPL vs MSFT 30d ATM` — Specific options contract comparison

## Mock Data

Mock data files are located in `mock-data/compare/` and include:
- `aapl-vs-msft.json` — Full comparison output for AAPL vs MSFT
- `tech-five-way.json` — Five-way comparison of mega-cap tech
- `options-cost-compare.json` — Options-specific metrics comparison

## API Endpoint

```
GET /api/analytics/compare
```

Query parameters:
- `symbols` (string, required) — Comma-separated tickers (2-5), e.g., "AAPL,MSFT,GOOGL"
- `dimensions` (string, default "all") — Comma-separated: "pillars", "options", "technicals", "valuations"
- `options_expiry` (string) — Target expiry for options comparison (e.g., "30d", "60d")

Response fields: `tickers[]`, `comparison_table`, `category_winners`, `overall_ranking[]`, `recommendation`

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-stock-analysis](../alphagbm-stock-analysis/) | Detailed single-stock analysis for deeper dives after comparison |
| [alphagbm-options-score](../alphagbm-options-score/) | The options score that feeds into the comparison |
| [alphagbm-iv-rank](../alphagbm-iv-rank/) | IV rank data used in the options metrics comparison |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options intelligence. 10K+ users.*
