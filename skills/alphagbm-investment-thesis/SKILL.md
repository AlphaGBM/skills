---
name: alphagbm-investment-thesis
description: >
  Record and track the "why I bought" and "when I sell" for each position.
  Each thesis is attached to a company profile: buy reasons in prose, sell
  conditions as structured triggers (price drop, PE spike, thesis breach).
  The system monitors conditions automatically and flips the thesis to
  "triggered" when one fires. Use when: writing buy logic, setting exit
  triggers, reviewing active theses, seeing which triggered.
  Triggers on: "write a thesis for NVDA", "why did I buy AAPL", "set a
  stop loss logic on TSLA", "which theses are triggered", "update my
  thesis", "投资论据", "卖出条件", "买入理由", "论据被打破".
---

# AlphaGBM Investment Thesis

Turn "I bought this because…" into a tracked, monitored record. Each thesis pairs a prose buy-reason with structured sell conditions so the system can auto-detect when the reasoning no longer holds.

## When to use

- User wants to document *why* they bought a stock
- User wants to set exit triggers (price, PE, fundamental breach)
- User asks which theses are still valid vs triggered
- User asks to update / refine an existing thesis
- User mentions "论据" / "买入理由" / "卖出条件" / "thesis" / "exit trigger"

## Prerequisites

- **API Key**: env `ALPHAGBM_API_KEY` (format `agbm_xxxx…`).
- **Base URL**: default `https://alphagbm.zeabur.app`. Override via `ALPHAGBM_BASE_URL`.
- **Profile required**: A thesis must attach to an existing company profile. If the user hasn't created a profile for the ticker, call `POST /api/research/profiles` first (see `alphagbm-company-profile`).

## API Endpoints

All endpoints require `Authorization: Bearer $ALPHAGBM_API_KEY`.

### 1. List theses

```
GET /api/research/theses?status=active
```

| Query | Values | Description |
|-------|--------|-------------|
| `status` | `active` / `triggered` / `closed` | Optional filter |

**Response:**
```json
{
  "success": true,
  "theses": [
    { "id": 12, "ticker": "NVDA", "buy_thesis": "...", "status": "active", ... }
  ]
}
```

### 2. Get thesis by ticker

```
GET /api/research/theses/<TICKER>
```

Returns the *active* thesis for a ticker. 404 if none exists.

### 3. Create thesis

```
POST /api/research/theses
Content-Type: application/json

{
  "ticker": "NVDA",
  "buy_thesis": "AI capex cycle; data-center GPU moat; FCF > $60B.",
  "sell_conditions": [
    { "type": "price_drop_pct",  "value": 20 },
    { "type": "pe_above",        "value": 60 },
    { "type": "growth_below",    "value": 15 },
    { "type": "thesis_breach",   "value": "cloud capex guidance cut > 20%" }
  ]
}
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ticker` | string | yes | Must match an existing profile |
| `buy_thesis` | string | yes | Free-form prose, recommend 2-4 sentences |
| `sell_conditions` | array | no | Structured triggers (see types below) |

**Common `sell_conditions` types:**
- `price_drop_pct` — drop from purchase/peak %
- `pe_above` / `pb_above` — valuation ceiling
- `growth_below` — revenue/earnings growth threshold
- `thesis_breach` — free-text qualitative trigger (monitored manually)

### 4. Update thesis (by id)

```
PUT /api/research/theses/<THESIS_ID>
Content-Type: application/json

{"buy_thesis": "updated prose", "sell_conditions": [...], "status": "closed"}
```

Partial updates allowed. Note: **uses `thesis_id` (int)**, not ticker — read the id from a prior `list` or `get`.

### 5. Delete thesis (by id)

```
DELETE /api/research/theses/<THESIS_ID>
```

Hard-delete. Also uses numeric id.

## Response schema — full thesis

```
{
  id, ticker,
  buy_thesis,                     // prose
  sell_conditions,                // [{type, value}]
  status,                         // "active" | "triggered" | "closed"
  thesis_score,                   // AI confidence 0-100 (if scored)
  ai_feedback,                    // AI critique of the thesis (markdown)
  triggered_at, trigger_detail,   // populated when status flips
  created_at, updated_at
}
```

## Status lifecycle

```
active ──(sell condition fires)──▶ triggered
   │                                   │
   └────────(user closes)──▶ closed ◀──┘
```

When `status = "triggered"`, `trigger_detail` shows which condition fired. Surface this to the user — it's the whole point of the system.

## Typical Workflow

```
1. User: "I'm buying NVDA because AI capex is still accelerating"
   → (ensure profile exists — see alphagbm-company-profile)
   → POST /api/research/theses with buy_thesis + sell_conditions
   → Confirm: "Saved. Monitoring: price drop > 20%, PE > 60, growth < 15%."

2. User: "What are my active theses?"
   → GET /api/research/theses?status=active
   → Table: ticker · one-line thesis · conditions · score

3. User: "Any theses triggered?"
   → GET /api/research/theses?status=triggered
   → Alert list with trigger_detail explaining why

4. User: "Update my NVDA thesis — exit if PE > 70 instead of 60"
   → GET /api/research/theses/NVDA to find id
   → PUT /api/research/theses/<id> with revised sell_conditions
```

## Output Formatting Tips

When presenting a thesis to the user, highlight:
1. **Ticker + status** (with color/emoji: active=green, triggered=red, closed=gray)
2. **Buy thesis** — first 2 sentences verbatim
3. **Sell conditions** — bulleted, human-phrased ("Exit if price drops 20%")
4. **If triggered** — which trigger fired, lead with that
5. **AI feedback / score** — if present, show as a pull-quote
6. **Age** — "written 3 weeks ago, reviewed 2 days ago"

## Related Skills

- **alphagbm-company-profile** — Prerequisite. A thesis attaches to a profile.
- **alphagbm-health-check** — Surfaces theses that may have drifted from their original premise
- **alphagbm-stock-analysis** — Run a fresh analysis to sanity-check a thesis

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence for traders and AI agents. 10K+ users.*
