---
name: alphagbm-tepper-signal
description: |
  Quantified version of David Tepper's 2009 (+132%) and 2020 (+82%) panic-buy
  playbook. Detects whether current conditions match Tepper's signal: VIX ≥ 35
  AND FearScore ≥ 80 AND quality filter (large-cap, positive margin). Only fires
  during genuine market panics — the rest of the time it returns the "waiting"
  state, which is ~80% of all days per Tepper's own framework. The API reuses
  our existing FearScore module, so the signal is directly comparable to the
  multi-indicator panic index.
  Triggers: "is this a Tepper buy signal", "panic-buy detector SPY", "should I
  buy the panic", "Tepper style entry check", "are we at a panic bottom", "is
  VIX 35+ and fear 80+", "historical bottom signal today"
globs:
  - "mock-data/tepper-signal/**"
---

# AlphaGBM Tepper Panic-Buy Signal

David Tepper made two historic panic-bottom calls: March 2009 ("I'm betting on
the Fed") and March 2020 (COVID bottom). Both had identical fingerprints: VIX
spiked > 40, multi-indicator fear was maxed, and Tepper loaded quality large-caps
(banks 2009, SPY/QQQ 2020).

This skill mechanizes that fingerprint.

## The Signal Logic

Three gates must all pass for the signal to arm:

1. **VIX ≥ 35** — extreme fear, not just elevated
2. **FearScore ≥ 80** — multi-indicator panic (reuses existing FearScore module:
   VIX + IV Rank + RSI + Volume + Put/Call + Consec-Down-Days)
3. **Quality filter** — market cap > $50B AND profit margin > 0 (no memes,
   concept stocks, or pre-revenue small caps)

When all three pass → `signal: true`, level: `armed`.

## Signal Levels

| Level | Condition | Prescription |
|-------|-----------|--------------|
| `armed` | VIX ≥ 35 AND Fear ≥ 80 | 🔥 Historic-level buying moment — scale into SPY/QQQ/DIA |
| `watch` | VIX ≥ 30 OR Fear ≥ 70 | ⚡ Approaching — prepare capital, don't act yet |
| `near` | VIX ≥ 25 OR Fear ≥ 60 | Lukewarm — far from Tepper-level panic |
| `cold` | below | Calm — **the patience state**, which is most of the time |

**Tepper's own framework includes "do nothing" as a first-class state.** Most
calls to this endpoint will return `cold` — that's by design. The value isn't
in the signal firing often, it's in *never missing* a VIX > 40 event.

## Why This Is a Separate Skill

`alphagbm-fear-score` gives the raw panic index. `alphagbm-vix-status` gives
the VIX tier. This skill combines them with Tepper's specific criteria
(quality filter + threshold rules) to produce a single yes/no decision.

## How to Use

**Input:**
- `ticker` (optional, default `SPY`) — the quality-filter applies to this ticker

**Output:**
- `vix`, `fear_score` — the two input signals
- `vix_pass`, `fear_pass`, `quality_pass` — per-gate booleans
- `signal` — final boolean
- `level` — `armed / watch / near / cold`
- `recommended_etfs` — `["SPY", "QQQ", "DIA"]` (quality large-cap universe)
- `advice_zh`, `advice_en` — natural-language prescription

## Example Queries

- `is this a Tepper buy signal` → call with default SPY
- `panic-buy check on QQQ` → substitute QQQ
- `should I buy the panic now` → returns `cold` if calm → "wait, this is the patience state"
- `am I missing a historic bottom` → the only time this fires, the answer is "yes, don't miss it"
- `Tepper-style entry for DIA` → quality large-cap → passes quality filter

## Mock Data

Mock data in `mock-data/tepper-signal/` — samples for `armed` (VIX 42, Fear 85) and `cold` (VIX 17, Fear 35).

## API Endpoint

```
POST /api/masters/tepper-signal
Content-Type: application/json
```

Request body:

```json
{"ticker": "SPY"}
```

Response shape:

```json
{
  "success": true,
  "ticker": "SPY",
  "vix": 42.0,
  "fear_score": 85,
  "vix_pass": true,
  "fear_pass": true,
  "quality_pass": true,
  "signal": true,
  "level": "armed",
  "recommended_etfs": ["SPY", "QQQ", "DIA"],
  "advice_zh": "信号激活 — VIX 42.0、FearScore 85。按 Tepper 2009/2020 规则,分批买入大盘质量 ETF (SPY, QQQ, DIA)。不要买概念股或小盘股。",
  "advice_en": "Signal armed — VIX 42.0, FearScore 85. Per Tepper 2009/2020, scale into quality large-cap ETFs (SPY, QQQ, DIA). No memes, no small caps.",
  "timestamp": "2026-04-24T08:00:00"
}
```

Pricing: 1 option-analysis credit per call; 5-min cache per ticker (cache hits free).

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-fear-score](../alphagbm-fear-score/) | The underlying panic index — component of this signal |
| [alphagbm-vix-status](../alphagbm-vix-status/) | Standalone VIX tier — complementary read |
| [alphagbm-duan-analysis](../alphagbm-duan-analysis/) | Duan's VIX ≥ 35 panic-buy philosophy on a specific ticker |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence. 10K+ users.*
