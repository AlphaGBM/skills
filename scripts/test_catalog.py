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
        self.assertEqual([item['name']['zh'] for item in self.catalog['tools'] if item['group'] == 'stocks'],
                         ['股票分析', '高息策略', '市场情绪', '研报查阅', '趋势跟踪', 'ETF策略', '网格计划', '定投计划', '聪明钱跟踪'])
        self.assertEqual(len(self.catalog['tools']), 22)
        builder.validate(self.catalog)

    def test_paths_frontmatter_and_category_counts_agree(self):
        from collections import Counter
        entries = self.catalog['workflows'] + self.catalog['tools']
        self.assertEqual(Counter(item['group'] for item in entries),
                         {'core': 5, 'stocks': 9, 'options': 11, 'commodities': 1, 'digital-assets': 1})
        for item in entries:
            self.assertEqual(item['path'], f"skills/{item['group']}/{item['id']}")
            self.assertIn(f"name: {item['id']}\n", (ROOT / item['path'] / 'SKILL.md').read_text())
            self.assertIn(item['id'], (ROOT / 'demo/CATALOG.md').read_text())

    def test_catalog_rejects_noncanonical_paths(self):
        self.catalog['tools'][0]['path'] = 'skills/alphagbm-stock-analysis'
        with self.assertRaisesRegex(AssertionError, 'canonical path'):
            builder.validate(self.catalog)

    def test_legacy_packages_keep_runners_and_instructions(self):
        for suffix, command in [('research-reader', 'research')]:
            item = next(item for item in self.catalog['tools'] if item['id'] == f'alphagbm-{suffix}')
            self.assertEqual(item['command'], command)
            self.assertEqual(item['status'], 'api')
            self.assertIn(command, (ROOT / item['path'] / 'SKILL.md').read_text())

    def test_all_generated_artifacts_match(self):
        for path, content in builder.outputs(self.catalog).items():
            self.assertEqual((ROOT / path).read_text(), content, path)

    def test_new_packages_are_standalone_and_do_not_need_key_for_help(self):
        import os
        import shutil
        import tempfile
        for item in self.catalog['workflows'] + self.catalog['tools']:
            if item['status'] == 'reference':
                self.assertFalse((ROOT / item['path'] / 'scripts/run.py').exists())
                continue
            command = item.get('command') or builder.COMMANDS[item['id']].split()[0]
            with tempfile.TemporaryDirectory() as workspace:
                directory = Path(workspace) / item['id']
                shutil.copytree(ROOT / item['path'], directory)
                environment = {key: value for key, value in os.environ.items() if not key.startswith('ALPHAGBM_')}
                result = subprocess.run([sys.executable, str(directory / 'scripts/run.py'), command, '--help'],
                                        cwd=workspace, env=environment, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(command, result.stdout)

    def test_local_review_does_not_claim_public_fetch(self):
        content = (ROOT / 'skills/core/alphagbm-investment-review/SKILL.md').read_text()
        self.assertIn('without network access', content)
        self.assertNotIn('This command reads published data', content)

    def test_every_strategy_has_an_explicit_demo_fixture(self):
        expected = {
            'options': 'options-strategy.json',
            'momentum': 'momentum-following.json',
            'etf': 'etf-strategy.json',
            'grid': 'grid-plan.json',
            'dca': 'dca-plan.json',
            'smart_money': 'smart-money.json',
            'dividend': 'dividend-strategy.json',
        }
        for strategy, filename in expected.items():
            path = ROOT / 'demo' / 'strategies' / filename
            self.assertTrue(path.is_file(), filename)
            payload = json.loads(path.read_text())
            self.assertEqual(payload['demo']['status'], 'illustrative_fixture')
            self.assertTrue(payload['demo']['notForTrading'])
            self.assertEqual(payload['strategy'], strategy)
            self.assertIn(payload['status'], ('ready', 'partial'))
            self.assertRegex(payload['resultId'], r'^sha256:[0-9a-f]{64}$')
            self.assertIsInstance(payload['missingData'], list)
            self.assertIsInstance(payload['nextChecks'], list)

    def test_every_focused_package_has_a_real_source_case(self):
        cases = json.loads((ROOT / 'demo/package-cases.json').read_text())
        package_ids = {item['id'] for item in self.catalog['tools'] if item['status'] != 'preview'}
        self.assertEqual(len(cases['cases']), len(package_ids))
        self.assertEqual({item['package'] for item in cases['cases']}, package_ids)
        for case in cases['cases']:
            self.assertIn(case['kind'], ('api', 'reference'))
            self.assertTrue(case['subject'])
            self.assertTrue(case['request'])
            self.assertTrue(case['sources'])
            self.assertTrue(case['expected'])
            self.assertTrue(all(source.startswith('https://') for source in case['sources']))


if __name__ == '__main__':
    unittest.main()
