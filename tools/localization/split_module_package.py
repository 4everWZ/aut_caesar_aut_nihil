#!/usr/bin/env python3
"""Split a verified module ZIP into ordinary ZIP packs; extract ALL into one folder."""
from pathlib import Path, PurePosixPath
import argparse, copy, hashlib, json, zipfile

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('archive',type=Path);ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--part-size-mib',type=int,default=256);args=ap.parse_args()
    if args.part_size_mib<1:ap.error('part size must be positive')
    out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.archive) as source:
        groups=[];group=[];size=0
        for info in source.infolist():
            path=PurePosixPath(info.filename)
            if path.is_absolute() or '..' in path.parts:raise ValueError('Unsafe ZIP path')
            if group and size+info.file_size>args.part_size_mib*1024*1024:groups.append(group);group=[];size=0
            group.append(info);size+=info.file_size
        if group:groups.append(group)
        names=[f'acan-zh-cn-INCOMPLETE-review.part{i:02}.zip' for i in range(1,len(groups)+1)]
        notice=('INCOMPLETE FULL-MODULE REVIEW CANDIDATE\n\nDownload and extract ALL '+str(len(names))+' ZIP packs into the SAME empty folder.\n'
            'These are ordinary ZIP files, not binary split volumes. Do not concatenate them.\n'
            'Each pack contains a different subset of the same Modules/Aut_Caesar_Aut_Nihil tree.\n'
            'After extracting every pack, read START_HERE.txt and Documentation/localization/PACKAGING.md.\n'
            'Three referenced sounds remain absent; this is NOT a complete/verified playable release.\n\nRequired packs:\n'+'\n'.join(names)+'\n').encode()
        results=[]
        for name,group in zip(names,groups):
            path=out/name;temp=path.with_suffix('.zip.tmp')
            with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as target:
                for info in group:target.writestr(copy.copy(info),source.read(info),compresslevel=6)
                zi=zipfile.ZipInfo('READ_ALL_PACKS.txt',source.infolist()[0].date_time);zi.compress_type=zipfile.ZIP_DEFLATED;target.writestr(zi,notice)
            with zipfile.ZipFile(temp) as check:
                assert check.testzip() is None
                for info in group:assert hashlib.sha256(check.read(info.filename)).digest()==hashlib.sha256(source.read(info)).digest()
            temp.replace(path)
            results.append(dict(file=name,bytes=path.stat().st_size,sha256=digest(path),source_members=len(group)))
            print(name,path.stat().st_size,flush=True)
    manifest=dict(complete=False,in_game_tested=False,source_archive=args.archive.name,source_sha256=digest(args.archive),instructions=notice.decode(),parts=results)
    (out/'PACKSET.json').write_text(json.dumps(manifest,indent=2)+'\n');(out/'READ_ALL_PACKS.txt').write_bytes(notice)

if __name__=='__main__':main()
