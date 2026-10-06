#!/usr/bin/env python3
"""Build a reproducible, text-only install/review ZIP from a clean local commit."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

from glyphs import font_report

ROOT = Path(__file__).resolve().parents[2]
BASE = '3ed34f35c94c974f9d2a9102750dbb4866e38f6d'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if output == ROOT or ROOT in output.parents:
        parser.error('write the package outside the source checkout')
    if git('status', '--porcelain').strip():
        parser.error('commit/review outstanding changes before packaging')
    subprocess.run([sys.executable, str(Path(__file__).with_name('check.py')), '--check'], cwd=ROOT, check=True)
    git('merge-base', '--is-ancestor', BASE, 'HEAD')
    changed = git('diff', '--name-only', '-z', BASE, 'HEAD').decode().split('\0')
    def allowed(path):
        if path in ('README.md', '.gitattributes', '.github/workflows/localization-prerelease.yml',
                    '.github/workflows/localization-full-module.yml', 'tools/localization/prepare_full_font.sh'):
            return True
        if path.startswith('tools/localization/font_candidate/'):
            return Path(path).suffix in ('.dds', '.xml', '.txt', '.json', '.png')
        if path.startswith('Aut_Caesar_Aut_Nihil/languages/cns/'):
            return Path(path).suffix == '.csv'
        return (path.startswith(('docs/localization/', 'tools/localization/'))
                and (Path(path).suffix in ('.md', '.json', '.py') or Path(path).name == '.gitignore'))
    unexpected = [name for name in changed if name and not allowed(name)]
    if unexpected:
        parser.error('patch contains non-localization paths: ' + ', '.join(unexpected))
    tracked = set(git('ls-files', '-z').decode().split('\0'))
    def committed_bytes(path):
        name = path.relative_to(ROOT).as_posix()
        if name not in tracked:
            parser.error('untracked/ignored package input: ' + name)
        return git('show', 'HEAD:' + name)
    commit = git('rev-parse', 'HEAD').decode().strip()
    stamp = datetime.fromtimestamp(int(git('show', '-s', '--format=%ct', 'HEAD')), timezone.utc)
    payload = {}
    for path in sorted((ROOT / 'Aut_Caesar_Aut_Nihil/languages/cns').glob('*.csv')):
        payload['Modules/Aut_Caesar_Aut_Nihil/languages/cns/' + path.name] = committed_bytes(path)
    for path in sorted((ROOT / 'docs/localization').glob('*')):
        if path.is_file() and path.suffix in ('.md', '.json'):
            payload['Documentation/localization/' + path.name] = committed_bytes(path)
    payload['Review/font-coverage.json'] = (json.dumps(font_report(texts=[data.decode('utf-8-sig') for name, data in payload.items() if name.endswith('.csv')], descriptor_bytes=committed_bytes(ROOT / 'Aut_Caesar_Aut_Nihil/Data/font_data.xml')), indent=2) + '\n').encode()
    payload['LICENSE'] = committed_bytes(ROOT / 'LICENSE')
    patch = git('diff', '--binary', BASE, 'HEAD')
    payload['Review/acan-zh-cn.patch'] = patch
    payload['Review/build.json'] = (json.dumps(dict(base_commit=BASE, commit=commit,
        branch=git('branch', '--show-current').decode().strip(), runtime_locale='cns',
        language='zh_CN', in_game_tested=False,
        fonts_included=False, shaders_included=False), indent=2) + '\n').encode()
    payload['START_HERE.txt'] = (
        'Aut Caesar Aut Nihil — 简体中文本地化（部分完成）\n'
        'Simplified Chinese localization — partial, no in-game QA\n\n'
        '1. 请先安装与基准提交匹配的原版模组，并备份已有中文语言目录。\n'
        '   Install the matching original mod first; back up any existing cns folder.\n'
        '2. 将本压缩包 Modules 内的文件夹合并到战团的 Modules 目录。\n'
        '   Merge this archive’s Modules folder into the game’s Modules directory.\n'
        '3. 在启动器选择简体中文和 ACAN 模组。\n'
        '   Select Simplified Chinese and the ACAN module in the launcher.\n'
        '4. 模组自带字体不含汉字。请先阅读 Documentation/localization/FONT_OPTIONS.md。\n'
        '   The bundled mod font lacks Chinese glyphs. Read FONT_OPTIONS.md before testing.\n'
        '   此包不附带字体、着色器或游戏文件，不自动修改字体设置。\n'
        '   This package contains no fonts, shaders or gameplay files and makes no automatic font changes.\n\n'
        'Coverage, unresolved terms and installation: Documentation/localization/README.md\n'
        'Review patch (for developers, not needed to install): Review/acan-zh-cn.patch\n'
        f'Source baseline: {BASE}\nBuild commit: {commit}\n'
    ).encode('utf-8-sig')
    sums = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
    payload['SHA256SUMS'] = ''.join(f'{digest}  {name}\n' for name,digest in sorted(sums.items())).encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + '.tmp')
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, data in sorted(payload.items()):
                info = zipfile.ZipInfo(name, date_time=stamp.timetuple()[:6])
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data, compresslevel=9)
        with zipfile.ZipFile(temporary) as archive:
            if archive.testzip() is not None:
                raise ValueError('ZIP CRC verification failed')
            for name, digest in sums.items():
                if hashlib.sha256(archive.read(name)).hexdigest() != digest:
                    raise ValueError(f'ZIP content mismatch: {name}')
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    print(json.dumps(dict(path=str(output), size_bytes=output.stat().st_size,
                         sha256=hashlib.sha256(output.read_bytes()).hexdigest(), files=len(payload))))


if __name__ == '__main__':
    main()
