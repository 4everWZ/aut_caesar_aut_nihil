#!/usr/bin/env python3
"""Report translated Han glyphs absent from the mod's bundled font descriptor."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]


def font_report(root=ROOT, texts=None, descriptor_bytes=None):
    locale = root / 'Aut_Caesar_Aut_Nihil/languages/cns'
    han = set()
    if texts is None:
        texts = [path.read_text(encoding='utf-8-sig') for path in locale.glob('*.csv')]
    for text in texts:
        for row in text.splitlines():
            _, separator, value = row.partition('|')
            if not separator:
                continue
            han.update(ord(c) for c in value if '\u3400' <= c <= '\u9fff' or '\uf900' <= c <= '\ufaff' or '\U00020000' <= c <= '\U000323af')
    path = root / 'Aut_Caesar_Aut_Nihil/Data/font_data.xml'
    data = path.read_bytes() if descriptor_bytes is None else descriptor_bytes
    descriptor = ET.fromstring(data)
    glyphs = {int(element.attrib['code']) for element in descriptor.iter('character')}
    missing = sorted(han - glyphs)
    return dict(translated_han_count=len(han), descriptor_glyph_count=len(glyphs),
        missing_han_count=len(missing), missing_han_codepoints=[f'U+{code:04X}' for code in missing],
        descriptor_sha256=hashlib.sha256(data).hexdigest(),
        interpretation='Descriptor-only check. Game language font fallback, shaders, wrapping and input are untested; no fonts included.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = font_report()
    text = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(text, encoding='utf-8')
    print(f"{report['missing_han_count']} / {report['translated_han_count']} translated Han glyphs absent from bundled descriptor")


if __name__ == '__main__':
    main()
