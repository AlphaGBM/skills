---
name: alphagbm-fear-score
description: |
  Per-ticker panic index (0-100) that weights six real signals: VIX, IV Rank, RSI-14,
  options volume anomaly, Put/Call ratio, and consecutive-down days. Scores ≥ 60
  trigger a Bull Put Spread entry signal. Based on the FearDesk methodology; tested
  at ~10.8% annualized ROC for BPS entries on signal vs ~3.5% unconditional.
  Triggers: "fear score QQQ", "is NVDA oversold", "panic index SPY", "BPS signal
  TSLA", "is it fear time", "BPS entry timing", "when to sell put", "is AAPL panic",
  "contrarian entry signal", "oversold reading", "VIX plus RSI"
globs:
  - "mock-data/fear-score/**"
---

# AlphaGBM FearScore

A weighted composite panic gauge, per ticker. Reconstructs the FearDesk framework in
one API call: six orthogonal fear signals, each scored 0–100, then combined with
fixed weights into a single number. **Score ≥ 60 is the historical trigger for Bull
Put Spread entries.**

## Scoring Weights

| Indicator | Weight | Source |
|-----------|--------|--------|
| VIX level | 20% | Global fear floor (market-wide) |
| **IV Rank** | 25% | Per-ticker option premium expensiveness |
| RSI-14 | 15% | Oversold intensity |
| Volume anomaly | 15% | Options or stock volume spike vs 5-day avg |
| Put/Call ratio | 15% | Bearish positioning skew |
| Consecutive down days | 10% | Selloff persistence |

Each indicator has its own 0–100 sub-score with thresholds tuned so extreme readings
contribute most. Missing inputs fall back to neutral values (and are flagged in
`components.*.fallback`), so the endpoint never 500s on partial data.

## Why It Exists

Most fear gauges are either VIX-only (miss per-ticker divergence) or opaque
("sentiment index: 72"). This breaks down exactly what drove the score so you can
decide whether to trust it.

**Backtest evidence:** Across 146 live Bull Put Spread trades, entries at
FearScore ≥ 60 delivered ~10.8% annualized ROC vs ~3.5% for unconditional entries —
roughly **3× the alpha** from a single filter. Use this as the market-timing layer
on any premium-selling strategy.

## How to Use

**Input:** A ticker symbol.

**Output:**
- `fear_score` — weighted total 0-100
- `signal` — boolean, true when `fear_score ≥ threshold` (default 60)
- `threshold` — current trigger value
- `confidence` — 0-1, fraction of the 6 indicators that used real (non-fallback) data
- `components.{vix,iv_rank,rsi,volume_anomaly,pc_ratio,consecutive_down}`:
  - `value` — raw input
  - `score` — 0-100 per-indicator score
  - `weight` — contribution weight
  - `fallback` — true if neutral default was used

**Example Queries:**
- `fear score QQQ` — Full breakdown of the 6 indicators for QQQ
- `is NVDA oversold right now` — RSI + FearScore composite
- `BPS signal SPY` — Check if entry threshold is hit
- `when should I sell put AAPL` — Timing via FearScore ≥ 60 rule
- `how panicked is TSLA today` — Per-ticker panic index with component breakdown
- `why is QQQ fear score low` — Component-by-component explanation

## Mock Data

Mock data in `mock-data/fear-score/` — example responses at neutral / elevated /
signal-triggered readings.

## API Endpoint

```
GET /api/options/fear-score?ticker={SYMBOL}
```

Query params:
- `ticker` (required) — stock symbol (US / HK / CN supported if whitelisted)

Response shape:

```json
{
  "success": true,
  "ticker": "QQQ",
  "fear_score": 68.2,
  "signal": true,
  "threshold": 60,
  "confidence": 1.0,
  "components": {
    "vix": {"value": 28.4, "score": 82, "weight": 0.20, "fallback": false},
    "iv_rank": {"value": 78, "score": 78, "weight": 0.25, "fallback": false},
    "rsi": {"value": 24.1, "score": 88, "weight": 0.15, "fallback": false},
    "volume_anomaly": {"value": 2.3, "score": 72, "weight": 0.15, "fallback": false},
    "pc_ratio": {"value": 1.6, "score": 80, "weight": 0.15, "fallback": false},
    "consecutive_down": {"value": 3, "score": 60, "weight": 0.10, "fallback": false}
  },
  "timestamp": "2026-04-24T08:00:00"
}
```

Pricing: 1 option-analysis credit per call; per-ticker 5-min cache (cache hits free).

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-vix-status](../alphagbm-vix-status/) | Market-wide version of the VIX input |
| [alphagbm-iv-rank](../alphagbm-iv-rank/) | IV Rank (25% of the composite) standalone |
| [alphagbm-options-strategy](../alphagbm-options-strategy/) | BPS/Sell-Put strategies that should respect the ≥60 signal |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence. 10K+ users.*
