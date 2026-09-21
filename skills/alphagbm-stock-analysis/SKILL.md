---
name: alphagbm-stock-analysis
description: "Stock Analysis via the published AlphaGBM interface. Use for this focused function, not as a promise that every website API accepts API keys."
---

# Stock Analysis

Read [access and evidence rules](references/access.md) first. This package is a focused function; full research workflows are listed in the repository catalogue. Its runner is self-contained and requires only Python 3.9+.

```bash
python3 "<skill-dir>/scripts/run.py" stock NVDA --confirm-usage
```

Requires ALPHAGBM_API_KEY. If the command uses --confirm-usage, first obtain approval to use the shared account allowance. Snapshot reads do not consume analysis credits, but still require account access.

Return only the successful API response, with its original asset identity, dates, units, missing-data flags and score type. Stock risk scores are not opportunity scores. Volatility fields can be missing; do not turn a snapshot into a fabricated 252-day IV Rank. Option candidates are not guaranteed fills or trade instructions. Never fall back silently to demo data. Nonzero exit must be surfaced as an error.
