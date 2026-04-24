---
name: alphagbm-bps-backtest
description: |
  Full walk-forward Bull Put Spread backtest over ~8 years of daily history. Runs
  both the signal (FearScore ≥ 60 entry) version AND a no-signal control in the
  same request, so you can quantify whether the fear-entry rule actually delivers
  alpha for this ticker under your parameters. Returns equity curve, 4 KPIs
  (annualized return / win rate / max drawdown / Sharpe), trade ledger, and a
  plain-language takeaway.
  Triggers: "backtest BPS on QQQ", "bull put spread backtest", "does FearScore
  work on SPY", "what DTE for BPS", "optimal bull put spread delta", "BPS strategy
  backtest", "credit spread backtest", "backtest short put spread"
globs:
  - "mock-data/bps-backtest/**"
---

# AlphaGBM BPS Backtest

Backtests the Bull Put Spread (short put + long put at lower strike) as a
mechanical strategy over 2018–present on any ticker, with two passes per call:

1. **With Signal** — only enters when the per-ticker FearScore is ≥ your threshold
2. **No Signal (Control)** — enters unconditionally every Monday

The side-by-side comparison shows whether the signal is doing work, or whether
you're paying 1 credit for noise.

## Parameters

All optional except `ticker`:

| Param | Default | Range | Meaning |
|-------|---------|-------|---------|
| `ticker` | required | US / HK / CN | Underlying |
| `dte_target` | 14 | 7–45 | Days to expiry on entry |
| `short_delta` | 0.25 | 0.15–0.35 | Absolute delta of the short put leg |
| `spread_width` | 5.0 | 2–10 | Dollar width of the spread |
| `take_profit_pct` | 0.50 | 0.20–0.80 | Close when realized % of max profit hits this |
| `fear_threshold` | 60 | 40–80 | FearScore ≥ X is entry signal |
| `start_date` | 2018-01-01 | YYYY-MM-DD | Backtest start |
| `end_date` | 2026-04-20 | YYYY-MM-DD | Backtest end |
| `include_control` | true | bool | Run no-signal control pass alongside |

## What's Returned

Per pass (`with_signal` and `no_signal`):
- `total_trades`, `win_rate_pct`, `annual_return_pct`, `sharpe`, `max_drawdown_pct`,
  `roc_pct`, `avg_holding_days`, `avg_pnl_per_trade`, `total_pnl`, `final_capital`
- `exit_reasons` — count by `take_profit / stop_loss / expiry_otm / expiry_itm / close_early`
- `trades[]` — full ledger (entry/exit date, strikes, credit, pnl, reason)
- `equity_curve[]` — per-day cumulative capital
- `pnl_histogram` — bucket counts for the P&L distribution

Plus:
- `summary` — one-paragraph zh/en takeaway comparing signal vs control, with ⚠️ flags
  when drawdown or win rate look problematic

## Methodology Notes

- IV is proxied by 20-day historical volatility (HV20) for BS pricing.
  Historical option-chain IV is unaffordable to source at scale; HV20 is a reasonable
  proxy but will under-estimate IV around events. Live results typically outperform
  backtest because of this.
- FearScore is reconstructed from the same 6 indicators the live version uses, but
  computed from cheap historical price + volume data only.
- Entries filtered by `max_positions` (3) and `min_entry_spacing_days` (3) and
  a `risk_per_trade` cap (0.5% of capital).

## How to Use

**Example Queries:**
- `backtest BPS on QQQ` — Default params, signal vs control comparison
- `does FearScore work on SPY` — Same call, reads the comparison summary
- `backtest bull put spread IWM DTE 21 delta 0.30` — Custom params
- `what DTE works best for BPS on QQQ` — Run a few with different DTEs, compare
- `bps fear threshold 70 vs 60 on NVDA` — Run two calls with different thresholds

## Mock Data

Mock data in `mock-data/bps-backtest/` — examples for QQQ with signal ON and OFF.

## API Endpoint

```
POST /api/options/bps-backtest
Content-Type: application/json
```

Request body:

```json
{
  "ticker": "QQQ",
  "dte_target": 14,
  "short_delta": 0.25,
  "spread_width": 5.0,
  "take_profit_pct": 0.50,
  "fear_threshold": 60,
  "start_date": "2018-01-01",
  "end_date": "2026-04-20",
  "include_control": true
}
```

Response:

```json
{
  "success": true,
  "ticker": "QQQ",
  "period": {"start": "2018-01-01", "end": "2026-04-20"},
  "with_signal": {
    "total_trades": 28, "win_rate_pct": 100, "annual_return_pct": 10.8,
    "sharpe": 16.3, "max_drawdown_pct": 0.0, "trades": [...], "equity_curve": [...],
    "pnl_histogram": {...}, "exit_reasons": {"take_profit": 20, "expiry_otm": 8}
  },
  "no_signal": {
    "total_trades": 185, "win_rate_pct": 82, "annual_return_pct": 3.5,
    "sharpe": 2.1, "max_drawdown_pct": -8.2, ...
  },
  "summary": {
    "zh": "QQQ · 2018-2026 · 使用 FearScore ≥ 60 触发 BPS 入场，共交易 28 笔，年化 +10.8%，胜率 100%，最大回撤 0.0%。 同参数无信号对照组年化 +3.5%、胜率 82%；信号版本高出无信号组 7.3 个百分点。",
    "en": "QQQ · 2018-2026 · BPS entry on FearScore ≥ 60 over 28 trades: annualized +10.8%, win rate 100%, max drawdown 0.0%. The no-signal control under the same params: annualized +3.5%, win rate 82%. Signal version outperforms by 7.3 pp."
  }
}
```

Pricing: 1 option-analysis credit per call; 30-min cache per parameter hash (cache
hits free). Expect ~5-10s compute for a fresh hash.

## Related Skills

| Skill | Relevance |
|-------|-----------|
| [alphagbm-fear-score](../alphagbm-fear-score/) | The live version of the entry signal being backtested |
| [alphagbm-options-strategy](../alphagbm-options-strategy/) | Build a custom BPS after deciding params |
| [alphagbm-pnl-simulator](../alphagbm-pnl-simulator/) | Forward-simulate a specific BPS at various future prices |

---

*Powered by [AlphaGBM](https://alphagbm.com) — Real-data options & research intelligence. 10K+ users.*
