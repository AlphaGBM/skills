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
                         ['股票机会', '期权策略', '新闻影响', '研报拆解', '投资复盘', '趋势跟踪', 'ETF策略', '网格计划', '定投计划', 'Smart Money跟踪'])
        self.assertEqual([item['command'] for item in self.catalog['workflows']],
                         ['stock', 'options', 'news', 'report', 'review', 'momentum', 'etf', 'grid', 'dca', 'smart-money'])
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


if __name__ == '__main__':
    unittest.main()
