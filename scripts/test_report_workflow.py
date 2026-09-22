import unittest
from unittest.mock import patch

from test_runtime import workflow


def payload():
    return {'success': True, 'data': {
        'contractVersion': 'report-breakdown.v1', 'status': 'partial', 'language': 'en',
        'kind': 'institutional_summary', 'resultId': 'sha256:' + 'a' * 64,
        'report': {'slug': 'example-report', 'revision': 3, 'title': 'Example Bank research', 'summary': 'Demand assumptions remain unverified.'},
        'sources': [], 'sections': [], 'symbols': [], 'missingData': [], 'limitations': [],
        'originalRatings': {'sectionIds': [], 'currentRecommendation': False, 'targetPriceIsForecast': True},
        'verification': {'sectionIds': [], 'independentlyChecked': False, 'automaticMonitoring': False},
        'access': {'basis': 'existing_public_research_only', 'analysisCharge': False, 'privateArchiveIncluded': False, 'paidAnalysisIncluded': False},
    }}


def args(*extra):
    return workflow.parser().parse_args(['report', '--slug', 'example-report', *extra])


class ReportWorkflowChecks(unittest.TestCase):
    def test_public_read_no_paid_call(self):
        with patch.object(workflow, 'fetch_json', return_value=payload()) as fetch, patch.object(workflow, 'paid') as paid:
            self.assertEqual(workflow.execute(args()), payload())
        fetch.assert_called_once_with('GET', '/api/insights/catalogue/example-report/report-breakdown?lang=en')
        paid.assert_not_called()

    def test_revision_language_and_report_kind(self):
        for kind in ['owned_research', 'institutional_summary', 'owned_research_summary']:
            result = payload()
            result['data'].update(kind=kind, language='zh')
            with patch.object(workflow, 'fetch_json', return_value=result) as fetch:
                self.assertEqual(workflow.execute(args('--revision', '3', '--lang', 'zh')), result)
            fetch.assert_called_once_with('GET', '/api/insights/catalogue/example-report/report-breakdown?lang=zh&revision=3')

    def test_missing_or_old_server_not_retried(self):
        for result in [{}, {'data': {}}, {'slug': 'example-report'}]:
            with patch.object(workflow, 'fetch_json', return_value=result) as fetch, self.assertRaises(workflow.WorkflowError):
                workflow.execute(args())
            self.assertEqual(fetch.call_count, 1)

    def test_access_rating_verification_flags_fail_closed(self):
        for group, field, value in [('access', 'analysisCharge', True), ('access', 'privateArchiveIncluded', True),
                                    ('access', 'paidAnalysisIncluded', True), ('access', 'basis', 'all_reports'),
                                    ('verification', 'independentlyChecked', True), ('verification', 'automaticMonitoring', True),
                                    ('originalRatings', 'currentRecommendation', True), ('originalRatings', 'targetPriceIsForecast', False)]:
            result = payload()
            result['data'][group][field] = value
            with self.subTest(field=field), patch.object(workflow, 'fetch_json', return_value=result), self.assertRaises(workflow.WorkflowError):
                workflow.execute(args())

    def test_required_structures_and_identity(self):
        for field, value in [('contractVersion', 'old'), ('status', 'verified'), ('language', 'zh'),
                             ('kind', 'private_report'), ('resultId', None), ('sources', {}), ('sections', None),
                             ('originalRatings', None), ('verification', {}), ('access', {}), ('report', {})]:
            result = payload()
            result['data'][field] = value
            with self.subTest(field=field), patch.object(workflow, 'fetch_json', return_value=result), self.assertRaises(workflow.WorkflowError):
                workflow.execute(args())

    def test_article_slug_revision_title_summary(self):
        for field, value in [('slug', 'other'), ('revision', True), ('revision', 0), ('summary', ''), ('title', None)]:
            result = payload()
            result['data']['report'][field] = value
            with self.subTest(field=field), patch.object(workflow, 'fetch_json', return_value=result), self.assertRaises(workflow.WorkflowError):
                workflow.execute(args())
        with patch.object(workflow, 'fetch_json', return_value=payload()), self.assertRaises(workflow.WorkflowError):
            workflow.execute(args('--revision', '2'))

    def test_invalid_input_does_not_contact_server(self):
        for argv in [['report', '--slug', '../private'], ['report', '--slug', 'https://example.com'],
                     ['report', '--slug', 'example-report', '--revision', '0']]:
            with patch.object(workflow, 'fetch_json') as fetch, self.assertRaises(workflow.WorkflowError):
                workflow.execute(workflow.parser().parse_args(argv))
            fetch.assert_not_called()

    def test_failure_not_retried_or_fallback_to_private_archive(self):
        with patch.object(workflow, 'fetch_json', side_effect=workflow.WorkflowError('NOT_FOUND', 'Unavailable')) as fetch, self.assertRaises(workflow.WorkflowError):
            workflow.execute(args())
        self.assertEqual(fetch.call_count, 1)


if __name__ == '__main__':
    unittest.main()
