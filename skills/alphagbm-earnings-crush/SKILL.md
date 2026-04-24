---
name: alphagbm-earnings-crush
description: |
  Full earnings-season IV analysis: historical crush, implied move forecast, IV Rank
  strategy tag, and a priced Iron Condor quote ready to trade. Triggers: "earnings
  crush AAPL", "NVDA IV before earnings", "implied move MSFT", "iron condor for META",
  "IV rank AAPL earnings", "earnings play TSLA", "should I short premium before AMZN
  earnings", "post-earnings IV drop", "straddle before earnings", "pre-earnings strategy"
globs:
  - "mock-data/earnings-crush/**"
---

# AlphaGBM Earnings IV Panel

Everything you need for earnings week — historical IV crush + forward-looking implied
move + IV Rank strategy recommendation + a priced Iron Condor centered on the implied
move — in a single API call.

## What This Skill Does

| Concept | Description |
|---------|-------------|
| IV Crush | The sharp drop in implied volatility after an earnings announcement |
| Average Crush % | Mean IV decline from pre-earnings peak to post-earnings trough (last 8 quarters) |
| **Implied Move ±X%** | What options are pricing the earnings move to be, derived from ATM IV × √(DTE/365) |
| **IV Rank** | Current ATM IV percentile vs 20-day HV over 2y — drives strategy recommendation |
| **Strategy Recommendation** | IV Rank > 70 → short-IV plays (Iron Condor); < 30 → directional (Long Call/Put); 30-70 → wait |
| **Iron Condor Quote** | Ready-to-trade 4-leg spread with short strikes at ±1× implied move, concrete credit / max profit / max loss / breakevens |
| Historical comparison | How implied move compared to actual move across past 8 earnings |

## How to Use

**Input:** A ticker with upcoming or past earnings.

**Output:**
- Days to next earnings (if scheduled)
- Current stock price + ATM IV + IV Rank
- **Implied Move ±X% and ±$Y** — most quoted number during earnings season
- **Recommendation tag** (🔥 short IV / wait / directional) with zh/en copy
- **Iron Condor pricing** — 4 strikes + credit + max profit + max loss + breakeven bounds (Pro tier)
- Last 8 quarters: pre-earnings IV / post-earnings IV / crush % / actual move / straddle PnL
- Avg crush % and straddle win rate

**Example Queries:**
- `earnings crush AAPL` — Full crush history + next earnings IM
- `implied move NVDA` — What the options are pricing for next earnings
- `iron condor for META` — Priced-ready short-premium setup
- `IV rank MSFT earnings` — Strategy tag + recommendation
- `should I short premium before TSLA` — Recommendation + IC quote
- `straddle pnl AMZN last 8 quarters` — Historical short-premium win rate

## Mock Data

Mock data files are in `mock-data/earnings-crush/`:
- `aapl-crush-history.json` — 8 quarters of AAPL crush + implied move + IC
- `nvda-crush-history.json` — Same for NVDA
- `crush-summary.json` — Aggregated crush statistics across tickers

## API Endpoint

```
GET /api/options/earnings-crush/{symbol}
```

Query parameters:
- `quarters` (int, default 8) — Number of past earnings to analyze
- `include_straddle_pnl` (bool, default true) — Include straddle P&L simulation
- `include_iron_condor` (bool, default true) — Include Iron Condor quote (Pro tier in UI)

Response fields (headline numbers):
- `next_earnings`, `days_to_earnings`, `current_atm_iv`, `current_stock_price`
- `implied_move_pct` — e.g. 5.1 means market prices ±5.1% move
- `iv_rank_pct` — 0-100 percentile; feeds `recommendation.level`
- `recommendation` — `{level: 'high'|'mid'|'low'|'unknown', iv_rank_pct, recommendation_zh, recommendation_en}`
- `iron_condor` — `{short_call, long_call, short_put, long_put, credit, max_profit, max_loss, breakeven_up, breakeven_down, wing_width_pct}`
- `crush_history[]`, `avg_crush_pct`, `avg_actual_move_pct`, `straddle_win_rate`
- `quarters_analyzed`, `timestamp`

Pricing: 1 option-analysis credit per call; cache hits (same symbol/params within 5 min) are free.

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-iv-rank](../alphagbm-iv-rank/) | Current IV percentile — is pre-earnings IV already elevated? |
| [alphagbm-options-strategy](../alphagbm-options-strategy/) | Strategy recommendations that factor in earnings timing |
| [alphagbm-vol-surface](../alphagbm-vol-surface/) | Term structure kink around earnings expiration |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence. 10K+ users.*
