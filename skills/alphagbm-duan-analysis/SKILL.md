---
name: alphagbm-duan-analysis
description: |
  Duan-Yongping-style seller playbook for any ticker: Sell Put at your "willing buy"
  price, Covered Call for yield enhancement, and a Panic-Buy context read off
  current VIX. The response is three tightly-scoped analysis cards — not a generic
  options screener — derived from the specific framework that made Duan Yongping
  famous in Chinese retail investing (seller-only, rent-collection logic, never
  a buyer of options).
  Triggers: "Duan Yongping style AAPL", "sell put NVDA willing to buy at 120",
  "covered call yield TSLA", "should I sell AAPL put here", "seller strategy MSFT",
  "Duan-style analysis", "premium collection setup", "nationalist seller playbook"
globs:
  - "mock-data/duan-analysis/**"
---

# AlphaGBM Duan Yongping Analysis

Instant Duan-style framing for a single ticker. Three scoped outputs:

1. **Sell Put** — if you're "willing to buy at $X", what does selling a Put at $X
   actually pay, and how does the cost basis work out if assigned?
2. **Covered Call** — if you hold 100 shares, what yield can you pick up by selling
   a ~5% OTM Call 25-50 DTE? If called away, what's the total return?
3. **Panic Buy Context** — what's VIX telling us right now? Are we at Duan's
   "extreme fear = extreme opportunity" tier (VIX ≥ 35), or is this a wait?

Each panel is tailored to the Duan framework: seller-only, rent-collection, holding
quality companies indefinitely, and treating extreme VIX spikes as opportunity
rather than threat.

## Why This Is a Separate Skill

The generic `alphagbm-options-strategy` can compute any spread. But Duan Yongping's
style has three very specific moves and a very specific philosophy. This skill
packages that philosophy into a single call with Chinese-native copy that fits how
Chinese retail investors actually talk about these trades.

## How to Use

**Input:**
- `ticker` (required)
- `buy_price` (optional) — your "I'd happily buy at this price" level; defaults to
  spot × 0.95 if omitted

**Output (each panel may be null if no suitable contract exists):**

- `sell_put`: `{strike, premium, annualized_yield_pct, if_assigned_cost_basis, delta, dte}`
- `covered_call`: `{strike, premium, annualized_yield_pct, upside_cap_pct,
  total_return_if_called_pct, dte}`
- `panic_buy`: `{vix, level, signal (bool), action_zh, action_en}`
  - `level` ∈ `normal / caution / extreme_fear`
  - `signal = true` when VIX ≥ 35 (Duan-buy tier)

Plus meta: `ticker, stock_price, expiry_date, dte, timestamp`.

## Example Queries

- `Duan Yongping style AAPL` — All three panels for Apple
- `sell put NVDA willing to buy at 110` — Sell-Put sized for $110 entry
- `covered call yield on TSLA` — CC analysis at current price
- `is VIX at Duan buy level` — Panic-Buy panel alone (can also use `alphagbm-vix-status`)
- `should I sell AAPL put at 180` — Sell-Put analysis at specific strike

## Mock Data

Mock data in `mock-data/duan-analysis/` — sample for AAPL with a 180 buy price.

## API Endpoint

```
GET /api/options/duan-analysis?ticker={SYMBOL}&buy_price={PRICE}
```

Query params:
- `ticker` (required)
- `buy_price` (optional, float) — your preferred entry strike for Sell Put; defaults to spot × 0.95

Response shape:

```json
{
  "success": true,
  "ticker": "AAPL",
  "stock_price": 185.4,
  "expiry_date": "2026-06-20",
  "dte": 41,
  "sell_put": {
    "strike": 180.0,
    "premium": 2.45,
    "annualized_yield_pct": 12.1,
    "implied_vol": 0.24,
    "delta": -0.28,
    "open_interest": 4821,
    "volume": 312,
    "if_assigned_cost_basis": 177.55,
    "dte": 41
  },
  "covered_call": {
    "strike": 195.0,
    "premium": 2.10,
    "annualized_yield_pct": 10.1,
    "implied_vol": 0.22,
    "delta": 0.32,
    "open_interest": 3200,
    "volume": 198,
    "upside_cap_pct": 5.18,
    "total_return_if_called_pct": 6.31,
    "dte": 41
  },
  "panic_buy": {
    "vix": 18.7,
    "level": "normal",
    "signal": false,
    "action_zh": "VIX 18.7 偏平静。段永平风格下此水位更适合卖 Put 等跌到心理价位，而不是主动抄底。",
    "action_en": "VIX 18.7 is calm. Duan-style strategy prefers Sell-Put \"waiting\" over proactive buying at this level."
  },
  "timestamp": "2026-04-24T08:00:00"
}
```

Pricing: 1 option-analysis credit per call; 5-min cache per (ticker, buy_price) pair.

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-vix-status](../alphagbm-vix-status/) | Standalone VIX-tier read (Panic-Buy panel uses same classification) |
| [alphagbm-options-score](../alphagbm-options-score/) | Broader multi-factor options scoring (not Duan-specific) |
| [alphagbm-options-strategy](../alphagbm-options-strategy/) | Custom multi-leg strategies |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence. 10K+ users.*
