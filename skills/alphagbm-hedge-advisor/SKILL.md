---
name: alphagbm-hedge-advisor
description: |
  Scenario-driven hedge recommendations for an existing stock position. Takes
  ticker + cost basis + purpose, auto-classifies the holding situation (falling
  knife / bottom-fishing / gain-protection / normal) and returns concrete Long Put,
  Collar, or Tier-down recommendations with live strikes and premiums from the
  current option chain.
  Triggers: "hedge my AAPL", "protect my NVDA gains", "collar strategy MSFT",
  "long put for TSLA", "how to hedge falling knife COIN", "reduce risk BABA",
  "lock in gains META", "downside protection", "portfolio hedge", "insurance for position"
globs:
  - "mock-data/hedge-advisor/**"
---

# AlphaGBM Hedge Advisor

"I own AAPL at $140 and it's now $180 — how do I protect the gains?"

Takes that question literally. Given a ticker + cost basis + position purpose, the
skill classifies the holding into one of four scenarios and returns ready-to-trade
hedge specs with strikes and costs already resolved from the live option chain.

## Scenarios

| Scenario | Trigger | Recommended Hedge |
|----------|---------|-------------------|
| **Falling Knife** | Recent drawdown ≥ 15% from 30-day high AND PnL ≤ +5% | Long Put 5% OTM, 75 DTE, 100% cover, budget ~5% |
| **Bottom Fishing** | PnL within ±8% of cost AND purpose = just_bought or long_term | Long Put 5% OTM, 90 DTE, 50-75% cover, budget ~3% |
| **Gain Protection** | PnL ≥ 15% | Collar 95/110 (zero-cost or net-credit) + Tier-down as alternative |
| **Normal Hold** | Fallback when no scenario fires | Position rules only, no urgent hedge |

## What's Returned

For each recommendation spec, the skill resolves **actual strikes and prices** from
the live option chain:

- **Long Put**: strike, DTE, `cost_per_share`, `cost_per_contract`, `cost_pct_of_spot`, delta, IV
- **Collar**: `long_put_strike`, `short_call_strike`, `put_cost`, `call_credit`,
  `net_cost_per_share` (negative = you receive a credit), breakeven analysis
- **Tier-down / Position rules**: static rules copy only

Also returns a `position_rules[]` array (single-name ≤20%, sector ≤30-35%, cash
reserve 10-15%, etc.) for the normal-hold case.

## How to Use

**Input:**
- `ticker` (required)
- `cost_basis` (required, float — your average entry price)
- `purpose` (optional, default `long_term`) — one of `long_term / short_term /
  pre_earnings / just_bought`

**Output:**
- Scenario label + reason (zh/en)
- Current price, cost basis, unrealized P&L %, recent drawdown %
- `recommendations[]` — each with type, priority, title, rationale, and
  `resolved` block containing the actual priced hedge
- `position_rules[]` — always-applicable sizing rules

**Example Queries:**
- `hedge my AAPL at $140, now it's $180` → Gain Protection → Collar 95/110 quote
- `I just bought NVDA at $110 on the dip, should I hedge?` → Falling Knife or Bottom
  Fishing → Long Put 5% OTM 60-90 DTE
- `how to protect my TSLA position` → Gain Protection or Bottom Fishing based on PnL
- `collar MSFT at cost 340 current 410` → Full collar pricing

## Mock Data

Mock responses in `mock-data/hedge-advisor/` — sample across all four scenarios.

## API Endpoint

```
GET /api/options/hedge-advisor?ticker={SYMBOL}&cost_basis={PRICE}&purpose={PURPOSE}
```

Query params:
- `ticker` (required)
- `cost_basis` (required, float > 0)
- `purpose` (default `long_term`) — one of `long_term / short_term / pre_earnings / just_bought`

Response shape:

```json
{
  "success": true,
  "ticker": "AAPL",
  "current_price": 180.0,
  "cost_basis": 140.0,
  "unrealized_pnl_pct": 28.57,
  "recent_drawdown_pct": 3.1,
  "purpose": "long_term",
  "scenario": {
    "scenario": "gain_protection",
    "label_zh": "浮盈怕坐电梯",
    "label_en": "Gain Protection",
    "reason_zh": "已浮盈 28.6%，需要保护已实现收益。",
    "reason_en": "Up 28.6% on cost — protect unrealized gains.",
    "unrealized_pnl_pct": 28.57
  },
  "recommendations": [
    {
      "type": "collar",
      "priority": 1,
      "title_zh": "Collar 95/110 锁定收益",
      "title_en": "Collar 95/110 lock-in",
      "rationale_zh": "...",
      "rationale_en": "...",
      "resolved": {
        "long_put_strike": 170.0,
        "short_call_strike": 200.0,
        "put_cost": 2.15,
        "call_credit": 2.45,
        "net_cost_per_share": -0.30,
        "net_cost_per_contract": -30,
        "is_credit": true,
        "dte": 62
      }
    },
    {"type": "tier_down", "priority": 2, ...}
  ],
  "position_rules": [
    {"rule_zh": "单票仓位 ≤ 20%", "rule_en": "Single ticker ≤20%", ...},
    ...
  ]
}
```

Pricing: 1 option-analysis credit per call; 5-min cache per (ticker, cost_basis, purpose).

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-options-strategy](../alphagbm-options-strategy/) | Multi-leg strategy builder (for custom hedges beyond presets) |
| [alphagbm-greeks](../alphagbm-greeks/) | Greeks of the resulting hedge position |
| [alphagbm-pnl-simulator](../alphagbm-pnl-simulator/) | Stress-test the hedge at various future prices |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence. 10K+ users.*
