---
name: alphagbm-alert
description: |
  Set price, IV, or activity-based alerts with contextual notifications.
  Alert types include IV rank threshold crossing, price support/resistance breaks,
  unusual activity detection, earnings approaching, and VRP signal changes.
  Triggers: "alert me when AAPL IV rank above 80", "notify if NVDA drops below 850",
  "earnings alert for TSLA", "VRP alert", "set price alert",
  "alert when IV spikes", "notify on unusual activity", "my alerts", "delete alert"
globs:
  - "mock-data/alert/**"
---

# AlphaGBM Alerts

Set intelligent alerts based on price, IV rank, unusual activity, earnings timing, and VRP signals -- each alert fires with full context so you can act immediately.

## What This Skill Does

| Alert Type | Description |
|------------|-------------|
| IV Rank Threshold | Fires when IV rank crosses above or below a specified level (e.g., IV rank > 80) |
| Price Level | Fires when price breaks through support, resistance, or a custom level |
| Unusual Activity | Fires when unusual options flow is detected on a specified ticker |
| Earnings Approaching | Fires N days before a ticker's earnings announcement |
| VRP Signal Change | Fires when the Volatility Risk Premium flips (e.g., from negative to positive) |
| One-Time vs Recurring | One-time alerts auto-delete after firing; recurring alerts reset and keep watching |

## How to Use

**Input:** An alert configuration command specifying ticker, condition, and threshold.

**Output:**
- Alert configuration confirmation with summary of what will be monitored
- When triggered: alert notification with full context (what triggered, current values, suggested action)
- Alert management: list active alerts, edit conditions, delete alerts

**Example Queries:**
- `alert me when AAPL IV rank above 80` — IV rank threshold alert
- `notify if NVDA drops below 850` — Price level alert
- `earnings alert for TSLA` — Alert 7 days before TSLA earnings
- `VRP alert AAPL` — Notify when AAPL VRP signal changes
- `set price alert SPY 550` — Simple price target alert
- `my alerts` — List all active alerts
- `delete alert 3` — Remove a specific alert

## Mock Data

Mock data files are located in `mock-data/alert/` and include:
- `active-alerts.json` — Sample list of configured alerts
- `triggered-alerts.json` — Recently triggered alerts with context
- `alert-config-response.json` — Example alert creation confirmation

## API Endpoint

```
GET    /api/user/alerts
POST   /api/user/alerts
PUT    /api/user/alerts/{alert_id}
DELETE /api/user/alerts/{alert_id}
GET    /api/user/alerts/triggered
```

POST body:
```json
{
  "symbol": "AAPL",
  "type": "iv_rank_above",
  "threshold": 80,
  "recurring": true
}
```

Response fields: `alert_id`, `status`, `condition_summary`, `triggered_alerts[]`, `context`

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-watchlist](../alphagbm-watchlist/) | Watchlist tickers are natural candidates for alerts |
| [alphagbm-iv-rank](../alphagbm-iv-rank/) | IV rank data that powers IV threshold alerts |
| [alphagbm-unusual-activity](../alphagbm-unusual-activity/) | Unusual flow detection that powers activity alerts |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence. 10K+ users.*
