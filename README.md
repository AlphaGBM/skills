# AlphaGBM Skills

**Evidence-first market research inside your AI workspace.**

Stock opportunities. Options strategies. News impact. Report breakdowns. Investment reviews.

**Release candidate:** five result-oriented workflows are staged with the matching AlphaGBM backend contract. News Impact and Research Report Breakdown read published material; Stock Opportunities and Options Strategies use account-backed research; Investment Review compares records you supply locally. Check [access status](docs/ACCESS.md) before treating any interface as production-ready.

[![MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![GitHub stars](https://img.shields.io/github/stars/AlphaGBM/skills)](https://github.com/AlphaGBM/skills)

**5 research workflows · 35 focused tools and reference packages.** The count includes reference packages; it is not a claim of 34 independently verified APIs. See the [generated catalogue and access status](docs/CATALOG.md).

[Website](https://www.alphagbm.com/skills) · [中文指南](docs/README.zh.md) · [Start here](#start-with-a-result) · [Demo outputs](demo/README.md) · [Access & usage](docs/ACCESS.md) · [What's new](docs/CHANGELOG.md)

## What changed in this release candidate

The catalogue is organized around the result a user wants, not around a long list of endpoints:

1. **Find an opportunity** — connect fundamentals, sentiment, risk and evidence.
2. **Compare an options strategy** — keep quote timing, capital, payoff and risk visible.
3. **Understand what changed** — separate reported news from impact inference.
4. **Break down a report** — preserve the institution's view, rating, assumptions and dates.
5. **Review a decision** — compare two supplied snapshots and identify what changed.

Every workflow is designed to return a conclusion, supporting and opposing evidence, and the next question to verify. The [demo fixtures](demo/README.md) are synthetic and clearly labelled; they never stand in for live quotes or a paid request.

## Start with a result

Install one workflow, not everything. For example, read published research without a key:

```bash
npx skills add AlphaGBM/skills --skill alphagbm-research-reader
```

Then ask your AI:

> Use AlphaGBM to find recent semiconductor research. Summarize the views and preserve the sources and dates.

The installer lets you choose your AI tool. Each workflow includes a Python 3.9+ runner and its own access instructions. **No separate AlphaGBM CLI installation is required.** Installing a package, reading a public result and running authenticated research are different checks; see [validation status](docs/ACCESS.md#verification-boundary).

## Choose a workflow

| You want to… | Install this | What you receive |
|---|---|---|
| Stock Opportunities | `alphagbm-stock-research` | Fundamentals, sentiment, available opportunity scores and evidence gaps |
| Options Strategies | `alphagbm-options-research` | Candidate scores, reference capital, payoff limits and risks |
| News Impact | `alphagbm-news-impact` | Reported claims, affected assets, impact inferences and checkpoints |
| Research Report Breakdown | `alphagbm-report-breakdown` | Published views, original ratings, assumptions and risks |
| Investment Review | `alphagbm-investment-review` | Local comparison of supplied records, not cloud-history access |

The previous `alphagbm-opportunity-radar`, `alphagbm-research-reader` and `alphagbm-thesis-check` packages remain in the focused catalogue with their existing install names and commands.

Replace the skill name in the install command. To see every package:

```bash
npx skills add AlphaGBM/skills --list
```

### Use your account for deeper research

Create an API key in [your AlphaGBM account](https://www.alphagbm.com/api-keys) and configure `ALPHAGBM_API_KEY` in your tool's local environment. Never paste the key into a conversation or commit it to a repository.

> Use AlphaGBM to research NVDA. Explain supporting evidence, counterevidence and what could change the conclusion. Ask before using my research allowance.

Installation is free. Account-backed research uses **the same account allowance as the website**. It does not grant a separate quota or a free Alpha Agent subscription. Public catalogue/candidate reads require no key. [Compare current plans](https://www.alphagbm.com/pricing).

## Why AlphaGBM?

- **Data plus research:** use AlphaGBM's published candidates, market-analysis endpoints and research catalogue—not an instruction to guess from model memory.
- **Evidence you can revisit:** preserve source dates, score types and returned evidence revisions. A stock risk score is not an opportunity score or a probability of profit.
- **One account, two places to work:** use the website or your AI workspace without a separate Skills allowance.
- **Small functions when you need them:** keep individual stock, option, volatility and research tools; treat methods and unpublished interfaces as references, not working APIs.

Data may be live, delayed or a dated snapshot depending on the endpoint. Coverage is not universal. The thesis workflow is on demand; it does **not** schedule monitoring, trade, or save records to your account automatically.

## Focused tools, without the wall of names

The [full catalogue](docs/CATALOG.md) groups individual packages into stocks, options, markets, risk, research and investor frameworks. It states which interfaces are supported by the access review and which are reference-only.

Investor frameworks are optional research lenses, not the primary product, endorsements by those investors, or validated promises of returns.

## See the output

<img src="assets/demo-workflow.svg" alt="Illustrative AlphaGBM stock opportunity workflow output; not a live quote" width="720">

This is an illustrative workflow fixture, not a current market observation and not evidence that a paid task has run. The exact JSON is in [`demo/stock-opportunities.json`](demo/stock-opportunities.json). Workflow runners return structured JSON for your AI to summarize; they do not silently replace failed requests with sample data.

## Developers

- [Access contract and failure handling](docs/ACCESS.md)
- [Generated catalogue](docs/CATALOG.md) · [Canonical JSON](catalog/catalog.json)
- [CLI](cli/README.md) remains available separately; CLI command count is not Skill count.
- `python3 scripts/build_catalog.py --check` validates package coverage and generated runners/docs.
- Edit `catalog/catalog.json` and `runtime/workflow.py`, then run `python3 scripts/build_catalog.py`. Do not hand-edit generated workflow files.
- Website releases import this catalogue from a pinned Git commit and verify its SHA-256. Publish the repository update before promoting the matching website release.

Research only. No trade execution or performance guarantees. [Contributing](CONTRIBUTING.md) · [License](LICENSE).
