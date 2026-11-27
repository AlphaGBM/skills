from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'skills/core/alphagbm-stock-research'
SPEC = importlib.util.spec_from_file_location('stock_split_demo', ROOT / 'runtime/stock_split_demo.py')
demo = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(demo)


class StockSplitDemoTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads((ROOT / 'demo/stock-split-basis.json').read_text())

    def test_computes_normalization_and_preserves_unknown(self):
        result = demo.evaluate(self.fixture)
        self.assertEqual(result['earlierNormalizedTarget'], '30')
        self.assertEqual(result['laterTarget'], '27')
        self.assertEqual(result['splitOnlyChangePercent'], '0')
        self.assertEqual(result['laterChangePercent'], '-10')
        self.assertEqual(result['incorrectMixedBasisChangePercent'], '-77.5')
        self.assertEqual(result['unknownTarget']['status'], 'unknown')
        self.assertIsNone(result['unknownTarget']['normalizedValue'])
        self.assertIsNone(result['unknownTarget']['sameBasisChangePercent'])

    def test_recomputes_instead_of_copying_expected_results(self):
        self.fixture['targets'][1]['value'] = '33'
        self.fixture['normalization']['results'][0]['normalizedValue'] = '999'
        self.fixture['comparisons'][1]['sameBasisChangePercent'] = '999'
        self.assertEqual(demo.evaluate(self.fixture)['laterChangePercent'], '10')

    def test_labels_both_languages_and_does_not_access_network(self):
        with patch('socket.socket', side_effect=AssertionError('Network not allowed')):
            for language, label in [('en', 'Synthetic demo'), ('zh', '合成演示')]:
                result = demo.evaluate(self.fixture, language)
                self.assertIn(label, result['summary'])
                for flag in ('synthetic', 'notForTrading', 'notLiveQuote',
                             'notInvestmentRecommendation', 'notPaidWorkflowEvidence'):
                    self.assertIs(result[flag], True)

    def test_rejects_non_synthetic_or_real_ticker(self):
        for flag in ('synthetic', 'notForTrading', 'notLiveQuote',
                     'notInvestmentRecommendation', 'notPaidWorkflowEvidence'):
            payload = deepcopy(self.fixture)
            payload['demo'][flag] = False
            with self.subTest(flag=flag), self.assertRaises(ValueError):
                demo.evaluate(payload)
        self.fixture['company']['symbol'] = 'NVDA'
        with self.assertRaises(ValueError):
            demo.evaluate(self.fixture)

    def test_rejects_invalid_ratio_prices_and_unknown_basis(self):
        for value in ('0', '-1', 'NaN', 'Infinity', True, 4):
            payload = deepcopy(self.fixture)
            payload['split']['newSharesPerOldShare'] = value
            with self.subTest(ratio=value), self.assertRaises(ValueError):
                demo.evaluate(payload)
            payload = deepcopy(self.fixture)
            payload['targets'][0]['value'] = value
            with self.subTest(price=value), self.assertRaises(ValueError):
                demo.evaluate(payload)
        self.fixture['targets'][0]['basis'] = 'unknown'
        with self.assertRaises(ValueError):
            demo.evaluate(self.fixture)

    def test_isolated_installed_cli_and_missing_fixture_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory) / 'skill'
            shutil.copytree(PACKAGE, installed)
            command = [sys.executable, str(installed / 'scripts/demo.py'), '--lang', 'zh']
            environment = {'PATH': os.environ['PATH']}
            result = subprocess.run(command, cwd=directory, env=environment, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['laterChangePercent'], '-10')
            payload = deepcopy(self.fixture)
            payload['demo'] = []
            (installed / 'assets/stock-split-basis.json').write_text(json.dumps(payload))
            result = subprocess.run(command, cwd=directory, env=environment, text=True, capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)['error'], 'DEMO_UNAVAILABLE')
            (installed / 'assets/stock-split-basis.json').unlink()
            result = subprocess.run(command, cwd=directory, env=environment, text=True, capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)['error'], 'DEMO_UNAVAILABLE')

    def test_generated_package_matches_sources_and_routes_demo_separately(self):
        self.assertEqual((PACKAGE / 'assets/stock-split-basis.json').read_text(),
                         (ROOT / 'demo/stock-split-basis.json').read_text())
        self.assertEqual((PACKAGE / 'scripts/demo.py').read_text(),
                         (ROOT / 'runtime/stock_split_demo.py').read_text())
        content = (PACKAGE / 'SKILL.md').read_text()
        self.assertIn('Only when the user asks for a demo', content)
        self.assertIn('Do not run `run.py stock` for this request', content)
        self.assertIn('only after the user has approved allowance consumption', content)
        self.assertIn('matching backend has not been verified in production', content)


if __name__ == '__main__':
    unittest.main()
