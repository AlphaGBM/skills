---
name: alphagbm-marks-cycle
description: |
  Howard Marks-style market cycle position 0-100, with 0 = panic bottom (hard
  offense) and 100 = euphoric top (hard defense). Blends VIX (40%) + SPY IV Rank
  (25%) + Put/Call ratio (20%) + valuation percentile (15%) into a single number
  and maps to an offense-vs-defense posture. Free endpoint, no auth, 5-min cache
  — the goal is to make "where are we in the cycle" a one-call lookup.
  Triggers: "where is the market in the cycle", "Howard Marks style cycle read",
  "am I supposed to be offensive or defensive", "is this a buying cycle", "cycle
  position right now", "Marks cycle score", "sentiment read for SPY"
globs:
  - "mock-data/marks-cycle/**"
---

# AlphaGBM Howard Marks Cycle

"Cycles are real — the shape just isn't predictable." Howard Marks's framework
rejects forecasting and replaces it with cycle-position awareness: offense when
others are pessimistic, defense when others are optimistic.

This skill gives you the one number Marks's entire philosophy implies: *where
are we right now*.

## The Cycle Score

Each signal is mapped to its own cycle component 0-100, then weighted:

| Signal | Weight | Interpretation |
|--------|--------|----------------|
| **VIX** | 40% | Low VIX → complacency → late cycle (high score). High VIX → fear → early cycle (low score) |
| **IV Rank (SPY)** | 25% | High IV rank → fear → early cycle |
| **Put/Call ratio** | 20% | Low P/C → complacent → late cycle |
| **Valuation percentile** | 15% | Higher PE percentile → later cycle |

Weights renormalize when data points are missing (e.g., P/C not available).

## Posture Bands

- **0-24** → `OFFENSE_HARD` — extreme fear is opportunity. Buy aggressively.
- **25-39** → `OFFENSE` — add, sell vol (short premium).
- **40-59** → `NEUTRAL` — maintain positions, watch for shifts.
- **60-74** → `DEFENSE` — don't add, brace for volatility.
- **75-100** → `DEFENSE_HARD` — trim, buy protection (long puts / collars).

## Why This Is a Separate Skill

`alphagbm-vix-status` gives just a VIX tier. `alphagbm-market-sentiment` gives a
sentiment dashboard. This skill is the one-call **Marks-specific** read:
"given everything I know about sentiment + valuation, what's the posture?"

## How to Use

**Input:** none (market-level, no ticker)

**Output:**
- `cycle_score`: integer 0-100
- `posture`: one of `OFFENSE_HARD / OFFENSE / NEUTRAL / DEFENSE / DEFENSE_HARD`
- `posture_zh`, `posture_en`: natural-language prescription
- `components`: per-signal `{value, cycle_component}` breakdown

## Example Queries

- `where are we in the cycle right now` → headline cycle number + posture
- `should I be playing offense or defense` → posture directly answers
- `Howard Marks read on the market` → same data, framed as Marks would
- `is this a buying cycle` → cycle < 30 → yes; cycle > 60 → no
- `current sentiment across VIX and IV rank` → components breakdown

## Mock Data

Mock data in `mock-data/marks-cycle/` — sample showing NEUTRAL position.

## API Endpoint

```
GET /api/masters/marks-cycle
```

No body, no auth required.

Response shape:

```json
{
  "success": true,
  "cycle_score": 47,
  "posture": "NEUTRAL",
  "posture_zh": "中性 — 维持既定仓位,观察情绪变化",
  "posture_en": "Neutral — maintain positions, watch sentiment",
  "components": {
    "vix": {"value": 22.5, "cycle_component": 48},
    "iv_rank": {"value": 55, "cycle_component": 45}
  },
  "timestamp": "2026-04-24T08:00:00"
}
```

Pricing: **free — no auth, no credit deduction**. 5-min cache.

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-vix-status](../alphagbm-vix-status/) | Raw VIX tier without Marks's multi-signal blend |
| [alphagbm-market-sentiment](../alphagbm-market-sentiment/) | Fuller sentiment dashboard (VIX + P/C + F&G) |
| [alphagbm-fear-score](../alphagbm-fear-score/) | Per-ticker version of the same "where's the fear" idea |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence. 10K+ users.*
