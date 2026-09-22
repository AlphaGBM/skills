# Release notes

## 3.1.0 — Website-aligned directory

- One canonical catalogue: 5 core Skills and 22 focused Skills (9 stocks, 11 options, 1 commodity and 1 digital-assets method).
- Move physical packages into `skills/core`, `stocks`, `options`, `commodities` and `digital-assets`. Retained install IDs stay unchanged; old flat file URLs must be updated.
- Move Momentum Following, ETF Strategy, Grid Plan, Dollar-Cost Averaging and Smart Money Tracking into focused stock Skills. Consolidate VIX/fear methods into Market Sentiment and keep Research Reports as the research-reading entry.
- Remove fourteen retired standalone entries from the latest installable directory. Historical versions and shared runtime compatibility commands remain, but do not count as active Skills.
- Generate bilingual README counts, category indexes and demo coverage from the same catalogue used by website copy instructions. No new data access, pricing or production-verification claims.

Older entries below describe their release-time inventory, not the current catalogue.

## 2026-09-22 — Workflow catalogue release candidate

- Reframed the public README around five result-oriented workflows instead of a flat tool list.
- Added explicitly synthetic demo fixtures and refreshed the visual demo so examples cannot be mistaken for live quotes.
- Clarified staged-backend, shared-account allowance, public-read and local-review boundaries.
- Kept legacy focused packages and install names compatible.

## 3.0.0 — workflow-first catalogue

- Final core names: Stock Opportunities, Options Strategies, News Impact, Research Report Breakdown, Investment Review. The last three now have standalone installable packages.
- The former radar, reader and thesis-check packages remain compatible focused tools: five workflows plus 34 focused tools/reference packages, not 39 live APIs.
- Investment Review is local-only. The four structured server workflows retain preview status until the matching deployment is verified; this draft is not a production release.

- Five self-contained workflows layered over the existing focused tool/reference packages.
- One bilingual JSON catalogue generates package metadata, bundled Python runners and the readable directory. Website imports are pinned and hash-checked.
- First use can read published research without a key; account calls retain shared usage and explicit approval.
- Research reader uses the current catalogue, separating original research, institutional views and news.
- Legacy interfaces without published API-key access are reference-only, not silently called or advertised as live.
- No backend prices, entitlements, trading operations or automatic monitoring are introduced.

This is a release candidate until its repository PR and matching website PR are approved. Installer checks are not a substitute for authenticated model/client tests.
