# AlphaGBM External Access Matrix

> This document defines the external calling contract for AlphaGBM Skills. It separates public reading, authenticated no-credit access, account-level free allowance, and subscription/credit-gated analysis.

**Last reviewed:** 2026-09-13  
**Backend reference:** latest staging source reviewed on 2026-09-13  
**Scope:** Skills and external API consumers; this is not a promise that every product page or deployment exposes every route.

## Core Rule

Installing a Skill is free. Installing a Skill does **not** grant free access to
AlphaGBM live data, analysis, subscription features, or a separate allowance.
Live calls are controlled by the endpoint's authentication policy and the
account's current entitlement.

Use these terms precisely:

- **Public** — no account or API key is required for the published read-only response.
- **Authenticated, no analysis credit** — an account/API key is required, but the endpoint is not an analysis-credit operation according to the current backend contract.
- **Account free allowance** — an authenticated analysis call may be covered by the account's current daily free allowance; it is not a per-Skill guarantee.
- **Subscription/credits** — the call requires available subscription credits or another paid entitlement after any applicable free allowance is exhausted.
- **Unconfirmed** — the route, deployment, or billing behavior has not been accepted as a stable external contract.

## Access Matrix

| Capability | Representative route or Skill | Login/API key | Analysis credits | Subscription after free allowance | Current external status |
|---|---|---:|---:|---:|---|
| Health and API metadata | `GET /api/health` | No | No | No | Public read-only |
| Stock discovery | `GET /api/stock/search` | No | No | No | Public read-only |
| Published research summary | `GET /api/insights`, `GET /api/insights/<slug>` | No in current public reader | No | No | Public published layer; not the original third-party archive |
| Published research catalogue | `GET /api/insights/catalogue` | No in current public reader | No | No | Public published layer; full research access may be tier-gated later |
| Homepage opportunity summaries | `GET /api/homepage/opportunities` | No in current public route | No | No | Public summary; option quality may be unavailable when the quality gate is not met |
| Compute-market summary | `GET /api/homepage/compute-market` | No in current public route | No | No | Public summary |
| Daily option recommendations | `GET /api/options/recommendations` | Public status must be verified per deployment | No | No | Public summary in the current route contract; do not treat it as full option scoring |
| VIX status | `GET /api/options/vix-status` | Yes | No | No | Authenticated, no analysis-credit deduction |
| Marks cycle | `GET /api/masters/marks-cycle` | Yes | No | No | Authenticated, no analysis-credit deduction |
| IV snapshot | `GET /api/options/snapshot/<SYMBOL>` | Yes | No | No | Authenticated, no analysis-credit deduction |
| Option expirations | `GET /api/options/expirations/<SYMBOL>` | Yes | Not classified as deep analysis | No | Authenticated route; confirm deployed policy before relying on it |
| Stock quick quote | `GET /api/stock/quick-quote/<TICKER>` | Yes on current live contract | No | No | Authenticated, no analysis-credit deduction; exact deployment policy must be respected |
| Stock deep analysis | `POST /api/stock/analyze-sync` or async | Yes | Yes, subject to account allowance | Yes after allowance/credits are exhausted | Paid-capable analysis |
| Canonical options score | `POST /api/v1/options/score` | Yes; API-key access is endpoint-specific | Yes | Yes after allowance/credits are exhausted | Paid-capable analysis |
| Option chain analysis | `/api/options/chain-sync`, `/api/options/chain-async` | Yes | Yes | Yes after allowance/credits are exhausted | Paid-capable analysis |
| Enhanced option analysis | `/api/options/enhanced-sync`, `/api/options/enhanced-async` | Yes | Yes | Yes after allowance/credits are exhausted | Paid-capable analysis |
| Strategy scan / simulator / Greeks tools | `/api/options/tools/*` | Yes unless a route explicitly says otherwise | Usually analysis-related; verify route contract | Usually subscription/credits after allowance | Do not infer billing from `OPTIONS 200` |
| Research Brain workspace | `/api/research/*` private workflows | Yes | Feature- and route-specific | Feature/tier-specific | Private; not equivalent to public published research |
| Research profile/theme/macro workflows | `/api/research/profiles`, `/api/research/themes`, `/api/research/macro` | Yes | Feature- and tier-specific | Tier limits apply | Authenticated product workflow |
| Research health check / event radar / AI assist | Research Brain feature routes | Yes | Feature- and tier-specific | Pro or applicable tier | Private feature; do not expose as public Skill promise |
| Full report, deep interpretation and ongoing verification | Future publication contract | To be defined | To be defined | To be defined | Product decision pending; do not change backend access yet |

## Authentication Contract

For authenticated calls, external clients should send:

```http
Authorization: Bearer agbm_xxxxxxxxxxxxxxxx
```

An API key is an account credential, not a free-standing Skills entitlement.
The backend checks whether the specific route allows API-key access. A route
that works for a browser session is not automatically available to an external
API key.

A missing header should be treated as an authentication failure, not as proof
that the endpoint is paid. A successful authentication should also not be
interpreted as proof that the operation is free.

## Quota and Billing Contract

The client must not hardcode plan limits in a Skill. Current limits are account-
and deployment-controlled. The correct flow is:

1. Authenticate with the user's AlphaGBM API key.
2. Call only the endpoint required for the user's request.
3. Treat public summary routes as read-only content, not as a substitute for deep analysis.
4. For analysis routes, expect the account-level free allowance or subscription credits to be checked by the backend.
5. Stop and explain the upgrade/credits requirement when the backend returns a quota or entitlement error.
6. Never retry a quota failure automatically.

The current API does not provide an accepted public quota preflight endpoint.
`/api/user/quota` must not be documented as available until it exists and has
been validated in the target deployment.

## Research Access Policy (Proposed)

The product direction is intentionally tiered:

- **Public:** title, institution, date, covered asset, short abstract, selected key facts and permitted source metadata.
- **Registered account:** fuller structured interpretation where the publication contract permits it.
- **Paid tier/credits:** deeper judgment, valuation decomposition, strategy impact, personalized analysis and ongoing verification.
- **Original third-party report:** never assume redistribution rights; preserve source attribution and licensing boundaries.

This policy is proposed for the next backend publication-contract change. Until
that change is approved and deployed, Skills must describe the current public
reader accurately and must not promise full-report gating or access.

## Evidence and Freshness

Every Skill that returns live or published data should preserve, when supplied by
the API:

- observation or publication time;
- source/provider metadata;
- freshness or cache information;
- market and symbol conventions;
- whether the result is a demo, public summary, or authenticated analysis.

Bundled `mock-data/` is offline sample data. It must never be presented as a
current quote, current score, or evidence that a live endpoint is anonymously
available.

## Release Checklist for New Skills

Before publishing a Skill, verify all of the following against the target
staging deployment:

- [ ] route and HTTP method are correct;
- [ ] anonymous versus authenticated behavior is tested;
- [ ] API-key opt-in is confirmed for the exact route;
- [ ] credit deduction or no-credit behavior is confirmed from source and a safe test;
- [ ] quota failure behavior is documented without triggering paid work;
- [ ] public summaries are not described as full analysis;
- [ ] mock mode is labeled as offline and static;
- [ ] source, timestamp and freshness fields are preserved;
- [ ] no write, editorial, subscription or payment operation is exposed accidentally.
