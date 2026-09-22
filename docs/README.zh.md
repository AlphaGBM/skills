# 把 AlphaGBM 带进你的 AI 工具

**股票机会、期权策略、新闻影响、研报拆解、投资复盘。**

当前为发布预览：结构化服务端工作流需要配套后端，尚未完成生产验收。投资复盘在本地比较你提供的记录。原有单项入口保留，不代表这个分支已经上线。

先选一个任务，不必一次安装全部。目录包含5个完整工作流、34个单项工具与参考包；文件数量不代表同等数量的已验证API。[完整目录与状态](CATALOG.md)

## 第一次使用：先读一份研究

```bash
npx skills add AlphaGBM/skills --skill alphagbm-research-reader
```

按安装提示选择自己的AI工具，然后直接说：

> 帮我调用 AlphaGBM，查找最近的半导体研报，区分机构观点和已披露事实，保留来源与日期。

这个工作流读取公开内容，不需要API Key，不触发付费研究。每个工作流自带执行脚本，需要Python 3.9或更高版本，无需另外安装AlphaGBM CLI。

## 选择你的任务

| 工作流 | 安装名称 | 交付结果 |
|---|---|---|
| 股票机会 | `alphagbm-stock-research` | 基本面、情绪、可用机会分与证据缺口 |
| 期权策略 | `alphagbm-options-research` | 期权评分、参考资金、损益边界与风险 |
| 新闻影响 | `alphagbm-news-impact` | 新闻事实、涉及标的、影响推断与验证节点 |
| 研报拆解 | `alphagbm-report-breakdown` | 已发布观点、原始评级、关键假设与风险 |
| 投资复盘 | `alphagbm-investment-review` | 本地比较你提供的前后记录，不读取云端历史 |

原有 `alphagbm-opportunity-radar`、`alphagbm-research-reader`、`alphagbm-thesis-check` 转入单项目录，安装名称与调用命令保留。

将安装命令中的名称替换成所选任务。工具安装位置的验证，不等于已经验证所有模型都能正确执行付费任务；具体边界见[接入说明](ACCESS.md)。

## 更深入的研究，共用你的账户额度

在[AlphaGBM账户](https://www.alphagbm.com/api-keys)中创建Key，通过自己工具的本地环境配置`ALPHAGBM_API_KEY`。不要将Key粘贴到对话或提交到Git。

> 帮我调用 AlphaGBM 研究 NVDA，先说明需要使用账户额度，再列出支持依据、反方证据和下一步要验证的事。

Skills免费安装，不等于所有数据与分析免费。账户型请求与网站共用额度，实际权限按[当前套餐](https://www.alphagbm.com/pricing)执行；安装不会额外赠送额度或解锁Alpha Agent。

## 单项工具和投资大师框架

需要一个具体功能时，在[目录](CATALOG.md)里选择股票、期权、波动率、研究等单项工具。参考包和未开放的外部接口会明确标注，不以文件存在冒充API可调用。

投资大师框架是可选分析方法，不是投资大师本人背书，也不保证收益。验证工作流是用户发起的一次研究，不会自动交易、写入账户档案或创建定时提醒。行情与研究日期按来源展示，不将历史快照称为实时行情。
