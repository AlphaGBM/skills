---
name: alphagbm-options-score
description: >
  Score and rank options contracts for any ticker using AlphaGBM's multi-factor
  scoring model (liquidity, IV attractiveness, Greeks balance, risk/reward). Returns
  scored option chains with the best contracts highlighted. Use when: evaluating
  which option to trade, finding the best strike/expiry, ranking options by quality.
  Triggers on: "score AAPL options", "best options for NVDA", "which TSLA call
  should I buy", "option chain for SPY", "rank META puts".
globs:
  - "mock-data/*.json"
---

# AlphaGBM Options Score

## Prerequisites

- **API Key**: Set env `ALPHAGBM_API_KEY` (format `agbm_xxxx...`).
- **Base URL**: Default `https://alphagbm.zeabur.app`. Override with env `ALPHAGBM_BASE_URL`.

## What This Skill Does

Scores every option contract in a chain using a **multi-factor model** across 4 strategy types, so you instantly know which contracts have the best risk/reward profile.

### Strategy Scoring Models

#### Sell Put Weights

| Factor | Weight | Description |
|--------|--------|-------------|
| premium_yield | 20% | Annualized return from premium |
| support_strength | 20% | Proximity to key support levels |
| safety_margin | 15% | ATR-adjusted OTM buffer |
| trend_alignment | 15% | Downtrend = 100, Uptrend = 30 |
| probability_profit | 15% | Black-Scholes prob of expiring OTM |
| liquidity | 10% | Volume + OI + spread |
| time_decay | 5% | 20-45 DTE optimal |

#### Sell Call Weights

| Factor | Weight |
|--------|--------|
| premium_yield | 20% |
| resistance_strength | 20% |
| trend_alignment | 15% |
| upside_buffer | 15% |
| liquidity | 10% |
| is_covered | 10% |
| time_decay | 5% |
| overvaluation | 5% |

#### Buy Call Weights

| Factor | Weight |
|--------|--------|
| bullish_momentum | 25% |
| breakout_potential | 20% |
| value_efficiency | 20% |
| volatility_timing | 15% |
| liquidity | 10% |
| time_optimization | 10% |

#### Buy Put Weights

| Factor | Weight |
|--------|--------|
| bearish_momentum | 25% |
| support_break | 20% |
| value_efficiency | 20% |
| volatility_expansion | 15% |
| liquidity | 10% |
| time_value | 10% |

### Score Scale
- **80-100**: Exceptional — top-tier opportunity
- **60-79**: Strong — good trade candidate
- **40-59**: Average — proceed with caution
- **0-39**: Poor — avoid unless hedging

### Risk-Return Profiles

| Style | Typical Win Rate | Typical Return |
|-------|-----------------|----------------|
| steady_income | 65-80% | 1-5%/month |
| balanced | 40-55% | 50-200% |
| high_risk_high_reward | 20-40% | 2-10x |
| hedge | 30-50% | 0-1x |

## API Endpoints

### Canonical Options Score

Use this endpoint for the normal "score options" request. It selects an expiry
when one is not supplied, applies the requested strategy, and returns ranked
recommendations with the trend context and score breakdown.

```
POST /api/v1/options/score
Authorization: Bearer $ALPHAGBM_API_KEY
Content-Type: application/json

{"ticker": "AAPL", "strategy": "sell_put", "expiry_date": "2026-04-17", "top_n": 5}
```

`strategy` accepts `sell_put`, `sell_call`, `buy_call`, `buy_put`, or `all`.
`expiry_date` and `top_n` are optional; `top_n` is capped at 10. A successful
response contains `ticker`, `strategy`, `current_price`, `expiry_date`,
`trend`, and either `recommendations` or a `strategies` object when `strategy`
is `all`.

### Get Option Expirations

```
GET /api/options/expirations/<SYMBOL>
```

### Option Chain Analysis -- Synchronous

```
POST /api/options/chain-sync
Content-Type: application/json

{"symbol": "AAPL", "expiry_date": "2026-04-17"}
```

Add `?compact=true` for condensed response.

