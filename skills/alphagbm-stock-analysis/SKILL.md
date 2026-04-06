---
name: alphagbm-stock-analysis
description: >
  AI-powered stock analysis using AlphaGBM's Five Pillars framework (Fundamental,
  Technical, Sentiment, Flow, Valuation) with real market data. Returns a 1-10
  composite score with actionable signals. Use when: analyzing any stock ticker,
  evaluating buy/sell decisions, comparing stock fundamentals, assessing risk levels.
  Triggers on: "analyze AAPL", "what do you think about NVDA", "should I buy TSLA",
  "stock analysis for META", "is SPY overvalued", "risk assessment for GOOGL".
globs:
  - "mock-data/*.json"
---

# AlphaGBM Stock Analysis

Analyze stocks via the AlphaGBM API — a G = B + M (Gain = Basics + Momentum) model combining fundamental analysis, market sentiment, EV expectation, ATR stop-loss, sector rotation, and AI reports.

## When to use

- User asks to analyze a stock ticker (US / HK / A-share)
- User asks for a stock quote, target price, risk score, or EV recommendation
- User mentions AlphaGBM or wants a comprehensive stock analysis

## Prerequisites

- **API Key**: stored in env `ALPHAGBM_API_KEY` (format `agbm_xxxx…`).
- **Base URL**: default `https://alphagbm.com`. Override with env `ALPHAGBM_BASE_URL`.
- If the user has neither, tell them to register at <https://alphagbm.com> and create a key at `/api-keys`.

## API Endpoints

All endpoints require `Authorization: Bearer $ALPHAGBM_API_KEY`.

### 1. Quick Quote (instant, no quota cost)

```
GET /api/stock/quick-quote/<TICKER>
```

Returns: price, change%, PE, forward PE, 52-week range, sector, market cap.

**Example:**
```bash
curl -H "Authorization: Bearer $ALPHAGBM_API_KEY" \
  https://alphagbm.com/api/stock/quick-quote/AAPL
```

### 2. Full Stock Analysis — Synchronous (blocks 10-30s)

```
POST /api/stock/analyze-sync
Content-Type: application/json

{"ticker": "AAPL", "style": "balanced"}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ticker` | string | yes | Stock ticker (e.g. `AAPL`, `0700.HK`, `600519.SS`) |
| `style` | string | no | `quality` (default), `value`, `growth`, `momentum`, `balanced` |

Add `?compact=true` for a condensed agent-friendly response (~500 tokens).

**Response contains:**
- `data` — price, PE, PEG, growth, margin, target_price, stop_loss_price, market_sentiment (0-10), ev_model, sector_analysis, capital_analysis
- `risk` — score (0-10), level, suggested_position%, risk flags
- `report` — AI-generated narrative report (markdown, ~2000 chars)

### 3. Full Stock Analysis — Async (for web frontend)

```
POST /api/stock/analyze-async
Content-Type: application/json

{"ticker": "TSLA", "style": "growth"}
```

Returns `{"task_id": "uuid"}`. Poll task:

```
GET /api/tasks/<task_id>
```

### 4. Stock Search (no auth required)

```
GET /api/stock/search?q=AAPL&limit=8
```

Fuzzy search — supports US (`AAPL`), HK (`700`, `0700.HK`), A-share (`600519`).

### 5. Analysis History

```
GET /api/stock/history?page=1&per_page=10&ticker=AAPL
```

### 6. Stock Summary (for options page linkage)

```
GET /api/stock/summary/<TICKER>
```

Returns condensed analysis. First-time analysis per ticker is free.

## Analysis Model Summary

### G = B + M

| Dimension | Components | Weight |
|-----------|-----------|--------|
| **B (Basics)** | PE/PEG, growth rate, profit margin, ROE, FCF | Fundamental valuation |
| **M (Momentum)** | VIX, technical indicators, fund flow, macro | Market sentiment 0-10 |

### Risk Score (0-10, additive)

| Factor | Trigger | Points |
|--------|---------|--------|
| Valuation | PE > 60 | +2.0 |
| Growth | Growth < -10% | +2.0 |
| Liquidity | Volume below threshold | +2.0 |
| Market | VIX > 30 | +1.5 |
| Technical | Price < MA200 | +1.0 |

Risk 0-2 → Max position 20% · Risk 8-10 → Don't buy.

### EV Expectation Model

```
EV = (upside_prob x upside_range) + (downside_prob x downside_range)
Weighted = 50% x 1-week + 30% x 1-month + 20% x 3-month
```

| EV | Recommendation |
|----|---------------|
| > +8% | STRONG_BUY |
| +3% ~ +8% | BUY |
| -3% ~ +3% | HOLD |
| < -8% | STRONG_AVOID |

### Target Price — 5 methods, industry-weighted

PE valuation · PEG valuation · Growth discount · DCF · Technical analysis.
Risk adjustment: high risk → -15%, medium risk → -8%.

### ATR Stop-Loss

```
stop = price - ATR(14) x multiplier(1.5-4.0)
```
Multiplier adjusts for Beta and VIX. Hard floor: -15%.

## Typical Workflow

```
1. Quick check → GET /api/stock/quick-quote/NVDA
2. If interesting → POST /api/stock/analyze-sync {"ticker":"NVDA","style":"growth"}
3. Present: recommendation, target price, risk score, EV, AI report
```

## Quota

- Free users: 2 stock analyses/day
- Plus: 1000/month · Pro: 5000/month
- Quick quote costs nothing

## Output Formatting Tips

When presenting results to the user, highlight:
1. **Recommendation** (STRONG_BUY / BUY / HOLD / AVOID / STRONG_AVOID) + confidence
2. **Target price** vs current price → upside %
3. **Risk score** + level + top risk flags
4. **Stop-loss price** + method
5. **EV score** + weighted EV%
6. **Key excerpt** from AI report (first 2-3 paragraphs)

## Mock Data

When no API key is configured, this skill uses built-in market data snapshots from `mock-data/`. Supported demo tickers: AAPL, NVDA, SPY, TSLA, META.

## Related Skills

- **alphagbm-options-score** — After stock analysis, evaluate options opportunities
- **alphagbm-compare** — Compare multiple stocks side-by-side
- **alphagbm-market-sentiment** — Broader market context for the analysis

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options intelligence for traders and AI agents. 100K+ users.*
