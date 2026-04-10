---
name: alphagbm-earnings-crush
description: |
  Analyzes IV Crush around earnings announcements. Shows historical IV before/after earnings,
  average crush percentage, implied vs actual move, and crush pattern classification.
  Triggers: "earnings crush AAPL", "NVDA IV before earnings", "earnings play TSLA",
  "crush analysis META", "implied move vs actual", "IV crush history", "pre-earnings IV",
  "post-earnings drop", "earnings premium", "straddle before earnings"
globs:
  - "mock-data/earnings-crush/**"
---

# AlphaGBM Earnings Crush Analysis

Quantifies the IV crush phenomenon around earnings announcements so you can decide whether to sell premium before earnings or buy after the crush.

## What This Skill Does

| Concept | Description |
|---------|-------------|
| IV Crush | The sharp drop in implied volatility after an earnings announcement, regardless of stock direction |
| Average Crush % | Historical mean IV decline from pre-earnings peak to post-earnings trough |
| Implied Move | The price move the options market is pricing in via straddle pricing |
| Actual Move | The realized stock move on earnings day |
| Crush Pattern | Classification: consistent crusher, variable, or IV-resilient |
| Earnings Straddle P&L | Whether selling the at-the-money straddle before earnings has been historically profitable |

## How to Use

**Input:** A ticker symbol (e.g., AAPL, NVDA, TSLA) with an earnings-related query.

**Output:**
- Crush history table (last 8 quarters): pre-earnings IV, post-earnings IV, crush %, implied move, actual move
- Average crush % and standard deviation
- Implied move vs actual move comparison (how often options overpriced the move)
- Win rate for short premium strategies around earnings
- Optimal earnings strategy recommendation (sell premium, buy post-crush, or avoid)

**Example Queries:**
- `earnings crush AAPL` — Full crush analysis for Apple
- `NVDA IV before earnings` — Pre-earnings IV levels and history
- `implied move vs actual TSLA` — Compare what options priced in vs what happened
- `earnings play META` — Best strategy for next META earnings
- `crush analysis AMZN last 8 quarters` — Historical crush data

## Mock Data

Mock data files are located in `mock-data/earnings-crush/` and include:
- `aapl-crush-history.json` — 8 quarters of AAPL crush data
- `nvda-crush-history.json` — 8 quarters of NVDA crush data
- `crush-summary.json` — Aggregated crush statistics across tickers

## API Endpoint

```
GET /api/options/earnings-crush/{symbol}
```

Query parameters:
- `quarters` (int, default 8) — Number of past earnings to analyze
- `include_straddle_pnl` (bool, default true) — Include straddle P&L simulation

Response fields: `crush_history[]`, `avg_crush_pct`, `implied_vs_actual[]`, `straddle_win_rate`, `recommended_strategy`

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-iv-rank](../alphagbm-iv-rank/) | Current IV percentile — is pre-earnings IV already elevated? |
| [alphagbm-options-strategy](../alphagbm-options-strategy/) | Strategy recommendations that factor in earnings timing |
| [alphagbm-vol-surface](../alphagbm-vol-surface/) | Term structure kink around earnings expiration |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options intelligence. 10K+ users.*
