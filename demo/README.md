# AlphaGBM workflow demos

These files are **synthetic, offline fixtures** for documentation and UI review.
They are not live quotes, not investment recommendations, and not evidence that a
paid request has run. The dates and scores are intentionally fixed so that the
README remains reproducible.

## Five result-shaped outputs

| Result | Fixture | What it demonstrates |
|---|---|---|
| Stock opportunity | [`stock-opportunities.json`](stock-opportunities.json) | Conclusion, evidence, score basis and next checkpoints |
| Options strategy | [`options-strategies.json`](options-strategies.json) | Quote timing, candidate score, payoff and risk |
| News impact | [`news-impact.json`](news-impact.json) | Reported facts, related assets and impact uncertainty |
| Report breakdown | [`report-breakdown.json`](report-breakdown.json) | Institution view, rating, assumptions and source date |
| Investment review | [`investment-review.json`](investment-review.json) | A local before/after comparison with no cloud history |

## Try the real workflows

Install the package you need and let your AI tool ask for the result:

```bash
npx skills add AlphaGBM/skills --skill alphagbm-stock-research
npx skills add AlphaGBM/skills --skill alphagbm-news-impact
```

Use the fixtures only to understand the shape of the output. Public reads and
account-backed research have different access rules; see [`../docs/ACCESS.md`](../docs/ACCESS.md).
