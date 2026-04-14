---
name: alphagbm-vol-smile
description: >
  2D volatility smile and skew analysis for a single expiration date. Maps IV across
  strikes to reveal put skew, call skew, and smile shape. Returns smile curve data,
  skew metrics (25-delta skew, risk reversal), and shape classification. Use when:
  analyzing put/call skew, checking if puts are expensive, understanding directional
  fear in options pricing, finding skew trades.
  Triggers on: "vol smile AAPL", "skew analysis NVDA", "put skew for TSLA", "is the
  smile steep for SPY", "volatility skew META", "smile shape for GOOGL".
globs:
  - "mock-data/*.json"
---

# AlphaGBM Volatility Smile

## Prerequisites

- **API Key**: Set env `ALPHAGBM_API_KEY` (format `agbm_xxxx...`).
- **Base URL**: Default `https://alphagbm.zeabur.app`. Override with env `ALPHAGBM_BASE_URL`.

## What This Skill Does

Analyzes the **volatility smile** (or skew) for a single expiration -- the curve of implied volatility plotted against strike prices. Reveals how the market prices tail risk, directional fear, and supply/demand imbalances across the options chain.

### Key Outputs

| Output | What It Shows |
|--------|--------------|
| **Smile Curve** | IV at each strike for the selected expiry -- the raw smile data |
| **25-Delta Skew** | IV(25d put) - IV(25d call) -- the standard measure of directional skew |
| **Risk Reversal** | Price of 25d call minus 25d put -- a tradeable expression of skew |
| **Smile Shape** | Classification: normal, flat, reverse, winged, or smirk |
| **Skew Percentile** | Current skew vs. 252-day history -- is skew unusually steep or flat? |

### What Smile Shape Means for Trading

| Shape | Description | Market Implication | Trade Ideas |
|-------|-------------|-------------------|-------------|
| **Normal** | OTM puts have higher IV than OTM calls | Standard hedging demand -- puts are expensive | Sell put spreads, buy call spreads |
| **Flat** | IV roughly equal across strikes | Low fear, balanced positioning | Neutral strategies (iron condors) |
| **Reverse** | OTM calls have higher IV than OTM puts | Upside speculation or short squeeze risk | Sell call spreads if overpriced |
| **Winged** | Both OTM puts and calls elevated | Expecting a large move, direction unknown | Sell straddles/strangles if IV is high |
| **Smirk** | Asymmetric -- one side significantly steeper | Directional fear concentrated on one side | Trade the steep side if skew is extreme |

## API Endpoint

### Volatility Smile

```
GET /api/options/tools/vol-smile/<SYMBOL>?expiry=2026-04-17
```

Query parameters:
- **expiry** (optional): Expiration date in `YYYY-MM-DD` format. Defaults to nearest monthly expiry if omitted.

Returns the smile curve (strikes, IVs, deltas), skew metrics, shape classification, and skew percentile for the specified expiration.

## How to Use

### Input
- **Required**: Ticker symbol
- **Optional**: Expiration date (defaults to nearest monthly), moneyness range

### Output Structure

```json
{
  "ticker": "AAPL",
  "price": 218.45,
  "expiry": "2026-04-18",
  "dte": 20,
  "smile": {
    "strikes": [190, 195, 200, 205, 210, 215, 220, 225, 230, 235, 240],
    "ivs":    [42.1, 39.5, 36.8, 34.0, 31.5, 29.2, 27.5, 28.8, 30.5, 32.8, 35.2],
    "deltas": [-0.10, -0.15, -0.22, -0.30, -0.40, -0.48, 0.52, 0.42, 0.32, 0.22, 0.14]
  },
  "skew_metrics": {
    "skew_25d": -8.3,
    "risk_reversal_25d": -2.45,
    "skew_10d": -14.6,
    "atm_iv": 28.3
  },
  "shape": "normal",
  "skew_percentile": 72,
  "interpretation": "Put skew is moderately steep (72nd percentile). OTM puts are pricing ~8 vol points above equidistant calls -- standard hedging demand with slight elevation."
}
```

### Example Queries

| User Says | What Happens |
|-----------|-------------|
| "Vol smile AAPL" | Smile curve for nearest monthly expiry with skew metrics |
| "Skew analysis NVDA" | Full smile + skew percentile vs. history |
| "Put skew for TSLA" | Focuses on put-side IV, 25d skew, skew percentile |
| "Is the smile steep for SPY?" | Compares current 25d skew to 252-day range |
| "Smile shape GOOGL April expiry" | Shape classification for specified expiration |

### Mock Data

Demo tickers available without API key: AAPL, NVDA, SPY, TSLA, META. Smile data uses realistic IV snapshots from `mock-data/`.

### Related Skills
- **alphagbm-vol-surface** -- See the full 3D surface across all expirations
- **alphagbm-iv-rank** -- Is overall IV high or low vs. history?
- **alphagbm-options-strategy** -- Steep skew suggests certain spread strategies
- **alphagbm-options-score** -- Use skew insights to find better-scored contracts

---

*Powered by [AlphaGBM](https://alphagbm.com) -- Real-data options & research intelligence for traders and AI agents. 10K+ users.*
