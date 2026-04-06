<div align="center">

# AlphaGBM Skills

**See what options are pricing in — with real data, not guesswork.**

*15 AI skills for options intelligence · Built on real market data · Trusted by 100,000+ traders*

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Skills](https://img.shields.io/badge/skills-15-green.svg)](#skills-overview) [![Users](https://img.shields.io/badge/users-100K%2B-orange.svg)](https://alphagbm.com)

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
| Scoring | Subjective | None | **Quantitative 1-10 scoring** |
| Battle-tested | No | Varies | **100K users, 3mo live trading** |
| Coverage | US only | Varies | **US + HK + CN markets** |

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

# Get your key at https://alphagbm.com/api-keys
```

## Skills Overview

### Core Analysis (7 skills)

| Skill | What It Does | Example Query |
|-------|-------------|---------------|
| [**Stock Analysis**](skills/alphagbm-stock-analysis/) | GBM Five Pillars scoring (1-10) for any stock | "Analyze AAPL" |
| [**Options Score**](skills/alphagbm-options-score/) | Rank every option contract by quality | "Best NVDA call to buy" |
| [**Options Strategy**](skills/alphagbm-options-strategy/) | Recommend optimal multi-leg strategies | "Bullish play on TSLA" |
| [**Vol Surface**](skills/alphagbm-vol-surface/) | 3D implied volatility across strikes & expiries | "Is AAPL IV expensive?" |
| [**Vol Smile**](skills/alphagbm-vol-smile/) | Skew analysis for a single expiration | "NVDA put skew" |
| [**Greeks**](skills/alphagbm-greeks/) | Full Greeks dashboard with scenarios | "Greeks for AAPL 220C" |
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
      (built-in, free)      (api.alphagbm.com)
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

- **IV 28.5%** -- calculated from actual option prices using Black-Scholes
- **IV Rank 62** -- current IV vs. 252 trading days of historical data
- **VRP +4.4%** -- IV minus realized HV, measures option overpricing
- **Score 8.2** -- weighted composite of liquidity, IV, Greeks, risk/reward

This is not *"based on my training data"* or *"I estimate with 85% confidence."*

This is math on market data.

## Example Workflow

> **You**: "Analyze AAPL, then find the best options play"

The agent chains skills automatically:

1. **Stock Analysis** → GBM score 7.8/10, moderately bullish, strong fundamentals
2. **Options Score** → ATM Apr 220 Call scores 8.2/10 (high liquidity + favorable Greeks)
3. **Options Strategy** → Recommends Bull Call Spread 220/230, max profit $685, max loss $315
4. **P&L Simulator** → Shows breakeven at $223.15, 48% probability of profit

> **You**: "Is that IV expensive?"

5. **IV Rank** → IV Rank 62/100 — mid-high range, options slightly overpriced
6. **Vol Surface** → ATM IV in contango, short-term elevated due to earnings in 26 days

All from real data. All verifiable.

## Roadmap

- [x] 15 Skills with mock data
- [x] Claude Code & Cursor support
- [ ] MCP Server (plug into Claude Desktop, Windsurf, any MCP client)
- [ ] CLI tool (`pip install alphagbm`)
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

**Built by the [AlphaGBM](https://alphagbm.com) team. Trusted by 100,000+ traders worldwide.**

*Real data. Real signals. Real edge.*

</div>
