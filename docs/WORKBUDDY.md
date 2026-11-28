# 在 WorkBuddy 中使用 AlphaGBM

**Stock Research 已有用户实测：按 WorkBuddy 宿主技能目录安装、通过 Skill 工具显式加载，并成功运行随包离线演示。** 不需要另装 Codex，不需要 AlphaGBM API Key 即可体验这个演示。

这里记录的是一套已实测的客户端与技能版本，不承诺所有 WorkBuddy 版本或所有 AlphaGBM 技能均已验收。先安装、显式调用即可使用；自动触发不是这条上手路径的前提。

## 实测范围

来源：2026-11-28 收到的用户文字测试报告。以下宿主与隔离执行结果由该报告记录，维护者未登录对方云电脑；本文不公开私人会话、原始环境变量或完整日志。

| 项目 | 报告记录 |
|---|---|
| 客户端 | WorkBuddy 云电脑，CodeBuddy CLI `2.184.0`，环境标识 `CloudAgent` / `WorkBuddy_APP` |
| 系统 | Ubuntu 24.04.3、Python 3.11.1 |
| 技能 | `alphagbm-stock-research`，完整 8 文件 |
| 固定源版本 | `2687f5dd37a0ff0a214801737aa2d4d1a2b38a8d`，不是“当前最新版本”的承诺 |
| 安装目录 | 当前宿主用户的 `~/.codebuddy/skills/alphagbm-stock-research/` |
| 宿主加载 | Skill 工具返回安装目录并注入 `SKILL.md`，不是单纯手动读文件 |
| 实际执行 | Agent 按技能指令通过终端运行包内 `scripts/demo.py --lang zh`；退出码 0、stderr 空 |
| 离线边界 | 报告记录 `unshare -n` 隔离及同一命名空间网络探针，脚本以 `env -i` 清空环境执行；这不代表宿主模型推理全程离线 |

**已验：目录安装、显式宿主加载、随包合成演示。未验：自动上下文触发、跨会话持久性、真实行情或付费研究接口、其他技能。** 不把演示成功当作线上研究验收；不要求为了体验演示先配置密钥。

## 1. 在 WorkBuddy 自己的云电脑安装

下面是 Linux 云电脑的固定发布版本安装命令，需要 Git 和 Python 3.9+。`skills-onboarding-v1` 增加了[简短双语介绍](INTRODUCTION.md)，未改变演示脚本；表中的用户宿主实测仍以原commit为准，新版宿主行为未单独实测。先确认你当前客户端确实使用 `~/.codebuddy/skills/`；路径不同就按其实际机制处理，不创建猜测的目录冒充安装成功。

命令只操作当前宿主用户的技能目录。目标已存在（包括符号链接）就停止，不覆盖你的旧技能或配置。下载目录通过 `mktemp` 新建并保留用于核对；失败时停止，不混用 tarball 和 clone 目录。

```bash
set -eu
version=skills-onboarding-v1
destination="$HOME/.codebuddy/skills/alphagbm-stock-research"
if [ -e "$destination" ] || [ -L "$destination" ]; then
  printf '%s\n' '目标技能已存在；先核对版本，不覆盖。' >&2
  exit 1
fi
workdir=$(mktemp -d)
git clone https://github.com/AlphaGBM/skills.git "$workdir/skills"
git -C "$workdir/skills" checkout --detach "$version"
commit=$(git -C "$workdir/skills" rev-parse "$version^{commit}")
test "$(git -C "$workdir/skills" rev-parse HEAD)" = "$commit"
source_dir="$workdir/skills/skills/core/alphagbm-stock-research"
test -f "$source_dir/SKILL.md"
test -f "$source_dir/scripts/demo.py"
test -f "$source_dir/assets/stock-split-basis.json"
mkdir -p "$HOME/.codebuddy/skills"
cp -a "$source_dir" "$destination"
diff -r "$source_dir" "$destination"
printf '源版本：%s\n安装目录：%s\n源副本：%s\n' "$commit" "$destination" "$source_dir"
```

