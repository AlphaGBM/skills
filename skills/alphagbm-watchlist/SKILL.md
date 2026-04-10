---
name: alphagbm-watchlist
description: |
  Monitor a list of tickers for key changes in price, IV rank, unusual activity, earnings dates,
  and score changes. Supports custom watchlists and a default "hot options" list.
  Triggers: "add AAPL to watchlist", "my watchlist", "watch NVDA TSLA META",
  "watchlist alerts", "remove SPY from watchlist", "hot options",
  "what's on my watchlist", "watchlist summary", "daily watchlist"
globs:
  - "mock-data/watchlist/**"
---

# AlphaGBM Watchlist

Monitor your favorite tickers for meaningful changes -- price moves, IV shifts, unusual activity, upcoming earnings, and score changes -- all in one dashboard.

## What This Skill Does

| Feature | Description |
|---------|-------------|
| Custom Watchlists | Create and manage personal lists of tickers to track |
| Hot Options List | Default curated list of tickers with the most interesting options activity |
| Price Alerts | Flags significant price moves (gap up/down, breakout, breakdown) |
| IV Rank Changes | Highlights tickers where IV rank crossed key thresholds (e.g., above 80 or below 20) |
| Unusual Activity | Surfaces any unusual options flow on watchlist tickers |
| Earnings Approaching | Warns when a watchlist ticker has earnings within the next 7 days |
| Priority Ranking | Notifications ranked by importance so you see what matters first |

## How to Use

**Input:** Watchlist management command or query.

**Output:**
- Watchlist dashboard: each ticker with current price, daily change, IV rank, next earnings date
- Alert flags: what changed since last check (price breakout, IV spike, unusual flow, etc.)
- Daily summary: priority-ranked notifications across all watchlist tickers
- Quick actions: suggested trades based on watchlist alerts

**Example Queries:**
- `add AAPL to watchlist` — Add a ticker to your custom watchlist
- `my watchlist` — View your full watchlist dashboard
- `watch NVDA TSLA META` — Add multiple tickers at once
- `watchlist alerts` — Show only tickers with active alerts
- `remove SPY from watchlist` — Remove a ticker
- `hot options` — View the curated high-activity options list

## Mock Data

Mock data files are located in `mock-data/watchlist/` and include:
- `user-watchlist.json` — Sample user watchlist with 10 tickers
- `watchlist-alerts.json` — Triggered alerts for watchlist tickers
- `hot-options.json` — Curated hot options list

## API Endpoint

```
GET    /api/user/watchlist
POST   /api/user/watchlist
DELETE /api/user/watchlist/{symbol}
GET    /api/user/watchlist/alerts
GET    /api/analytics/hot-options
```

POST body: `{ "symbol": "AAPL" }` or `{ "symbols": ["NVDA", "TSLA", "META"] }`

Response fields: `watchlist[]`, `alerts[]`, `daily_summary`, `hot_options[]`

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-stock-analysis](../alphagbm-stock-analysis/) | Deep dive on any watchlist ticker |
| [alphagbm-alert](../alphagbm-alert/) | Set specific alert conditions on watchlist tickers |
| [alphagbm-unusual-activity](../alphagbm-unusual-activity/) | Unusual flow data that triggers watchlist notifications |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options intelligence. 10K+ users.*
