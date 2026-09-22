---
name: alphagbm-chokepoint
description: |
  Serenity-style "Chokepoint Theory" applied to AI supply chains. Identifies
  physically irreplaceable bottleneck suppliers — small-cap near-monopolies
  buried 4–7 layers deep — whose capacity constraints force violent repricing
  when demand outgrows supply. Uses a 5-factor scoring model (Concentration,
  Irreplaceability, Qualification Gate, Discovery Gap, Demand Tension) to
  screen and rank candidates. This is AlphaGBM's independent reading of
  Serenity (@aleabitoreddit)'s publicly shared methodology — NOT affiliated
  with or endorsed by Serenity.
  Triggers: "chokepoint analysis", "AI supply chain bottleneck", "find the
  shiso leaf", "Serenity-style screen", "which small-caps own the bottleneck",
  "InP substrate play", "co-packaged optics chokepoint", "irreplaceable
  supplier in AI buildout", "supply chain concentration risk"
---

# AlphaGBM Chokepoint Analysis (Serenity-style)

In a piece of sushi, the tuna belly is the expensive part — but the shiso leaf
is the one thing you cannot skip.

Everyone owns the "tuna": NVIDIA, TSMC, the hyperscalers. The alpha hides in
the "shiso leaf" — the tiny, overlooked, near-monopoly suppliers buried 4–7
layers deep in the AI supply chain, whose failure would halt the entire buildout.

This skill codifies the **Chokepoint Theory** as publicly described by Serenity
(@aleabitoreddit), one of the most discussed retail AI-supply-chain analysts.

> ⚠️ **Disclaimer**: This is AlphaGBM's independent interpretation of publicly
> available ideas. Not affiliated with, endorsed by, or connected to Serenity.
> Nothing here is financial advice. These are typically small-cap, illiquid,
> highly volatile names — you can lose everything.

## The 5-Factor Chokepoint Test

A true chokepoint is a supply-chain node that satisfies **all five** criteria
simultaneously. Each factor is scored 0–100; the overall Chokepoint Score is the
weighted composite.

| # | Factor | Weight | What It Measures | Strong Signal |
|---|--------|--------|------------------|---------------|
| 1 | **Concentration** | 25% | Top 1–3 suppliers hold ≥ 70% market share | HHI > 2500, CR3 ≥ 70% |
| 2 | **Irreplaceability** | 25% | Material-science or physics moat; no viable second source | No drop-in substitute exists |
| 3 | **Qualification Gate** | 20% | Design-in / qualification cycle ≥ 12 months | 12–24 month cycle, customer switching cost |
| 4 | **Discovery Gap** | 15% | Under-owned, under-covered by institutions | Institutional ownership < 40%, analyst coverage ≤ 3 |
| 5 | **Demand Tension** | 15% | Downstream demand growing ≥ 50% CAGR vs flat/constrained supply | Demand CAGR ≥ 50%, capacity utilization > 85% |

### Scoring Thresholds

- **≥ 80** → **CORE** — highest-conviction chokepoint, full position
- **60–79** → **BUILD** — strong candidate, scale in on confirmation
- **40–59** → **STARTER** — early signal, small position, monitor closely
- **< 40** → **PASS** — does not meet chokepoint criteria

## The Logic: Why Chokepoints Reprice

When demand grows at 50–100% CAGR but the chokepoint physically cannot expand
capacity at the same rate (constrained by physics, materials, clean-room build
time, or qualification cycles), the screw gets repriced violently upward.

The framework is **not** about:
- Betting on earnings beats
- Momentum / technical analysis
- Macro timing

It **is** about:
- Mapping the physical supply chain end-to-end
- Finding the narrowest point where supply is inelastic
- Entering before the market prices in the constraint

## Canonical Example: AXTI (AXT Inc.)

The AXTI thesis illustrates the framework in action:

- **What they make**: Indium Phosphide (InP) substrates — the base wafer for
  photonic integrated circuits (PICs) used in co-packaged optics
- **Concentration**: AXTI + 2 others control ~85% of global InP substrate supply
- **Irreplaceability**: InP is the only material that works for 800G+ optical
  transceivers; GaAs and Si cannot substitute at these wavelengths
- **Qualification Gate**: 18-month qualification cycle with each foundry customer
- **Discovery Gap**: Was a $200M market cap, <5 analyst coverage when the thesis
  was formed
- **Demand Tension**: Co-packaged optics demand growing at ~80% CAGR; substrate
  capacity expansion takes 2+ years

Result: the stock repriced ~30x as the market recognized the bottleneck.

## How to Use This Skill

This is a **methodology skill** — it provides the analytical framework for an
AI agent to evaluate whether a given company or supply-chain node qualifies as
a chokepoint.

### Input

Provide one of:
- A **ticker** to evaluate against the 5-factor test
- A **supply-chain segment** (e.g., "InP substrates", "HBM packaging",
  "advanced substrates for AI servers") to map and identify chokepoint candidates
- A **thesis** to stress-test (e.g., "AXTI is a chokepoint in co-packaged optics")

### Output

The agent should return:
1. **Supply-chain map** — where the company sits in the value chain
2. **5-factor scorecard** — each factor scored 0–100 with evidence
3. **Overall Chokepoint Score** — weighted composite + tier (CORE/BUILD/STARTER/PASS)
4. **Key risks** — what could break the thesis (second source emerging,
   demand destruction, technology shift)
5. **Comparable chokepoints** — other names in the same supply chain that may
   also qualify

### Example Queries

- `Is AXTI a chokepoint in co-packaged optics?`
- `Map the HBM supply chain and find the bottleneck`
- `Which InP substrate makers qualify as chokepoints?`
- `Evaluate CEVA as a chokepoint in sensor fusion IP`
- `Find the shiso leaf in the AI server power delivery chain`

## Key Supply-Chain Domains to Watch

| Domain | Why It Matters | Example Chokepoints |
|--------|----------------|---------------------|
| **Co-packaged Optics** | 800G→1.6T transceiver migration | InP substrates, EEL lasers |
| **Advanced Packaging** | HBM + chiplet integration | CoWoS capacity, bonding equipment |
| **AI Power Delivery** | 1MW+ per rack power density | GaN/SiC power semis, busbar/PDU |
| **Specialty Materials** | Enabling substrates & gases | InP wafers, ultra-high-purity gases |
| **Cooling** | Liquid cooling for AI clusters | CDU units, cold plate connectors |

## Risk Factors

Every chokepoint thesis has kill conditions. The agent must surface these:

1. **Second source qualification** — a new supplier completing qual breaks the monopoly
2. **Technology substitution** — a different material or architecture bypasses the bottleneck
3. **Demand destruction** — AI capex slowdown reduces urgency
4. **Customer vertical integration** — hyperscaler builds in-house
5. **Geopolitical risk** — export controls or sanctions disrupt supply chain

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-stock-analysis](../alphagbm-stock-analysis/) | Complement with G=B+M scoring for overall stock quality |
| [alphagbm-company-profile](../alphagbm-company-profile/) | Deep fundamental profile for chokepoint candidates |
| [alphagbm-theme-research](../alphagbm-theme-research/) | Map broader AI themes before drilling into chokepoints |
| [alphagbm-investment-thesis](../alphagbm-investment-thesis/) | Convert chokepoint finding into a trackable thesis |
| [alphagbm-unusual-activity](../alphagbm-unusual-activity/) | Detect institutional accumulation in chokepoint names |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence.*
