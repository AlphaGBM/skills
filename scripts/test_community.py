import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CommunityTests(unittest.TestCase):
    def test_contribution_templates_exist(self):
        content = '\n'.join((ROOT / filename).read_text() for filename in
                            ['CONTRIBUTING.md', 'docs/COMMUNITY.md'])
        templates = set(re.findall(r'issues/new\?template=([a-z_]+\.md)', content))
        self.assertEqual(templates, {'bug_report.md', 'skill_proposal.md', 'documentation.md'})
        for filename in templates:
            template = (ROOT / '.github/ISSUE_TEMPLATE' / filename).read_text()
            self.assertTrue(template.startswith('---\n'))
            for field in ('name:', 'about:', 'title:', 'labels:'):
                self.assertIn(field, template.split('---', 2)[1])
            self.assertIn('## ', template)

    def test_both_readmes_expose_community_and_example_boundaries(self):
        for filename in ['README.md', 'docs/README.zh.md']:
            content = (ROOT / filename).read_text()
            self.assertIn('https://github.com/AlphaGBM/skills/discussions', content)
            self.assertIn('https://github.com/AlphaGBM/skills/issues/new/choose', content)
            self.assertIn('demo/stock-opportunities.json', content)
        self.assertIn('not live market data', (ROOT / 'README.md').read_text())
        self.assertIn('不是实时行情', (ROOT / 'docs/README.zh.md').read_text())

    def test_local_document_links_resolve(self):
        for filename in ['README.md', 'docs/README.zh.md', 'docs/COMMUNITY.md', 'CONTRIBUTING.md']:
            document = ROOT / filename
            for target in re.findall(r'\]\(([^)]+)\)', document.read_text()):
                if '://' in target or target.startswith('#'):
                    continue
                self.assertTrue((document.parent / target.split('#', 1)[0]).exists(),
                                f'{filename}: {target}')


if __name__ == '__main__':
    unittest.main()
