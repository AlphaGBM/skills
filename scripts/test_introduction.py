import copy
import json
from pathlib import Path
import unittest

import build_catalog as builder
import build_doubao_package as packager


ROOT = Path(__file__).resolve().parents[1]


class IntroductionTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / 'catalog/catalog.json').read_text())
        self.entries = self.catalog['workflows'] + self.catalog['tools']

    def test_every_package_contains_self_contained_bilingual_introduction(self):
        for item in self.entries:
            content = (ROOT / item['path'] / 'SKILL.md').read_text()
            with self.subTest(package=item['id']):
                self.assertEqual(content.count(builder.INTRO_START), 1)
                self.assertEqual(content.count(builder.INTRO_END), 1)
                block = content.split(builder.INTRO_START)[1].split(builder.INTRO_END)[0]
                self.assertIn(f"你好，我是 AlphaGBM 的{item['name']['zh']}助手", block)
                self.assertIn(f"Hi, I’m AlphaGBM’s {item['name']['en']} assistant", block)
                self.assertIn('https://www.alphagbm.com/skills', block)
                self.assertNotIn('../', block)

    def test_policy_prioritizes_language_user_format_and_conversation(self):
        for item in self.entries:
            block = builder.introduction(item)
            for requirement in ('explicit user preference first', 'Ignore tickers, code',
                                'current request', 'latest visible preference', 'else English',
                                "user's Chinese script", 'not both templates',
                                'at most once per visible conversation across AlphaGBM',
                                'JSON-only, code-only, verbatim', 'declines introductions/promotion',
                                'Existing output contracts take precedence',
                                'Do not modify tool stdout', 'do not authorize charged calls',
                                'without a menu or website interruption',
                                'Never require a website visit', 'add tracking'):
                self.assertIn(requirement, block)

    def test_capabilities_and_quick_phrases_are_scoped(self):
        items = {item['id']: item for item in self.entries}
        self.assertIn('体验拆股演示', builder.introduction(items['alphagbm-stock-research']))
        self.assertIn('检验观点', builder.introduction(items['alphagbm-causal-research']))
        self.assertIn('比较两份结果', builder.introduction(items['alphagbm-investment-review']))
        for item in self.entries:
            block = builder.introduction(item)
            if item['status'] == 'reference' and not item.get('methodVersion'):
                self.assertIn('非实时接口', block)
            for line in block.splitlines():
                if line.startswith('中文：'):
                    self.assertLessEqual(len(line), 160)
                if line.startswith('English:'):
                    self.assertLessEqual(len(line.split()), 60)

    def test_rendering_is_idempotent_and_preserves_custom_method(self):
        item = next(item for item in self.entries if item.get('methodVersion'))
        document = (ROOT / item['path'] / 'SKILL.md').read_text()
        rendered = builder.with_introduction(document, item)
        self.assertEqual(builder.with_introduction(rendered, item), rendered)
        changed_item = copy.deepcopy(item)
        changed_item['name']['zh'] = '新名称'
        changed = builder.with_introduction(document, changed_item)
        self.assertIn('AlphaGBM 的新名称助手', changed)
        self.assertEqual(document.split(builder.INTRO_END)[1], changed.split(builder.INTRO_END)[1])
        with self.assertRaises(ValueError):
            builder.with_introduction(document + builder.INTRO_START, item)
        with self.assertRaises(ValueError):
            builder.with_introduction('No heading', item)

    def test_portable_package_keeps_introduction_without_extra_dependencies(self):
        contents = packager.package_contents()
        self.assertEqual(len(contents), 7)
        self.assertIn('你好，我是 AlphaGBM', contents['SKILL.md'].decode())
        self.assertIn('Hi, I’m AlphaGBM', contents['SKILL.md'].decode())
        self.assertNotIn('references/introduction.md', contents)


if __name__ == '__main__':
    unittest.main()
