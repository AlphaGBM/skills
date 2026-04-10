# AlphaGBM CLI 使用文档

## 概述

`alphagbm` 是 AlphaGBM 金融分析平台的命令行工具，支持股票分析、期权评分推荐、快速行情查询等功能。通过 API Key 认证访问 AlphaGBM 后端，适合在终端中快速获取分析结果，也可集成到自动化脚本或 AI Agent 中。

## 安装

```bash
cd cli
pip install -e .
```

安装后即可在终端中使用 `alphagbm` 命令。

### 依赖

- Python >= 3.10
- click（命令行框架）
- httpx（HTTP 客户端）
- rich（美观终端输出）

---

## 配置

### 设置 API Key

```bash
alphagbm config set-key agbm_xxxxxxxxxxxxxxxxxxxxxx
```

API Key 以 `agbm_` 开头，可在 AlphaGBM 网站的个人设置中生成。

### 设置 API 地址

```bash
# 使用线上服务（默认）
alphagbm config set-url https://alphagbm.zebabur.app

# 使用本地开发服务
alphagbm config set-url http://localhost:5000
```

### 查看当前配置

```bash
alphagbm config show
```

输出示例：
```
Config file: /Users/lewis/.alphagbm/config.json
API Key:     agbm_a1b…f4e2
Base URL:    https://alphagbm.zebabur.app
```

### 配置优先级

1. 环境变量 `ALPHAGBM_API_KEY` / `ALPHAGBM_BASE_URL`（最高）
2. 配置文件 `~/.alphagbm/config.json`
3. 默认值（base_url = https://alphagbm.zebabur.app）

---

## 命令一览

| 命令 | 功能 | 消耗额度 |
|------|------|---------|
| `alphagbm stock analyze TICKER` | 股票全面分析 | ✅ 1次 |
| `alphagbm stock quote TICKER` | 快速行情报价 | ❌ 免费 |
| `alphagbm options score TICKER` | 期权评分推荐 | ✅ 1次 |
| `alphagbm options recommend` | 每日期权推荐 | ✅ 1次 |
| `alphagbm options snapshot TICKER` | IV/VRP 快照 | ❌ 免费 |
| `alphagbm config set-key` | 设置 API Key | — |
| `alphagbm config set-url` | 设置 API 地址 | — |
| `alphagbm config show` | 查看配置 | — |

---

## 股票分析命令

### `alphagbm stock analyze TICKER`

对指定股票进行完整分析，包含风险评估、EV 期望值模型、目标价格、ATR 止损、市场情绪、AI 报告等。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `TICKER` | 字符串 | ✅ | 股票代码，如 AAPL、00700.HK、600519.SH |
| `--style, -s` | 选项 | ❌ | 分析风格，默认 balanced |
| `--json` | 标志 | ❌ | 输出原始 JSON |

**可选分析风格：**
- `quality` — 质量投资（低风险偏好）
- `value` — 价值投资（关注估值）
- `growth` — 成长投资（关注增长）
- `momentum` — 动量投资（关注趋势）
- `balanced` — 均衡分析（默认）

**示例：**

```bash
# 基础分析（均衡风格）
alphagbm stock analyze AAPL

# 价值投资风格分析
alphagbm stock analyze MSFT --style value

# 输出 JSON 格式（适合脚本/AI处理）
alphagbm stock analyze TSLA --json

# 港股分析
alphagbm stock analyze 00700.HK

# A股分析
alphagbm stock analyze 600519.SH --style quality
```

**返回内容（Rich 表格模式）：**
- 基础数据：价格、PE/PEG、市值、52周高低
- 风险评分：五大支柱评分（0-100）
- 市场情绪：M 维度评分
- EV 模型：期望值、胜率、推荐操作
- 目标价格：5种估值方法结果
- ATR 止损：动态止损价位
- AI 分析报告摘要

**JSON 输出结构（--json）：**

