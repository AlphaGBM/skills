# Contributing to AlphaGBM Skills

Thanks for your interest in contributing! AlphaGBM Skills is open source and we welcome contributions from the community.

## Ways to Contribute

### Report Bugs

Found something broken? [Open an issue](https://github.com/AlphaGBM/skills/issues/new?template=bug_report.md) with:

- Which skill is affected
- What you asked your AI agent to do
- What happened vs. what you expected
- Your environment (Claude Code / Cursor / other)

### Propose a New Skill

Have an idea for a new skill? [Open a proposal](https://github.com/AlphaGBM/skills/issues/new?template=skill_proposal.md) with:

- **What it does** -- one sentence
- **Example queries** -- 3-5 things a user might ask
- **Data needed** -- what market data does it require?
- **Mock data plan** -- can you provide realistic sample output?

We'll discuss feasibility and design before you start coding.

### Add Mock Data

Every skill ships with built-in demo data so users can try it without an API key. To add mock data for a new ticker:

1. Pick a ticker not already covered (current: AAPL, NVDA, SPY, TSLA, META)
2. Add realistic JSON data to `mock-data/<TICKER>/`
3. Follow the existing format -- see `mock-data/AAPL/` for reference
4. Include: stock quote, options chain (at least 2 expirations), IV history
5. All numbers must be realistic and internally consistent

### Improve Existing Skills

Each skill lives in `skills/<skill-name>/` and contains:

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
5. **Be patient** -- we review PRs within a few days

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

# No build step needed -- skills are plain Markdown + JSON
# Just point your AI agent at the skills directory

# For Claude Code
cp -r skills/ /path/to/your/project/.claude/skills/alphagbm/

# For Cursor
cp -r skills/ /path/to/your/project/.cursor/skills/alphagbm/
```

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold a welcoming, respectful environment for everyone.

## Questions?

- [Discord](https://discord.gg/alphagbm) -- fastest way to get help
- [GitHub Discussions](https://github.com/AlphaGBM/skills/discussions) -- longer-form questions
- [Twitter/X](https://x.com/alphagbm) -- announcements and updates

---

Thank you for helping make options & research intelligence accessible to everyone.
