---
name: alphagbm-pnl-simulator
description: >
  P&L simulation engine for any single-leg or multi-leg option position. Generates
  profit/loss diagrams at expiry, P&L over time, what-if scenarios (price, IV, time),
  breakeven analysis, and probability distributions. Use when: testing a trade idea,
  visualizing risk/reward, running what-if scenarios, checking breakeven points,
  stress-testing a position.
  Triggers on: "simulate PnL for AAPL bull call spread", "what if NVDA drops 10%",
  "P&L diagram", "test my iron condor", "breakeven analysis", "stress test my position",
  "what happens at expiry".
globs:
  - "mock-data/*.json"
---

# AlphaGBM P&L Simulator

## Prerequisites

- **API Key**: Set env `ALPHAGBM_API_KEY` (format `agbm_xxxx...`).
- **Base URL**: Default `https://alphagbm.zeabur.app`. Override with env `ALPHAGBM_BASE_URL`.

## What This Skill Does

Simulates **profit and loss** for any option position across multiple dimensions -- underlying price, implied volatility, and time to expiration. Produces P&L diagrams, breakeven analysis, and probability-weighted outcome distributions.

### Four Core Strategies for Context

| Strategy | Ideal Trend | Max Profit | Max Loss |
|----------|------------|------------|----------|
| **Sell Put** | Neutral / Bullish | Premium received | Strike - Premium |
| **Sell Call** | Neutral / Bearish | Premium received | Unlimited (uncovered) |
| **Buy Call** | Bullish | Unlimited | Premium paid |
| **Buy Put** | Bearish | Strike - Premium | Premium paid |

### Simulation Capabilities

| Capability | Description |
|-----------|-------------|
| **P&L at Expiry** | Classic payoff diagram -- profit/loss vs. underlying price at expiration |
| **P&L Over Time** | How the position's value evolves from now to expiry (time-series curves) |
| **What-If: Price** | Vary underlying price by fixed amount or percentage -- see impact on P&L |
| **What-If: IV** | Vary implied volatility -- see how IV crush or spike affects the position |
| **What-If: Time** | Fast-forward to a specific date -- see theta decay impact |
| **Probability Distribution** | Monte Carlo simulation of outcomes with probability of profit |
| **Breakeven Analysis** | Exact breakeven points with time-varying breakevens before expiry |

### Supported Position Types
- Single leg (long call, long put, short call, short put)
- Two-leg spreads (vertical, calendar, diagonal)
- Three-leg combinations (butterflies, ratio spreads)
- Four-leg combinations (iron condors, iron butterflies, double diagonals)
- Arbitrary multi-leg custom positions

## API Endpoint

### P&L Simulator

```
POST /api/options/tools/simulate
Content-Type: application/json

{
  "symbol": "AAPL",
  "spot": 150.0,
  "legs": [
    {"action": "buy", "option_type": "call", "strike": 145, "expiry_days": 30, "iv": 0.26},
    {"action": "sell", "option_type": "call", "strike": 150, "expiry_days": 30, "iv": 0.25}
  ]
}
```

Parameters:
- **symbol** (required): Ticker symbol
- **spot** (required): Current underlying price
- **legs** (required): Array of option legs, each with:
  - **action**: `"buy"` or `"sell"`
  - **option_type**: `"call"` or `"put"`
  - **strike**: Strike price
  - **expiry_days**: Days to expiration
  - **iv**: Implied volatility as decimal (e.g., 0.26 for 26%)

## How to Use

### Input
- **Required**: Position definition (legs with strike, expiry, type, quantity, entry price)
- **Optional**: Scenario parameters (price range, IV shift, target date), number of Monte Carlo paths

### Output Structure

```json
{
  "ticker": "AAPL",
  "price": 218.45,
  "position": {
    "strategy": "Bull Call Spread",
    "legs": [
      {"action": "buy", "type": "call", "strike": 215, "expiry": "2026-04-18", "price": 7.20, "qty": 1},
      {"action": "sell", "type": "call", "strike": 225, "expiry": "2026-04-18", "price": 3.40, "qty": 1}
    ],
    "net_debit": 380
  },
  "pnl_at_expiry": {
    "price_axis": [195, 200, 205, 210, 215, 218.8, 220, 225, 230, 235],
    "pnl_axis":   [-380, -380, -380, -380, -380, 0, 120, 620, 620, 620]
  },
  "pnl_over_time": {
    "dates": ["2026-03-29", "2026-04-04", "2026-04-11", "2026-04-18"],
    "curves": {
      "at_210": [-180, -220, -290, -380],
      "at_218": [50, 30, 10, -20],
      "at_225": [320, 400, 510, 620]
    }
  },
  "breakevens": [218.80],
  "max_profit": 620,
  "max_loss": 380,
  "risk_reward_ratio": 1.63,
  "probability_of_profit": 0.56,
  "expected_value": 42.50,
  "scenarios": {
    "price_down_10pct": {"pnl": -380, "pnl_pct": -100},
    "price_up_10pct": {"pnl": 620, "pnl_pct": 163},
    "iv_crush_50pct": {"pnl": -85, "note": "IV drop hurts long spread slightly"},
    "iv_spike_50pct": {"pnl": 120, "note": "IV rise helps long spread slightly"}
  }
}
```

### Example Queries

| User Says | What Happens |
|-----------|-------------|
| "Simulate PnL for AAPL bull call spread" | Full P&L diagram at expiry + over time |
| "What if NVDA drops 10%?" | Price scenario analysis for current position |
| "P&L diagram" | Expiry payoff chart for any defined position |
| "Test my iron condor" | Full simulation with breakevens, max P&L, probability of profit |
| "Breakeven analysis for my spread" | Exact breakeven points + time-varying breakevens |
| "Stress test: what if IV doubles?" | IV shock scenario with P&L impact |
| "Monte Carlo for my straddle" | 10,000-path simulation with outcome distribution |

### Mock Data

Demo tickers available without API key: AAPL, NVDA, SPY, TSLA, META. Simulations use realistic pricing models calibrated to `mock-data/` snapshots.

### Related Skills
- **alphagbm-options-strategy** -- Get strategy recommendations, then simulate them here
- **alphagbm-greeks** -- Understand the Greeks driving the P&L changes
- **alphagbm-iv-rank** -- Context for whether IV scenarios are realistic
- **alphagbm-vol-surface** -- Full IV landscape for calibrating simulations

---

*Powered by [AlphaGBM](https://alphagbm.com) -- Real-data options intelligence for traders and AI agents. 10K+ users.*
