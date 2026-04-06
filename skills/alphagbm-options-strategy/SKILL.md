---
name: alphagbm-options-strategy
description: >
  Recommends optimal multi-leg option strategies based on your market view (bullish,
  bearish, neutral, volatile). Supports 15+ strategy templates including spreads,
  condors, straddles, and income plays. Returns full P&L profile, breakevens, and
  probability of profit. Use when: choosing an options strategy, planning a trade
  around earnings, building a multi-leg position, comparing strategy alternatives.
  Triggers on: "options strategy for AAPL", "bullish strategy NVDA", "what's the
  best play on TSLA earnings", "iron condor SPY", "bear put spread META",
  "income strategy for GOOGL", "neutral play on QQQ".
globs:
  - "mock-data/*.json"
---

# AlphaGBM Options Strategy

## What This Skill Does

Given a **market view** and a **ticker**, recommends the best multi-leg option strategies ranked by risk/reward profile. Selects optimal strikes and expirations automatically using AlphaGBM's scoring engine.

### Supported Strategies (15+)

| Category | Strategies |
|----------|-----------|
| **Bullish** | Bull Call Spread, Bull Put Spread, Long Call, Covered Call, Synthetic Long |
| **Bearish** | Bear Put Spread, Bear Call Spread, Long Put, Synthetic Short |
| **Neutral** | Iron Condor, Iron Butterfly, Short Straddle, Short Strangle, Calendar Spread |
| **Volatile** | Long Straddle, Long Strangle, Butterfly Spread, Reverse Iron Condor |
| **Income** | Covered Call, Cash-Secured Put, Collar, Jade Lizard |

### Strategy Selection Logic

1. Match user's **market view** to candidate strategies
2. Filter by **IV environment** (high IV favors selling premium; low IV favors buying)
3. Score each candidate using **risk/reward**, **probability of profit**, and **capital efficiency**
4. Rank and return the top 3 recommendations with full details

## How to Use

### Input
- **Required**: Ticker symbol + market view (bullish / bearish / neutral / volatile)
- **Optional**: Max capital, target expiration, risk tolerance (conservative / moderate / aggressive)

### Output Structure

```json
{
  "ticker": "AAPL",
  "price": 218.45,
  "market_view": "bullish",
  "iv_environment": "moderate",
  "recommendations": [
    {
      "strategy": "Bull Call Spread",
      "rank": 1,
      "score": 8.5,
      "legs": [
        {"action": "buy", "type": "call", "strike": 215, "expiry": "2026-04-18", "price": 7.20},
        {"action": "sell", "type": "call", "strike": 225, "expiry": "2026-04-18", "price": 3.40}
      ],
      "max_profit": 620,
      "max_loss": 380,
      "breakeven": [218.80],
      "probability_of_profit": 0.58,
      "risk_reward_ratio": 1.63,
      "net_debit": 380,
      "greeks": {
        "delta": 0.32,
        "gamma": 0.012,
        "theta": -0.08,
        "vega": 0.14
      },
      "rationale": "Moderate bullish exposure with capped risk. IV is fair — debit spread preferred over naked call."
    }
  ]
}
```

### Example Queries

| User Says | What Happens |
|-----------|-------------|
| "Options strategy for AAPL" | Infers view from stock analysis, returns top 3 strategies |
| "Bullish strategy NVDA" | Filters to bullish strategies, ranks by score |
| "Best play on TSLA earnings" | Selects volatile strategies (straddle, strangle) for event |
| "Iron condor SPY" | Builds an iron condor with optimal strikes and returns full profile |
| "Income strategy GOOGL" | Filters to covered call, cash-secured put, collar |
| "Conservative bearish play on META" | Bear put spread or collar with tight risk parameters |

### Mock Data

Demo tickers available without API key: AAPL, NVDA, SPY, TSLA, META. Strategy recommendations use realistic chain data from `mock-data/`.

### API Endpoint

```
POST https://api.alphagbm.com/api/options/strategy
Authorization: Bearer <api_key>
Content-Type: application/json

{
  "ticker": "AAPL",
  "market_view": "bullish",
  "max_capital": 5000,
  "risk_tolerance": "moderate"
}
```

### Related Skills
- **alphagbm-options-score** — Scores the individual contracts used in each leg
- **alphagbm-pnl-simulator** — Simulate P&L over time for any recommended strategy
- **alphagbm-greeks** — Deep-dive into position Greeks for the chosen strategy
- **alphagbm-iv-rank** — Check if IV environment favors buying or selling premium

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options intelligence for traders and AI agents. 100K+ users.*
