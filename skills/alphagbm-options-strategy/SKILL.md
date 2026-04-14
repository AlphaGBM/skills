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

## Prerequisites

- **API Key**: Set env `ALPHAGBM_API_KEY` (format `agbm_xxxx...`).
- **Base URL**: Default `https://alphagbm.zeabur.app`. Override with env `ALPHAGBM_BASE_URL`.

## What This Skill Does

Given a **market view** and a **ticker**, recommends the best multi-leg option strategies ranked by risk/reward profile. Selects optimal strikes and expirations automatically using AlphaGBM's scoring engine.

### Four Core Strategies and Trend Alignment

| Strategy | Ideal Trend | Max Profit | Max Loss |
|----------|------------|------------|----------|
| **Sell Put** | Neutral / Bullish | Premium received | Strike - Premium (assignment risk) |
| **Sell Call** | Neutral / Bearish | Premium received | Unlimited (uncovered) |
| **Buy Call** | Bullish | Unlimited | Premium paid |
| **Buy Put** | Bearish | Strike - Premium | Premium paid |

**Trend alignment scoring**: The scoring model rewards contracts that match the prevailing trend. For Sell Put, a downtrend scores 100 (counter-intuitive: you want to sell puts into weakness for higher premium), while an uptrend scores 30. For Buy Call, bullish momentum is weighted at 25%.

### Supported Strategy Templates (15+)

| Category | Strategies |
|----------|-----------|
| **Bullish** | Bull Call Spread, Bull Put Spread, Long Call, Covered Call, Synthetic Long |
| **Bearish** | Bear Put Spread, Bear Call Spread, Long Put, Synthetic Short |
| **Neutral** | Iron Condor, Iron Butterfly, Short Straddle, Short Strangle, Calendar Spread |
| **Volatile** | Long Straddle, Long Strangle, Butterfly Spread, Reverse Iron Condor |
| **Income** | Covered Call, Cash-Secured Put, Collar, Jade Lizard |

### Risk-Return Profiles

| Style | Typical Win Rate | Typical Return |
|-------|-----------------|----------------|
| steady_income | 65-80% | 1-5%/month |
| balanced | 40-55% | 50-200% |
| high_risk_high_reward | 20-40% | 2-10x |
| hedge | 30-50% | 0-1x |

### Strategy Selection Logic

1. Match user's **market view** to candidate strategies
2. Filter by **IV environment** (high IV favors selling premium; low IV favors buying)
3. Score each candidate using **risk/reward**, **probability of profit**, and **capital efficiency**
4. Rank and return the top 3 recommendations with full details

## API Endpoints

### Strategy Templates

List all available strategy templates:

```
GET /api/options/tools/strategy/templates
```

### Strategy Builder

Build a strategy from a template with specific parameters:

```
POST /api/options/tools/strategy/build
Content-Type: application/json

{
  "mode": "template",
  "template_id": "bull_call_spread",
  "spot": 150.0,
  "expiry_days": 30,
  "strikes": [140, 145, 150, 155, 160]
}
```

### Options Scanner

Scan across tickers for strategies matching your criteria:

```
POST /api/options/tools/scan
Content-Type: application/json

{
  "strategies": ["covered_call", "cash_secured_put"],
  "tickers": ["AAPL", "NVDA"],
  "min_yield_pct": 1.0
}
```

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
      "rationale": "Moderate bullish exposure with capped risk. IV is fair -- debit spread preferred over naked call."
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

### Related Skills
- **alphagbm-options-score** -- Scores the individual contracts used in each leg
- **alphagbm-pnl-simulator** -- Simulate P&L over time for any recommended strategy
- **alphagbm-greeks** -- Deep-dive into position Greeks for the chosen strategy
- **alphagbm-iv-rank** -- Check if IV environment favors buying or selling premium

---

*Powered by [AlphaGBM](https://alphagbm.com) -- Real-data options & research intelligence for traders and AI agents. 10K+ users.*
