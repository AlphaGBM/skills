from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_runtime import workflow


ROOT = Path(__file__).resolve().parents[1]
specification = importlib.util.spec_from_file_location('review_engine', ROOT / 'runtime/review_engine.py')
engine = importlib.util.module_from_spec(specification)
specification.loader.exec_module(engine)


def snapshot(price=100, observed='2026-09-20T20:00:00+00:00', generated='2026-09-20T21:00:00+00:00'):
    value = {'contractVersion': 'stock-opportunities.v1', 'language': 'en', 'status': 'partial',
             'instrument': {'type': 'stock', 'symbol': 'DEMO', 'market': 'US'}, 'style': 'quality',
             'metrics': {'price': price}, 'currencySymbol': '$', 'quoteTime': {'source': 'synthetic', 'observed_at': observed, 'trading_date': observed[:10]}}
    return {**value, 'resultId': engine.digest(value), 'generatedAt': generated}


class ReviewWorkflowChecks(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.before_path = Path(self.directory.name) / 'before.json'
        self.after_path = Path(self.directory.name) / 'after.json'
        self.before = snapshot()
        self.after = snapshot(110, '2026-09-21T20:00:00+00:00', '2026-09-21T21:00:00+00:00')
        self.before_path.write_text(json.dumps({'workflow': 'stock', 'result': {'success': True, 'data': self.before}}))
        self.after_path.write_text(json.dumps({'workflow': 'stock', 'result': {'success': True, 'data': self.after}}))

    def args(self):
        return workflow.parser().parse_args(['review', '--baseline', str(self.before_path), '--current', str(self.after_path), '--lang', 'zh'])

    def test_no_network_key_usage_or_file_changes(self):
        originals = [path.read_bytes() for path in (self.before_path, self.after_path)]
        with patch.object(workflow, 'fetch_json') as fetch, patch.object(workflow, 'paid') as paid, \
                patch.object(workflow, 'base_url') as origin, patch.dict(os.environ, {'ALPHAGBM_API_KEY': 'not-sent'}):
            result = workflow.execute(self.args())
        self.assertEqual(result['data']['access']['networkRequests'], 0)
        self.assertEqual(result['data']['language'], 'zh')
        self.assertEqual(result['data']['judgment']['status'], 'requires_review')
        fetch.assert_not_called()
        paid.assert_not_called()
        origin.assert_not_called()
        self.assertEqual(originals, [path.read_bytes() for path in (self.before_path, self.after_path)])
        self.assertEqual(len(list(Path(self.directory.name).iterdir())), 2)

    def test_actual_packaged_command_from_unrelated_directory(self):
        command = [sys.executable, str(ROOT / 'skills/core/alphagbm-stock-research/scripts/run.py'),
                   'review', '--baseline', str(self.before_path), '--current', str(self.after_path), '--lang', 'en']
        result = subprocess.run(command, cwd=self.directory.name, env={'PATH': os.environ.get('PATH', '')}, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)['result']['data']
        self.assertEqual(output['contractVersion'], 'investment-review.v1')
        self.assertEqual(next(item for item in output['changes'] if item['field'] == 'metrics.price')['delta'], 10)

    def test_packaged_engine_matches_runtime(self):
        source = (ROOT / 'runtime/review_engine.py').read_bytes()
        for directory in (ROOT / 'skills').rglob('scripts/review_engine.py'):
            self.assertEqual(directory.read_bytes(), source)

    def test_missing_input_is_not_history_lookup(self):
        self.before_path.unlink()
        with patch.object(workflow, 'fetch_json') as fetch, self.assertRaises(workflow.WorkflowError) as error:
            workflow.execute(self.args())
        self.assertEqual(error.exception.code, 'INVALID_REVIEW_FILE')
        fetch.assert_not_called()

    def test_invalid_or_duplicate_json_is_rejected_without_echo(self):
        for content in ['{"secret":"DO_NOT_ECHO", "price": NaN}', '{"x": 1,"x": 2}', 'not-json']:
            self.before_path.write_text(content)
            with self.assertRaises(workflow.WorkflowError) as error:
                workflow.execute(self.args())
            self.assertNotIn('DO_NOT_ECHO', str(error.exception))
            self.assertEqual(error.exception.code, 'INVALID_REVIEW_FILE')

    def test_oversized_and_nonregular_file_rejected(self):
        self.before_path.write_bytes(b' ' * (engine.MAX_BYTES + 1))
        with self.assertRaises(workflow.WorkflowError):
            workflow.execute(self.args())
        self.before_path.unlink()
        self.before_path.mkdir()
        with self.assertRaises(workflow.WorkflowError):
            workflow.execute(self.args())

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'FIFO is not supported')
    def test_fifo_cannot_block_the_runner(self):
        self.before_path.unlink()
        os.mkfifo(self.before_path)
        with self.assertRaises(workflow.WorkflowError) as error:
            workflow.execute(self.args())
        self.assertEqual(error.exception.code, 'INVALID_REVIEW_FILE')

    def test_incompatible_or_tampered_snapshots_do_not_trigger_research(self):
        tampered = deepcopy(self.after)
        tampered['metrics']['price'] = 999
        for value in [tampered, {'success': False}, {'not': 'history'}]:
            self.after_path.write_text(json.dumps(value))
            with patch.object(workflow, 'fetch_json') as fetch, self.assertRaises(workflow.WorkflowError) as error:
                workflow.execute(self.args())
            self.assertEqual(error.exception.code, 'INCOMPARABLE_REVIEW')
            fetch.assert_not_called()


if __name__ == '__main__':
    unittest.main()
