---
name: alphagbm-buffett-analysis
description: |
  Warren Buffett-lens scorecard for any ticker. Scores 4 dimensions 0-100 each
  (business / circle of competence, moat / durable advantage, management / capital
  allocation, valuation / fair price vs 10Y treasury) and returns a weighted
  overall HOLDABLE / WATCHABLE / AVOID verdict. This is NOT a generic fundamental
  screener — it's Buffett's specific framework mechanically applied: sector
  simplicity, gross margin + ROE + profit margin thresholds, FCF yield vs treasury,
  and dividend-continuity as management proxy.
  Triggers: "Buffett analysis AAPL", "score KO with Buffett lens", "would Buffett
  buy MSFT", "JNJ Buffett scorecard", "AAPL moat analysis", "fair price vs bonds",
  "Buffett-style verdict on NVDA", "long-term hold analysis"
globs:
  - "mock-data/buffett-analysis/**"
---

# AlphaGBM Buffett Analysis

The 4 lenses Buffett himself says he applies, computed from yfinance fundamentals
and returned as a single-number verdict plus reasoning for each lens.

## The 4 Lenses

1. **Business (20% weight)** — circle of competence. Simple sectors (consumer
   staples, utilities, industrials) score high. Complex sectors (tech, healthcare,
   financials) score lower unless mega-cap like AAPL.
2. **Moat (30% weight)** — durable advantage. Gross margin > 40%, ROE > 20%,
   profit margin > 15%, and market cap > $100B each contribute to the moat score.
3. **Management (15% weight)** — capital allocation proxy via dividend continuity
   + payout ratio (15-60% is ideal balance) + 5yr avg div yield.
4. **Valuation (35% weight)** — fair price check. PE < 15 → +20, PEG < 1 → +15,
   FCF yield > 10Y treasury + 2pp → +20. PE > 40 or PEG > 2.5 → deductions.

## Overall Verdict

- **≥ 75** → HOLDABLE (color green) — meets Buffett standards, long-term hold
- **55-74** → WATCHABLE (color amber) — wait for better price or clearer evidence
- **< 55** → AVOID (color red) — fails Buffett's standards

## Why This Is a Separate Skill

The generic `alphagbm-stock-analysis` runs a G=B+M style/momentum score. Buffett's
framework is different — it weights moat + valuation much more heavily than
momentum, and penalizes complex businesses regardless of growth. This skill
codifies *Buffett's* rules, not AlphaGBM's house rules.

## How to Use

**Input:**
- `ticker` (required) — US stock symbol

**Output:**
- `scorecard.business`: `{score, sector, industry, verdict_zh, verdict_en}`
- `scorecard.moat`: `{score, gross_margin, roe, profit_margin, market_cap_b, reasons_zh, reasons_en}`
- `scorecard.management`: `{score, dividend_rate, payout_ratio, reasons_zh, reasons_en}`
- `scorecard.valuation`: `{score, pe, forward_pe, peg, pb, fcf_yield_pct, ten_year_treasury, reasons_zh, reasons_en}`
- `scorecard.overall`: `{score, verdict, verdict_zh, verdict_en, color}`

## Example Queries

- `Buffett analysis on KO` → likely HOLDABLE (simple business, strong moat, 30+ year hold by Buffett himself)
- `would Buffett buy NVDA` → likely WATCHABLE or AVOID (complex sector, high valuation)
- `Buffett scorecard JNJ` → likely HOLDABLE (consumer defensive, strong margins, reasonable PE)
- `score AAPL with Buffett lens` → reference Berkshire's own holding for context
- `apply Buffett's checklist to WMT` → retail-native test case

## Mock Data

Mock data in `mock-data/buffett-analysis/` — sample for KO (HOLDABLE).

## API Endpoint

```
POST /api/masters/buffett-analyze
Content-Type: application/json
```

Request body:

```json
{"ticker": "KO"}
```

Response shape:

```json
{
  "success": true,
  "ticker": "KO",
  "current_price": 63.4,
  "scorecard": {
    "business": {
      "score": 85,
      "sector": "Consumer Defensive",
      "industry": "Beverages - Non-Alcoholic",
      "verdict_zh": "业务相对简单,在巴菲特能力圈范围内",
      "verdict_en": "Relatively simple business within Buffett's circle"
    },
    "moat": {
      "score": 100,
      "gross_margin": 60.3,
      "roe": 41.8,
      "profit_margin": 22.4,
      "market_cap_b": 273.4,
      "reasons_zh": ["毛利率 60.3% > 40%,显示定价权", "ROE 41.8% > 20%,资本效率强", "市值 $273B > $100B,规模壁垒", "净利率 22.4% > 15%,强定价权"],
      "reasons_en": ["Gross margin 60.3% > 40% shows pricing power", "ROE 41.8% > 20% — strong capital efficiency", "Market cap $273B > $100B — scale moat", "Net margin 22.4% > 15% — strong pricing power"]
    },
    "management": {
      "score": 80,
      "dividend_rate": 1.94,
      "payout_ratio": 77.0,
      "reasons_zh": ["派息 $1.94 — 体现向股东返现意愿", "5 年平均股息率 3.1%"],
      "reasons_en": ["Dividend $1.94 — willingness to return cash", "5-yr avg div yield 3.1%"]
    },
    "valuation": {
      "score": 45,
      "pe": 24.8,
      "forward_pe": 22.1,
      "peg": 3.2,
      "pb": 10.5,
      "fcf_yield_pct": 3.5,
      "ten_year_treasury": 4.3,
      "reasons_zh": ["FCF 收益率 3.5% < 10Y 美债 4.3%,不如债券"],
      "reasons_en": ["FCF yield 3.5% < 10Y 4.3% — bonds beat it"]
    },
    "overall": {
      "score": 78.3,
      "verdict": "HOLDABLE",
      "verdict_zh": "符合巴菲特标准 — 值得长期持有",
      "verdict_en": "Meets Buffett standards — worth a long-term hold",
      "color": "green"
    }
  },
  "timestamp": "2026-04-24T08:00:00"
}
```

Pricing: 1 stock-analysis credit per call; **30-min cache** per ticker (cache hits free).

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-stock-analysis](../alphagbm-stock-analysis/) | House G=B+M model — complementary, different weights |
| [alphagbm-company-profile](../alphagbm-company-profile/) | Deep fundamental profile once Buffett flags HOLDABLE |
| [alphagbm-investment-thesis](../alphagbm-investment-thesis/) | Turn Buffett verdict into a trackable thesis |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence. 10K+ users.*
