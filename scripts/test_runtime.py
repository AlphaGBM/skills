import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from urllib.error import HTTPError, URLError

source = Path(__file__).resolve().parents[1] / 'runtime/workflow.py'
spec = importlib.util.spec_from_file_location('workflow', source)
workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)


class Response(io.BytesIO):
    pass


class RunnerChecks(unittest.TestCase):
    def test_smart_money_document_example_and_invalid_fields(self):
        import re
        document = (source.parents[1] / 'docs/SMART_MONEY_INPUT.md').read_text()
        example = re.search(r'```json\n(.*?)\n```', document, re.S).group(1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'transactions.json'
            path.write_text(example)
            rows = workflow.read_transactions(path)
            self.assertEqual(sum(row['value'] * (1 if row['side'] == 'buy' else -1) for row in rows), 750)
            invalid = [
                {'disclosedAt': '2026-09-01', 'action': 'buy', 'value': 100, 'source': 'Example'},
                {**rows[0], 'date': '2026-02-30'},
                {**rows[0], 'side': 'BUY'},
                {**rows[0], 'source': ''},
                {**rows[0], 'value': True},
                {**rows[0], 'value': float('nan')},
                {**rows[0], 'value': -1},
            ]
            for row in invalid:
                with self.subTest(row=row):
                    path.write_text(json.dumps([row]))
                    with patch.object(workflow, 'fetch_json') as request, patch.dict(os.environ, {'ALPHAGBM_API_KEY': 'agbm_test'}):
                        with self.assertRaises(workflow.WorkflowError):
                            workflow.execute(workflow.parser().parse_args(['smart-money', '--ticker', 'NVDA', '--transactions-file', str(path), '--confirm-usage']))
                        request.assert_not_called()

    def test_catalog_scripts_identical(self):
        root = source.parents[1]
        catalogue = json.loads((root / 'catalog/catalog.json').read_text())
        for entry in catalogue['workflows'] + [entry for entry in catalogue['tools'] if entry['status'] != 'reference']:
            self.assertEqual((root / entry['path'] / 'scripts/run.py').read_bytes(), source.read_bytes())

    def test_paid_confirmation_precedes_request(self):
        for command in ['stock NVDA', 'options NVDA', 'dividend 0700.HK', 'verify NVDA --prompt claim --idempotency-key example-001']:
            with self.subTest(command=command), patch.object(workflow, 'fetch_json') as request:
                with self.assertRaises(workflow.WorkflowError) as error:
                    workflow.execute(workflow.parser().parse_args(command.split()))
                self.assertEqual(error.exception.code, 'CONFIRM_USAGE')
                request.assert_not_called()

    def test_public_read_no_key(self):
        with patch.dict(os.environ, {'ALPHAGBM_API_KEY':'do-not-send'}, clear=True), patch.object(workflow, 'build_opener') as opener:
            opener.return_value.open.return_value = Response(b'{"articles":[]}')
            workflow.fetch_json('GET', '/api/insights/catalogue')
            request = opener.return_value.open.call_args.args[0]
            self.assertIsNone(request.get_header('Authorization'))

    def test_missing_auth_before_network(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(workflow, 'build_opener') as opener:
            with self.assertRaises(workflow.WorkflowError):
                workflow.fetch_json('POST', '/api/stock/analyze-sync', authenticated=True)
            opener.assert_not_called()

    def test_origin_allowlist(self):
        for origin in ['http://www.alphagbm.com', 'https://evil.test', 'https://www.alphagbm.com.evil.test', 'https://user@www.alphagbm.com', 'https://www.alphagbm.com/?key=private', 'https://www.alphagbm.com:9999', 'https://www.alphagbm.com/api']:
            with self.subTest(origin=origin), patch.dict(os.environ, {'ALPHAGBM_BASE_URL':origin}):
                with self.assertRaises(workflow.WorkflowError):
                    workflow.base_url()

    def test_http_error_no_raw_response_or_secret(self):
        for code in [301, 302, 401, 402, 403, 404, 429, 500, 503]:
            with self.subTest(code=code), patch.object(workflow, 'build_opener') as opener:
                opener.return_value.open.side_effect = HTTPError('https://www.alphagbm.com', code, 'error', {'Retry-After':'30'}, io.BytesIO(b'private-key-text'))
                with self.assertRaises(workflow.WorkflowError) as error:
                    workflow.fetch_json('GET', '/public')
                self.assertNotIn('private-key-text', str(error.exception))
                self.assertEqual(error.exception.details['httpStatus'], code)
                self.assertEqual(opener.return_value.open.call_count, 1)

    def test_invalid_response(self):
        for payload in [b'not-json', b'[]', b'{"price":NaN}', b'{"price":Infinity}', b'{"success":false}', b'{"error":"private"}']:
            with self.subTest(payload=payload), patch.object(workflow, 'build_opener') as opener:
                opener.return_value.open.return_value = Response(payload)
                with self.assertRaises(workflow.WorkflowError):
                    workflow.fetch_json('GET', '/public')

    def test_size_bound(self):
        with patch.object(workflow, 'MAX_BYTES', 4), patch.object(workflow, 'build_opener') as opener:
            opener.return_value.open.return_value = Response(b'{"large":true}')
            with self.assertRaises(workflow.WorkflowError) as error:
                workflow.fetch_json('GET', '/public')
            self.assertEqual(error.exception.code, 'RESPONSE_TOO_LARGE')

    def test_timeout_no_retry(self):
        with patch.object(workflow, 'build_opener') as opener:
            opener.return_value.open.side_effect = URLError('secret-provider-url')
            with self.assertRaises(workflow.WorkflowError) as error:
                workflow.fetch_json('POST', '/paid')
            self.assertEqual(error.exception.code, 'NETWORK_ERROR')
            self.assertNotIn('secret-provider-url', str(error.exception))
            self.assertEqual(opener.return_value.open.call_count, 1)

    def test_redirect_disabled(self):
        self.assertIsNone(workflow.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://evil.test'))

    def test_radar_eligibility_market_and_order(self):
        items = []
        now = datetime.now(timezone.utc)
        for ticker, score in [('LOW', 10), ('HIGH', 90)]:
            items.append({'kind': 'stock', 'market': 'US', 'stockRecommendationEligible': True,
                'stockScoreState': 'complete', 'score': 100 - score, 'symbol': ticker, 'asOf': 'old-date', 'points': [1, 2],
                'stockOpportunityScore': {'symbol': ticker, 'market': 'US', 'score': score,
                    'availability': 'complete', 'recommendationEligible': True, 'method': 'stock-opportunity-composite-v2',
                    'snapshotId': 'a' * 64, 'asOf': (now - timedelta(hours=1)).isoformat(),
                    'expiresAt': (now + timedelta(hours=1)).isoformat()}})
        items += [dict(items[0],symbol='LOSS',score=100,stockRecommendationEligible=False),dict(items[0],market='HK',score=100),dict(items[0],score=float('nan'))]
        with patch.object(workflow, 'fetch_json', return_value={'data':{'items':items,'generatedAt':'new-date','partial':True}}):
            result = workflow.execute(workflow.parser().parse_args(['radar','--limit','1']))
        self.assertEqual(result['items'][0]['symbol'], 'HIGH')
        self.assertEqual(result['items'][0]['asOf'], 'old-date')
        self.assertNotIn('points', result['items'][0])
        self.assertTrue(result['partial'])

    def test_research_views_and_query(self):
        with patch.object(workflow, 'fetch_json', return_value={'articles':[]}) as request:
            workflow.execute(workflow.parser().parse_args(['research','--collection','news','--view','research','--query','半导体','--lang','zh']))
            self.assertIn('view=research', request.call_args.args[1])
            self.assertIn('sort=date', request.call_args.args[1])
        with self.assertRaises(workflow.WorkflowError):
            workflow.execute(workflow.parser().parse_args(['research','--view','news']))

    def test_slug_rejects_traversal(self):
        with patch.object(workflow, 'fetch_json') as request:
            with self.assertRaises(workflow.WorkflowError):
                workflow.execute(workflow.parser().parse_args(['research','--slug','../../admin']))
            request.assert_not_called()

    def test_stock_exact_contract(self):
        with patch.object(workflow, 'fetch_json', return_value={'data':{'symbol':'NVDA'},'risk':{'score':3}}) as request:
            result = workflow.execute(workflow.parser().parse_args(['stock','NVDA','--confirm-usage']))
            self.assertEqual(request.call_args.args, ('POST','/api/stock/analyze-sync'))
            self.assertEqual(request.call_args.kwargs['body'], {'ticker':'NVDA','style':'quality'})
            self.assertEqual(result['risk']['score'], 3)

    def test_options_exact_contract(self):
        with patch.object(workflow, 'fetch_json', return_value={'strategies': {name: [] for name in ('sell_put', 'sell_call', 'buy_call', 'buy_put')}}) as request:
            workflow.execute(workflow.parser().parse_args(['options','NVDA','--limit','2','--expiry','2026-10-02','--confirm-usage']))
            self.assertEqual(request.call_args.kwargs['body'], {'ticker':'NVDA','strategy':'all','top_n':2,'expiry_date':'2026-10-02'})

    def test_dividend_exact_contract(self):
        contract = {
            'contractVersion': 'dividend-opportunities.v1',
            'instrument': {'type': 'stock', 'symbol': '0700.HK', 'market': 'hk'},
        }
        payload = {
            'success': True,
            'data': {
                **contract,
                'status': 'partial',
                'resultId': 'sha256:' + 'a' * 64,
                'missingData': ['dividend_years'],
                'score': {'score': None},
            },
        }
        with patch.object(workflow, 'fetch_json', side_effect=[contract, payload]) as request:
            result = workflow.execute(workflow.parser().parse_args(['dividend', '0700.HK', '--confirm-usage', '--lang', 'zh']))
        self.assertEqual(request.call_args_list[0].args[1], '/api/v1/dividend/workflow-contract?ticker=0700.HK')
        self.assertEqual(request.call_args_list[1].args[1], '/api/v1/dividend/score?lang=zh')
        self.assertEqual(request.call_args_list[1].kwargs['body'], {'ticker': '0700.HK'})
        self.assertEqual(result['data']['status'], 'partial')

    def test_strategy_contract_preflight_then_single_paid_request(self):
        contract = {
            'contractVersion': 'strategy-workflows.v1',
            'strategy': 'momentum',
            'ticker': 'NVDA',
            'endpoint': '/api/v1/strategies/run',
        }
        payload = {
            'success': True,
            'data': {
                **contract,
                'status': 'ready',
                'resultId': 'sha256:' + 'b' * 64,
                'missingData': [],
            },
        }
        with patch.object(workflow, 'fetch_json', side_effect=[contract, payload]) as request:
            result = workflow.execute(workflow.parser().parse_args(['momentum', 'NVDA', '--confirm-usage', '--lang', 'zh']))
        self.assertEqual(request.call_count, 2)
        self.assertEqual(request.call_args_list[0].args[0], 'GET')
        self.assertEqual(request.call_args_list[1].args[1], '/api/v1/strategies/run?lang=zh')
        self.assertEqual(request.call_args_list[1].kwargs['body'], {'strategy': 'momentum', 'ticker': 'NVDA'})
        self.assertEqual(result['data']['resultId'], 'sha256:' + 'b' * 64)

    def test_strategy_parameter_payload_is_normalized(self):
        contract = {
            'contractVersion': 'strategy-workflows.v1',
            'strategy': 'grid',
            'ticker': 'NVDA',
            'endpoint': '/api/v1/strategies/run',
        }
        payload = {'success': True, 'data': {
            **contract, 'status': 'ready', 'resultId': 'sha256:' + 'c' * 64, 'missingData': [],
        }}
        with patch.object(workflow, 'fetch_json', side_effect=[contract, payload]) as request:
            workflow.execute(workflow.parser().parse_args([
                'grid', '--ticker', 'NVDA', '--lower-price', '100', '--upper-price', '140',
                '--current-price', '120', '--capital', '1000', '--grid-count', '8', '--confirm-usage',
            ]))
        self.assertEqual(request.call_args_list[1].kwargs['body'], {
            'strategy': 'grid', 'ticker': 'NVDA', 'lowerPrice': 100.0, 'upperPrice': 140.0,
            'currentPrice': 120.0, 'capital': 1000.0, 'gridCount': 8,
        })

    def test_smart_money_reads_only_json_array(self):
        contract = {
            'contractVersion': 'strategy-workflows.v1',
            'strategy': 'smart_money',
            'ticker': 'NVDA',
            'endpoint': '/api/v1/strategies/run',
        }
        payload = {'success': True, 'data': {
            **contract, 'status': 'ready', 'resultId': 'sha256:' + 'd' * 64, 'missingData': [],
        }}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'transactions.json'
            transactions = [{'date': '2026-09-01', 'side': 'buy', 'value': 100, 'source': '13F'}]
            path.write_text(json.dumps(transactions))
            with patch.object(workflow, 'fetch_json', side_effect=[contract, payload]) as request:
                workflow.execute(workflow.parser().parse_args([
                    'smart-money', '--ticker', 'NVDA', '--transactions-file', str(path), '--confirm-usage',
                ]))
        self.assertEqual(request.call_args_list[1].kwargs['body']['transactions'], transactions)

    def test_snapshot_authenticated(self):
        with patch.object(workflow, 'fetch_json', return_value={'iv_rank':None}) as request:
            result = workflow.execute(workflow.parser().parse_args(['snapshot','NVDA']))
            self.assertTrue(request.call_args.kwargs['authenticated'])
            self.assertIsNone(result['iv_rank'])

    def task(self, status='completed'):
        return {'contractVersion':'research-task.v1','taskId':'task-001','status':status,'resultRevision':'sha256:'+'a'*64,'evidenceRevision':'sha256:'+'b'*64,'result':{'contractVersion':'quick-validation-result.v2'},'usageReceipt':{'charged':True}}

    def test_verify_uses_idempotency(self):
        with patch.object(workflow, 'fetch_json', return_value={'data':self.task()}) as request:
            result = workflow.execute(workflow.parser().parse_args(['verify','NVDA','--prompt','growth','--idempotency-key','nvda-case-001','--confirm-usage']))
            self.assertEqual(request.call_args.kwargs['idempotency_key'], 'nvda-case-001')
            self.assertEqual(result['taskId'], 'task-001')

    def test_resume_never_posts(self):
        with patch.object(workflow, 'fetch_json', return_value={'data':self.task()}) as request:
            workflow.execute(workflow.parser().parse_args(['verify','--resume','task-001']))
            self.assertEqual(request.call_args.args[0], 'GET')
            self.assertEqual(request.call_count, 1)

    def test_failed_receipt_preserved(self):
        with patch.object(workflow, 'fetch_json', return_value={'data':self.task('failed')}):
            with self.assertRaises(workflow.WorkflowError) as error:
                workflow.execute(workflow.parser().parse_args(['verify','--resume','task-001']))
            self.assertEqual(error.exception.details['usageReceipt'], {'charged':True})

    def test_bad_task_schema(self):
        for task in [{},dict(self.task(),taskId='../private'),dict(self.task(),evidenceRevision=None),dict(self.task(),status='unknown')]:
            with self.subTest(task=task),self.assertRaises(workflow.WorkflowError):
                workflow.checked_task({'data':task})

    def test_no_inferred_option(self):
        with patch.object(workflow, 'fetch_json') as request:
            with self.assertRaises(workflow.WorkflowError):
                workflow.execute(workflow.parser().parse_args(['verify','NVDA','--option','next-friday-call','--prompt','growth','--idempotency-key','nvda-case-001','--confirm-usage']))
            request.assert_not_called()


if __name__ == '__main__':
    unittest.main()
