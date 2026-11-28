# Installation, updates and version checks

## WorkBuddy: local skill directory and explicit invocation

See the [WorkBuddy installation and first-use guide](WORKBUDDY.md). A user report records CodeBuddy CLI 2.184.0 in WorkBuddy loading `alphagbm-stock-research` from `~/.codebuddy/skills/` through its Skill tool, then executing the bundled offline demo. The guide pins the tested source commit and stops rather than overwriting an existing installation. Automatic activation, cross-session persistence, other packages and live/paid research remain unverified. This is a host-directory route, not a verified third-party installer target; no separate Codex installation is needed.

## Doubao Work: native import or a file workflow

See the [Chinese Doubao guide and portable package](DOUBAO.md). This route uses the existing Causal Research method and the current host's own tools, not a nested Codex installation. Do not invent an installer `--agent` target or equate downloading files with registering a skill. Native import and cross-session discovery remain unverified; the file workflow is explicitly scoped to the current session. No AlphaGBM account access is included.

## Install from the repository

```bash
npx skills@1.9.0 add AlphaGBM/skills --skill alphagbm-stock-research --agent codex --copy -y
```

Use an already-installed AI client. This command selects project-local Codex;
replace `codex` with `claude-code` or `cursor` for your intended client. Do not
omit `--agent` in an unattended install: the installer may target many clients.
Codex and Cursor use `.agents/skills`; Claude Code uses `.claude/skills` in
installer 1.9.0. A missing `.codex` or `.cursor` project directory is not an error.
Repeat with another package ID from `catalog/catalog.json`. Installing the open-source package does not grant
paid data access; use your own AlphaGBM account and its existing allowance.

For a reproducible project-local example, see the [2026-11-27 installation check](INSTALLATION-CHECK-2026-11-27.md): `skills` 1.9.0 installed one pinned package and Codex CLI 0.147.0 discovered it without a model or research request. This is one tested client/version, not universal compatibility or live-backend validation.

中文：这份[安装实测记录](INSTALLATION-CHECK-2026-11-27.md)包含隔离目录、固定版本、实际安装位置及客户端发现结果；没有使用研究额度，不代表所有客户端都已验收。

## First use without an account or research allowance

See the [installed-package and offline first-use check](INSTALLATION-FIRST-USE-2026-11-27.md)
for the six targeted installations, actual Codex discovery, demo execution and limits.

```bash
python3 .agents/skills/alphagbm-stock-research/scripts/demo.py --lang en
```

For Claude Code, change `.agents` to `.claude`. The script and synthetic fixture
are both inside the installed package; no repository clone, extra download or API
key is needed. Python 3.9+ is required. It computes the one-share-to-four-shares
split example from decimal inputs, keeps unknown bases unknown, and labels the
JSON as synthetic and not for trading. Missing or invalid assets fail with
`DEMO_UNAVAILABLE`; the script never falls back to a live research request.

In your AI client, explicitly ask: “Use AlphaGBM's offline synthetic stock-split
demo; do not access the network or use research allowance.” The client should
read the skill, run `scripts/demo.py`, and explain its actual output. Installer
listing alone is not proof that the AI client discovered or executed the skill.

中文：先用已安装的 AI 客户端运行包内离线合成演示，不需要 Key、联网或研究额度。
它不是实时行情或收费研究的替代品；只有用户明确要求演示时才运行。真实研究仍需
单独授权额度，而且结构化工作流的生产后端尚未核验，不能承诺配置 Key 就能跑通。

## Updating a local-source installation

A local directory is a snapshot, not an upstream subscription. Do not assume
`skills update` can discover its repository or refresh every client installation.
Re-run the repository install command above for each intended client. If you must
use a local checkout, update that checkout first, then repeat the same local
installation procedure. Preserve your private configuration outside the Skill.

After reinstalling, check the selected client's actual installed `SKILL.md`, its
bundled `scripts/run.py`, and the relative `references/` links. A global and a
project-local install can coexist: check which one the client is resolving.
Do not delete other Skills or copy API keys into any lockfile.

## Reproducible local checkout

```bash
git clone https://github.com/AlphaGBM/skills.git
cd skills
git rev-parse HEAD
python3 -c 'import json; c=json.load(open("catalog/catalog.json")); print(c["version"], len(c["workflows"])+len(c["tools"]))'
```

Record the repository URL, the printed commit and catalogue version, package ID,
installer version, chosen client and project/global scope in your own deployment
notes. Use a reviewed commit for reproducible rollouts, not an unrecorded moving
branch. The website separately pins its catalogue revision.

The third-party installer owns `skills-lock.json`; AlphaGBM does not add custom
fields to it or promise that restoring it rebuilds both `.agents/skills` and
`.claude/skills`. Verify the actual selected directories after restore, and
reinstall missing clients. For a bug report, include the command, installer
version and installed commit, never the API key.

中文：本地目录安装不会自动获得远端更新。升级时重新执行仓库安装，并确认客户端与
项目/全局范围。锁文件由第三方安装器管理，不能只凭它存在就认为所有工具目录均已恢复。
保留版本号与实际安装路径，不要将 API Key 放进仓库、提示词或锁文件。
