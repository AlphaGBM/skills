---
name: alphagbm-research-insights
description: "Published Research via the published AlphaGBM interface. Use for this focused function, not as a promise that every website API accepts API keys."
---

# Published Research

Read [access and evidence rules](references/access.md) first. This package is a focused function; full research workflows are listed in the repository catalogue. Its runner is self-contained and requires only Python 3.9+.

```bash
python3 "<skill-dir>/scripts/run.py" research --collection research --limit 3
```

This public read requires no key. Use --collection research for original research, or --collection news --view research for institutional views.

Return only the successful API response, with its original asset identity, dates, units, missing-data flags and score type. Stock risk scores are not opportunity scores. Volatility fields can be missing; do not turn a snapshot into a fabricated 252-day IV Rank. Option candidates are not guaranteed fills or trade instructions. Never fall back silently to demo data. Nonzero exit must be surfaced as an error.
