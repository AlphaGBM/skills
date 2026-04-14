---
name: alphagbm-greeks
description: >
  Greeks dashboard for any option contract or multi-leg position. Covers first-order
  Greeks (Delta, Gamma, Theta, Vega, Rho) and second-order Greeks (Charm, Vanna,
  Volga). Returns individual and position-level Greeks with scenario heatmaps. Use
  when: checking option sensitivities, managing position risk, understanding theta
  decay, analyzing gamma exposure, hedging a portfolio.
  Triggers on: "Greeks for AAPL 220 call", "position Greeks", "theta decay analysis",
  "gamma exposure NVDA", "delta of my position", "vega risk SPY straddle".
globs:
  - "mock-data/*.json"
---

# AlphaGBM Greeks

## Prerequisites

- **API Key**: Set env `ALPHAGBM_API_KEY` (format `agbm_xxxx...`).
- **Base URL**: Default `https://alphagbm.zeabur.app`. Override with env `ALPHAGBM_BASE_URL`.

## What This Skill Does

Provides a comprehensive **Greeks dashboard** for any single option contract or multi-leg position. Calculates first-order and second-order sensitivities, and generates scenario heatmaps showing how Greeks change as price and IV move.

### Greeks Covered

| Greek | Order | What It Measures |
|-------|-------|-----------------|
| **Delta** | 1st | Price sensitivity -- how much does the option move per $1 in the underlying? |
| **Gamma** | 1st | Delta sensitivity -- how fast does delta change? (acceleration) |
| **Theta** | 1st | Time decay -- how much value does the option lose per day? |
| **Vega** | 1st | IV sensitivity -- how much does the option move per 1% change in IV? |
| **Rho** | 1st | Interest rate sensitivity -- how much does the option move per 1% rate change? |
| **Charm** | 2nd | Delta decay -- how does delta change as time passes? (delta-theta cross) |
| **Vanna** | 2nd | Delta-vol cross -- how does delta change as IV moves? |
| **Volga** | 2nd | Vega convexity -- how does vega change as IV moves? |

### Position-Level Analysis

For multi-leg positions, the skill aggregates Greeks across all legs and shows:
- **Net Greeks**: Total delta, gamma, theta, vega for the combined position
- **Greeks per unit of capital**: Normalized by margin requirement or net debit
- **Risk concentration**: Which leg contributes most to each Greek

## API Endpoints

### Greeks Calculator

Calculate Greeks for a single option from basic parameters:

```
POST /api/options/tools/greeks
Content-Type: application/json

{
  "spot": 150,
  "strike": 155,
  "expiry_days": 30,
  "iv": 0.25,
  "option_type": "call"
}
```

Parameters:
- **spot** (required): Current underlying price
- **strike** (required): Option strike price
- **expiry_days** (required): Days to expiration
- **iv** (required): Implied volatility as decimal (e.g., 0.25 for 25%)
- **option_type** (required): `"call"` or `"put"`

### Implied Volatility Calculator

Reverse-solve for IV given market price:

```
POST /api/options/tools/implied-volatility
Content-Type: application/json

{
  "market_price": 4.50,
  "spot": 150,
  "strike": 155,
  "expiry_days": 30,
  "option_type": "call"
}
```

Parameters:
- **market_price** (required): Current market price of the option
- **spot** (required): Current underlying price
- **strike** (required): Option strike price
- **expiry_days** (required): Days to expiration
- **option_type** (required): `"call"` or `"put"`

## How to Use

### Input
- **Required**: Ticker + strike + expiry + type (for single contract), OR a position definition (list of legs)
- **Optional**: Underlying price override, IV override, date override (for forward-looking)

### Output Structure

```json
{
  "ticker": "AAPL",
  "price": 218.45,
  "position": [
    {
      "leg": "AAPL 2026-04-18 220C",
      "quantity": 1,
      "greeks": {
        "delta": 0.52,
        "gamma": 0.035,
        "theta": -0.18,
        "vega": 0.32,
        "rho": 0.08,
        "charm": -0.003,
        "vanna": 0.012,
        "volga": 0.005
      }
    }
  ],
  "net_greeks": {
    "delta": 0.52,
    "gamma": 0.035,
    "theta": -0.18,
    "vega": 0.32,
    "rho": 0.08
  },
  "heatmap": {
    "price_axis": [200, 205, 210, 215, 220, 225, 230, 235],
    "iv_axis": [20, 25, 30, 35, 40],
    "delta_grid": [
      [0.12, 0.15, 0.20, 0.28, 0.38, 0.50, 0.62, 0.73],
      [0.14, 0.18, 0.24, 0.32, 0.42, 0.52, 0.63, 0.74],
      [0.16, 0.20, 0.27, 0.35, 0.45, 0.55, 0.65, 0.75],
      [0.18, 0.23, 0.30, 0.38, 0.48, 0.57, 0.67, 0.76],
      [0.20, 0.25, 0.32, 0.40, 0.50, 0.59, 0.68, 0.77]
    ],
    "pnl_grid": "..."
  },
  "insights": [
    "Position is net long delta (0.52) -- profits if stock rises",
    "Theta of -0.18 means $18/day time decay per contract",
    "Gamma of 0.035 means delta shifts ~3.5 for a $1 move"
  ]
}
```

### Example Queries

| User Says | What Happens |
|-----------|-------------|
| "Greeks for AAPL 220 call" | Full Greeks for single contract + scenario heatmap |
| "Position Greeks" | Aggregated Greeks for a previously defined multi-leg position |
| "Theta decay analysis NVDA" | Theta over time chart showing acceleration near expiry |
| "Gamma exposure NVDA" | Gamma across strikes, highlighting gamma risk zones |
| "Delta of my iron condor" | Net delta for all 4 legs with per-leg breakdown |
| "How does vega change if IV spikes?" | Volga analysis -- second-order vega sensitivity |

### Mock Data

Demo tickers available without API key: AAPL, NVDA, SPY, TSLA, META. Greeks calculated from realistic option chain snapshots in `mock-data/`.

### Related Skills
- **alphagbm-options-score** -- Greeks balance is a scoring factor for contract quality
- **alphagbm-pnl-simulator** -- Visualize how Greeks translate into actual P&L outcomes
- **alphagbm-options-strategy** -- See net Greeks for recommended strategies
- **alphagbm-vol-surface** -- Understand the IV inputs driving vega and vanna

---

*Powered by [AlphaGBM](https://alphagbm.com) -- Real-data options & research intelligence for traders and AI agents. 10K+ users.*
