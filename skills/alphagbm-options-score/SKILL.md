---
name: alphagbm-options-score
description: >
  Score and rank options contracts for any ticker using AlphaGBM's multi-factor
  scoring model (liquidity, IV attractiveness, Greeks balance, risk/reward). Returns
  scored option chains with the best contracts highlighted. Use when: evaluating
  which option to trade, finding the best strike/expiry, ranking options by quality.
  Triggers on: "score AAPL options", "best options for NVDA", "which TSLA call
  should I buy", "option chain for SPY", "rank META puts".
globs:
  - "mock-data/*.json"
---

# AlphaGBM Options Score

## What This Skill Does

Scores every option contract in a chain using a **4-factor model**, so you instantly know which contracts have the best risk/reward profile.

### Scoring Factors

| Factor | Weight | What It Measures |
|--------|--------|-----------------|
| **Liquidity** | 25% | Bid-ask spread, volume, open interest — can you get in/out? |
| **IV Attractiveness** | 30% | Is IV high/low vs. history? VRP positive? — is the option cheap or expensive? |
| **Greeks Balance** | 20% | Delta exposure, theta decay rate, gamma risk — is the risk profile clean? |
| **Risk/Reward** | 25% | Max profit vs. max loss, probability of profit, breakeven distance |

### Score Scale
- **9-10**: Exceptional — rare, act quickly
- **7-8**: Strong — good trade candidate
- **5-6**: Average — proceed with caution
- **1-4**: Poor — avoid unless hedging

## How to Use

### Input
- **Required**: Ticker symbol
- **Optional**: Expiration date, option type (call/put), strike range

### Output Structure

```json
{
  "ticker": "AAPL",
  "price": 218.45,
  "chain": [
    {
      "expiry": "2026-04-18",
      "type": "call",
      "strike": 220,
      "bid": 5.80,
      "ask": 6.10,
      "iv": 30.5,
      "delta": 0.52,
      "gamma": 0.035,
      "theta": -0.18,
      "vega": 0.32,
      "score": 8.2,
      "score_breakdown": {
        "liquidity": 9,
        "iv_attractiveness": 7,
        "greeks_balance": 8,
        "risk_reward": 8.5
      }
    }
  ],
  "top_picks": {
    "best_call": {"strike": 220, "expiry": "2026-04-18", "score": 8.2},
    "best_put": {"strike": 215, "expiry": "2026-04-18", "score": 7.8}
  }
}
```

### Example Queries

| User Says | What Happens |
|-----------|-------------|
| "Score AAPL options" | Full chain with scores, top picks highlighted |
| "Best NVDA call to buy" | Filtered to calls, sorted by score descending |
| "TSLA puts for next Friday" | Filtered by expiry + type |
| "Which SPY option has the best risk/reward?" | Sorted by risk_reward factor |

### Mock Data

Demo tickers available without API key: AAPL, NVDA, SPY, TSLA, META. Uses realistic option chain snapshots from `mock-data/`.

### API Endpoint

```
GET https://api.alphagbm.com/api/options/chain/{symbol}/{expiry}
Authorization: Bearer <api_key>
```

### Related Skills
- **alphagbm-stock-analysis** — Analyze the underlying stock first
- **alphagbm-options-strategy** — Build multi-leg strategies with top-scored contracts
- **alphagbm-greeks** — Deep-dive into Greeks for a specific contract
- **alphagbm-vol-surface** — See if IV is cheap or expensive across strikes

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options intelligence. 100K+ users.*