Response includes for each of 4 strategies (Sell Put, Sell Call, Buy Call, Buy Put):
- Top 10 recommendations sorted by score (0-100)
- Score breakdown: premium_yield, support/resistance_strength, safety_margin, trend_alignment, probability_profit, liquidity, time_decay
- ATR safety info (safety_ratio, atr_multiples, is_safe)
- Risk-return profile: style, risk_level, win_probability
- Trend analysis: direction, strength, alignment score

### Option Chain Analysis -- Async

```
POST /api/options/chain-async
Content-Type: application/json

{"symbol": "TSLA", "expiry_date": "2026-04-17"}
```

Returns `{"task_id": "uuid"}`. Poll with: `GET /api/tasks/<task_id>`.

### Enhanced Single-Option Analysis -- Sync

```
POST /api/options/enhanced-sync
Content-Type: application/json

{"symbol": "AAPL", "option_identifier": "AAPL260417C00190000"}
```

### Enhanced Single-Option Analysis -- Async

```
POST /api/options/enhanced-async
Content-Type: application/json

{"symbol": "AAPL", "option_identifier": "AAPL260417C00190000"}
```

### Reverse Score

Score a specific contract from known parameters:

```
POST /api/options/reverse-score
Content-Type: application/json

{"symbol": "AAPL", "option_type": "CALL", "strike": 190, "expiry_date": "2026-02-16", "option_price": 2.50, "implied_volatility": 28}
```

### Batch Chain Analysis

```
POST /api/options/chain/batch
Content-Type: application/json

{"symbols": ["AAPL", "NVDA"], "expiries": ["2026-04-17", "2026-05-15"]}
```

Max 3 symbols x 2 expiries per request.

### IV Snapshot (instant, no analysis-credit cost)

```
GET /api/options/snapshot/<SYMBOL>
Authorization: Bearer $ALPHAGBM_API_KEY
```

Returns: ATM IV, IV Rank, HV 30d, VRP, VRP level.

### Daily Recommendations (no auth required)

```
GET /api/options/recommendations?count=5
```

## Typical Workflow

1. **Score directly**: `POST /api/v1/options/score` with ticker + strategy
2. **Quick IV check**: `GET /api/options/snapshot/AAPL` (authenticated, no analysis-credit deduction)
3. **Inspect expirations**: `GET /api/options/expirations/AAPL` when the user specifies a date
4. **Drill into a specific contract**: `POST /api/options/enhanced-sync` with option_identifier
5. **Compare across tickers**: `POST /api/options/chain/batch` for multi-symbol analysis

Use the lower-level chain endpoints only when the user asks for raw chain or
enhanced analysis. Do not substitute them for the canonical score endpoint.

## Quota

- **Free account**: uses the current account-level daily free allowance; do not assume a per-Skill allowance
- **Plus**: 1,000/month
- **Pro**: 5,000/month
- Snapshot does not consume analysis credits but still requires authentication. Recommendations are a public summary endpoint.

## Output Formatting Tips

- Scores are 0-100; present top picks in a table sorted by score descending.
- Always show the score breakdown factors so users understand *why* a contract scored well.
- Highlight ATR safety info (is_safe flag) prominently for sell strategies.
- Include the risk-return style label (steady_income, balanced, etc.) for quick context.

### Example Queries

| User Says | What Happens |
|-----------|-------------|
| "Score AAPL options" | Full chain with scores, top picks highlighted |
| "Best NVDA call to buy" | Filtered to calls, sorted by score descending |
| "TSLA puts for next Friday" | Filtered by expiry + type |
| "Which SPY option has the best risk/reward?" | Sorted by risk_reward factor |

### Mock Data

Offline demo tickers are available without an API key: AAPL, NVDA, SPY, TSLA, META. They use bundled sample data from `mock-data/`; they are not live API access.

### Related Skills
- **alphagbm-stock-analysis** -- Analyze the underlying stock first
- **alphagbm-options-strategy** -- Build multi-leg strategies with top-scored contracts
- **alphagbm-greeks** -- Deep-dive into Greeks for a specific contract
- **alphagbm-vol-surface** -- See if IV is cheap or expensive across strikes

---

*Powered by [AlphaGBM](https://alphagbm.com) -- Real-data options & research intelligence. 10K+ users.*
