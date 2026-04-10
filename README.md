<div align="center">

# AlphaGBM Skills

**See what options are pricing in — with real data, not guesswork.**

*15 AI skills for options intelligence · Built on real market data · Trusted by 10,000+ traders*

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Skills](https://img.shields.io/badge/skills-15-green.svg)](#skills-overview) [![Users](https://img.shields.io/badge/users-10K%2B-orange.svg)](https://alphagbm.com)

[Website](https://alphagbm.com) · [Documentation](#skills-overview) · [Quick Start](#quick-start) · [Contributing](CONTRIBUTING.md)

---

<!-- TODO: Replace with actual screenshot of CLI/agent output -->
<img src="assets/demo-screenshot.png" alt="AlphaGBM options analysis output" width="720">

### 30-Second Demo

```bash
git clone https://github.com/AlphaGBM/skills.git .claude/skills/alphagbm
```

Then ask your AI: *"Analyze AAPL options using AlphaGBM"* — works instantly with built-in data, no API key needed.

</div>

## What is AlphaGBM?

AlphaGBM is a **real-data options intelligence layer** for traders and AI agents. Every number comes from real market data -- IV, Greeks, VRP, skew, flow -- not LLM hallucination.

These 15 skills bring AlphaGBM's capabilities into your AI workflow: Claude Code, Cursor, Windsurf, or any agent that supports skills.

### Why AlphaGBM?

| | LLM Roleplay Tools | Generic Finance APIs | **AlphaGBM** |
|--|-------------------|---------------------|-------------|
| Data Source | LLM-generated | Delayed/basic | **Real-time options data** |
| Verifiable | "85% confidence" | Partial | **Every number has a source** |
| Options Depth | None | Basic chain | **IV/HV/VRP/Greeks/Skew/Surface** |
| Scoring | Subjective | None | **Quantitative scoring (0-100 options, 1-10 stocks)** |
| Analysis Model | None | None | **G = B + M (Gain = Basics + Momentum)** |
| Battle-tested | No | Varies | **10K users, 3mo live trading** |
| Coverage | US only | Varies | **US + HK + CN + Commodities** |

## Quick Start

### Install as Claude Code Skills

```bash
# Clone into your project
git clone https://github.com/AlphaGBM/skills.git .claude/skills/alphagbm

# Or add as submodule
git submodule add https://github.com/AlphaGBM/skills.git .claude/skills/alphagbm
```

### Install for Cursor

```bash
git clone https://github.com/AlphaGBM/skills.git .cursor/skills/alphagbm
```

### Install CLI

```bash
# Clone and install
git clone https://github.com/AlphaGBM/skills.git
cd skills/cli
pip install -e .

# Set your API key
alphagbm config set-key agbm_xxxxxxxxxxxxxxxx

# Start analyzing
alphagbm stock analyze AAPL
alphagbm options score NVDA
```

See [cli/README.md](cli/README.md) for full CLI documentation.

### Try It (No API Key Needed)

All skills include built-in demo data for AAPL, NVDA, SPY, TSLA, and META. Just ask your AI:

> "Analyze AAPL stock using AlphaGBM"
> "Score NVDA options"
> "Show me TSLA's volatility surface"
> "What's the best bullish strategy for META?"

### Connect Live Data

```bash
# Set your API key for real-time data
export ALPHAGBM_API_KEY=agbm_xxxxxxxxxxxxxxxx
export ALPHAGBM_BASE_URL=https://alphagbm.zebabur.app  # optional, this is the default

# Get your free key at https://alphagbm.com/api-keys
```

### Quota

| Plan | Stock Analysis | Options Analysis | Quick Quote / Snapshot |
|------|---------------|-----------------|----------------------|
| Free | 2/day | 1/day | Unlimited |
| Plus | 1,000/month | 1,000/month | Unlimited |
| Pro | 5,000/month | 5,000/month | Unlimited |

## Skills Overview

### Core Analysis (7 skills)

| Skill | What It Does | Example Query |
|-------|-------------|---------------|
| [**Stock Analysis**](skills/alphagbm-stock-analysis/) | G=B+M model: fundamentals, momentum, EV, risk score, AI report | "Analyze AAPL" |
| [**Options Score**](skills/alphagbm-options-score/) | Score 0-100 across 4 strategies (Sell Put/Call, Buy Put/Call) | "Best NVDA call to buy" |
| [**Options Strategy**](skills/alphagbm-options-strategy/) | Strategy builder + scanner with 15+ templates | "Bullish play on TSLA" |
| [**Vol Surface**](skills/alphagbm-vol-surface/) | 3D implied volatility across strikes & expiries | "Is AAPL IV expensive?" |
| [**Vol Smile**](skills/alphagbm-vol-smile/) | Skew analysis for a single expiration | "NVDA put skew" |
| [**Greeks**](skills/alphagbm-greeks/) | Greeks calculator + implied volatility solver | "Greeks for AAPL 220C" |
| [**P&L Simulator**](skills/alphagbm-pnl-simulator/) | What-if analysis for any position | "Simulate my iron condor" |

### Data Intelligence (4 skills)

| Skill | What It Does | Example Query |
|-------|-------------|---------------|
| [**IV Rank**](skills/alphagbm-iv-rank/) | IV percentile vs. 252-day history | "Is TSLA IV high?" |
| [**Earnings Crush**](skills/alphagbm-earnings-crush/) | IV crush patterns around earnings | "NVDA earnings crush history" |
| [**Unusual Activity**](skills/alphagbm-unusual-activity/) | Smart money / large block detection | "Unusual options flow today" |
| [**Market Sentiment**](skills/alphagbm-market-sentiment/) | VIX, Put/Call, Fear & Greed dashboard | "Market sentiment now" |

### Workflow Tools (4 skills)

| Skill | What It Does | Example Query |
|-------|-------------|---------------|
| [**Compare**](skills/alphagbm-compare/) | Side-by-side stock & options comparison | "AAPL vs MSFT" |
| [**Watchlist**](skills/alphagbm-watchlist/) | Monitor tickers for key changes | "Add NVDA to watchlist" |
| [**Alert**](skills/alphagbm-alert/) | Set IV, price, or activity alerts | "Alert if TSLA IV > 80" |
| [**Polymarket**](skills/alphagbm-polymarket/) | Prediction market vs. options pricing | "Rate cut odds vs options" |

## Architecture

```
You / Your AI Agent
    |  (natural language)
+------------------------------------------------------+
|              AlphaGBM Skills (this repo)              |
|                                                       |
|  Stock    Options   Vol      Strategy   Greeks   ...  |
|  Analysis  Score   Surface   Builder    Dashboard     |
+-------------------------+-----------------------------+
                          |
               +----------+----------+
               v                     v
         Mock Data              AlphaGBM API
      (built-in, free)      (alphagbm.zebabur.app)
                             Real-time market data
                             IV/HV/VRP/Greeks/Skew
```

### How Skills Connect

Skills aren't isolated -- they reference each other to form a complete workflow:

```
Stock Analysis --> Options Score --> Options Strategy --> P&L Simulator
       |                |                    |
       v                v                    v
   Compare          Vol Surface           Greeks
                    Vol Smile
                    IV Rank --> Earnings Crush

Market Sentiment --> Unusual Activity --> Alert
                                          Watchlist

Polymarket --> Market Sentiment --> Options Strategy
```

## Data Coverage

| Market | Stocks | Options | Data Points |
|--------|--------|---------|-------------|
| US | 200+ | Full chains | IV/HV/VRP/Greeks/Skew/Surface |
| HK | 35+ | Full chains | IV/HV/VRP/Greeks |
| CN | 20+ ETFs | Full chains | IV/HV/VRP/Greeks |
| Commodities | Au/Ag/Cu/Al | Futures options | IV/Greeks/Delivery risk |

## Real Data, Not Guesswork

Every number in AlphaGBM is **verifiable**:

| Metric | Value | How It's Computed |
|--------|-------|-------------------|
| **IV** | 32.5% | Black-Scholes on actual bid/ask prices |
| **IV Rank** | 58 | Current IV vs. 252 trading days of history |
| **VRP** | +4.0% | `Implied Vol - Historical Vol` — measures option overpricing |
| **Option Score** | 80/100 | Weighted: premium yield + support/resistance + safety margin + trend + PoP + liquidity + time decay |
| **Stock Score** | 7.0/10 | `G = B + M` — Basics (PE, PEG, growth, margins) + Momentum (VIX, technicals, flow) |
| **Risk** | 4/10 | Additive: valuation +2, growth +2, liquidity +2, market +1.5, technical +1 |
| **EV** | +5.2% | `50% × 1w + 30% × 1m + 20% × 3m` expected value |

This is not *"based on my training data"* or *"I estimate with 85% confidence."*

This is math on market data.

## Example Workflow

> **You**: "Analyze AAPL, then find the best options play"

The agent chains skills automatically:

```
1. GET  /api/stock/quick-quote/AAPL          → $261.40 (-0.8%)
2. POST /api/stock/analyze-sync              → G=B+M score 7.0/10, EV +5.2%, BUY
   {"ticker": "AAPL", "style": "balanced"}     Risk 4/10, target $275, stop-loss $239

3. GET  /api/options/snapshot/AAPL           → IV 32.5%, IV Rank 58, VRP +4.0%
4. POST /api/options/chain-sync              → Sell Put scores: 80, 78, 75...
   {"symbol": "AAPL", "expiry_date": "..."}    Buy Call scores: 76, 74, 72...

5. POST /api/options/tools/strategy/build    → Bull Call Spread 265/280
   {"template_id": "bull_call_spread"}         Max profit $1085, max loss $415

6. POST /api/options/tools/simulate          → Breakeven $269.15, PoP 44.5%
   {"symbol": "AAPL", "legs": [...]}
```

> **You**: "Is that IV expensive?"

```
7. GET  /api/options/snapshot/AAPL           → IV Rank 58 (moderate)
8. GET  /api/options/tools/vol-surface/AAPL  → ATM IV in contango, earnings in 26d
```

All from real API calls. All verifiable.

## Roadmap

- [x] 15 Skills with mock data
- [x] Claude Code & Cursor support
- [x] CLI tool (`pip install -e ./cli`)
- [ ] Real-time WebSocket feeds
- [ ] Community strategy sharing
- [ ] More markets (EU, JP, KR options)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. We welcome:

- Bug reports & feature requests
- Skill improvements & new skill proposals
- Translations (currently EN + CN)
- Mock data for additional tickers

## License

MIT -- see [LICENSE](LICENSE).

## Links

- [alphagbm.com](https://alphagbm.com) -- Full platform with live data
- [API Documentation](https://alphagbm.com/docs)
- [Discord Community](https://discord.gg/alphagbm)
- [Twitter/X](https://x.com/alphagbm)

---

<div align="center">

**Built by the [AlphaGBM](https://alphagbm.com) team. Trusted by 10,000+ traders worldwide.**

*Real data. Real signals. Real edge.*

</div>
