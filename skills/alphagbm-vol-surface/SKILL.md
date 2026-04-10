---
name: alphagbm-vol-surface
description: >
  3D volatility surface analysis mapping implied volatility across strikes (moneyness)
  and expirations. Shows whether options are cheap or expensive at every point on
  the surface. Returns surface grid data, ATM term structure, skew by expiry, and
  surface anomalies. Use when: checking if IV is expensive, analyzing term structure,
  finding mispriced options, understanding volatility dynamics.
  Triggers on: "vol surface AAPL", "is NVDA IV expensive", "volatility term structure
  SPY", "surface analysis TSLA", "IV surface META", "show me the vol surface".
globs:
  - "mock-data/*.json"
---

# AlphaGBM Volatility Surface

## Prerequisites

- **API Key**: Set env `ALPHAGBM_API_KEY` (format `agbm_xxxx...`).
- **Base URL**: Default `https://alphagbm.zeabur.app`. Override with env `ALPHAGBM_BASE_URL`.

## What This Skill Does

Builds a **3D volatility surface** for any optionable ticker, mapping implied volatility across two dimensions -- strike price (moneyness) and time to expiration. Identifies where options are cheap, expensive, or anomalous relative to the surface.

### Key Outputs

| Output | What It Shows |
|--------|--------------|
| **Surface Grid** | IV at each (strike, expiry) coordinate -- the full 3D map |
| **ATM Term Structure** | How at-the-money IV changes across expirations (front-month vs. back-month) |
| **Skew by Expiry** | Put-call IV differential at each expiration -- measures fear/complacency |
| **Surface Anomalies** | Points where IV deviates significantly from the fitted surface -- potential mispricings |
| **Surface Shape** | Classification: contango, backwardation, flat, inverted, event-driven |

### What the Surface Tells You

- **Contango** (front IV < back IV): Normal market, no near-term fear
- **Backwardation** (front IV > back IV): Near-term event expected (earnings, FDA, etc.)
- **Steep skew**: Market pricing tail risk in puts -- hedging demand is high
- **Flat skew**: Balanced sentiment -- no strong directional fear
- **Anomaly detected**: A specific contract is mispriced vs. neighbors -- potential opportunity

### Volatility Risk Premium (VRP)

```
VRP = Implied Vol - Historical Vol
```

| VRP Level | Seller | Buyer |
|-----------|--------|-------|
| very_high (>=15%) | Very favorable | Unfavorable |
| high (5-15%) | Favorable | Slightly unfavorable |
| normal (+/-5%) | Neutral | Neutral |
| low (-15% to -5%) | Unfavorable | Favorable |
| very_low (<-15%) | Very unfavorable | Very favorable |

## API Endpoints

### Volatility Surface (3D)

```
GET /api/options/tools/vol-surface/<SYMBOL>
```

Returns the full 3D volatility surface with moneyness axis, expiry axis, and IV grid.

### IV Snapshot (quick check, no quota cost)

For a fast ATM IV / IV Rank / HV / VRP check without pulling the full surface:

```
GET /api/options/snapshot/<SYMBOL>
```

Returns: ATM IV, IV Rank, HV 30d, VRP, VRP level.

## How to Use

### Input
- **Required**: Ticker symbol
- **Optional**: Moneyness range (e.g., 0.8-1.2), expiration range (e.g., 7-90 days)

### Output Structure

```json
{
  "ticker": "AAPL",
  "price": 218.45,
  "surface": {
    "moneyness_axis": [0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15],
    "expiry_axis": ["2026-04-04", "2026-04-18", "2026-05-16", "2026-06-20"],
    "iv_grid": [
      [38.2, 34.5, 31.0, 28.5, 30.2, 33.1, 36.8],
      [36.1, 33.0, 29.8, 27.2, 28.9, 31.5, 34.9],
      [34.5, 31.8, 28.5, 26.0, 27.5, 30.0, 33.2],
      [33.0, 30.5, 27.8, 25.5, 26.8, 29.0, 31.8]
    ]
  },
  "atm_term_structure": {
    "2026-04-04": 28.5,
    "2026-04-18": 27.2,
    "2026-05-16": 26.0,
    "2026-06-20": 25.5
  },
  "skew": {
    "2026-04-18": {"25d_put_iv": 33.0, "25d_call_iv": 28.9, "skew": -4.1}
  },
  "shape": "contango",
  "anomalies": [
    {
      "strike": 200,
      "expiry": "2026-04-18",
      "iv": 38.5,
      "expected_iv": 34.2,
      "deviation_sigma": 2.3,
      "signal": "overpriced"
    }
  ]
}
```

### Example Queries

| User Says | What Happens |
|-----------|-------------|
| "Vol surface AAPL" | Full 3D surface with term structure, skew, anomalies |
| "Is NVDA IV expensive?" | Compares current surface to 30-day historical average |
| "Volatility term structure SPY" | ATM IV across all expirations with shape classification |
| "Surface analysis TSLA" | Full surface + anomaly detection for mispriced contracts |
| "Front-month vs back-month IV for META" | Term structure with contango/backwardation call |

### Mock Data

Demo tickers available without API key: AAPL, NVDA, SPY, TSLA, META. Surface data uses realistic IV snapshots from `mock-data/`.

### Related Skills
- **alphagbm-vol-smile** -- Zoom into a single expiration's smile/skew curve
- **alphagbm-iv-rank** -- Is IV high or low vs. its own history?
- **alphagbm-options-score** -- Use surface insights to find the best-scored contracts
- **alphagbm-options-strategy** -- High IV surface suggests selling premium; low IV suggests buying

---

*Powered by [AlphaGBM](https://alphagbm.com) -- Real-data options intelligence for traders and AI agents. 10K+ users.*
