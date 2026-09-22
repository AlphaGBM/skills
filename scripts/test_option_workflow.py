import unittest
from unittest.mock import patch

from test_runtime import workflow


STRATEGIES = ['sell_put', 'sell_call', 'buy_call', 'buy_put']
INSTRUMENT = {'symbol': 'AAPL', 'market': 'US', 'currency': 'USD'}
CONTRACT = {'contractVersion': 'option-strategies.v1', 'instrument': INSTRUMENT}


def payload():
    return {'success': True, 'data': {
        **CONTRACT, 'status': 'partial', 'resultId': 'sha256:' + 'a' * 64,
        'requestedStrategy': 'all', 'expiry': '2026-10-16',
        'strategies': {name: [] for name in STRATEGIES},
    }}


def args(*extra):
    return workflow.parser().parse_args(['options', 'AAPL', *extra])


class OptionWorkflowChecks(unittest.TestCase):
    def test_confirmation_before_any_call(self):
        with patch.object(workflow, 'fetch_json') as fetch, self.assertRaises(workflow.WorkflowError):
            workflow.execute(args('--workflow'))
        fetch.assert_not_called()

    def test_old_server_does_not_receive_paid_request(self):
        with patch.object(workflow, 'fetch_json', return_value={}) as fetch, self.assertRaises(workflow.WorkflowError) as caught:
            workflow.execute(args('--workflow', '--confirm-usage'))
        self.assertEqual(caught.exception.code, 'WORKFLOW_UNAVAILABLE')
        fetch.assert_called_once_with('GET', '/api/v1/options/workflow-contract?ticker=AAPL')

    def test_workflow_preflight_and_exact_options_call(self):
        with patch.object(workflow, 'fetch_json', side_effect=[CONTRACT, payload()]) as fetch:
            result = workflow.execute(args('--workflow', '--lang', 'zh', '--confirm-usage'))
        self.assertEqual(result, payload())
        self.assertEqual(fetch.call_count, 2)
        fetch.assert_called_with('POST', '/api/v1/options/score?format=workflow&lang=zh', authenticated=True,
                                 body={'ticker': 'AAPL', 'strategy': 'all', 'top_n': 3}, timeout=90)

    def test_bad_response_never_silently_accepted_or_retried(self):
        for field, value in [('contractVersion', 'old'), ('instrument', {'symbol': 'MSFT'}),
                             ('resultId', 'bad'), ('status', 'ready'), ('strategies', []),
                             ('strategies', {'sell_put': []}), ('requestedStrategy', 'buy_put')]:
            result = payload()
            result['data'][field] = value
            with self.subTest(field=field), patch.object(workflow, 'fetch_json', side_effect=[CONTRACT, result]) as fetch, self.assertRaises(workflow.WorkflowError) as caught:
                workflow.execute(args('--workflow', '--confirm-usage'))
            self.assertEqual(caught.exception.code, 'INVALID_WORKFLOW_RESPONSE')
            self.assertEqual(fetch.call_count, 2)

    def test_explicit_expiry_and_single_strategy(self):
        result = payload()
        result['data']['requestedStrategy'] = 'sell_put'
        result['data']['strategies'] = {'sell_put': []}
        with patch.object(workflow, 'fetch_json', side_effect=[CONTRACT, result]) as fetch:
            workflow.execute(args('--strategy', 'sell_put', '--expiry', '2026-10-16', '--workflow', '--confirm-usage'))
        self.assertEqual(fetch.call_args.kwargs['body']['expiry_date'], '2026-10-16')
        with patch.object(workflow, 'fetch_json', side_effect=[CONTRACT, result]), self.assertRaises(workflow.WorkflowError):
            workflow.execute(args('--strategy', 'sell_put', '--expiry', '2026-10-23', '--workflow', '--confirm-usage'))

    def test_invalid_expiry_never_calls_server(self):
        with patch.object(workflow, 'fetch_json') as fetch, self.assertRaises(workflow.WorkflowError):
            workflow.execute(args('--expiry', '2026-02-30', '--workflow', '--confirm-usage'))
        fetch.assert_not_called()

    def test_legacy_default_all_accepts_strategy_map(self):
        result = {'strategies': {name: [] for name in STRATEGIES}}
        with patch.object(workflow, 'fetch_json', return_value=result) as fetch:
            self.assertEqual(workflow.execute(args('--confirm-usage')), result)
        fetch.assert_called_once_with('POST', '/api/v1/options/score', authenticated=True,
                                     body={'ticker': 'AAPL', 'strategy': 'all', 'top_n': 3}, timeout=90)

    def test_legacy_single_accepts_recommendations(self):
        with patch.object(workflow, 'fetch_json', return_value={'recommendations': []}):
            workflow.execute(args('--strategy', 'buy_call', '--confirm-usage'))

    def test_legacy_all_rejects_incomplete_map(self):
        for result in ({'recommendations': []}, {'strategies': {'sell_put': []}}):
            with patch.object(workflow, 'fetch_json', return_value=result), self.assertRaises(workflow.WorkflowError):
                workflow.execute(args('--confirm-usage'))


if __name__ == '__main__':
    unittest.main()
