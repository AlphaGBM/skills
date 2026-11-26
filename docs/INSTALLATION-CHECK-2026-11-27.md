# Project-scoped installation check / 项目级安装实测

This is a maintainer-run installation and client-discovery check, not a user testimonial, paid-workflow result or claim of universal client compatibility.

这是一份维护者实测记录：验证一个技能能安装并被一个客户端发现，不代表研究接口已上线、模型已执行技能或产生真实用户转化。

## Tested configuration

| Item | Observed value |
|---|---|
| Date | 2026-11-27, Asia/Shanghai |
| OS | macOS 26.4.1, arm64 |
| Node.js | 24.22.1 |
| Installer | `skills` 1.9.0 |
| Client | Codex CLI 0.147.0, local app-server discovery |
| Source | `AlphaGBM/skills` |
| Source commit | `c16a96bd2761402b1d827494f1ab82402449047a` |
| Selected Skill | `alphagbm-stock-research` |
| Scope | Project-local; not global |
| Installed location | `.agents/skills/alphagbm-stock-research/` |

The pinned revision includes the synthetic split example but precedes this record. The installation check is for that exact package revision, not whichever version a moving branch serves later.

## Reproduce the installation

Prerequisites: the listed client and Node.js are available on `PATH`; Python 3.9+ is available for the runner's help command. Use a new temporary directory, not your active project or global Skill directory.

```bash
CHECK_ROOT=$(mktemp -d)
mkdir -p "$CHECK_ROOT/project" "$CHECK_ROOT/home/.codex"
git -C "$CHECK_ROOT/project" init -q
cd "$CHECK_ROOT/project"
env -i PATH="$PATH" HOME="$CHECK_ROOT/home" \
  CODEX_HOME="$CHECK_ROOT/home/.codex" \
  DISABLE_TELEMETRY=1 DO_NOT_TRACK=1 CI=1 \
  npm_config_cache="$CHECK_ROOT/npm-cache" \
  npx --yes skills@1.9.0 add \
  https://github.com/AlphaGBM/skills/tree/c16a96bd2761402b1d827494f1ab82402449047a \
  --skill alphagbm-stock-research --agent codex --yes
```

Observed: the installer found 28 packages, selected exactly one, and copied it into the project-local directory above. `skills-lock.json` recorded the requested commit and Skill path. All six installed package files matched that pinned source byte-for-byte. A separate temporary installation with Codex's bundled GitHub Skill installer also matched those six files; neither installation touched the user's global Skills.

Installation used public GitHub/npm downloads. No AlphaGBM API key, login, market-data request or paid analysis was used.

## Verify actual client discovery

With the same isolated `HOME` and `CODEX_HOME`, start `codex app-server --stdio` from the temporary project. In this check the process ran under macOS `sandbox-exec` with `(version 1) (allow default) (deny network*)`; discovery was offline, not just assumed to be offline.

Send these JSON-lines messages in order, waiting for the initialize response before continuing. Replace the absolute project-path placeholder with the directory created above:

```json
{"id":1,"method":"initialize","params":{"clientInfo":{"name":"alphagbm-install-check","version":"1.0"},"capabilities":{"experimentalApi":true}}}
{"method":"initialized","params":{}}
{"id":2,"method":"skills/list","params":{"cwds":["<absolute temporary project path>"],"forceReload":true}}
```

Observed for the selected Skill: `name=alphagbm-stock-research`, `enabled=true`, `scope=repo`, path ending in `.agents/skills/alphagbm-stock-research/SKILL.md`; the project error list was empty. This checks the client's own discovery, not merely the existence of a copied file.

The bundled command below also exited successfully with usage text while network access was denied and no AlphaGBM credentials were present:

```bash
python3 .agents/skills/alphagbm-stock-research/scripts/run.py stock --help
```

No conversation, model turn or research command was submitted. Stop the app-server after receiving the discovery response. To clean up, remove only the temporary directory created at the start; do not delete or replace any global Skill/configuration directory.

## Additional repositories / 另外两仓

Two separate empty projects were also checked with the same isolated Codex CLI 0.147.0 setup. These do not add packages to the Skills catalogue.

| Repository and pinned revision | Installation | Actual client discovery |
|---|---|---|
| `AlphaGBM/investment-masters` at `30e239c6fa04f2ed97f5859c44d4f74040016926` | `skills` 1.9.0, `--skill investment-masters --agent codex --yes`, project-local | `investment-masters`, enabled, `scope=repo`, no discovery errors |
| `AlphaGBM/alphagbm-trading-skills` at `a0ecd079ab55a2db658608b42c13dd51aec1164c` | Copy all 13 `gbm*` directories and `_shared` into a fresh project's `.agents/skills/` | All 13 names discovered and enabled with `scope=repo`; no discovery errors |

For Investment Masters, repeat the isolated installer command with source `https://github.com/AlphaGBM/investment-masters/tree/30e239c6fa04f2ed97f5859c44d4f74040016926` and `--skill investment-masters`. For Trading Skills, preserve `_shared` as a sibling of the 13 Skill directories; do not assume an installer copying only one directory preserves these shared references. The Trading README includes an isolated-copy example.

The Trading names observed were `gbm`, `gbm-benchmark`, `gbm-coach`, `gbm-deconstruct`, `gbm-diagnosis`, `gbm-event-attribution`, `gbm-market-research`, `gbm-model`, `gbm-report`, `gbm-research`, `gbm-restore`, `gbm-save` and `gbm-trade`. The `_shared` directory is a dependency, not a 14th Skill.

这两仓也只验证同一客户端的项目级安装与发现，不验证模型执行效果、复盘质量、实时数据或交易能力。所有发现检查均禁止网络，没有提交模型任务。

## Limits / 未验证的范围

- This does not verify model reasoning, actual research output, live backend compatibility, account entitlements or billing.
- This does not verify Claude Code, Cursor, a graphical client, global installation, upgrades or other operating systems.
- The installed Skill explicitly describes its structured backend workflow as a release preview; successful installation does not change that status.
- 本次只确认安装、客户端发现及离线帮助命令；没有执行收费研究，也没有把合成示例当成真实调用结果。

See [installation and update guidance](INSTALLATION.md), [access boundaries](ACCESS.md) and the [community guide](COMMUNITY.md). If your client/version behaves differently, report the versions and redacted steps rather than retrying paid research.
