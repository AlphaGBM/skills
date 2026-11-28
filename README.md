# AlphaGBM Skills

**Open-source AI agent skills for stock analysis, options research and financial research in Claude Code, Cursor and compatible tools.**

Research stocks. Compare options strategies. Understand news. Break down research. Review investment decisions.

[![MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![GitHub stars](https://img.shields.io/github/stars/AlphaGBM/skills)](https://github.com/AlphaGBM/skills)

[Website](https://www.alphagbm.com/skills) · [中文](docs/README.zh.md) · [Catalogue](docs/CATALOG.md) · [Demos](demo/CATALOG.md) · [Access & usage](docs/ACCESS.md) · [Start here](https://github.com/AlphaGBM/skills/discussions/21) · [Discussions](https://github.com/AlphaGBM/skills/discussions) · [Report an issue](https://github.com/AlphaGBM/skills/issues/new/choose)

**New here?** Inspect a [synthetic stock-research output](demo/stock-opportunities.json) without an account, then follow the [installation guide](docs/INSTALLATION.md). This example is not live market data. Installation is free; account-backed requests have separate access and usage limits.

The example score of 74 is illustrative, not a 74% win rate. Research scores are not win rates or buy/sell signals; installation does not unlock Alpha Agent or add research quota.

<!-- catalog:start -->
**28 Skills · 5 core Skills + 23 focused Skills**

| Category / 分类 | Count / 数量 |
|---|---|
| [Core Skills](skills/core/) | 5 |
| [Stocks](skills/stocks/) | 10 |
| [Options](skills/options/) | 11 |
| [Commodities](skills/commodities/) | 1 |
| [Digital Assets](skills/digital-assets/) | 1 |

<!-- catalog:end -->

Counts include method-reference packages, not just callable APIs. The catalogue preserves each package's access and release status; a preview is not a claim of verified production availability.

## Doubao Work / 豆包工作

[豆包中文上手指南](docs/DOUBAO.md) offers a portable **Causal Research** package for evidence, calculations and counterarguments using your own authorized materials, or public primary sources with your explicit permission. No files? Choose upload or authorize public-source retrieval instead of preparing a full research dossier first. No separate Codex installation or AlphaGBM API key is required. Use native skill import where available, or the explicitly labelled current-session file workflow. Native Doubao import and cross-session discovery are **not yet verified**; this is not access to paid research or the private report library.

## Start with the result you need

| Core Skill | What you receive | Package |
|---|---|---|
| Stock Opportunities | Fundamentals, sentiment, risk and available opportunity scores | `alphagbm-stock-research` |
| Options Strategies | Candidate scores, capital requirements and risk limitations | `alphagbm-options-research` |
| News Impact | Reported facts, affected assets and impact inferences | `alphagbm-news-impact` |
| Research Report Breakdown | Institutional views, original ratings, assumptions and sources | `alphagbm-report-breakdown` |
| Investment Review | Changes between two supplied snapshots, compared locally | `alphagbm-investment-review` |

Install one Skill:

```bash
npx skills@1.9.0 add AlphaGBM/skills --skill alphagbm-stock-research --agent codex --copy -y
```

This project-local command targets Codex only. For Claude Code or Cursor, replace `codex` with `claude-code` or `cursor`; use your installed client, not every agent. Codex and Cursor use `.agents/skills`, while Claude Code uses `.claude/skills` with this installer version.

Try the bundled synthetic example without a key or research allowance:

```bash
python3 .agents/skills/alphagbm-stock-research/scripts/demo.py --lang en
```

Or ask your AI client: **“Use AlphaGBM's offline synthetic stock-split demo; do not access the network or use research allowance.”** For Claude Code, the command path starts with `.claude/skills`. This is an offline example, not live research; the structured live workflow remains a release preview.

Then ask your AI:

> Use AlphaGBM to research NVDA. Explain supporting evidence, counterevidence and what could change the conclusion. Ask before using my research allowance.

The installer lets you choose your AI tool. Callable packages contain a self-contained Python 3.9+ runner; no separate AlphaGBM CLI installation is required.

[Installation, local-source upgrades and version checks](docs/INSTALLATION.md).

## Choose a focused tool

<!-- stock-tools:start -->
**Stocks (10):** Causal Research · Stock Analysis · Dividend Strategy · Market Sentiment · Research Reports · Momentum Following · ETF Strategy · Grid Plan · Dollar-Cost Averaging · Smart Money Tracking.
<!-- stock-tools:end -->

**Options:** Scoring, volatility, Greeks, strategy comparisons, payoff analysis and risk methods. See the [options directory](skills/options/) for the exact eleven packages and their access status.

**Commodities and digital assets:** focused research methods, clearly labelled as references rather than live data integrations.

```bash
npx skills add AlphaGBM/skills --list
npx skills@1.9.0 add AlphaGBM/skills --skill alphagbm-etf-strategy --agent codex --copy -y
npx skills@1.9.0 add AlphaGBM/skills --skill alphagbm-research-reader --agent codex --copy -y
```

Market Sentiment includes VIX and fear indicators within one method; these are no longer separate cards. Smart Money Tracking summarizes disclosed records and never copies or places trades.

## Your workspace, your AlphaGBM account

Create a personal key in [your account](https://www.alphagbm.com/api-keys) and configure `ALPHAGBM_API_KEY` securely in your tool's environment. Never paste a key into a conversation or commit it to a repository.

- Installation is free; account-backed research shares the website's allowance and subscription rules. Installation does not unlock Alpha Agent or grant additional quota.
- Published research reads need no key; this does not grant access to the private research archive. Investment Review compares files you supply locally.
- Reference packages explain methods; they do not expose a live API. Runners check supported workflow contracts before applicable paid calls and never replace failures with demos.
- Preserve source dates, missing data and score definitions. Research is not a return guarantee or an order to trade.

[Account plans](https://www.alphagbm.com/pricing) · [Verification boundary](docs/ACCESS.md#verification-boundary)

## Examples you can inspect

Every current package has an entry in the [demo index](demo/CATALOG.md): either an explicitly synthetic output fixture or a source-based example request. Neither is presented as a captured live paid response. [Demo guide](demo/README.md).

## One catalogue, matching website cards

[`catalog/catalog.json`](catalog/catalog.json) defines names, categories, stable IDs and exact package paths. The website imports a commit-pinned copy and uses those paths in copied instructions. Core Skills live under `skills/core/`; focused tools live under their asset categories. [Contributing](CONTRIBUTING.md).

Investor-inspired methods are maintained separately in [AlphaGBM/investment-masters](https://github.com/AlphaGBM/investment-masters); they are not counted or duplicated here.

### Upgrading from the flat directory

Retained package IDs and `--skill` install names are unchanged, but file paths have moved. Reinstall using the commands above; replace old `skills/<id>/` bookmarks with catalogue paths. Research-management cards and retired standalone packages are removed from the latest catalogue, not silently mapped to unrelated functions. Existing pinned versions remain available in Git history. The shared runner's compatibility commands are not new catalogue entries.

## Community and contributions

This is also the shared help entry for [Investment Masters](https://github.com/AlphaGBM/investment-masters) and [Trading Skills](https://github.com/AlphaGBM/alphagbm-trading-skills). Mention the source repository when asking a question; these separate method repositories do not add live APIs to this catalogue.

Use [Discussions](https://github.com/AlphaGBM/skills/discussions) for setup questions, workflow ideas and reproducible examples; use [Issues](https://github.com/AlphaGBM/skills/issues/new/choose) for actionable bugs or scoped changes. English and Chinese are welcome. Do not post keys, account details or private research.

Want to help? Start with [good first issues](https://github.com/AlphaGBM/skills/issues?q=is%3Aissue%20is%3Aopen%20label%3A%22good%20first%20issue%22) or [help wanted](https://github.com/AlphaGBM/skills/issues?q=is%3Aissue%20is%3Aopen%20label%3A%22help%20wanted%22). See the [community guide](docs/COMMUNITY.md) and [contribution checklist](CONTRIBUTING.md). Stars are optional; useful feedback and verified examples are welcome without one.

## Development

```bash
python3 scripts/build_catalog.py
python3 scripts/build_catalog.py --check
python3 -m unittest discover -s scripts -p 'test_*.py'
npx skills add . --list
```

MIT licensed. See [LICENSE](LICENSE).
