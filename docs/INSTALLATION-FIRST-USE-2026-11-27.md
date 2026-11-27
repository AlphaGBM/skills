# Installation and offline first-use check — 2026-11-27

This is a maintainer-run check, not a user testimonial or evidence that live
research works. It follows the earlier [installation check](INSTALLATION-CHECK-2026-11-27.md)
and covers the new self-contained packages and explicit synthetic demo.

## Versions and source revisions

- macOS 26.4.1 arm64; Node 24.22.1; Python 3.11.6.
- Installer: `skills` 1.9.0; Codex CLI 0.147.0.
- Skills package revision: `b1606ebe47390e057fe0c9d1ac43d6bc37393c46`.
- Trading package revision: `be9e67e1966e4eae11c1657c959c6eece841238d`.

These revisions precede this record. Later documentation-only changes are not
silently treated as a fresh install; the merge receipts include a separate check
that the installed package trees match the final default branches.

## Actual installations

Six separate Git projects, initially empty, used an isolated HOME and npm cache.
Stock copies were refreshed after hardening malformed-fixture handling, then all
installed bytes and checks were revalidated against the final revision. No global
client configuration or AlphaGBM key was supplied. Each install specified exactly
one agent target and used `--copy`; none created directories for unrelated agents.
Installer downloads use the network; the demo and Codex discovery checks below
ran with OS-enforced network denial.

| Package | Installer target | Skill directory | Installed skills | Files matching pinned source |
|---|---|---|---:|---:|
| Stock Research | `codex` | `.agents/skills` | 1 | 8 |
| Stock Research | `claude-code` | `.claude/skills` | 1 | 8 |
| Stock Research | `cursor` | `.agents/skills` | 1 | 8 |
| Trading | `codex` | `.agents/skills` | 13 | 16 |
| Trading | `claude-code` | `.claude/skills` | 13 | 16 |
| Trading | `cursor` | `.agents/skills` | 13 | 16 |

All six commands exited 0. Each lockfile identified the corresponding exact source
commit. Every tracked package file was compared byte-for-byte with that commit.
Local Markdown links resolved within the installed package. Trading discovery
reported 13 skills, not 14; `gbm-example` was absent. Both protocol files were
present inside their consuming packages, without any top-level `_shared` folder:

- `gbm-research/references/shared/evidence-standards.md`
- `gbm-event-attribution/references/shared/event-attribution.md`

Reproduce in a fresh project with an isolated HOME. Choose one target; substitute
`claude-code` or `cursor` only if that is your intended client:

```bash
npx --yes skills@1.9.0 add https://github.com/AlphaGBM/skills/tree/b1606ebe47390e057fe0c9d1ac43d6bc37393c46 --skill alphagbm-stock-research --agent codex --copy -y
```

In a different empty project:

```bash
npx --yes skills@1.9.0 add https://github.com/AlphaGBM/alphagbm-trading-skills/tree/be9e67e1966e4eae11c1657c959c6eece841238d --skill '*' --agent codex --copy -y
```

## Client discovery and agent execution are separate checks

Actual Codex `app-server --stdio` discovery returned Stock Research and all 13
Trading skills as `enabled: true`, `scope: repo`, with an empty error list. This
used `initialize`, `initialized`, then `skills/list` with the project cwd and
`forceReload: true`, not the installer's own listing command. The temporary
`CODEX_HOME` directory must exist before starting the client. No model request
was submitted through this discovery process.

A separate fresh-context agent received only the installed Stock Research skill
path and the request below, not expected numeric answers, source code or test
results:

> 用 AlphaGBM 跑一次离线合成拆股演示，不联网、不消耗研究额度，并解释结果和未知项。

The agent read the installed instructions, ran the bundled command, and explained
its actual output, including the unknown-basis case. The local command was:

```bash
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' env -i PATH="$PATH" python3 -I -B .agents/skills/alphagbm-stock-research/scripts/demo.py --lang zh
```

Exit code: **0**. Selected actual JSON fields:

```json
{
  "mode": "synthetic_demo",
  "synthetic": true,
  "notForTrading": true,
  "notLiveQuote": true,
  "notInvestmentRecommendation": true,
  "notPaidWorkflowEvidence": true,
  "splitRatio": "4",
  "earlierNormalizedTarget": "30",
  "laterTarget": "27",
  "splitOnlyChangePercent": "0",
  "laterChangePercent": "-10",
  "incorrectMixedBasisChangePercent": "-77.5",
  "unknownTarget": {
    "value": "25",
    "status": "unknown",
    "normalizedValue": null,
    "sameBasisChangePercent": null
  }
}
```

The same demo command also exited 0 from the Claude Code and Cursor installation
directories under network denial. That validates the installed files and Python
command, **not** execution inside those two AI clients. The fresh-agent run and
Codex discovery are separate observations, not a claim that a model turn ran
through the tested app-server session.

## Safety and regression checks

- A one-old-share-to-four-new-shares split turns 120 per old share into 30 per
  new share, not a downgrade. A later 27 on that basis is a 10% reduction.
- The script computes from raw decimal inputs rather than copying the fixture's
  expected answers. Unknown bases remain unknown; no ratio is inferred.
- Tests cover mutated inputs, synthetic-data flags, non-finite numbers, missing
  assets, package-only execution and generated-file consistency.
- In each Stock Research installation, a `run.py stock NVDA --workflow --lang zh`
  request without approval exited 1 with `CONFIRM_USAGE` on stderr under network
  denial. The allowance guard remains intact; no paid request was made.
- Local suites passed: 109 Skills tests and 18 Trading tests, both under network
  denial. Catalogue generation, protocol bundling and Trading privacy checks passed.

## What this does not establish

No live quote, account-backed research, strategy performance, paid backend or
production deployment was validated. The structured stock workflow remains a
release preview. There is no automatic demo fallback when real research fails.
Claude Code and Cursor model execution, graphical clients, global installation,
and other operating systems remain outside this check.

中文：本轮证明指定客户端安装不会铺开到无关目录、Trading 包内依赖完整、模板不被
误装、离线演示可从安装目录直接运行。Codex 发现与独立代理执行分别记录，不冒充
Claude/Cursor 对话验收，也不证明收费研究可用。合成演示不消耗 AlphaGBM 研究额度；
这不代表宿主模型服务本身免费。
