#!/usr/bin/env python3
"""Build a full-tree review candidate, never silently label missing assets complete."""
from pathlib import Path
import argparse, hashlib, json, subprocess, zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
MODULE = 'Aut_Caesar_Aut_Nihil'
FONT = ROOT / 'tools/localization/font_candidate'
EXCLUDE = {'fxc.exe', 'compile_fx.bat'}

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
    args = ap.parse_args()
    output = args.output.resolve()
    if output == ROOT or ROOT in output.parents:
        ap.error('Output must be outside the checkout')
    if git('status', '--porcelain').strip():
        ap.error('Commit reviewed changes before packaging')
    audit = json.loads((ROOT/'docs/localization/asset_audit.json').read_text())
    missing = audit['module_resources']['missing'] + audit['compiled_tables']['missing'] + audit['unknown_external_sounds']
    if audit['lfs_pointers']:
        ap.error('LFS pointers cannot be packaged as assets')
    if missing and not args.allow_incomplete_review:
        ap.error('Unresolved required inputs: ' + ', '.join(missing) + '; use --allow-incomplete-review only for an explicitly incomplete review bundle')
    for name in ('font_data.xml', 'font.dds', 'OFL.txt', 'font_report.json'):
        if not (FONT/name).is_file():
            ap.error('Missing font candidate: ' + name)
    commit = git('rev-parse','HEAD').decode().strip()
    stamp = datetime.fromtimestamp(int(git('show','-s','--format=%ct','HEAD')),timezone.utc).timetuple()[:6]
    tracked = git('ls-files','-z').decode().split('\0')
    if any(str((FONT/name).relative_to(ROOT)) not in tracked for name in ('font_data.xml','font.dds','OFL.txt','font_report.json')):
        ap.error('Font inputs must be tracked and committed')
    entries = {}
    for name in tracked:
        if name.startswith(MODULE+'/'):
            target=archive_path(name)
            if target: entries[target]=ROOT/name
    # Deliberate packaging-only font substitution; source mod font is unchanged.
    entries[f'Modules/{MODULE}/Data/font_data.xml']=FONT/'font_data.xml'
    entries[f'Modules/{MODULE}/Textures/font.dds']=FONT/'font.dds'
    entries[f'Modules/{MODULE}/LICENSE']=ROOT/'LICENSE'
    entries[f'Modules/{MODULE}/UPSTREAM_README.md']=ROOT/'README.md'
    entries[f'Modules/{MODULE}/FONT_OFL.txt']=FONT/'OFL.txt'
    for name in tracked:
        if name.startswith('docs/localization/') and Path(name).suffix in ('.md','.json'):
            entries['Documentation/'+name.removeprefix('docs/')]=ROOT/name
    entries['Review/font_report.json']=FONT/'font_report.json'
    entries['Review/font-preview.png']=FONT/'comparison.png'
    sums={}
    metadata=dict(commit=commit,base_commit='3ed34f35c94c974f9d2a9102750dbb4866e38f6d',
        package_kind='full_tree_incomplete_review_candidate' if missing else 'full_tree_untested_prerelease_candidate',
        complete=False if missing else None,in_game_tested=False,unresolved_inputs=missing,
        excluded_build_tools=sorted(EXCLUDE),font='OFL Chinese atlas candidate; untested in engine',gameplay_modified=False)
    status='INCOMPLETE REVIEW BUNDLE — NOT A VERIFIED INSTALLABLE RELEASE' if missing else 'UNTESTED PRERELEASE CANDIDATE'
    notice=(status+'\n\nContains the full tracked module runtime tree, not merely a language overlay.\n'
        'Unresolved audio inputs: '+', '.join(missing)+'\n'
        'Do not publish this as a complete or verified-playable module. Obtain missing assets or verified installed-game fallback evidence first.\n'
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
                write_bytes(z,name,p.read_bytes())
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
