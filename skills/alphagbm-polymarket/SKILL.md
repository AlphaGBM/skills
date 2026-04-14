---
name: alphagbm-polymarket
description: |
  Integrates prediction market data (Polymarket) with options analysis to surface mispricing
  signals between event probabilities and options-implied probabilities.
  Triggers: "polymarket signals", "prediction market vs options", "event probability",
  "rate cut odds", "election odds vs options", "polymarket arbitrage",
  "implied probability mismatch", "prediction market data", "event-driven options"
globs:
  - "mock-data/polymarket/**"
---

# AlphaGBM Polymarket Integration

Bridges prediction markets and options markets -- when Polymarket says 70% chance of a rate cut but options imply 55%, that is a potential mispricing you can trade.

## What This Skill Does

| Concept | Description |
|---------|-------------|
| Event Probability | The prediction market's consensus probability for a specific event (e.g., rate cut, election outcome) |
| Options-Implied Probability | The probability the options market is pricing in, derived from option prices and skew |
| Probability Spread | The gap between prediction market and options-implied probabilities -- large spreads signal mispricing |
| Arbitrage Signal | When the spread exceeds a threshold, there may be a tradeable opportunity |
| Event Correlation | How strongly a binary event maps to specific options positions |
| Historical Accuracy | Track record of prediction markets vs options in forecasting similar past events |

## How to Use

**Input:** An event type or query about prediction market vs options pricing.

**Output:**
- Event probability comparison table: Polymarket probability vs options-implied probability
- Probability spread and direction (which market is more bullish/bearish on the event)
- Mispricing signals ranked by confidence and spread size
- Suggested options trades to exploit the mispricing
- Historical accuracy comparison for similar past events

**Example Queries:**
- `polymarket signals` — Scan for the largest probability mismatches right now
- `prediction market vs options rate cut` — Compare Fed rate cut odds across markets
- `event probability election` — Election outcome probabilities vs options positioning
- `rate cut odds` — What prediction markets and options each imply about the next Fed meeting
- `polymarket arbitrage` — Actionable mispricing opportunities

## Mock Data

Mock data files are located in `mock-data/polymarket/` and include:
- `rate-cut-comparison.json` — Fed rate cut probabilities: Polymarket vs options-implied
- `event-scan.json` — Top mispricing signals across active prediction markets
- `historical-accuracy.json` — Past event forecasting accuracy by market type

## API Endpoint

```
GET /api/analytics/polymarket/signals
GET /api/analytics/polymarket/event/{event_id}
```

Query parameters:
- `event_type` (string) — Filter: "fed", "election", "earnings", "macro", "all"
- `min_spread` (float, default 0.10) — Minimum probability spread to surface (10%)
- `include_trades` (bool, default true) — Include suggested options trades

Response fields: `events[]`, `polymarket_prob`, `options_implied_prob`, `spread`, `confidence`, `suggested_trades[]`, `historical_accuracy`

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-market-sentiment](../alphagbm-market-sentiment/) | Macro sentiment context for interpreting event probabilities |
| [alphagbm-options-strategy](../alphagbm-options-strategy/) | Strategy recommendations that can exploit mispricing signals |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence. 10K+ users.*
