# Installation, updates and version checks

## Install from the repository

```bash
npx skills add AlphaGBM/skills --skill alphagbm-stock-research
```

Choose the workspace/client in the installer. Repeat with another package ID
from `catalog/catalog.json`. Installing the open-source package does not grant
paid data access; use your own AlphaGBM account and its existing allowance.

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
