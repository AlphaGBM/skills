import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SKILL_ID = 'alphagbm-causal-research'
SOURCE_PATH = Path('skills/stocks') / SKILL_ID
PACKAGE_FILES = (
    'SKILL.md',
    'agents/openai.yaml',
    'references/execution.md',
    'references/sectors.md',
    'references/worksheet.md',
    'scripts/calculate.py',
)


def package_contents(root=ROOT):
    source = root / SOURCE_PATH
    contents = {}
    paths = {name: source / name for name in PACKAGE_FILES}
    paths['LICENSE'] = root / 'LICENSE'
    for name, path in sorted(paths.items()):
        relative = path.relative_to(root)
        if any((root / part).is_symlink() for part in (relative, *relative.parents)):
            raise ValueError(f'Symlinks are not allowed in package sources: {name}')
        if not path.is_file():
            raise ValueError(f'Missing package source: {name}')
        contents[name] = path.read_bytes()
    return contents


def build_package(output_dir, root=ROOT):
    contents = package_contents(root)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in contents.items():
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, content, compresslevel=9)
    archive_bytes = buffer.getvalue()
    archive_name = f'{SKILL_ID}.zip'
    manifest = {
        'schemaVersion': 'alphagbm-client-package.v1',
        'skillId': SKILL_ID,
        'sourcePath': SOURCE_PATH.as_posix(),
        'nativeDoubaoImport': 'not_verified',
        'includesPrivateDataOrApiAccess': False,
        'archive': {
            'name': archive_name,
            'sha256': hashlib.sha256(archive_bytes).hexdigest(),
            'bytes': len(archive_bytes),
        },
        'files': [
            {'path': name, 'sha256': hashlib.sha256(content).hexdigest(), 'bytes': len(content)}
            for name, content in contents.items()
        ],
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / archive_name).write_bytes(archive_bytes)
    (output_dir / f'{SKILL_ID}.manifest.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return manifest


def main():
    parser = argparse.ArgumentParser(description='Package the existing portable research method for local skill import.')
    parser.add_argument('--output-dir', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(build_package(args.output_dir), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