```json
{
  "success": true,
  "ticker": "AAPL",
  "style": "balanced",
  "analysis": {
    "market_data": {
      "price": 185.50,
      "pe_ratio": 28.5,
      "peg_ratio": 1.8,
      "market_cap": 2850000000000,
      "beta": 1.21,
      "52w_high": 199.62,
      "52w_low": 164.08
    },
    "risk_assessment": {
      "overall_score": 42,
      "pillars": {
        "fundamental": 35,
        "technical": 48,
        "macro": 55,
        "sentiment": 38,
        "geopolitical": 40
      }
    },
    "ev_model": {
      "ev": 0.15,
      "win_rate": 0.62,
      "recommendation": "BUY",
      "upside": 0.12,
      "downside": -0.08
    },
    "target_price": {
      "consensus": 195.00,
      "methods": ["DCF", "PE_Band", "PEG", "Growth", "Analyst"]
    },
    "stop_loss": {
      "atr_stop": 172.30,
      "atr_value": 4.52,
      "risk_percent": -7.1
    },
    "ai_report": "..."
  }
}
```

---

### `alphagbm stock quote TICKER`

快速获取股票实时报价，不消耗额度。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `TICKER` | 字符串 | ✅ | 股票代码 |
| `--json` | 标志 | ❌ | 输出原始 JSON |

**示例：**

```bash
alphagbm stock quote NVDA
alphagbm stock quote 00700.HK --json
```

**返回内容：** 当前价格、涨跌幅、成交量、52周高低、PE、市值等。

---

## 期权分析命令

### `alphagbm options score TICKER`

对指定股票的期权进行评分，返回 Top-N 推荐合约。核心功能。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `TICKER` | 字符串 | ✅ | 股票代码，如 AAPL |
| `--strategy, -s` | 选项 | ❌ | 策略类型，默认 all |
| `--expiry, -e` | 日期 | ❌ | 到期日 YYYY-MM-DD，不填自动选最近月度（≥14天） |
| `--top, -n` | 数字 | ❌ | 返回数量，默认 5，最大 10 |
| `--json` | 标志 | ❌ | 输出原始 JSON |

**策略选项：**
- `sell-put` — 卖出看跌期权（看涨/中性，赚权利金）
- `sell-call` — 卖出看涨期权（看跌/中性，赚权利金）
- `buy-call` — 买入看涨期权（看涨，杠杆做多）
- `buy-put` — 买入看跌期权（看跌，对冲/做空）
- `all` — 四种策略全部评分（默认）

**示例：**

```bash
# 评分 AAPL 所有策略
alphagbm options score AAPL

# 只看 Sell Put 推荐
alphagbm options score AAPL --strategy sell-put

# 指定到期日 + Top 3
alphagbm options score TSLA --strategy sell-put --expiry 2026-04-17 --top 3

# JSON 输出
alphagbm options score NVDA --strategy buy-call --json
```

**返回内容（Rich 表格模式）：**
- 当前股价
- 趋势方向 + 强度
- 到期日
- Top-N 推荐列表：
  - 排名、行权价、评分（0-100）
  - 权利金、Delta、IV
  - ATR 安全度（距离 ATR 止损的百分比）
  - 风格标签（如 🛡️保守型、⚡激进型、💰收入型）
  - 估算胜率

**JSON 输出结构（--json）：**

```json
{
  "success": true,
  "ticker": "AAPL",
  "strategy": "sell_put",
  "current_price": 185.50,
  "expiry_date": "2026-04-17",
  "trend": {
    "direction": "uptrend",
    "strength": 0.72,
    "alignment_score": 85
  },
  "recommendations": [
    {
      "rank": 1,
      "strike": 170.0,
      "score": 87.5,
      "premium": 2.35,
      "delta": -0.22,
      "iv": 0.28,
      "atr_safety": "safe",
      "atr_distance_pct": 5.2,
      "style_tag": "conservative_yield",
      "style_label": "🛡️ 保守收入",
      "estimated_win_rate": 0.78,
      "max_loss": 16765.0,
      "return_on_risk": 1.4
    }
  ],
  "meta": {
    "scored_count": 45,
    "filtered_count": 12,
    "scoring_time_ms": 320
  }
}
```

