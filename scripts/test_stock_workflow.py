import importlib.util
from datetime import datetime, timedelta, timezone
from pathlib import Path
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('workflow', ROOT / 'runtime/workflow.py')
workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)


def candidate(symbol, composite, legacy):
    now = datetime.now(timezone.utc)
    return {'kind': 'stock', 'market': 'US', 'symbol': symbol, 'score': legacy,
            'stockRecommendationEligible': True, 'stockScoreState': 'complete',
            'stockOpportunityScore': {'symbol': symbol, 'market': 'US', 'score': composite,
                'method': 'stock-opportunity-composite-v2', 'snapshotId': 'a' * 64,
                'availability': 'complete', 'recommendationEligible': True,
                'asOf': (now - timedelta(hours=1)).isoformat(), 'expiresAt': (now + timedelta(hours=1)).isoformat()}}


class StockWorkflowTests(unittest.TestCase):
    def test_radar_orders_by_composite_not_legacy_score(self):
        items = [candidate('LOW', 30, 99), candidate('HIGH', 85, 1)]
        with patch.object(workflow, 'fetch_json', return_value={'data': {'items': items}}) as fetch:
            result = workflow.execute(workflow.parser().parse_args(['radar']))
        self.assertEqual([row['symbol'] for row in result['items']], ['HIGH', 'LOW'])
        self.assertEqual(result['items'][0]['score'], 85)
        self.assertEqual(result['items'][0]['scoreBasis'], 'stock-opportunity-composite-v2')
        self.assertEqual(items[0]['score'], 99)
        fetch.assert_called_once_with('GET', '/api/homepage/opportunities')

    def test_unqualified_or_expired_scores_do_not_become_candidates(self):
        for field, value in [('score', float('nan')), ('score', True), ('score', 101),
                             ('availability', 'partial'), ('symbol', 'OTHER'), ('market', 'HK'),
                             ('expiresAt', '2020-01-01T00:00:00Z'), ('asOf', '2099-01-01T00:00:00Z'),
                             ('asOf', '2026-09-20'), ('asOf', None), ('snapshotId', 'bad'),
                             ('recommendationEligible', False), ('method', 'risk-score')]:
            item = candidate('AAPL', 80, 90)
            item['stockOpportunityScore'][field] = value
            with self.subTest(field=field, value=value), patch.object(workflow, 'fetch_json', return_value={'data': {'items': [item]}}):
                self.assertEqual(workflow.execute(workflow.parser().parse_args(['radar']))['availableCandidates'], 0)

    def test_no_fallback_to_legacy_or_missing_score(self):
        item = candidate('AAPL', 80, 90)
        item['stockOpportunityScore'] = None
        with patch.object(workflow, 'fetch_json', return_value={'data': {'items': [item]}}):
            self.assertEqual(workflow.execute(workflow.parser().parse_args(['radar']))['items'], [])

    def test_allowance_confirmation_precedes_workflow_request(self):
        with patch.object(workflow, 'fetch_json') as fetch, self.assertRaises(workflow.WorkflowError):
            workflow.execute(workflow.parser().parse_args(['stock', 'AAPL', '--workflow']))
        fetch.assert_not_called()

    def test_workflow_exact_contract_and_partial_result(self):
        for requested, returned, market in [('AAPL', 'AAPL', 'US'), ('00700.HK', '0700.HK', 'HK'), ('700', '0700.HK', 'HK'), ('688981.SH', '688981.SS', 'CN')]:
            instrument = {'type': 'stock', 'symbol': returned, 'market': market}
            payload = {'success': True, 'data': {'contractVersion': 'stock-opportunities.v1',
                'instrument': instrument, 'resultId': 'sha256:' + 'a' * 64, 'status': 'partial'}}
            with self.subTest(ticker=requested), patch.object(workflow, 'fetch_json', side_effect=[{'contractVersion': 'stock-opportunities.v1', 'instrument': instrument}, payload]) as fetch:
                result = workflow.execute(workflow.parser().parse_args(['stock', requested, '--workflow', '--lang', 'zh', '--confirm-usage']))
                self.assertEqual(result, payload)
                fetch.assert_called_with('POST', '/api/stock/analyze-sync?format=workflow&lang=zh',
                    authenticated=True, body={'ticker': requested, 'style': 'quality'}, timeout=90)
                self.assertEqual(fetch.call_count, 2)
                self.assertEqual(fetch.call_args_list[0].args, ('GET', '/api/stock/workflow-contract?ticker=' + requested))

    def test_old_server_response_is_not_silently_accepted_or_retried(self):
        contract = {'contractVersion': 'stock-opportunities.v1', 'instrument': {'type': 'stock', 'symbol': 'AAPL', 'market': 'US'}}
        with patch.object(workflow, 'fetch_json', side_effect=[contract, {'data': {'symbol': 'AAPL'}}]) as fetch:
            with self.assertRaises(workflow.WorkflowError) as caught:
                workflow.execute(workflow.parser().parse_args(['stock', 'AAPL', '--workflow', '--confirm-usage']))
            self.assertEqual(caught.exception.code, 'INVALID_WORKFLOW_RESPONSE')
            self.assertEqual(fetch.call_count, 2)

    def test_unsupported_server_never_receives_a_charged_request(self):
        with patch.object(workflow, 'fetch_json', return_value={}) as fetch:
            with self.assertRaises(workflow.WorkflowError) as caught:
                workflow.execute(workflow.parser().parse_args(['stock', 'AAPL', '--workflow', '--confirm-usage']))
            self.assertEqual(caught.exception.code, 'WORKFLOW_UNAVAILABLE')
            fetch.assert_called_once_with('GET', '/api/stock/workflow-contract?ticker=AAPL')

    def test_legacy_stock_command_still_uses_existing_endpoint(self):
        with patch.object(workflow, 'fetch_json', return_value={'data': {'symbol': 'AAPL'}}) as fetch:
            workflow.execute(workflow.parser().parse_args(['stock', 'AAPL', '--confirm-usage']))
            self.assertEqual(fetch.call_args.args, ('POST', '/api/stock/analyze-sync'))


if __name__ == '__main__':
    unittest.main()
