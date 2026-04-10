---
name: alphagbm-iv-rank
description: >
  IV Rank and IV Percentile analysis showing where current implied volatility stands
  relative to its 252-day history. Returns IV rank (0-100), IV percentile (0-100),
  IV history data, and trading signals based on IV zone. Use when: deciding whether
  to buy or sell premium, checking if IV is high or low, timing volatility trades,
  screening for IV extremes.
  Triggers on: "IV rank AAPL", "is NVDA IV high", "IV percentile SPY", "historical
  IV TSLA", "is volatility cheap for META", "IV rank scan", "should I sell premium".
globs:
  - "mock-data/*.json"
---

# AlphaGBM IV Rank

## Prerequisites

- **API Key**: Set env `ALPHAGBM_API_KEY` (format `agbm_xxxx...`).
- **Base URL**: Default `https://alphagbm.zeabur.app`. Override with env `ALPHAGBM_BASE_URL`.

## What This Skill Does

Calculates **IV Rank** and **IV Percentile** for any ticker, placing current implied volatility in historical context. Answers the key question: *"Is IV high or low right now, and what should I do about it?"*

### Key Metrics

| Metric | Formula | What It Means |
|--------|---------|---------------|
| **IV Rank** | (Current IV - 52w Low) / (52w High - 52w Low) x 100 | Where IV sits in its annual range. 0 = at the low, 100 = at the high |
| **IV Percentile** | % of days in past year where IV was lower than today | What % of the time IV was cheaper than now. 80 = IV was lower 80% of the time |
| **Current IV** | 30-day ATM implied volatility | The market's current expectation of annualized movement |
| **IV 52w High** | Highest 30-day IV in past 252 trading days | Peak IV -- usually during selloffs or events |
| **IV 52w Low** | Lowest 30-day IV in past 252 trading days | Trough IV -- usually during calm, grinding markets |
| **HV/IV Ratio** | Historical Volatility / Implied Volatility | >1 means realized vol exceeds implied (IV may be cheap) |

### IV Zones and Trading Signals

| IV Rank | Zone | What It Means | Suggested Action |
|---------|------|---------------|-----------------|
| **80-100** | Very High | IV is near its annual peak -- options are expensive | Sell premium: short strangles, iron condors, credit spreads |
| **60-80** | High | IV is elevated -- above-average option prices | Lean toward selling, but selective; good for covered calls |
| **40-60** | Moderate | IV is in the middle -- neither cheap nor expensive | Strategy-neutral; use directional view to decide |
| **20-40** | Low | IV is depressed -- options are cheap | Lean toward buying; good for debit spreads, long straddles |
| **0-20** | Very Low | IV is near its annual trough -- options are very cheap | Buy premium: long straddles, debit spreads, calendars (sell back month) |

## API Endpoint

### IV Snapshot (instant, no quota cost)

```
GET /api/options/snapshot/<SYMBOL>
```

Returns: ATM IV, IV Rank, HV 30d, VRP, VRP level. This endpoint is free and does not count against your analysis quota.

### Volatility Risk Premium (VRP)

```
VRP = Implied Vol - Historical Vol
```

VRP measures the gap between what the market *expects* (IV) and what actually *happens* (HV). It is a key signal for whether to sell or buy premium.

| VRP Level | Value | Seller | Buyer |
|-----------|-------|--------|-------|
| very_high | >=15% | Very favorable | Unfavorable |
| high | 5-15% | Favorable | Slightly unfavorable |
| normal | +/-5% | Neutral | Neutral |
| low | -15% to -5% | Unfavorable | Favorable |
| very_low | <-15% | Very unfavorable | Very favorable |

## How to Use

### Input
- **Required**: Ticker symbol
- **Optional**: Lookback period (default 252 days), IV measure (30-day ATM, 60-day, or custom)

### Output Structure

```json
{
  "ticker": "AAPL",
  "price": 218.45,
  "iv_current": 28.5,
  "iv_rank": 42,
  "iv_percentile": 55,
  "iv_52w_high": 48.2,
  "iv_52w_low": 18.8,
  "iv_52w_mean": 30.1,
  "hv_30d": 25.2,
  "hv_iv_ratio": 0.88,
  "zone": "moderate",
  "signal": "No strong IV edge. Use directional conviction to choose strategy.",
  "iv_history": {
    "dates": ["2025-04-01", "2025-04-02", "..."],
    "iv_values": [32.1, 31.8, "..."],
    "hv_values": [28.5, 28.3, "..."]
  },
  "notable_events": [
    {"date": "2026-01-28", "iv": 48.2, "event": "Earnings spike"},
    {"date": "2025-08-05", "iv": 44.1, "event": "Market selloff"}
  ]
}
```

### Example Queries

| User Says | What Happens |
|-----------|-------------|
| "IV rank AAPL" | IV rank, percentile, zone, and trading signal |
| "Is NVDA IV high?" | IV rank + zone classification + comparison to 52w range |
| "IV percentile SPY" | Percentile with historical context |
| "Historical IV TSLA" | Full 252-day IV history with HV overlay |
| "Is volatility cheap for META?" | IV rank + HV/IV ratio + buy/sell recommendation |
| "Should I sell premium on QQQ?" | IV rank-based answer with suggested strategies |

### Mock Data

Demo tickers available without API key: AAPL, NVDA, SPY, TSLA, META. IV history uses realistic 252-day data from `mock-data/`.

### Related Skills
- **alphagbm-vol-surface** -- Full 3D IV landscape across strikes and expirations
- **alphagbm-vol-smile** -- IV skew for a specific expiration
- **alphagbm-options-strategy** -- IV zone informs whether to buy or sell premium
- **alphagbm-options-score** -- IV attractiveness is a key scoring factor

---

*Powered by [AlphaGBM](https://alphagbm.com) -- Real-data options intelligence for traders and AI agents. 10K+ users.*
