# Community / 社区参与

This is the maintainer's entry point for genuine feedback and contributions, not a collection of invented user testimonials. English and Chinese are welcome; a Star is never required for help.

这里欢迎真实使用反馈与贡献，不制造用户评价或虚假活跃；提问无需先 Star。

Start with the [maintainer welcome / 入门公告](https://github.com/AlphaGBM/skills/discussions/21). This is also the shared help entry for `investment-masters` and `alphagbm-trading-skills`; mention the source repository when posting.

另外两个仓也从这里提问，请注明来源仓库；属于某仓文件的具体缺陷可以留在该仓跟踪，不必重复开帖。

## Where to post / 发到哪里

| Need / 需求 | Entry / 入口 |
|---|---|
| Installation or usage questions / 安装和用法 | [Q&A](https://github.com/AlphaGBM/skills/discussions/categories/q-a) |
| Installation failed after following the docs / 按说明安装仍失败 | [Installation report](https://github.com/AlphaGBM/skills/issues/new?template=install.yml) |
| New workflows or feedback / 流程建议和反馈 | [Ideas](https://github.com/AlphaGBM/skills/discussions/categories/ideas) |
| Reproducible bugs / 可复现故障 | [Bug report](https://github.com/AlphaGBM/skills/issues/new?template=bug_report.yml) |
| A scoped new capability / 范围明确的新能力 | [Proposal](https://github.com/AlphaGBM/skills/issues/new?template=skill_proposal.yml) |
| Documentation or examples / 文档和示例 | [Documentation gap](https://github.com/AlphaGBM/skills/issues/new?template=documentation.yml) |
| A first contribution / 首次贡献 | [Good first issues](https://github.com/AlphaGBM/skills/issues?q=is%3Aissue%20is%3Aopen%20label%3A%22good%20first%20issue%22) |

Search existing posts before opening another. An open proposal is not a release promise. Maintainers may clarify scope before accepting a change; there is no fixed response-time guarantee.

提交前先搜索已有帖子；开放建议不代表承诺排期或上线。请先对齐范围，再投入大量实现时间。

Maintainer-created issues are welcome for real, scoped work; they are not evidence of external user adoption. Use `needs-triage` for unreviewed reports, remove it after review, and use `needs-info` only while waiting for necessary details. Link a fix or explain the next step rather than closing without context. Mark a Q&A answer only when it actually resolves the question.

维护者可以开真实任务，但不能冒充用户反馈。标签用于分诊，不为制造活跃；没有新问题时无需发帖，也不承诺固定回复时限。

## Include useful evidence / 怎样提供有效信息

- Name the package, installed commit, AI client, operating system and relevant Python/installer versions.
- Describe expected and actual behavior, plus the smallest safe reproduction. Separate a method-reference package from an API-backed workflow.
- Label examples as synthetic, public-source or an actual observed result. Do not present a fixture as a real paid call.
- For installation checks, use an isolated project scope. Do not overwrite global configuration or create chargeable requests just to file a report.
- For financial calculations, include units, observation dates, formulas and limitations. A score or model output is not a profit guarantee.

Checking a published analyst target against its source or normalizing it for a stock split is welcome research verification; asking maintainers what price to buy or sell at is not. Cite the dated source and distinguish its claim from your calculation.

可以核对公开研报的目标价出处、日期及拆股口径；不替用户给买卖目标价。请区分来源陈述与自己的计算，不把得分说成胜率。

请提供技能 ID、安装版本、客户端和最小复现；区分合成样例与真实结果。遇到扣费或状态不明的问题，不要为了截图重复提交分析任务。

## Privacy and conduct / 隐私与参与边界

Issues and Discussions are public. Never upload API keys, tokens, account identifiers, private portfolios, unredacted logs or copyrighted research you cannot share. Use synthetic examples and redact local paths or identities. Use the support contact on the [AlphaGBM website](https://www.alphagbm.com) for account-specific help. If you need a private channel for a security concern, ask a maintainer how to report it without publishing sensitive details.

不要上传密钥、账户信息、私人持仓、完整未脱敏日志或未经许可的研报原文；账户问题请通过官网客服渠道处理。安全问题若没有已确认的私密反馈渠道，可先询问维护者接收方式，不要在公开帖子披露细节。

Discuss reproducible behavior rather than people. No harassment, spam, guaranteed-return claims or unsolicited promotion. Maintainers may moderate unsafe or off-topic content. See [access and usage limits](ACCESS.md) before making account-backed requests and [contribution guidance](../CONTRIBUTING.md) before a PR.
