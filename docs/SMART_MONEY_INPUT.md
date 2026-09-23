# Smart Money transaction input

The file contains a non-empty JSON array, not an object wrapping `transactions`.
The runner adds that wrapper when calling the API. Obtain consent before using
the account allowance. Invalid local inputs must not trigger a paid request.

| Field | Required value |
| --- | --- |
| `date` | Disclosure date, `YYYY-MM-DD`; retain the trade date separately if known. |
| `side` | Exactly `buy` or `sell`, lowercase. |
| `source` | Non-empty public disclosure citation or source URL. |
| `value` | Positive, finite traded amount in currency units, not shares or thousands/millions. |
| `symbol` | Optional asset code, such as `NVDA`. |

All entries in one request must use the same currency and amount basis. The API
does not convert currencies; split currencies into separate requests. State the
currency in the final explanation. Do not infer buys/sells from a single holdings
snapshot, treat a 13F holding value as a trade, or invent a missing amount.
Preserve disclosure lag and missing information. This does not execute trades.

## Format-only example

These are fictional records for testing the input format, not actual trades or
market evidence. Save as `disclosed-transactions.json` only for an explicit test.

```json
[
  {"date":"2026-09-01","side":"buy","value":1000,"source":"Format-only example A; USD; not a real disclosure","symbol":"EXAMPLE"},
  {"date":"2026-09-02","side":"sell","value":250,"source":"Format-only example B; USD; not a real disclosure","symbol":"EXAMPLE"}
]
```

Expected arithmetic: buys 1000, sells 250, net 750, gross 1250, net-flow ratio
0.6. A positive net flow is not a forecast or a buy recommendation.

Run the command in `SKILL.md` with authorized, real disclosures for research.
Do not use `disclosedAt` or `action`: those are not API field names.

中文：必填字段为披露日期 `date`、买卖方向 `side`、公开来源 `source`、成交金额
`value`。同一请求必须使用同一种货币、相同金额单位；不要把股数或持仓市值当成成交金额。
示例仅供格式测试，不代表真实交易，不可用于投资判断。
