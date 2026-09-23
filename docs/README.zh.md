# AlphaGBM Skills

[安装、升级与版本核对](INSTALLATION.md)：本地源需要重新安装；确认所选客户端与安装范围。

**在你自己的 AI 工具中，调用 AlphaGBM 的研究能力。**

股票机会、期权策略、新闻影响、研报拆解、投资复盘：按需要选择，不必一次安装全部。

<!-- catalog:start -->
**27 Skills · 5 核心技能 + 22 单项技能**

| Category / 分类 | Count / 数量 |
|---|---|
| [核心技能](../skills/core/) | 5 |
| [股票](../skills/stocks/) | 9 |
| [期权](../skills/options/) | 11 |
| [商品](../skills/commodities/) | 1 |
| [虚拟资产](../skills/digital-assets/) | 1 |

<!-- catalog:end -->

数量包含方法参考包，不等于已开放的数据接口数量。每个技能保留实际权限与发布状态；发布预览不代表已完成生产实测。

## 开始使用

```bash
npx skills add AlphaGBM/skills --skill alphagbm-stock-research
```

然后告诉你的 AI：

> 用 AlphaGBM 研究 NVDA，给出支持依据、反方证据和下一步验证点。使用我的研究额度前先征得同意。

可调用的技能自带 Python 3.9+ 运行器，无需另外安装 AlphaGBM CLI。账户型调用与官网共用额度，安装不会赠送额外额度或解锁 Alpha Agent。在账户中创建 API Key 后，安全配置到本地环境；不要粘贴到对话中。

## 单项技能

**股票九项：**股票分析、高息策略、市场情绪、研报查阅、趋势跟踪、ETF策略、网格计划、定投计划、聪明钱跟踪。

市场情绪统一涵盖 VIX 和恐慌指标，不再拆成重复卡片。聪明钱跟踪整理已披露记录，不自动跟单或下单。

期权、商品与虚拟资产按[完整目录](CATALOG.md)选择。方法参考不会自动获取实时数据；发布预览保留后端可用性检查。公开研报查阅不等于开放内部研报数据库。

## 示例与目录

[每项技能的示例索引](../demo/CATALOG.md)区分合成输出示例与带来源的请求案例，不将二者冒充真实付费调用结果。

官网卡片与 GitHub 共用[唯一清单](../catalog/catalog.json)，名称、分组、技能 ID 和复制路径保持一致。投资大师方法在 [investment-masters](https://github.com/AlphaGBM/investment-masters) 单独维护，不重复计数。

旧版平铺目录已改为 `skills/<类别>/<技能ID>/`；保留的安装名称不变。请重新安装或使用新目录链接。研究管理等已移除项目不再出现在最新版清单，旧的固定版本仍可从 Git 历史读取。

[官网](https://www.alphagbm.com/skills) · [账户权益](https://www.alphagbm.com/pricing) · [权限说明](ACCESS.md) · [English](../README.md)
