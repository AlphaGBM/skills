# Stock-split basis example / 拆股口径示例

This is a **synthetic, offline example** about a fictional company. It is not a
live market quote, not an investment recommendation, and not evidence that a
paid workflow has run. The fixture is
[`stock-split-basis.json`](stock-split-basis.json).

## English

Two prices or target prices can only be compared when both are expressed on the
same stock-split basis.

| Item | Value |
|---|---|
| Split | 4-for-1: each old share becomes 4 new shares |
| Earlier target (before the split) | 120 USD per pre-split (old) share |
| Same target on the post-split basis | 120 / 4 = 30 USD per post-split (new) share |
| Later target (after the split) | 27 USD per post-split (new) share |

- Moving from 120 per old share to 30 per new share is only a change of basis.
  The same-basis change is 0%; it is **not a downgrade**. Reading it as -75%
  mixes two bases.
- The later target of 27 is compared with 30, not with 120:
  (27 - 30) / 30 x 100 = **-10%**. Using 120 would give a wrong -77.5%.
- If the split ratio or the basis of a price is missing, mark the comparison as
  **unknown**. Do not guess a ratio and do not assume which basis was used.

## 中文

两个价格或目标价只有在同一拆股口径下才能比较。

| 项目 | 数值 |
|---|---|
| 拆股 | 1 拆 4：每 1 股旧股变为 4 股新股 |
| 较早目标价（拆股前） | 每股拆股前（旧）股 120 美元 |
| 换算到拆股后口径 | 120 / 4 = 每股拆股后（新）股 30 美元 |
| 较晚目标价（拆股后） | 每股拆股后（新）股 27 美元 |

- 从每股旧股 120 变为每股新股 30 只是口径变化，同口径变化为 0%，**不是下调**。
  把它读作 -75% 是混用了两种口径。
- 较晚的 27 应与 30 比较，而不是与 120 比较：(27 - 30) / 30 x 100 = **-10%**。
  若与 120 比较会得出错误的 -77.5%。
- 如果缺少拆股比例或价格口径，比较结果应标记为**未知**，不要猜测比例，也不要假定口径。

本示例为合成的离线数据，涉及虚构公司，不是实时行情，不构成投资建议，也不能证明任何付费流程已经运行。
