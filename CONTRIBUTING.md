# Contributing to AlphaGBM Skills

Thanks for your interest in contributing! AlphaGBM Skills is open source and we welcome contributions from the community.

## Ways to Contribute

### Report Bugs

Found something broken? Check existing issues, then [open an issue](https://github.com/AlphaGBM/skills/issues/new?template=bug_report.yml) with:

- Which skill is affected
- What you asked your AI agent to do
- What happened vs. what you expected
- Your environment (Claude Code / Cursor / other)

Include the installed commit, installer/runtime versions and a minimal redacted reproduction. Unknown versions are fine. Do not retry a potentially charged request just to produce evidence. Use the [installation form](https://github.com/AlphaGBM/skills/issues/new?template=install.yml) if following the docs failed; use [Q&A](https://github.com/AlphaGBM/skills/discussions/categories/q-a) for how-to questions.

### Propose a New Skill

Have a concrete improvement or new skill in mind? [Open a proposal](https://github.com/AlphaGBM/skills/issues/new?template=skill_proposal.yml) with:

- **What it does** -- one sentence
- **Desired result** -- the behavior or an explicitly synthetic example
- **Optional context** -- known data/access needs, safe tests or how you could help; unknowns are fine

We'll discuss feasibility and design before you start coding.

### Add Mock Data

Samples are optional and must be explicitly requested and labelled. Workflow runners never replace a failed or unauthenticated request with sample data. To propose a dated sample for a ticker:

1. Pick a ticker not already covered (current: AAPL, NVDA, SPY, TSLA, META)
2. Add realistic JSON data to `mock-data/<TICKER>/`
3. Follow the existing format -- see `mock-data/AAPL/` for reference
4. Include: stock quote, options chain (at least 2 expirations), IV history
5. All numbers must be realistic and internally consistent

### Improve Existing Skills

Each skill lives at its canonical `path` in `catalog/catalog.json`, under `skills/<category>/<skill-name>/`, and contains:

- `SKILL.md` -- the skill definition (what the AI reads)
- `examples/` -- example queries and expected outputs
- `mock-data/` -- symlinks or references to shared mock data

To improve a skill:

1. Fork the repo and create a branch: `git checkout -b improve/<skill-name>`
2. Edit the skill files
3. Test with your AI agent (Claude Code or Cursor)
4. Submit a PR with before/after examples

## Pull Request Process

1. **Fork & branch** -- create a feature branch from `main`
2. **Keep it focused** -- one skill or one fix per PR
3. **Test it** -- verify the skill works in at least one AI agent
4. **Describe it** -- explain what changed and why in the PR description
5. **Describe the verification boundary** -- state what was actually tested; review timing depends on maintainer availability

### PR Checklist

- [ ] Skill output is accurate and verifiable
- [ ] Mock data is realistic (not random numbers)
- [ ] SKILL.md follows the existing format
- [ ] No API keys, secrets, or personal data included
- [ ] Tested in at least one AI agent environment

## Development Setup

```bash
# Clone the repo
git clone https://github.com/AlphaGBM/skills.git
cd skills

python3 scripts/build_catalog.py
python3 scripts/build_catalog.py --check
npx skills add . --list
```

The catalogue and shared runner are the editable sources. Generated workflow documents, scripts and directory pages must match them. Reference-only packages must not claim live API access; adding an interface requires an access contract and failure/usage checks. Install a selected local package into an isolated test project before testing the client; never overwrite a contributor's global AI configuration.

## Code of Conduct

Be respectful, discuss evidence rather than people, and avoid spam, harassment and unsolicited promotion. Do not publish secrets, personal account information or restricted research. See the [community guide](docs/COMMUNITY.md) for routing and safe examples.

## Questions?

- [GitHub Discussions](https://github.com/AlphaGBM/skills/discussions) -- setup questions and workflow ideas in English or Chinese
- [Issue chooser](https://github.com/AlphaGBM/skills/issues/new/choose) -- reproducible bugs, documentation gaps and scoped proposals

---

Thank you for helping make options & research intelligence accessible to everyone.
