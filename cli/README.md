# AlphaGBM CLI

Command-line tool for [AlphaGBM](https://alphagbm.com) stock & options analysis.

## Install

```bash
cd cli
pip install -e .
```

## Quick Start

```bash
# 1. Set your API key (get one at https://alphagbm.com/api-keys)
alphagbm config set-key agbm_your_api_key_here

# 2. Stock analysis
alphagbm stock quote AAPL
alphagbm stock analyze NVDA --style growth

# 3. Options scoring
alphagbm options score AAPL --strategy sell-put
alphagbm options score TSLA --strategy all --expiry 2026-04-17
alphagbm options snapshot AAPL
alphagbm options recommend

# 4. JSON output (pipe to jq, etc.)
alphagbm stock analyze AAPL --json | jq '.risk'
```

## Commands

| Command | Description |
|---------|-------------|
| `alphagbm stock quote TICKER` | Quick price quote (free) |
| `alphagbm stock analyze TICKER` | Full analysis (10-30s) |
| `alphagbm options score TICKER` | Score options, return top picks |
| `alphagbm options snapshot TICKER` | IV/VRP snapshot (free) |
| `alphagbm options recommend` | Daily recommendations |
| `alphagbm config set-key KEY` | Save API key |
| `alphagbm config set-url URL` | Set API base URL |
| `alphagbm config show` | Show current config |

## Options

- `--style` / `-s`: Analysis style — `quality`, `value`, `growth`, `momentum`, `balanced`
- `--strategy` / `-s`: Options strategy — `sell-put`, `sell-call`, `buy-call`, `buy-put`, `all`
- `--expiry` / `-e`: Expiry date `YYYY-MM-DD` (auto-selects if omitted)
- `--top` / `-n`: Number of recommendations (default 5, max 10)
- `--json`: Output raw JSON instead of formatted tables

## Configuration

Config stored at `~/.alphagbm/config.json`. Env vars override file:

- `ALPHAGBM_API_KEY` — API key
- `ALPHAGBM_BASE_URL` — Base URL (default: `https://alphagbm.zebabur.app`)
