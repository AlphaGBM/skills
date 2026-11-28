import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CommunityTests(unittest.TestCase):
    def test_shared_guide_distinguishes_new_reports_from_existing_threads(self):
        content = (ROOT / 'docs/COMMUNITY.md').read_text()
        self.assertIn('Send all new questions and bug reports through the entries below', content)
        self.assertIn('If an issue already exists, continue in its original thread', content)
        self.assertIn('所有新问题与缺陷', content)
        self.assertIn('若已有对应 Issue，请在原帖继续', content)
        self.assertNotIn('属于某仓文件的具体缺陷可以留在该仓跟踪', content)

    def test_contribution_templates_exist(self):
        content = '\n'.join((ROOT / filename).read_text() for filename in
                            ['CONTRIBUTING.md', 'docs/COMMUNITY.md'])
        templates = set(re.findall(r'issues/new\?template=([a-z_]+\.yml)', content))
        self.assertEqual(templates, {'install.yml', 'bug_report.yml', 'skill_proposal.yml', 'documentation.yml'})
        self.assertFalse(list((ROOT / '.github/ISSUE_TEMPLATE').glob('*.md')))
        for filename in templates:
            template = (ROOT / '.github/ISSUE_TEMPLATE' / filename).read_text()
            for field in ('name:', 'description:', 'title:', 'labels:', 'body:'):
                self.assertRegex(template, rf'(?m)^{field}')
            self.assertIn('needs-triage', template)
            self.assertIn('Do not post secrets or personal data', template)
            self.assertNotIn('assignees:', template)
            fields = re.findall(r'^    id: (.+)$', template, re.MULTILINE)
            self.assertEqual(len(fields), len(set(fields)))
            self.assertEqual(len(fields), 3)
            self.assertLessEqual(template.count('required: true'), 3)

    def test_optional_suggestions_and_welcome_link(self):
        for filename, field in [('documentation.yml', 'suggestion'), ('skill_proposal.yml', 'constraints')]:
            template = (ROOT / '.github/ISSUE_TEMPLATE' / filename).read_text()
            self.assertIn('required: false', template.split(f'id: {field}', 1)[1])
        chooser = (ROOT / '.github/ISSUE_TEMPLATE/config.yml').read_text()
        self.assertIn('blank_issues_enabled: false', chooser)
        self.assertIn('https://github.com/AlphaGBM/skills/discussions/21', chooser)
        self.assertIn('https://github.com/AlphaGBM/skills/discussions/categories/q-a', chooser)

    def test_both_readmes_expose_community_and_example_boundaries(self):
        for filename in ['README.md', 'docs/README.zh.md']:
            content = (ROOT / filename).read_text()
            self.assertIn('https://github.com/AlphaGBM/skills/discussions', content)
            self.assertIn('https://github.com/AlphaGBM/skills/discussions/21', content)
            self.assertIn('https://github.com/AlphaGBM/skills/issues/new/choose', content)
            self.assertIn('demo/stock-opportunities.json', content)
        self.assertIn('not live market data', (ROOT / 'README.md').read_text())
        self.assertIn('不是实时行情', (ROOT / 'docs/README.zh.md').read_text())
        self.assertIn('not a 74% win rate', (ROOT / 'README.md').read_text())
        self.assertIn('不代表 74% 胜率', (ROOT / 'docs/README.zh.md').read_text())
        for filename in ['README.md', 'docs/README.zh.md']:
            content = (ROOT / filename).read_text()
            for repository in ['investment-masters', 'alphagbm-trading-skills']:
                self.assertIn(f'https://github.com/AlphaGBM/{repository}', content)

    def test_local_document_links_resolve(self):
        for filename in ['README.md', 'docs/README.zh.md', 'docs/COMMUNITY.md', 'CONTRIBUTING.md',
                         'docs/INSTALLATION.md', 'docs/INSTALLATION-CHECK-2026-11-27.md',
                         'docs/INSTALLATION-FIRST-USE-2026-11-27.md', 'docs/DOUBAO.md']:
            document = ROOT / filename
            for target in re.findall(r'\]\(([^)]+)\)', document.read_text()):
                if '://' in target or target.startswith('#'):
                    continue
                self.assertTrue((document.parent / target.split('#', 1)[0]).exists(),
                                f'{filename}: {target}')


if __name__ == '__main__':
    unittest.main()
