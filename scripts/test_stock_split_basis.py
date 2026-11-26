from decimal import Decimal
import json
import re
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'demo/stock-split-basis.json'
EXPLANATION = ROOT / 'demo/STOCK_SPLIT_BASIS.md'


def to_post_split(value, basis, new_shares_per_old_share):
    if basis == 'post_split':
        return value
    if basis == 'pre_split' and new_shares_per_old_share is not None:
        return value / new_shares_per_old_share
    return None


def percent_change(old, new):
    if old is None or new is None:
        return None
    return (new - old) / old * Decimal('100')


class StockSplitBasisTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads(FIXTURE.read_text())
        self.ratio = Decimal(self.payload['split']['newSharesPerOldShare'])
        self.targets = {item['id']: item for item in self.payload['targets']}

    def normalized(self, target_id):
        target = self.targets[target_id]
        return to_post_split(Decimal(target['value']), target['basis'], self.ratio)

    def test_fixture_is_explicitly_synthetic_and_fictional(self):
        demo = self.payload['demo']
        self.assertEqual(demo['status'], 'illustrative_fixture')
        for flag in ('synthetic', 'notForTrading', 'notLiveQuote',
                     'notInvestmentRecommendation', 'notPaidWorkflowEvidence'):
            self.assertIs(demo[flag], True, flag)
        self.assertTrue(self.payload['company']['fictional'])
        self.assertIsNone(self.payload['company']['symbol'])

    def test_units_and_split_basis_are_explicit(self):
        split = self.payload['split']
        self.assertEqual(split['label'], '4-for-1')
        self.assertEqual(self.ratio, Decimal('4'))
        self.assertEqual((split['beforeBasis'], split['afterBasis']), ('pre_split', 'post_split'))
        for target in self.payload['targets']:
            unit = split['beforeUnit'] if target['basis'] == 'pre_split' else split['afterUnit']
            self.assertEqual(target['unit'], unit)
        for result in self.payload['normalization']['results']:
            self.assertEqual(result['unit'], split['afterUnit'])

    def test_normalization_to_post_split_basis(self):
        self.assertEqual(self.normalized('T1'), Decimal('30'))
        self.assertEqual(self.normalized('T2'), Decimal('27'))
        for result in self.payload['normalization']['results']:
            self.assertEqual(Decimal(result['normalizedValue']), self.normalized(result['id']))

    def test_split_adjustment_alone_is_not_a_downgrade(self):
        comparison = self.payload['comparisons'][0]
        before = Decimal(self.targets['T1']['value'])
        self.assertEqual(percent_change(self.normalized('T1'), Decimal(comparison['toValue'])), 0)
        self.assertEqual(Decimal(comparison['sameBasisChangePercent']), 0)
        self.assertEqual(percent_change(before, Decimal(comparison['toValue'])),
                         Decimal(comparison['mistakenRawChangePercent']))
        self.assertEqual(Decimal(comparison['mistakenRawChangePercent']), Decimal('-75'))

    def test_later_target_is_ten_percent_below_thirty_not_one_twenty(self):
        comparison = self.payload['comparisons'][1]
        change = percent_change(self.normalized('T1'), self.normalized('T2'))
        self.assertEqual(change, Decimal('-10'))
        self.assertEqual(Decimal(comparison['fromValue']), self.normalized('T1'))
        self.assertEqual(Decimal(comparison['toValue']), self.normalized('T2'))
        self.assertEqual(Decimal(comparison['sameBasisChangePercent']), change)
        mixed_basis = percent_change(Decimal(self.targets['T1']['value']), self.normalized('T2'))
        self.assertEqual(mixed_basis, Decimal('-77.5'))
        self.assertEqual(Decimal(comparison['mistakenRawChangePercent']), mixed_basis)

    def test_missing_split_information_remains_unknown(self):
        missing = self.payload['missingSplitInformation']
        self.assertEqual(missing['status'], 'unknown')
        self.assertEqual(missing['basis'], 'unknown')
        self.assertIsNone(missing['newSharesPerOldShare'])
        self.assertIsNone(missing['normalizedValue'])
        self.assertIsNone(missing['sameBasisChangePercent'])
        value = Decimal(missing['value'])
        self.assertIsNone(to_post_split(value, missing['basis'], None))
        self.assertIsNone(to_post_split(value, 'pre_split', None))
        self.assertIsNone(percent_change(self.normalized('T1'), to_post_split(value, 'unknown', None)))

    def test_explanation_is_bilingual_linked_and_offline(self):
        explanation = ' '.join(EXPLANATION.read_text().split())
        for text in ('## English', '## 中文', '120 / 4 = 30', '(27 - 30) / 30 x 100',
                     'not a live market quote', 'not an investment recommendation',
                     'not evidence that a paid workflow has run', 'unknown',
                     '不是实时行情', '不构成投资建议', '未知'):
            self.assertIn(text, explanation)
        self.assertNotRegex(EXPLANATION.read_text() + FIXTURE.read_text(), r'https?://')
        readme = (ROOT / 'demo/README.md').read_text()
        for target in ('STOCK_SPLIT_BASIS.md', 'stock-split-basis.json'):
            self.assertIn(f']({target})', readme)
        for document in (EXPLANATION, ROOT / 'demo/README.md'):
            for target in re.findall(r'\]\(([^)]+)\)', document.read_text()):
                if '://' not in target and not target.startswith('#'):
                    self.assertTrue((document.parent / target.split('#', 1)[0]).exists(),
                                    f'{document.name}: {target}')


if __name__ == '__main__':
    unittest.main()
