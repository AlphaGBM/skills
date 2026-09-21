# AlphaGBM Skills

**Market research that works inside your AI workspace.**

Find a stock worth researching. Understand the evidence. Compare options. Revisit the judgment when facts change.

[![MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![GitHub stars](https://img.shields.io/github/stars/AlphaGBM/skills)](https://github.com/AlphaGBM/skills)

**5 research workflows · 31 focused tools and reference packages.** Counts include reference packages, not 36 independently verified APIs. See the [generated catalogue and access status](docs/CATALOG.md).

[Website](https://www.alphagbm.com/skills) · [中文指南](docs/README.zh.md) · [Start here](#start-with-a-result) · [Access & usage](docs/ACCESS.md) · [What's new](docs/CHANGELOG.md)

## Start with a result

Install one workflow, not everything. For example, read published research without a key:

```bash
npx skills add AlphaGBM/skills --skill alphagbm-research-reader
```

Then ask your AI:

> Use AlphaGBM to find recent semiconductor research. Summarize the views and preserve the sources and dates.

The installer lets you choose your AI tool. Each workflow includes a Python 3.9+ runner and its own access instructions. **No separate AlphaGBM CLI installation is required.** Installing a package and testing an authenticated model session are different checks; see [validation status](docs/ACCESS.md#verification-boundary).

## Choose a workflow

| You want to… | Install this | What you receive |
|---|---|---|
| Find opportunities | `alphagbm-opportunity-radar` | Covered-stock candidates, published scores, evidence and dates |
| Research a company | `alphagbm-stock-research` | Fundamentals, sentiment, risk and questions to verify |
| Compare options | `alphagbm-options-research` | Candidates, score components, quote timing and funding risks |
| Read research & news | `alphagbm-research-reader` | Public research, institutional views, sources and related assets |
| Verify a thesis | `alphagbm-thesis-check` | Supporting/counterevidence, invalidation conditions and a versioned result ID |

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

<img src="assets/demo-screenshot.png" alt="Illustrative AlphaGBM CLI research output; not a live quote" width="720">

This is an illustrative CLI screenshot, not a current market observation or a claim that a new task has run. Workflow runners return structured JSON for your AI to summarize. They do not silently replace failed requests with sample data.

## Developers

- [Access contract and failure handling](docs/ACCESS.md)
- [Generated catalogue](docs/CATALOG.md) · [Canonical JSON](catalog/catalog.json)
- [CLI](cli/README.md) remains available separately; CLI command count is not Skill count.
- `python3 scripts/build_catalog.py --check` validates package coverage and generated runners/docs.
- Edit `catalog/catalog.json` and `runtime/workflow.py`, then run `python3 scripts/build_catalog.py`. Do not hand-edit generated workflow files.
- Website releases import this catalogue from a pinned Git commit and verify its SHA-256. Publish the repository update before promoting the matching website release.

Research only. No trade execution or performance guarantees. [Contributing](CONTRIBUTING.md) · [License](LICENSE).
