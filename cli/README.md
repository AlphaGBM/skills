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

# 4. Published research insights (no API key required)
alphagbm research insights --market us --lang en
alphagbm research read <SLUG_FROM_LIST> --lang zh

# 5. JSON output (pipe to jq, etc.)
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
| `alphagbm research insights` | List published research and market insights |
| `alphagbm research read SLUG` | Read one published insight |
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
- `ALPHAGBM_BASE_URL` — Base URL (default: `https://alphagbm.zeabur.app`)

## Research Reader Behavior

`research insights` accepts `--market us|hk|a|commodity`, `--tag`, `--lang zh|en`,
`--page` (at least 1), and `--limit` (1–50). Copy a slug from its output into
`research read`. These legacy endpoints do not provide date-range or full-text
search filters. The separate structured catalogue API is not yet a CLI command.

Research reads do not require or send an API key. `--json` writes only the API JSON
to stdout; errors go to stderr with a nonzero exit code. Network failures,
redirects and malformed API data are errors, not empty result sets.

Text output preserves publication metadata, upstream sources when supplied and
the API's returned language. `--lang` requests a language but does not translate
missing article content. Bracketed text is displayed literally, not as terminal
markup. No authenticated analysis or editorial write is triggered by these commands.
