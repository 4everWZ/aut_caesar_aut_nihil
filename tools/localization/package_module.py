#!/usr/bin/env python3
"""Build an untested full-module installer preserving the pinned upstream runtime."""
from pathlib import Path
import argparse, hashlib, json, subprocess, zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
MODULE = 'Aut_Caesar_Aut_Nihil'
FONT = ROOT / 'tools/localization/font_candidate'
EXCLUDE = {'fxc.exe', 'compile_fx.bat'}
BASE = '3ed34f35c94c974f9d2a9102750dbb4866e38f6d'

def classify_missing(audit):
    # Missing upstream audio is disclosed, not silently substituted or fatal to packaging.
    return (audit['module_resources']['missing'] + audit['compiled_tables']['missing'],
            audit['unknown_external_sounds'])

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def archive_path(relative):
    parts = Path(relative).parts
    if not parts or parts[0] != MODULE or '..' in parts:
        raise ValueError('Not a safe module-relative file')
    if '/'.join(parts[1:]) in EXCLUDE:
        return None
    return 'Modules/' + relative

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--allow-incomplete-review', action='store_true', help='Explicitly permit documented missing dependencies; package remains INCOMPLETE')
    ap.add_argument('--font-dir', type=Path, default=FONT, help='Validated generated OFL font directory outside the checkout')
    args = ap.parse_args()
    output = args.output.resolve()
    if output == ROOT or ROOT in output.parents:
        ap.error('Output must be outside the checkout')
    if git('status', '--porcelain').strip():
        ap.error('Commit reviewed changes before packaging')
    audit = json.loads((ROOT/'docs/localization/asset_audit.json').read_text())
    structural_missing, missing = classify_missing(audit)
    if audit['lfs_pointers']:
        ap.error('LFS pointers cannot be packaged as assets')
    if structural_missing:
        ap.error('Missing runtime structure: ' + ', '.join(structural_missing))
    git('merge-base', '--is-ancestor', BASE, 'HEAD')
    changed = git('diff', '--name-only', BASE, 'HEAD', '--', MODULE).decode().splitlines()
    unexpected = [name for name in changed if not name.startswith(MODULE+'/languages/cns/')]
    if unexpected:
        ap.error('Upstream runtime changed: ' + ', '.join(unexpected))
    font = args.font_dir.resolve()
    for name in ('Data/font_data.xml', 'Textures/font.dds', 'OFL.txt', 'font_report.json'):
        if not (font/name).is_file():
            ap.error('Missing font candidate: ' + name)
    report = json.loads((font/'font_report.json').read_text())
    for name, digest in report['output_sha256'].items():
        if hashlib.sha256((font/name).read_bytes()).hexdigest() != digest:
            ap.error('Font output checksum mismatch: ' + name)
    if report['missing_required'] or report['missing_gb2312']:
        ap.error('Generated font lacks required glyphs')
    for name, digest in report['inputs'].items():
        if hashlib.sha256(git('show', 'HEAD:' + name)).hexdigest() != digest:
            ap.error('Font generated for different translation input: ' + name)
    if (font/'OFL.txt').read_bytes() != git('show', 'HEAD:tools/localization/font_candidate/OFL.txt'):
        ap.error('Font license must match the committed complete OFL notice')
    commit = git('rev-parse','HEAD').decode().strip()
    stamp = datetime.fromtimestamp(int(git('show','-s','--format=%ct','HEAD')),timezone.utc).timetuple()[:6]
    tracked = git('ls-files','-z').decode().split('\0')
    entries = {}
    for name in tracked:
        if name.startswith(MODULE+'/'):
            target=archive_path(name)
            if target:
                # Retain exact baseline runtime bytes; only translation and font overlays differ.
                entries[target]=ROOT/name
    # Deliberate packaging-only font substitution; source mod font is unchanged.
    entries[f'Modules/{MODULE}/Data/font_data.xml']=font/'Data/font_data.xml'
    entries[f'Modules/{MODULE}/Textures/font.dds']=font/'Textures/font.dds'
    entries[f'Modules/{MODULE}/LICENSE']=ROOT/'LICENSE'
    entries[f'Modules/{MODULE}/UPSTREAM_README.md']=ROOT/'README.md'
    entries[f'Modules/{MODULE}/FONT_OFL.txt']=font/'OFL.txt'
    entries[f'Modules/{MODULE}/THIRD_PARTY_NOTICES.md']=ROOT/'docs/localization/REDISTRIBUTION.md'
    for name in tracked:
        if name.startswith('docs/localization/') and Path(name).suffix in ('.md','.json'):
            entries['Documentation/'+name.removeprefix('docs/')]=ROOT/name
    entries['Review/font_report.json']=font/'font_report.json'
    sums={}
    metadata=dict(commit=commit,base_commit='3ed34f35c94c974f9d2a9102750dbb4866e38f6d',
        package_kind='full_module_untested_installer',
        in_game_tested=False,upstream_missing_audio=missing,public_redistribution='Roman Models Extravaganza category/permission confirmation pending',
        excluded_build_tools=sorted(EXCLUDE),font='OFL Chinese atlas candidate; untested in engine',gameplay_modified=False)
    status='完整模组汉化安装包 / FULL MODULE LOCALIZED INSTALLER — 未实机测试 / NOT IN-GAME TESTED'
    notice=(status+'\n\nContains the full tracked module runtime tree, not merely a language overlay.\n'
        'Unresolved audio inputs: '+', '.join(missing)+'\n'
        'These sounds are absent from the preserved upstream baseline; no substitutes or gameplay edits are made. Runtime impact is unverified.\n'
        'User-authorized prerelease publication; the Roman Models Extravaganza permission/category remains unconfirmed; see details in ROMAN_MODELS_PERMISSION.md.\n'
        'For controlled testing, copy Modules/Aut_Caesar_Aut_Nihil into the game Modules directory, after backing up any existing module.\n'
        'Requires a lawful Warband installation and its Native/CommonRes resources; those game assets are not included.\n'
        'Select Simplified Chinese. The included OFL Chinese font is a static-checked candidate, not in-game validated.\n'
        'Game logic and upstream assets remain unchanged except the two packaged font files. No executable compiler is included.\n'
        'See Documentation/localization/PACKAGING.md, ASSET_AUDIT.md, REDISTRIBUTION.md and FONT_CANDIDATE.md.\n').encode('utf-8-sig')
    output.parent.mkdir(parents=True,exist_ok=True)
    temp=output.with_suffix(output.suffix+'.tmp')
    def write_bytes(z,name,data):
        zi=zipfile.ZipInfo(name,stamp);zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=0o100644<<16
        z.writestr(zi,data,compresslevel=6);sums[name]=hashlib.sha256(data).hexdigest()
    try:
        with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
            for name,p in sorted(entries.items()):
                if p.is_symlink():raise ValueError('Symlink input: '+str(p))
                relative = p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else None
                write_bytes(z,name,git('show','HEAD:'+relative) if relative else p.read_bytes())
            write_bytes(z,'START_HERE.txt',notice)
            write_bytes(z,'Review/build.json',(json.dumps(metadata,indent=2)+'\n').encode())
            write_bytes(z,'SHA256SUMS',''.join(f'{v}  {k}\n' for k,v in sorted(sums.items())).encode())
        with zipfile.ZipFile(temp) as z:
            assert z.testzip() is None
            for name,digest in sums.items():
                assert hashlib.sha256(z.read(name)).hexdigest()==digest,name
            assert f'Modules/{MODULE}/module.ini' in z.namelist()
            assert not any(n.endswith('/fxc.exe') for n in z.namelist())
        if git('status','--porcelain').strip():raise ValueError('Checkout changed during packaging')
        temp.replace(output)
    finally:
        temp.unlink(missing_ok=True)
    from split_module_package import digest
    print(json.dumps(dict(path=str(output),size_bytes=output.stat().st_size,sha256=digest(output),files=len(sums),**metadata),ensure_ascii=False))

if __name__=='__main__':main()
