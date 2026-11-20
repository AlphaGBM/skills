import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


PACKAGE = Path(__file__).resolve().parents[1] / 'skills/stocks/alphagbm-causal-research'
SPEC = importlib.util.spec_from_file_location('causal_calculator', PACKAGE / 'scripts/calculate.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CausalResearchTests(unittest.TestCase):
    def payload(self, operation='difference', values=None):
        values = ['80', '110'] if values is None else values
        return {'operation': operation, 'values': values, 'unit': 'CNY million', 'evidenceIds': ['E1'] * len(values)}

    def test_decimal_execution_and_units(self):
        for operation, values, result, unit in [
            ('sum', ['0.1', '0.2'], '0.3', 'CNY million'),
            ('difference', ['80', '110'], '-30', 'CNY million'),
            ('ratio', ['1', '4'], '0.25', 'ratio'),
            ('percent_change', ['45', '50'], '-10.0', '%'),
        ]:
            output = MODULE.calculate(self.payload(operation, values))
            self.assertEqual(output['result'], result)
            self.assertEqual(output['outputUnit'], unit)
            self.assertEqual(output['status'], 'executed')
            self.assertFalse(output['inputFactsVerified'])

    def test_rejects_invalid_inputs(self):
        for payload in [self.payload('eval'), self.payload(values=['NaN', '1']),
                        self.payload(values=['1e9', '1']), self.payload(values=['1', None]),
                        self.payload('ratio', ['1', '0']), self.payload('percent_change', ['1', '-1']),
                        self.payload(values=['1']), self.payload(values=['1'] * 33),
                        {**self.payload(), 'path': '/etc/passwd'},
                        {**self.payload(), 'evidenceIds': []}]:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                MODULE.calculate(payload)

    def test_cli_runs_and_bounds_input(self):
        for raw, status in [(json.dumps(self.payload()), 0), (' ' * 16385, 1), ('{', 1)]:
            response = subprocess.run([sys.executable, str(PACKAGE / 'scripts/calculate.py')], input=raw, text=True, capture_output=True)
            self.assertEqual(response.returncode, status)
            self.assertEqual(json.loads(response.stdout or response.stderr)['status'], 'executed' if status == 0 else 'error')

    def test_no_unavailable_workspace_dependencies(self):
        content = (PACKAGE / 'SKILL.md').read_text()
        self.assertNotIn('skills/fact-check-gate/', content)
        self.assertIn('部分验证 / partial', content)
        for name in ('execution', 'sectors', 'worksheet'):
            self.assertIn(f'references/{name}.md', content)
            self.assertTrue((PACKAGE / f'references/{name}.md').is_file())


if __name__ == '__main__':
    unittest.main()
