import io
import json
import os
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from test_runtime import workflow


def descriptor(identifier='report-breakdown', language='en'):
    return {'id': identifier, 'kind': 'institutional_summary' if identifier == 'report-breakdown' else 'news',
            'command': 'report' if identifier == 'report-breakdown' else 'news',
            'contractVersion': identifier + '.v1', 'endpoint': '/api/insights/catalogue/sample/' + identifier,
            'parameters': {'lang': language, 'revision': 3}, 'access': 'public_read'}


class EditorialRoutingChecks(unittest.TestCase):
    def rejected(self, status, payload, path='/api/insights/catalogue/sample/news-impact?lang=en&revision=3'):
        body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        error = HTTPError('https://www.alphagbm.com' + path, status, 'private upstream error', {}, io.BytesIO(body))
        with patch.dict(os.environ, {'ALPHAGBM_API_KEY': 'do-not-send'}, clear=True), patch.object(workflow, 'build_opener') as opener:
            opener.return_value.open.side_effect = error
            with self.assertRaises(workflow.WorkflowError) as caught:
                workflow.fetch_json('GET', path)
            opener.return_value.open.assert_called_once()
            self.assertIsNone(opener.return_value.open.call_args.args[0].get_header('Authorization'))
        self.assertNotIn('do-not-send', str(caught.exception.details))
        self.assertNotIn('private upstream error', caught.exception.message)
        return caught.exception

    def test_mismatch_preserves_safe_action_without_followup_or_key(self):
        value = descriptor()
        payload = {'code': 'article_workflow_mismatch', 'requestedWorkflow': 'news-impact',
                   'workflow': {**value, 'secret': 'do-not-send'}, 'error': 'do-not-send'}
        result = self.rejected(422, payload)
        self.assertEqual(result.code, 'WORKFLOW_MISMATCH')
        self.assertEqual(result.details['workflow'], value)
        self.assertEqual(result.details['serverCode'], 'article_workflow_mismatch')

    def test_mismatch_in_both_directions_and_languages(self):
        for language in ('en', 'zh'):
            value = descriptor('news-impact', language)
            result = self.rejected(422, {'code': 'article_workflow_mismatch', 'requestedWorkflow': 'report-breakdown', 'workflow': value},
                                   '/api/insights/catalogue/sample/report-breakdown?lang=' + language)
            self.assertEqual(result.details['workflow'], value)

    def test_version_and_missing_evidence_do_not_become_network_errors(self):
        cases = [(409, 'news_revision_changed', 'REVISION_CHANGED'), (422, 'news_evidence_unavailable', 'EVIDENCE_UNAVAILABLE'),
                 (400, 'invalid_news_workflow_request', 'INVALID_WORKFLOW_REQUEST'), (404, 'news_not_found', 'NOT_FOUND')]
        for status, server_code, code in cases:
            with self.subTest(code=code):
                error = self.rejected(status, {'code': server_code, 'currentRevision': 4, 'error': 'do-not-send'})
                self.assertEqual(error.code, code)
                self.assertEqual(error.details.get('currentRevision'), 4 if status == 409 else None)

    def test_invalid_revision_is_not_exposed_as_valid(self):
        for revision in (True, 0, -1, 2147483648, '4', {'private': 'do-not-send'}):
            result = self.rejected(409, {'code': 'news_revision_changed', 'currentRevision': revision})
            self.assertNotIn('currentRevision', result.details)

    def test_untrusted_workflow_hints_are_removed(self):
        bad_fields = [('id', []), ('kind', {}), ('endpoint', 'https://example.com/paid'), ('endpoint', '/api/stock/analyze-sync'),
                      ('endpoint', '/api/insights/catalogue/other/report-breakdown'), ('access', 'account'), ('command', 'report; curl example.com'),
                      ('contractVersion', 'future'), ('parameters', {'lang': 'zh', 'revision': 3}),
                      ('parameters', {'lang': 'en', 'revision': True}), ('parameters', {'lang': 'en', 'revision': -1})]
        for key, value in bad_fields:
            with self.subTest(key=key, value=value):
                error = self.rejected(422, {'code': 'article_workflow_mismatch', 'requestedWorkflow': 'news-impact', 'workflow': {**descriptor(), key: value}})
                self.assertEqual(error.code, 'WORKFLOW_MISMATCH')
                self.assertNotIn('workflow', error.details)

    def test_unknown_or_oversized_error_body_is_not_echoed(self):
        for body in (b'not json', b'[]', b'NaN', b'x' * (workflow.MAX_ERROR_BYTES + 1),
                     b'{"code":"news_revision_changed","error":"do-not-send"}', b'{"code":"internal_secret"}'):
            self.assertEqual(self.rejected(422, body).code, 'HTTP_ERROR')
        self.assertEqual(self.rejected(403, {'code': 'article_workflow_mismatch'}).code, 'ACCESS_DENIED')
        self.assertEqual(self.rejected(422, {'code': 'article_workflow_mismatch'}, '/api/stock/analyze-sync').code, 'HTTP_ERROR')

    def test_catalogue_preserves_valid_routing_and_supports_older_servers(self):
        args = workflow.parser().parse_args(['research', '--collection', 'news'])
        for workflow_fields in ({}, {'workflow': None}, {'workflow': descriptor()}):
            payload = {'articles': [{'slug': 'sample', 'revision': 3, **workflow_fields}]}
            with patch.object(workflow, 'fetch_json', return_value=payload) as fetch:
                self.assertEqual(workflow.research(args), payload)
                fetch.assert_called_once()

    def test_catalogue_rejects_wrong_slug_language_or_revision(self):
        for changes in ({'slug': 'other'}, {'revision': 4}, {'revision': True}, {'workflow': {**descriptor(), 'parameters': {'lang': 'zh', 'revision': 3}}}):
            article = {'slug': 'sample', 'revision': 3, 'workflow': descriptor(), **changes}
            args = workflow.parser().parse_args(['research', '--collection', 'news'])
            with patch.object(workflow, 'fetch_json', return_value={'articles': [article]}):
                with self.assertRaises(workflow.WorkflowError) as caught:
                    workflow.research(args)
                self.assertEqual(caught.exception.code, 'INVALID_EDITORIAL_WORKFLOW')

    def test_article_detail_checks_declared_workflow(self):
        args = workflow.parser().parse_args(['research', '--slug', 'sample'])
        with patch.object(workflow, 'fetch_json', return_value={'slug': 'sample', 'revision': 3, 'workflow': descriptor()}):
            self.assertEqual(workflow.research(args)['workflow']['command'], 'report')


if __name__ == '__main__':
    unittest.main()