---

### `alphagbm options recommend`

获取每日期权推荐列表。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `TICKER` | 字符串 | ❌ | 可选，指定单只股票 |
| `--count, -n` | 数字 | ❌ | 推荐数量，默认 5，最大 10 |
| `--json` | 标志 | ❌ | 输出原始 JSON |

**示例：**

```bash
alphagbm options recommend
alphagbm options recommend --count 10
alphagbm options recommend --json
```

---

### `alphagbm options snapshot TICKER`

快速获取 IV/VRP 快照，不消耗额度。适合快速判断某只股票是否适合做期权。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `TICKER` | 字符串 | ✅ | 股票代码 |
| `--json` | 标志 | ❌ | 输出原始 JSON |

**示例：**

```bash
alphagbm options snapshot AAPL
alphagbm options snapshot TSLA --json
```

**返回内容：**
- 当前价格
- 最近到期日
- ATM 隐含波动率（IV）
- IV Rank（IV 在历史中的分位数）
- 30 天历史波动率（HV）
- VRP（波动率风险溢价 = IV - HV）
  - 正 VRP → 适合卖期权
  - 负 VRP → 适合买期权

---

## 通用选项

### `--json` 标志

所有分析命令都支持 `--json`，输出原始 JSON 数据。适合：
- 管道操作：`alphagbm stock quote AAPL --json | jq '.price'`
- AI Agent 解析
- 脚本集成

### `--version`

```bash
alphagbm --version
```

### `--help`

```bash
alphagbm --help
alphagbm stock --help
alphagbm options score --help
```

---

## 错误处理

| 错误信息 | 原因 | 解决 |
|---------|------|------|
| `No API key configured` | 未设置 API Key | `alphagbm config set-key YOUR_KEY` |
| `HTTP 401: Unauthorized` | API Key 无效或已过期 | 重新生成 Key |
| `HTTP 429: Too Many Requests` | 超过限流（60次/分钟） | 稍后重试 |
| `HTTP 402: Quota exceeded` | 额度用完 | 充值或等待重置 |
| `HTTP 400: Symbol not in whitelist` | 港股/A股不在支持列表 | 检查支持的股票列表 |
| `Connection refused` | 后端服务未启动 | 检查 API 地址 |

---

## 配置文件

配置存储在 `~/.alphagbm/config.json`：

```json
{
  "api_key": "agbm_a1b2c3d4e5f6...",
  "base_url": "https://alphagbm.zebabur.app"
}
```

环境变量会覆盖配置文件：
- `ALPHAGBM_API_KEY` — 覆盖 api_key
- `ALPHAGBM_BASE_URL` — 覆盖 base_url

---

## 支持的市场

| 市场 | 代码格式 | 示例 |
|------|---------|------|
| 美股 | TICKER | AAPL, TSLA, NVDA |
| 港股 | XXXXX.HK | 00700.HK, 09988.HK |
| A股 | XXXXXX.SH / .SZ | 600519.SH, 000858.SZ |

> 期权分析目前仅支持美股市场。港股/A股期权支持需要白名单。

---

## 典型使用场景

### 场景 1：快速筛选期权

```bash
# 1. 先看 IV 环境
alphagbm options snapshot AAPL

# 2. VRP > 0 → 适合卖期权，评分
alphagbm options score AAPL --strategy sell-put --top 3

# 3. 详细看股票基本面
alphagbm stock analyze AAPL
```

### 场景 2：脚本批量分析

```bash
for ticker in AAPL MSFT NVDA TSLA AMZN; do
  echo "=== $ticker ==="
  alphagbm options score $ticker --strategy sell-put --top 1 --json | jq '{ticker: .ticker, top_strike: .recommendations[0].strike, score: .recommendations[0].score}'
done
```

### 场景 3：AI Agent 集成

```bash
# 在 OpenClaw skill 中调用
result=$(alphagbm options score AAPL --strategy sell-put --json)
echo "$result" | jq .
```

---

## 版本

```bash
alphagbm --version
# alphagbm, version 0.1.0
```
