# AlphaGBM Skills

[安装、升级与版本核对](INSTALLATION.md)：本地源需要重新安装；确认所选客户端与安装范围。

**用于股票分析、期权研究和金融研究的开源 AI Agent Skills，可在 Claude Code、Cursor 等兼容工具中使用。**

股票机会、期权策略、新闻影响、研报拆解、投资复盘：按需要选择，不必一次安装全部。

第一次来？可以先看[股票研究合成示例](../demo/stock-opportunities.json)，无需账户；它不是实时行情，也不是付费调用实录。再按[安装说明](INSTALLATION.md)选择一个技能。安装免费，账户型调用另有权限与额度限制。

示例中的 74 分只是示意，不代表 74% 胜率。研究得分不是胜率或买卖信号；安装不会解锁 Alpha Agent，也不会增加研究额度。

[社区入门](https://github.com/AlphaGBM/skills/discussions/21) · [提问与讨论](https://github.com/AlphaGBM/skills/discussions) · [报告问题](https://github.com/AlphaGBM/skills/issues/new/choose) · [参与贡献](COMMUNITY.md)

<!-- catalog:start -->
**28 Skills · 5 核心技能 + 23 单项技能**

| Category / 分类 | Count / 数量 |
|---|---|
| [核心技能](../skills/core/) | 5 |
| [股票](../skills/stocks/) | 10 |
| [期权](../skills/options/) | 11 |
| [商品](../skills/commodities/) | 1 |
| [虚拟资产](../skills/digital-assets/) | 1 |

<!-- catalog:end -->

数量包含方法参考包，不等于已开放的数据接口数量。每个技能保留实际权限与发布状态；发布预览不代表已完成生产实测。

## 豆包工作用户从这里开始

[豆包上手指南与下载入口](DOUBAO.md)：用现有的**产业因果研究**方法分析你有权使用的材料，或经你明确授权检索公开原件，交付追问、证据、实际计算和反证。没材料就选择「上传／授权公开检索」，不用先备齐整套研报。**不需要另装 Codex，也不需要 AlphaGBM API Key**。有原生技能导入入口就导入；没有则按本次会话的文件工作流使用。豆包原生导入及跨会话自动发现尚未验收，不代表开放内部研报库或付费研究。

## WorkBuddy 用户从这里开始

[WorkBuddy 安装与首次使用指南](WORKBUDDY.md)：用户已实测宿主技能目录安装、显式 Skill 加载和 Stock Research 随包离线演示，环境为 WorkBuddy 中的 CodeBuddy CLI 2.184.0。演示不需要另装 Codex 或配置 AlphaGBM API Key；自动触发、其他技能及真实付费研究不在本次验收范围内。

新版每个技能自带[简短首次介绍](INTRODUCTION.md)、自然语言快捷用法和可选官网入口；跟随你的语言，不反复宣传，不打断明确任务，也不破坏JSON等严格输出。

## 开始使用

```bash
npx skills@1.9.0 add AlphaGBM/skills --skill alphagbm-stock-research --agent codex --copy -y
```

这条命令只安装到当前项目的 Codex 目录。使用 Claude Code 或 Cursor 时，将 `codex` 改为 `claude-code` 或 `cursor`，不要省略目标客户端。此安装器版本的 Codex/Cursor 项目目录为 `.agents/skills`，Claude Code 为 `.claude/skills`。

安装后无需 Key、无需研究额度，先跑包内合成演示：

```bash
python3 .agents/skills/alphagbm-stock-research/scripts/demo.py --lang zh
```

也可在已安装的 AI 客户端中说：**“用 AlphaGBM 跑一次离线合成拆股演示，不联网、不消耗研究额度。”** Claude Code 的命令路径改为 `.claude/skills`。这是离线示例，不是真实研究；结构化在线工作流仍为发布预览。

然后告诉你的 AI：

> 用 AlphaGBM 研究 NVDA，给出支持依据、反方证据和下一步验证点。使用我的研究额度前先征得同意。

可调用的技能自带 Python 3.9+ 运行器，无需另外安装 AlphaGBM CLI。账户型调用与官网共用额度，安装不会赠送额外额度或解锁 Alpha Agent。在账户中创建 API Key 后，安全配置到本地环境；不要粘贴到对话中。

## 单项技能

<!-- stock-tools:start -->
**股票10项：**产业因果研究、股票分析、高息策略、市场情绪、研报查阅、趋势跟踪、ETF策略、网格计划、定投计划、聪明钱跟踪。
<!-- stock-tools:end -->

市场情绪统一涵盖 VIX 和恐慌指标，不再拆成重复卡片。聪明钱跟踪整理已披露记录，不自动跟单或下单。

期权、商品与虚拟资产按[完整目录](CATALOG.md)选择。方法参考不会自动获取实时数据；发布预览保留后端可用性检查。公开研报查阅不等于开放内部研报数据库。

## 示例与目录

[每项技能的示例索引](../demo/CATALOG.md)区分合成输出示例与带来源的请求案例，不将二者冒充真实付费调用结果。

官网卡片与 GitHub 共用[唯一清单](../catalog/catalog.json)，名称、分组、技能 ID 和复制路径保持一致。投资大师方法在 [investment-masters](https://github.com/AlphaGBM/investment-masters) 单独维护，不重复计数。

旧版平铺目录已改为 `skills/<类别>/<技能ID>/`；保留的安装名称不变。请重新安装或使用新目录链接。研究管理等已移除项目不再出现在最新版清单，旧的固定版本仍可从 Git 历史读取。

## 社区参与

这里也统一接收 [Investment Masters](https://github.com/AlphaGBM/investment-masters) 和 [Trading Skills](https://github.com/AlphaGBM/alphagbm-trading-skills) 的使用反馈，请注明来源仓库。它们是独立的方法仓库，不代表本目录增加了实时接口。

安装求助、使用方法和研究流程建议请到 Discussions；可复现的故障或范围明确的改动请提交 Issue。中英文均可。可从 [good first issue](https://github.com/AlphaGBM/skills/issues?q=is%3Aissue%20is%3Aopen%20label%3A%22good%20first%20issue%22) 开始；不要求先 Star，不承诺投资收益或固定回复时间。

请只提交合成或可公开使用的材料，不要发布 API Key、账户资料、私人报告或未经许可的研报原文。详见[社区指南](COMMUNITY.md)。

[官网](https://www.alphagbm.com/skills) · [账户权益](https://www.alphagbm.com/pricing) · [权限说明](ACCESS.md) · [English](../README.md)