这里采用用户实测的目录安装方式。本仓库现有 `npx skills@1.9.0` 示例覆盖 Codex、Claude Code、Cursor，**未据此验证该第三方安装器的 WorkBuddy 路径**；不要把指南未列出某目标，推断成上游一定不支持，也不要猜测一个 `--agent` 参数。

若要严格复现原用户报告，将命令中的`version`改为`2687f5dd37a0ff0a214801737aa2d4d1a2b38a8d`；那一版不含新的品牌介绍。安装新版不会自动替换现有技能，命令仍会先停止，请先核对并保留已有目录。

## 2. 让 WorkBuddy 显式调用技能

回到 WorkBuddy 对话中发送：

```text
请通过你自身的技能调用入口显式加载 alphagbm-stock-research，确认实际解析到的技能目录。
然后按技能指令运行包内离线合成拆股演示，使用中文输出。
不要安装或调用其他AI客户端，不使用API Key，不执行run.py stock，不调用付费研究或消耗AlphaGBM额度。
请保留实际命令、退出码和原始JSON，并说明这是合成演示，不是真实行情或投资建议。
如果技能入口未发现它，请如实报告，不用手动读文件冒充宿主加载成功。
```

报告中的宿主在安装后支持显式 Skill 调用，但会话启动时的静态清单没有自动更新。如果你的版本找不到，可按客户端实际提供的刷新方式或新会话再查；这只是排障步骤，不是已验证的跨会话持久性承诺。仍未发现就反馈客户端版本、实际目录和原始错误，不另外安装 Codex 来代测。

**Agent 加载技能后调用终端执行脚本，是本包的正常使用方式。** 不需要额外 hook、MCP server 或自动执行器；`SKILL.md` 提供工作指令，脚本负责确定性计算。仅终端运行成功则只证明脚本可运行，不证明宿主加载成功。

## 3. 看见什么算成功

先看到宿主技能加载记录，再看到随包脚本实际执行回执。该固定版本演示应包含：

- `mode: synthetic_demo`，`synthetic: true`，非交易、非行情、非投资建议、非付费工作流证据标记。
- 拆股前 120 按 4-for-1 归一化为 30；纯拆股变化为 0%。
- 后期目标 27，对同口径 30 的变化为 −10%；错误混用 120 与 27 会得到 −77.5%。
- 缺少拆股口径的目标保留 `unknown`，归一化值和同口径变化为 `null`。

不要把文档中的预期值复制成运行回执。下载需要网络；演示脚本不需要网络，宿主模型和工具服务仍可能需要联网或有费用。`unshare -n` 是此次报告环境的验证方法，不是所有用户必须具备的安装条件；若无隔离权限，就明确未验证强制断网，不修改平台安全限制。

## 排障、升级与反馈

- 下载 TLS 抖动：保留错误，可有限重试或尝试单次 `git -c http.version=HTTP/1.1 clone ...`；不关闭 TLS 校验，不改全局 Git 设置。一次成功不能证明某个参数就是根因修复。
- 若另用 GitHub 归档下载，放在不同的新目录，独立核对固定提交及文件；不要解压到已有 clone 中制造混合副本。
- 更新本地复制的技能不是自动订阅上游。先核对并保留已有目录和私有配置，重新取得所选版本，再经你确认替换；不要删除其他技能或把密钥放进包内。新版与其他包需要分别验证，不能沿用本页的固定版本结论。
- 安装问题走[安装反馈入口](https://github.com/AlphaGBM/skills/issues/new?template=install.yml)，使用问题走[社区指南](COMMUNITY.md)。仅提供脱敏命令、错误、版本和实际路径类型，不上传密钥、完整环境变量或私人材料。

要研究真实公司，请另看[权限与使用边界](../skills/core/alphagbm-stock-research/references/access.md)；本页没有验证收费端点，不能承诺配置 Key 即可使用。豆包用户请走[豆包工作入口](DOUBAO.md)，不要混同两个宿主或两个技能的验收范围。
