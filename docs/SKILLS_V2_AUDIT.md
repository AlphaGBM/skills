# Skills v2 Audit

> Audit updated: 2026-09-13. Backend source baselines: staging `2ed6f7b`, production branch `467a0fd`. Source inspection is distinct from live endpoint acceptance.

## Executive Summary

This PR contains 31 `SKILL.md` packages, including the new public Research Insights reader. Existing market, scoring and research capabilities need to be mapped to externally supported APIs; an implementation inside the product does not automatically make it accessible to an API-key client.

## Current Inventory

| Area | Current packages | Assessment |
| --- | ---: | --- |
| Opportunity and core analysis | 8 | Good base; needs a unified opportunity entry point |
| Market and options intelligence | 6 | Broad coverage; endpoint and quota audit still required |
| Workflow tools | 4 | Useful for watch, alerts and comparison |
| Risk and portfolio discipline | 3 | Strong differentiator; should be surfaced earlier |
| Investor frameworks | 4 | Keep as optional methodology overlays, not the main product promise |
| Research and knowledge | 6 | Includes the new public reader; private Research Brain API-key access still requires review |
| **Total** | **31** | README inventory matches this PR |

## Capability Gaps

These are Skills integration tasks, not a claim that the underlying product must be rebuilt:

1. **Unified Opportunity Radar** — one natural-language entry point across stocks, ETFs, options and commodities instead of separate tools only.
2. **ETF Analysis** — a first-class ETF score and comparison workflow, including holdings, exposure, liquidity, valuation and momentum evidence.
3. **Commodity and Compute Monitoring** — a public Skill that explains contract/price-curve signals and separates them from stock opportunities.
4. **Research and Verification** — structured summaries of external research with source, date, license context, evidence and follow-up checkpoints.
5. **CLI parity** — stock, options and public research reads are implemented; multi-asset parity remains unverified.

### Source-Level Findings

- Staging includes an ETF scorer at `app/services/opportunity_scoring/etf.py`
  and ETF metadata work. Its public HTTP contract has not been accepted by this
  audit; do not equate that with an absent ETF implementation.
- Public `GET /api/homepage/compute-market` and
  `GET /api/homepage/opportunities` routes exist. They must be checked for
  field semantics, freshness and availability before adding corresponding Skills.
- Commodity contract discovery is also present at
  `GET /api/options/commodity/contracts/<product>`; it is a separate capability.
- The production branch includes both legacy public insight reads and the
  structured `/api/insights/catalogue` family. The new Skill/CLI use the legacy
  read routes; collection/search support is not yet exposed by the CLI.
- Staging authentication requires explicit API-key opt-in. The existence of
  private research routes does not prove that an `agbm_` key can use them.
  Do not bypass a 403 by requesting browser cookies or broader credentials.

### Superseded Conclusions

The first pass inspected local backend checkout `ae5fb22` from 2026-08-08 rather
than the current staging branch. The statements that ETF implementation and
compute-monitor endpoints were absent were not valid and are withdrawn.
Earlier route matching was static inspection, not a live contract test.
The claim that all 31 packages ship mock data was also unsupported; the new
Research Insights Skill reads published articles and has no bundled demo data.

## API Contract Audit Boundary

The maintained external access matrix is in [`EXTERNAL_ACCESS_MATRIX.md`](EXTERNAL_ACCESS_MATRIX.md). It is the concise reference for public, authenticated no-credit, account-free-allowance and subscription/credit-gated calls.

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

This PR now documents `POST /api/v1/options/score` as the normal scoring path,
matching the existing CLI. Lower-level chain routes remain separate. No paid
scoring call was made in this audit, so authentication, billing and score
correctness are not claimed as live-tested.

## Reader Validation

- Anonymous staging GETs returned HTTP 200 for the insight list, catalogue and
  selected article details. List envelopes and detail fields matched the new reader.
- The legacy list returned 12 articles; the news catalogue returned 9 at the
  time of this check. These are observations, not a daily-update guarantee.
- 36 offline CLI checks passed, covering filters, JSON-only stdout, Chinese/English display,
  null metadata, literal Rich markup, malformed JSON/payloads, timeouts,
  connection errors, redirects, HTTP failures and invalid slug rejection.
- Four anonymous staging CLI requests passed: Chinese and English list/detail
  pairs. All 31 Skill YAML headers parsed; the new Skill validator and edited
  README/Skill relative-link checks passed. These checks were local, not CI.
- No authenticated analysis, billing call, editorial write or production
  deployment was performed. This PR has not been merged.

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
