---
name: alphagbm-take-profit
description: |
  Quantifies whether a stock is suitable for long-term holding or requires tiered
  profit-taking — using a novel "rollercoaster rate" metric (probability that an
  entry's paper profit reaches +50% then falls back >50% from peak before exit).
  Runs 15 exit strategies over ~10 years of daily history per ticker and returns
  medians for each. First query for a new ticker takes ~30s and gets cached
  globally; subsequent queries are instant.
  Triggers: "should I hold TQQQ long-term", "take-profit strategy for NVDA",
  "is AAPL holdable", "rollercoaster rate for TSLA", "sell strategy COIN",
  "when to sell NVDA", "profit-taking plan for QQQ", "exit strategy for my stock",
  "leveraged ETF hold analysis"
globs:
  - "mock-data/take-profit/**"
---

# AlphaGBM Take-Profit Strategy Lab

Answer one question mechanically for any ticker: **Can you just hold it, or do you
need to actively take profits?** Most retail losses come from poor exits, not poor
entries. This skill quantifies the exit decision with 10 years of daily data.

## The Core Metric: Rollercoaster Rate

A "rollercoaster event" happens when an entry's paper profit exceeds +50% and then
falls more than 50% from that peak before exit. Example: enter at 100, peak at
190, fall back to 90 — you didn't lose money, but the 90 of peak profit you
"touched" evaporated, and the journey was brutal.

Rollercoaster rate varies **up to 97 percentage points** across instruments:
- Broad-index ETFs (SPY, VTI): 0% — hold forever
- Blue chips (AAPL, MSFT): 0% — hold forever
- Sector ETFs (SOXX, XLK): 0% — hold forever
- Large-cap mega-caps (META, AMZN): ~47% — tiered exit preferred
- HK tech (腾讯, 阿里): ~49% — tiered exit preferred
- High growth (NVDA, TSLA, AMD): ~85% — tiered exit mandatory
- Crypto-related (COIN, MSTR): ~90% — tiered exit mandatory
- **Leveraged ETFs (TQQQ, SOXL): ~97% — structurally un-holdable**

**Whether you can hold is an instrument property, not an attitude problem.**

## Strategy Universe (15 total)

- **A family** (sell all at trigger): A_+50%, A_+100%, A_+200%
- **B family** (tiered): B_50/100/200 (default), B_30/60/100, B2_20/40/80, B3_40/80/150,
  B5 back-weighted, B6 front-weighted
- **C_10x** (conviction hold)
- **D** (-20% / -30% trailing stop) — **loses to hold on every tested ticker**
- **E** (never sell / long-hold)
- **F** (peak-pullback after +50% activation)
- **G** (HV-aware: picks A_+100% or A_+200% based on entry-day vol)

## How to Use

**Input:**
- `ticker` (required) — any US / HK / CN stock, ETF, or leveraged ETF

**Output:**
- **Profile**: `color` (green/amber/red) + `special_flag` (`no_hold` for leveraged ETFs,
  `reverse_alpha` for declining stocks where active selling beats hold)
- **Headline numbers**: `rollercoaster_rate`, `max_drawdown`, `hold_cagr`
- **`strategy_results`**: 15 strategies, each with `{cagr, rc, mdd}` medians
- **Provenance**: `sample_size` (typically ~120 entry points), `period`, `computed_at`

The caller is expected to:
1. Display the headline profile
2. Recommend a strategy matching user's personality + position size (front-end logic)
3. Generate concrete GTC limit-sell orders at `entry × 1.5 / 2.0 / 3.0` etc.

## Example Queries

- `should I hold TQQQ long-term` → no_hold flag + rollercoaster 97% → tiered exit
- `take-profit strategy for NVDA` → high-growth profile, B_50/100/200 default
- `is AAPL holdable` → blue-chip profile, 0% rollercoaster, hold recommended
- `when should I sell COIN` → crypto profile, mandatory tiered exit
- `rollercoaster rate for SPY` → 0%, long-hold optimal
- `backtest sell strategies for MSFT` → full 15-strategy comparison

## Mock Data

Mock data in `mock-data/take-profit/` — sample responses for TQQQ (no_hold), AAPL
(hold-optimal), and PYPL (reverse_alpha).

## API Endpoint

```
POST /api/stock/take-profit-analyze
Content-Type: application/json
```

Request body:

```json
{"ticker": "TQQQ"}
```

Also available for reading the cached library (no quota):

```
GET /api/stock/take-profit-library
```

Returns list of already-cached tickers with their headline numbers — useful for
agents to know which queries are instant vs first-time.

Response shape:

```json
{
  "success": true,
  "ticker": "TQQQ",
  "color": "red",
  "special_flag": "no_hold",
  "rollercoaster_rate": 97,
  "max_drawdown": -82,
  "hold_cagr": 37.0,
  "strategy_results": {
    "A_50": {"cagr": 6.0, "rc": 21, "mdd": -32},
    "A_100": {"cagr": 11.5, "rc": 44, "mdd": -50},
    "A_200": {"cagr": 17.6, "rc": 64, "mdd": -62},
    "B_50_100_200": {"cagr": 12.0, "rc": 36, "mdd": -42},
    "B6_front": {"cagr": 11.0, "rc": 29, "mdd": -37},
    "E_hold": {"cagr": 37.0, "rc": 97, "mdd": -82},
    "...": "..."
  },
  "sample_size": 120,
  "period": {"start": "2014-04-20", "end": "2026-04-20"},
  "computed_at": "2026-04-24T08:00:00"
}
```

Pricing: 1 stock-analysis credit per first-time ticker compute; **DB-cached for 30
days globally** — once computed, all users get instant reads (including cache hits
within 5 min in-process). Cache hits do not deduct credits.

First-time compute takes ~30s (10 years of daily data × 15 strategies × ~120 entry
points = ~1800 simulations). Subsequent reads are <100 ms.

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-stock-analysis](../alphagbm-stock-analysis/) | Deep fundamental + momentum analysis — complements the exit decision |
| [alphagbm-watchlist](../alphagbm-watchlist/) | Bulk queries across a portfolio |
| [alphagbm-hedge-advisor](../alphagbm-hedge-advisor/) | Option-based hedging for positions flagged as "high rollercoaster" |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence. 10K+ users.*
