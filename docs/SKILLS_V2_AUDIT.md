# Skills v2 Audit

> Audit baseline: 2026-09-13. This document records the upgrade boundary between the public Skills repository and the AlphaGBM product API.

## Executive Summary

The repository contains 30 `SKILL.md` packages. The existing options and research tools form a useful base, but the public surface still describes AlphaGBM primarily as an options toolkit. The product now spans opportunity scoring, stocks, ETFs, commodities/compute signals, research and verification, so the next release should close the documentation and capability gaps in that order.

## Current Inventory

| Area | Current packages | Assessment |
| --- | ---: | --- |
| Opportunity and core analysis | 8 | Good base; needs a unified opportunity entry point |
| Market and options intelligence | 6 | Broad coverage; endpoint and quota audit still required |
| Workflow tools | 4 | Useful for watch, alerts and comparison |
| Risk and portfolio discipline | 3 | Strong differentiator; should be surfaced earlier |
| Investor frameworks | 4 | Keep as optional methodology overlays, not the main product promise |
| Research Brain | 5 | Good foundation; needs clearer distinction between personal research and public research/news |
| **Total** | **30** | README inventory now matches the repository |

## Capability Gaps

These are product-level gaps, not claims that new API endpoints already exist:

1. **Unified Opportunity Radar** — one natural-language entry point across stocks, ETFs, options and commodities instead of separate tools only.
2. **ETF Analysis** — a first-class ETF score and comparison workflow, including holdings, exposure, liquidity, valuation and momentum evidence.
3. **Commodity and Compute Monitoring** — a public Skill that explains contract/price-curve signals and separates them from stock opportunities.
4. **Research and Verification** — structured summaries of external research with source, date, license context, evidence and follow-up checkpoints.
5. **CLI parity** — the CLI currently exposes stock and options commands, but not the newer multi-asset and research workflows.

### Source-Level Findings

- The current backend exposes `GET /api/options/commodity/contracts/<product>`
  for commodity option contract discovery. That is not yet a commodity price,
  curve, or compute-market monitoring contract, so a public commodity Skill
  should not imply those capabilities are already available through Skills.
- No ETF-specific backend route or ETF Skill is present in the reviewed source
  tree. ETF support should therefore be added only after the score inputs and
  response contract are defined, rather than by aliasing stock analysis.
- Public research articles are available through the insights API, but there is
  no public Skill that defines how an agent should retrieve, summarize, cite and
  follow up on those articles. This is a documentation and workflow gap, not a
  reason to expose the editorial write endpoints.

## API Contract Audit Boundary

The following routes are present in the current product backend source and already have corresponding Skill documentation or CLI usage:

- Stock: quick quote, search, sync/async analysis, history, summary and take-profit analysis.
- Options: expirations, chains, enhanced analysis, reverse score, snapshots, recommendations, volatility tools, unusual activity, fear/VIX signals and backtests.
- Research Brain: profiles, theses, macro, themes and health checks.
- Workflow: compare, watchlist and alerts.
- Investor frameworks: Buffett, Marks and Tepper endpoints.

These areas still require a staging contract test before they should be advertised as fully supported:

- response fields and nullable fields for each Skill;
- quota category and cache behavior;
- authentication behavior for free, Plus and Pro users;
- market coverage and symbol normalization for US, HK, CN, ETF and commodity inputs;
- source timestamp and evidence fields where the output is presented as verifiable.

### Confirmed Documentation Gap

The `alphagbm-options-score` Skill documents the chain/enhanced/reverse-score building blocks, but it does not document the product's primary scoring endpoint: `POST /api/v1/options/score`. The CLI already calls this route. The Skill should expose this as the canonical path and keep the lower-level routes as implementation-specific alternatives only when an agent needs them.

## Upgrade Order

### V2.1 — Contract correctness

- Generate an endpoint matrix from every `SKILL.md`.
- Compare method/path/parameters against the backend OpenAPI or route map.
- Add one non-billing staging smoke test per public endpoint family.
- Remove or label claims that cannot be verified from the response.

### V2.2 — Product entry points

- Add `alphagbm-opportunity-radar` only after a stable backend contract exists.
- Add `alphagbm-etf-analysis` after the ETF score endpoint is stable.
- Add `alphagbm-commodity-monitor` for contract and compute-market data.
- Add `alphagbm-research-verify` for source-backed research interpretation.

### V2.3 — Workflow parity

- Add matching CLI commands or explicitly label a Skill as agent-only.
- Standardize bilingual examples and error handling.
- Document quota consumption per call, including free/cache-hit paths.

## Release Gate

A new Skill is publishable only when all of the following are true:

- The endpoint exists in the target environment.
- The request and response contract is tested.
- Authentication and quota behavior are documented.
- At least one real-data or explicitly labelled demo response is available.
- The Skill does not present an inference as a sourced fact.
- The README category, count and example are updated in the same change.
