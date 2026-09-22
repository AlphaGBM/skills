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

## Every strategy has a demo

The strategy fixtures below are also **synthetic, offline fixtures**. Each one
shows the input scope, the result shape, missing data, risks and the next checks
an agent should preserve. They are not live quotes, trade instructions or proof
that an account-backed request has run.

| Strategy | Fixture | What it demonstrates |
|---|---|---|
| Options strategy | [`strategies/options-strategy.json`](strategies/options-strategy.json) | Candidate payoff, quote timing and risk |
| Momentum following | [`strategies/momentum-following.json`](strategies/momentum-following.json) | Trend state, supporting evidence and reversal risk |
| ETF strategy | [`strategies/etf-strategy.json`](strategies/etf-strategy.json) | Valuation, quality, drawdown and momentum factors |
| Grid plan | [`strategies/grid-plan.json`](strategies/grid-plan.json) | Price range, levels, capital allocation and range-break risk |
| Dollar-cost averaging | [`strategies/dca-plan.json`](strategies/dca-plan.json) | Contribution schedule, path assumptions and missing inputs |
| Smart Money tracking | [`strategies/smart-money.json`](strategies/smart-money.json) | Disclosed-flow aggregation without copying trades |
| Dividend strategy | [`strategies/dividend-strategy.json`](strategies/dividend-strategy.json) | Yield quality, durability, cash flow, valuation and momentum |

## Try the real workflows

Install the package you need and let your AI tool ask for the result:

```bash
npx skills add AlphaGBM/skills --skill alphagbm-stock-research
npx skills add AlphaGBM/skills --skill alphagbm-news-impact
npx skills add AlphaGBM/skills --skill alphagbm-momentum-following
npx skills add AlphaGBM/skills --skill alphagbm-etf-strategy
npx skills add AlphaGBM/skills --skill alphagbm-grid-plan
npx skills add AlphaGBM/skills --skill alphagbm-dca-plan
npx skills add AlphaGBM/skills --skill alphagbm-smart-money
npx skills add AlphaGBM/skills --skill alphagbm-dividend-strategy
```

Use the fixtures only to understand the shape of the output. Public reads and
account-backed research have different access rules; see [`../docs/ACCESS.md`](../docs/ACCESS.md).

## Every focused package has a real-source case

The [complete demo index](CATALOG.md) maps every current Skill to its example.
The [package case manifest](package-cases.json) contains source-based requests for retained focused packages; the strategy fixtures above cover the remaining strategies. These are not frozen
market quotes: each case names a popular subject, a public source and a real
request an agent can reproduce. API cases should fetch the source at run time;
reference cases should explain the method without inventing a live result.

To inspect one case:

```bash
jq '.cases[] | select(.package == "alphagbm-stock-analysis")' demo/package-cases.json
```
