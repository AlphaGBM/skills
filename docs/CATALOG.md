# AlphaGBM Skills catalogue

Version 3.0.0: 5 workflows and 34 focused tools/reference packages.

Package counts are not a count of independently verified APIs. The workflow runners are self-contained. Account actions require explicit permission to use quota; installation itself is free.

## Workflows

| Workflow | 中文 | Access | Output |
|---|---|---|---|
| [Stock Opportunities](../skills/alphagbm-stock-research/) | 股票机会 | account | Research conclusion, Evidence and risks, Questions to verify |
| [Options Strategies](../skills/alphagbm-options-research/) | 期权策略 | account | Option candidates, Scores and quote times, Funding and risks |
| [News Impact](../skills/alphagbm-news-impact/) | 新闻影响 | public | Event and related assets, Impact evidence and limits, Next checkpoints |
| [Research Report Breakdown](../skills/alphagbm-report-breakdown/) | 研报拆解 | public | Views and original ratings, Assumptions and risks, Sources and checkpoints |
| [Investment Review](../skills/alphagbm-investment-review/) | 投资复盘 | local | Changes since the baseline, Comparability and gaps, Judgments to revisit |

## Focused tools and reference packages

`api` means the documented route is covered by the current access contract review, not that every model/client has completed a live authenticated test. `reference` means method/legacy contract documentation only; do not call its legacy private endpoints with an API key. Use the website or a supported workflow instead.

| Function | 中文 | Category | Status |
|---|---|---|---|
| [Stock Analysis](../skills/alphagbm-stock-analysis/) | 股票分析 | stocks | api |
| [Compare Assets](../skills/alphagbm-compare/) | 标的对比 | stocks | reference |
| [Options Score](../skills/alphagbm-options-score/) | 期权评分 | options | api |
| [Volatility Snapshot](../skills/alphagbm-iv-rank/) | 波动率快照 | options | api |
| [Volatility Surface](../skills/alphagbm-vol-surface/) | 波动率曲面 | options | reference |
| [Volatility Smile](../skills/alphagbm-vol-smile/) | 波动率微笑 | options | reference |
| [Greeks](../skills/alphagbm-greeks/) | 希腊值 | options | reference |
| [Strategy Builder](../skills/alphagbm-options-strategy/) | 策略构建 | options | reference |
| [Payoff Simulation](../skills/alphagbm-pnl-simulator/) | 损益模拟 | options | reference |
| [Earnings IV Crush](../skills/alphagbm-earnings-crush/) | 财报波动率回落 | options | reference |
| [Unusual Options Activity](../skills/alphagbm-unusual-activity/) | 期权异动 | market | reference |
| [Market Sentiment](../skills/alphagbm-market-sentiment/) | 市场情绪 | market | reference |
| [VIX Status](../skills/alphagbm-vix-status/) | VIX状态 | market | reference |
| [Fear Score](../skills/alphagbm-fear-score/) | 恐慌指标 | market | reference |
| [Prediction Markets](../skills/alphagbm-polymarket/) | 预测市场观察 | market | reference |
| [Supply-chain Bottlenecks](../skills/alphagbm-chokepoint/) | 产业链瓶颈 | market | reference |
| [Hedging Scenarios](../skills/alphagbm-hedge-advisor/) | 对冲情景 | risk | reference |
| [Put-spread Backtest](../skills/alphagbm-bps-backtest/) | 价差策略回测 | risk | reference |
| [Exit Strategy Comparison](../skills/alphagbm-take-profit/) | 退出策略对照 | risk | reference |
| [Watchlist](../skills/alphagbm-watchlist/) | 关注列表 | research | reference |
| [Conditional Alerts](../skills/alphagbm-alert/) | 条件提醒 | research | reference |
| [Company Profile](../skills/alphagbm-company-profile/) | 公司研究档案 | research | reference |
| [Investment Thesis](../skills/alphagbm-investment-thesis/) | 投资论据 | research | reference |
| [Macro View](../skills/alphagbm-macro-view/) | 宏观观察 | research | reference |
| [Theme Research](../skills/alphagbm-theme-research/) | 主题研究 | research | reference |
| [Research Health Check](../skills/alphagbm-health-check/) | 研究档案检查 | research | reference |
| [Published Research](../skills/alphagbm-research-insights/) | 已发布研究阅读 | research | api |
| [Duan Yongping Framework](../skills/alphagbm-duan-analysis/) | 段永平框架 | methods | reference |
| [Buffett Framework](../skills/alphagbm-buffett-analysis/) | 巴菲特框架 | methods | reference |
| [Marks Cycle Framework](../skills/alphagbm-marks-cycle/) | 马克斯周期框架 | methods | reference |
| [Tepper Framework](../skills/alphagbm-tepper-signal/) | 泰珀框架 | methods | reference |
| [Find Opportunities](../skills/alphagbm-opportunity-radar/) | 发现机会 | stocks | api |
| [Read Research & News](../skills/alphagbm-research-reader/) | 读研报与新闻 | research | api |
| [Verify a Thesis](../skills/alphagbm-thesis-check/) | 验证与复查判断 | risk | api |
