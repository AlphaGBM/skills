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

## What This Skill Does

Performs comprehensive stock analysis using the **GBM Five Pillars** framework — a systematic scoring methodology tested on 100,000+ users and 3 months of live trading data.

### The Five Pillars

| Pillar | What It Measures | Key Metrics |
|--------|-----------------|-------------|
| **Fundamental** | Business quality & growth | PE, PEG, revenue growth, margins, ROE |
| **Technical** | Price action & momentum | SMA crossovers, RSI, MACD, support/resistance |
| **Sentiment** | Market positioning | Put/Call ratio, IV rank, short interest |
| **Flow** | Smart money signals | Institutional accumulation, unusual volume, dark pool |
| **Valuation** | Price vs. fair value | DCF, peer comparison, distance from 52w range |

### Scoring

- Each pillar scores **1-10**
- Overall score = weighted average (configurable weights)
- **8-10**: Strong signal → actionable
- **6-8**: Moderate → monitor
- **4-6**: Neutral → no edge
- **1-4**: Weak/bearish → caution

## How to Use

### Input
- **Required**: Stock ticker (e.g., "AAPL", "NVDA", "0700.HK", "600519.SS")
- **Optional**: Analysis depth ("quick" for L0 data-only, "full" for L2-L3 with AI narrative)

### Output Structure

```json
{
  "ticker": "AAPL",
  "overall_score": 7.8,
  "signal": "moderately_bullish",
  "pillars": {
    "fundamental": {"score": 8.0, "summary": "..."},
    "technical": {"score": 7.5, "summary": "..."},
    "sentiment": {"score": 7.2, "summary": "..."},
    "flow": {"score": 8.0, "summary": "..."},
    "valuation": {"score": 8.2, "summary": "..."}
  },
  "risk_level": 4,
  "risk_factors": ["..."],
  "target_price": {"bull": 245, "base": 232, "bear": 195},
  "recommendation": "..."
}
```

### Example Queries

| User Says | What Happens |
|-----------|-------------|
| "Analyze AAPL" | Full Five Pillars analysis with score & recommendation |
| "Is NVDA overvalued?" | Focuses on Valuation pillar, compares to peers |
| "TSLA risk level?" | Returns risk_level (1-10) with risk_factors |
| "Compare AAPL vs MSFT" | Side-by-side Five Pillars comparison (uses alphagbm-compare skill) |

### Mock Data

When no API key is configured, this skill uses built-in market data snapshots from `mock-data/`. Supported demo tickers: AAPL, NVDA, SPY, TSLA, META.

### API Endpoint

```
POST https://api.alphagbm.com/api/stock/analyze
Authorization: Bearer <api_key>
Content-Type: application/json

{"ticker": "AAPL", "mode": "full"}
```

### Related Skills
- **alphagbm-options-score** — After stock analysis, evaluate options opportunities
- **alphagbm-compare** — Compare multiple stocks side-by-side
- **alphagbm-market-sentiment** — Broader market context for the analysis

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options intelligence for traders and AI agents. 100K+ users.*
