import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('catalog_builder', ROOT / 'scripts/build_catalog.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / 'catalog/catalog.json').read_text())

    def test_approved_names_and_order(self):
        self.assertEqual([item['name']['zh'] for item in self.catalog['workflows']],
                         ['股票机会', '期权策略', '新闻影响', '研报拆解', '投资复盘'])
        self.assertEqual([item['command'] for item in self.catalog['workflows']],
                         ['stock', 'options', 'news', 'report', 'review'])
        builder.validate(self.catalog)

    def test_legacy_packages_keep_runners_and_instructions(self):
        for suffix, command in [('opportunity-radar', 'radar'), ('research-reader', 'research'), ('thesis-check', 'verify')]:
            item = next(item for item in self.catalog['tools'] if item['id'] == f'alphagbm-{suffix}')
            self.assertEqual(item['command'], command)
            self.assertEqual(item['status'], 'api')
            self.assertIn(command, (ROOT / 'skills' / item['id'] / 'SKILL.md').read_text())

    def test_all_generated_artifacts_match(self):
        for path, content in builder.outputs(self.catalog).items():
            self.assertEqual((ROOT / path).read_text(), content, path)

    def test_new_packages_are_standalone_and_do_not_need_key_for_help(self):
        for suffix, command in [('news-impact', 'news'), ('report-breakdown', 'report'), ('investment-review', 'review')]:
            directory = ROOT / 'skills' / f'alphagbm-{suffix}'
            result = subprocess.run([sys.executable, str(directory / 'scripts/run.py'), command, '--help'],
                                    cwd='/tmp', capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(command, result.stdout)

    def test_local_review_does_not_claim_public_fetch(self):
        content = (ROOT / 'skills/alphagbm-investment-review/SKILL.md').read_text()
        self.assertIn('without network access', content)
        self.assertNotIn('This command reads published data', content)


if __name__ == '__main__':
    unittest.main()
