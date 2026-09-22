import unittest
from unittest.mock import patch

from test_runtime import workflow


def payload():
    return {'success': True, 'data': {
        'contractVersion': 'news-impact.v1', 'status': 'partial', 'language': 'en',
        'resultId': 'sha256:' + 'a' * 64, 'newsVerified': False, 'impactEstablished': False,
        'article': {'slug': 'facility-news', 'revision': 3, 'category': 'announcement', 'summary': 'An issuer announced a facility.'},
        'sources': [], 'reportedFacts': [], 'publishedImpactAnalysis': [],
        'publishedUncertainties': [], 'verificationNodes': [],
        'missingData': ['public_source_links'], 'nextChecks': ['Read the original announcement.'],
    }}


def args(*extra):
    return workflow.parser().parse_args(['news', '--slug', 'facility-news', *extra])


class NewsWorkflowChecks(unittest.TestCase):
    def test_one_key_free_read_without_any_paid_call(self):
        with patch.object(workflow, 'fetch_json', return_value=payload()) as fetch, patch.object(workflow, 'paid') as paid:
            result = workflow.execute(args())
        self.assertEqual(result, payload())
        fetch.assert_called_once_with('GET', '/api/insights/catalogue/facility-news/news-impact?lang=en')
        paid.assert_not_called()

    def test_revision_and_language_pinned(self):
        result = payload()
        result['data']['language'] = 'zh'
        with patch.object(workflow, 'fetch_json', return_value=result) as fetch:
            workflow.execute(args('--revision', '3', '--lang', 'zh'))
        fetch.assert_called_once_with('GET', '/api/insights/catalogue/facility-news/news-impact?lang=zh&revision=3')

    def test_incorrect_revision_rejected(self):
        with patch.object(workflow, 'fetch_json', return_value=payload()), self.assertRaises(workflow.WorkflowError):
            workflow.execute(args('--revision', '2'))

    def test_old_endpoint_not_a_workflow_or_reason_to_call_paid(self):
        with patch.object(workflow, 'fetch_json', return_value={'slug': 'facility-news'}) as fetch, self.assertRaises(workflow.WorkflowError):
            workflow.execute(args())
        self.assertEqual(fetch.call_count, 1)

    def test_invalid_slug_and_revision_do_not_request_anything(self):
        for arguments in (['news', '--slug', '../private'], ['news', '--slug', 'https://evil.example'],
                          ['news', '--slug', 'facility-news', '--revision', '0']):
            with self.subTest(args=arguments), patch.object(workflow, 'fetch_json') as fetch, self.assertRaises(workflow.WorkflowError):
                workflow.execute(workflow.parser().parse_args(arguments))
            fetch.assert_not_called()

    def test_proof_boundaries_and_structures_are_required(self):
        for field, value in [('newsVerified', True), ('impactEstablished', True), ('status', 'verified'),
                             ('language', 'zh'), ('resultId', None), ('sources', {}), ('missingData', None),
                             ('contractVersion', 'old'), ('article', {})]:
            result = payload()
            result['data'][field] = value
            with self.subTest(field=field), patch.object(workflow, 'fetch_json', return_value=result), self.assertRaises(workflow.WorkflowError):
                workflow.execute(args())

    def test_article_identity_category_and_summary_checked(self):
        for field, value in [('slug', 'other-news'), ('revision', True), ('revision', 0), ('summary', ''),
                             ('category', 'institutional-note'), ('category', 'research-note')]:
            result = payload()
            result['data']['article'][field] = value
            with self.subTest(field=field), patch.object(workflow, 'fetch_json', return_value=result), self.assertRaises(workflow.WorkflowError):
                workflow.execute(args())

    def test_failure_not_retried_or_routed_to_another_service(self):
        with patch.object(workflow, 'fetch_json', side_effect=workflow.WorkflowError('NOT_FOUND', 'Unavailable')) as fetch, self.assertRaises(workflow.WorkflowError):
            workflow.execute(args())
        self.assertEqual(fetch.call_count, 1)


if __name__ == '__main__':
    unittest.main()
