import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

import build_doubao_package as builder


class DoubaoPackageTests(unittest.TestCase):
    def test_archive_is_flat_self_contained_and_matches_source(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = builder.build_package(directory)
            with zipfile.ZipFile(Path(directory) / manifest['archive']['name']) as archive:
                self.assertEqual(set(archive.namelist()), set(builder.PACKAGE_FILES) | {'LICENSE'})
                for name, content in builder.package_contents().items():
                    self.assertEqual(archive.read(name), content)
                for name in archive.namelist():
                    self.assertFalse(name.startswith('/') or '..' in Path(name).parts)
                    self.assertEqual(archive.getinfo(name).external_attr >> 16, 0o100644)

    def test_manifest_hashes_and_deterministic_build(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            first = builder.build_package(output / 'first')
            second = builder.build_package(output / 'second')
            self.assertEqual(first, second)
            archive_bytes = (output / 'first' / first['archive']['name']).read_bytes()
            self.assertEqual(hashlib.sha256(archive_bytes).hexdigest(), first['archive']['sha256'])
            self.assertEqual(len(archive_bytes), first['archive']['bytes'])
            for entry in first['files']:
                content = builder.package_contents()[entry['path']]
                self.assertEqual(hashlib.sha256(content).hexdigest(), entry['sha256'])
                self.assertEqual(len(content), entry['bytes'])
            self.assertEqual(first['nativeDoubaoImport'], 'not_verified')
            self.assertFalse(first['includesPrivateDataOrApiAccess'])

    def test_installed_calculator_runs_without_other_packages(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            manifest = builder.build_package(output)
            installed = output / 'installed'
            with zipfile.ZipFile(output / manifest['archive']['name']) as archive:
                archive.extractall(installed)
            calculator = installed / 'scripts/calculate.py'
            for values, code, expected in [(['84', '126'], 0, '-42'), (['NaN', '126'], 1, None)]:
                payload = {'operation': 'difference', 'values': values, 'unit': 'CNY million', 'evidenceIds': ['E1', 'E2']}
                result = subprocess.run([sys.executable, '-I', '-B', str(calculator)],
                                        input=json.dumps(payload), text=True, capture_output=True,
                                        cwd=output, env={'PATH': os.environ['PATH']})
                self.assertEqual(result.returncode, code)
                actual = json.loads(result.stdout or result.stderr)
                if expected is not None:
                    self.assertEqual(actual['result'], expected)
                    self.assertFalse(actual['inputFactsVerified'])
                else:
                    self.assertEqual(actual['status'], 'error')

    def test_all_local_markdown_links_stay_inside_package(self):
        contents = builder.package_contents()
        for name, content in contents.items():
            if not name.endswith('.md'):
                continue
            for target in re.findall(r'\]\(([^)]+)\)', content.decode()):
                if '://' in target or target.startswith('#'):
                    continue
                relative = (Path(name).parent / target.split('#', 1)[0]).as_posix()
                self.assertIn(relative, contents, f'{name}: {target}')

    def test_only_allowlisted_files_are_packaged(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(builder.ROOT / builder.SOURCE_PATH, root / builder.SOURCE_PATH)
            shutil.copy2(builder.ROOT / 'LICENSE', root / 'LICENSE')
            (root / builder.SOURCE_PATH / '.env').write_text('PRIVATE_TEST_SENTINEL')
            (root / builder.SOURCE_PATH / 'scripts/run.py').write_text('PRIVATE_TEST_SENTINEL')
            contents = builder.package_contents(root)
            self.assertNotIn('.env', contents)
            self.assertNotIn('scripts/run.py', contents)
            self.assertFalse(any(b'PRIVATE_TEST_SENTINEL' in content for content in contents.values()))

    def test_missing_or_symlinked_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(builder.ROOT / builder.SOURCE_PATH, root / builder.SOURCE_PATH)
            shutil.copy2(builder.ROOT / 'LICENSE', root / 'LICENSE')
            calculator = root / builder.SOURCE_PATH / 'scripts/calculate.py'
            calculator.unlink()
            with self.assertRaisesRegex(ValueError, 'Missing package source'):
                builder.build_package(root / 'output', root)
            calculator.symlink_to(builder.ROOT / builder.SOURCE_PATH / 'scripts/calculate.py')
            with self.assertRaisesRegex(ValueError, 'Symlinks are not allowed'):
                builder.build_package(root / 'output', root)
            self.assertFalse((root / 'output').exists())

    def test_guidance_does_not_substitute_another_host_or_claim_native_support(self):
        execution = (builder.ROOT / builder.SOURCE_PATH / 'references/execution.md').read_text()
        self.assertIn('不要求另装或调用Codex', execution)
        self.assertIn('下载、解压或建一个目录不等于注册', execution)
        self.assertIn('计算未执行', execution)
        guide = (builder.ROOT / 'docs/DOUBAO.md').read_text()
        self.assertIn('跨会话自动调用尚未验收', guide)
        self.assertIn('不开放 AlphaGBM 内部研报库', guide)
        self.assertIn('本次会话的文件工作流', guide)

    def test_packaged_method_routes_missing_materials_without_implied_consent(self):
        contents = builder.package_contents()
        skill = contents['SKILL.md'].decode()
        execution = contents['references/execution.md'].decode()
        self.assertIn('资料入口', skill)
        for requirement in ('已有文件', '无文件且未授权检索', '已授权公开检索',
                            '工具不可用或取证失败', '上传材料／授权公开原件检索',
                            '不等于同意联网', '用户未选择前不检索',
                            '不重复索要同一授权', '只有文件授权时，不额外联网'):
            self.assertIn(requirement, execution)

    def test_packaged_method_requires_small_real_research_with_boundaries(self):
        execution = builder.package_contents()['references/execution.md'].decode()
        for requirement in ('1—3份关键原件', '不晚于截止日发布', '不编造数字',
                            '反证清单不是反证检索', '被推翻的结论', '实际尝试',
                            '不借其他AI客户端', '额外付费、登录、私有来源',
                            '不重复做安装和合成演示'):
            self.assertIn(requirement, execution)

    def test_guide_has_explicit_public_mode_and_consistent_onboarding_downloads(self):
        guide = (builder.ROOT / 'docs/DOUBAO.md').read_text()
        for requirement in ('允许你用当前宿主自己的工具', '尚未明确的事项',
                            '没有文件且未授权检索', '不登录、不付费、不外传我的材料',
                            '不要混用两个版本的包与清单'):
            self.assertIn(requirement, guide)
        release_tags = re.findall(r'releases/(?:download|tag)/([^/\s)]+)', guide)
        self.assertEqual(len(release_tags), 5)
        self.assertEqual(set(release_tags), {'skills-onboarding-v1'})

    def test_cli_emits_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(Path(builder.__file__)), '--output-dir', directory],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads(result.stdout)
            saved = json.loads((Path(directory) / f'{builder.SKILL_ID}.manifest.json').read_text())
            self.assertEqual(manifest, saved)


if __name__ == '__main__':
    unittest.main()
