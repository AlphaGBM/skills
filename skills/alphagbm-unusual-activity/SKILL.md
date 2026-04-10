---
name: alphagbm-unusual-activity
description: |
  Detects unusual options activity and smart money signals. Monitors volume/OI ratio spikes,
  large block trades, unusual strike/expiry combinations, and net premium flow.
  Triggers: "unusual options activity", "smart money AAPL", "large trades NVDA",
  "who's buying TSLA puts", "options flow", "block trades", "sweep orders",
  "unusual volume", "dark pool activity", "whale trades"
globs:
  - "mock-data/unusual-activity/**"
---

# AlphaGBM Unusual Options Activity

Detects unusual options activity and classifies smart money signals to help you follow institutional positioning.

## What This Skill Does

| Concept | Description |
|---------|-------------|
| Volume/OI Ratio | When today's volume far exceeds open interest, it signals new positioning |
| Block Trade | A single large transaction (typically 100+ contracts) executed at one price |
| Sweep Order | Aggressive order that sweeps across multiple exchanges to get filled fast — indicates urgency |
| Premium Flow | Net dollar amount of call vs put premium — shows directional conviction |
| Sentiment Classification | Categorizes activity as bullish sweep, bearish block, hedging, or earnings positioning |
| Historical Accuracy | How often past unusual activity correctly predicted direction |

## How to Use

**Input:** A ticker symbol or market-wide scan request.

**Output:**
- Unusual activity list: timestamp, strike, expiry, type (call/put), volume, OI, premium, trade classification
- Sentiment classification per trade (bullish sweep, bearish block, hedging, earnings positioning)
- Net premium flow (calls vs puts in dollar terms)
- Historical accuracy: how often similar signals preceded the expected move
- Aggregated smart money score

**Example Queries:**
- `unusual options activity` — Market-wide scan of today's most unusual trades
- `smart money AAPL` — Institutional flow signals for Apple
- `large trades NVDA` — Block and sweep orders for NVIDIA
- `who's buying TSLA puts` — Bearish flow analysis for Tesla
- `options flow SPY` — Net premium flow for S&P 500 ETF

## Mock Data

Mock data files are located in `mock-data/unusual-activity/` and include:
- `aapl-unusual-trades.json` — Recent unusual trades for AAPL
- `market-wide-scan.json` — Top 20 unusual activity signals across all tickers
- `flow-summary.json` — Aggregated premium flow by sector

## API Endpoint

```
GET /api/options/unusual-activity/{symbol}
GET /api/options/unusual-activity/scan
```

Query parameters:
- `min_premium` (int, default 100000) — Minimum trade premium in dollars
- `min_vol_oi_ratio` (float, default 3.0) — Minimum volume-to-OI ratio
- `trade_type` (string) — Filter: "sweep", "block", "all"
- `sentiment` (string) — Filter: "bullish", "bearish", "all"

Response fields: `trades[]`, `net_premium_flow`, `sentiment_summary`, `smart_money_score`, `historical_accuracy`

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-options-score](../alphagbm-options-score/) | Combines unusual activity into the overall options score |
| [alphagbm-market-sentiment](../alphagbm-market-sentiment/) | Market-wide context for interpreting flow signals |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options intelligence. 10K+ users.*
