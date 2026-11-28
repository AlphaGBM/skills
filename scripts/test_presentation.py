import json
from pathlib import Path
import unittest

import build_catalog as builder
import build_doubao_package as packager


ROOT = Path(__file__).resolve().parents[1]


class PresentationTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / 'catalog/catalog.json').read_text())
        self.entries = self.catalog['workflows'] + self.catalog['tools']

    def test_all_packages_have_inline_policy_after_introduction(self):
        for item in self.entries:
            document = (ROOT / item['path'] / 'SKILL.md').read_text()
            with self.subTest(package=item['id']):
                self.assertEqual(document.count(builder.PRESENTATION_START), 1)
                self.assertEqual(document.count(builder.PRESENTATION_END), 1)
                self.assertIn(builder.PRESENTATION, document)
                self.assertLess(document.index(builder.INTRO_END),
                                document.index(builder.PRESENTATION_START))
                self.assertNotIn('../', builder.PRESENTATION)

    def test_generated_policy_is_idempotent_and_preserves_method_body(self):
        item = next(item for item in self.entries if item.get('methodVersion'))
        document = (ROOT / item['path'] / 'SKILL.md').read_text()
        rendered = builder.with_presentation(document)
        self.assertEqual(rendered, document)
        self.assertEqual(builder.with_presentation(rendered), rendered)
        before, tail = document.split(builder.PRESENTATION_START)
        block, after = tail.split(builder.PRESENTATION_END)
        without_policy = before.rstrip() + after
        self.assertEqual(builder.with_presentation(without_policy), document)
        stale = before + builder.PRESENTATION_START + '\nold policy\n' + builder.PRESENTATION_END + after
        self.assertEqual(builder.with_presentation(stale), document)

    def test_invalid_markers_fail_without_dropping_content(self):
        for document in ('missing anchor', builder.PRESENTATION_START,
                         builder.PRESENTATION_END,
                         builder.PRESENTATION_END + builder.PRESENTATION_START,
                         builder.PRESENTATION * 2):
            with self.subTest(document=document):
                with self.assertRaises(ValueError):
                    builder.with_presentation(document)

    def test_output_boundaries_and_evidence_are_retained(self):
        for requirement in ('output contracts take precedence', 'runner stdout and evidence unchanged',
                            'simple questions directly', 'up to three supported findings',
                            'at most two heading levels', 'at most three columns',
                            'source locator beside each', 'actual calculation receipts',
                            'hypothetical reversal condition', 'required retracted conclusions',
                            'planned, available and actually used', 'obtain permission before saving',
                            'after the useful result', 'including any introduction link'):
            self.assertIn(requirement, builder.PRESENTATION)

    def test_portable_package_contains_path_and_policy_without_extra_files(self):
        contents = packager.package_contents()
        self.assertEqual(len(contents), 7)
        self.assertIn(builder.PRESENTATION, contents['SKILL.md'].decode())
        execution = contents['references/execution.md'].decode()
        for requirement in ('利润质量快查', '少数股东口径差异', '保留原始精度',
                            '期末余额变化与现金流调节项目', '净利润为零或负数',
                            '实际找能削弱主解释的证据', '不退回合成拆股演示'):
            self.assertIn(requirement, execution)

    def test_examples_do_not_present_assumptions_as_executed_research(self):
        document = (ROOT / 'docs/PRESENTATION.md').read_text()
        self.assertIn('不是公司研究、真实来源或脚本运行回执', document)
        self.assertIn('not company research, a real source or an execution receipt', document)
        self.assertIn('Simulations are not fresh Doubao/WorkBuddy client acceptance tests', document)


if __name__ == '__main__':
    unittest.main()
