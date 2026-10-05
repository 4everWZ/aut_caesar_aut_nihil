#!/usr/bin/env python3
"""Build an UNTESTED optional ACAN Chinese bitmap-font candidate from OFL outlines.
No game assets are copied. Requires Pillow and fontTools. See docs/localization/FONT_CANDIDATE.md.
Metric correspondence: Swyter's primary Mount&Blade BMFont converter
https://github.com/Swyter/swyter.bitbucket.org/blob/master/index.html#L81-L101
This is an independent rasterizer implementation, not copied converter code.
"""
import argparse,hashlib,json,sys,xml.etree.ElementTree as ET
from pathlib import Path
import PIL,fontTools
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops,features
from fontTools.ttLib import TTCollection,TTFont

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--root',type=Path,required=True)
 p.add_argument('--cjk-font',type=Path,required=True)
 p.add_argument('--latin-font',type=Path,required=True)
 p.add_argument('--face-index',type=int,default=2)
 p.add_argument('--out',type=Path,required=True)
 p.add_argument('--license-file',type=Path,required=True,help='Full OFL and both original copyright notices; copied into output')
 a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 license_text=a.license_file.read_text()
 assert 'SIL OPEN FONT LICENSE Version 1.1' in license_text and 'Adobe' in license_text and 'Google' in license_text
 (a.out/'OFL.txt').write_text(license_text)
 primary=TTCollection(a.cjk_font).fonts[a.face_index];secondary=TTFont(a.latin_font)
 assert primary['name'].getDebugName(1)=='Noto Sans CJK SC','Select Simplified Chinese face explicitly'
 for f in (primary,secondary):assert 'Open Font License' in f['name'].getDebugName(13)
 sys.path.insert(0,str(a.root/'tools/localization'));import check
 source_records=check.inventory()[0]
 source=''.join(r['text'] for r in source_records)
 files=sorted((a.root/'Aut_Caesar_Aut_Nihil/languages/cns').glob('*.csv'))
 target=''.join(l.split('|',1)[1] for f in files for l in f.read_text(encoding='utf-8-sig').splitlines() if '|' in l)
 required={ord(c) for c in source+target if c.isprintable()}
 gb=set()
 for lead in range(0xa1,0xf8):
  for trail in range(0xa1,0xff):
   try:c=bytes((lead,trail)).decode('gb2312')
   except UnicodeDecodeError:continue
   if c.isprintable():gb.add(ord(c))
 repertoire=required|gb|set(range(32,127))
 maps=[primary.getBestCmap(),secondary.getBestCmap()]
 missing=repertoire-maps[0].keys()-maps[1].keys()
 assert not missing, sorted(missing)
 fonts=[ImageFont.truetype(str(a.cjk_font),40,index=a.face_index),ImageFont.truetype(str(a.latin_font),40)]
 ascent=fonts[0].getmetrics()[0];pad=3;size=4096;gap=1
 glyphs=[]
 for code in sorted(repertoire):
  fi=0 if code in maps[0] else 1;f=fonts[fi];ch=chr(code)
  # 'ls' explicitly anchors at a common baseline; a second face never shifts the line.
  x0,y0,x1,y1=f.getbbox(ch,anchor='ls');w=max(1,x1-x0+2*pad);h=max(1,y1-y0+2*pad)
  im=Image.new('L',(w,h));ImageDraw.Draw(im).text((pad-x0,pad-y0),ch,font=f,anchor='ls',fill=255)
  glyphs.append(dict(code=code,mask=im,w=w,h=h,preshift=x0-pad,yadjust=-y0+pad,postshift=round(f.getlength(ch)),face=fi))
 # Tallest-first shelf packing is deterministic and leaves one transparent pixel between rectangles.
 x=y=rowheight=0
 for g in sorted(glyphs,key=lambda g:(-g['h'],-g['w'],g['code'])):
  if x+g['w']>size:x=0;y+=rowheight+gap;rowheight=0
  assert y+g['h']<=size,'Atlas overflow: do not silently increase GPU texture size'
  g.update(x=x,y=y);x+=g['w']+gap;rowheight=max(rowheight,g['h'])
 alpha=Image.new('L',(size,size));outline=Image.new('L',(size,size))
 for g in glyphs:
  alpha.paste(g['mask'],(g['x'],g['y']))
  outline.paste(g['mask'].filter(ImageFilter.MaxFilter(3)),(g['x'],g['y']))
 # HLSL: alpha=fill, inverse red=outline ring; fill RGB stays white for map_font.
 # Therefore (1-red)+alpha=complete outline coverage, without double-counting fill.
 rgb=ImageChops.invert(ImageChops.subtract(outline,alpha))
 atlas=Image.merge('RGBA',(rgb,rgb,rgb,alpha))
 texture=a.out/'Textures/font.dds';texture.parent.mkdir(exist_ok=True)
 # Uncompressed 32-bit DDS avoids lossy outline artifacts and DX10-only compressed formats.
 atlas.save(texture,format='DDS')
 xml=ET.Element('FontData',dict(width=str(size),height=str(size),padding=str(2*pad),font_size=str(ascent),font_scale='100',line_spacing='100'))
 detail=ET.SubElement(xml,'FontDetails')
 for g in glyphs:
  ET.SubElement(detail,'character',{k:str(v) for k,v in dict(code=g['code'],page=0,u=g['x'],v=g['y'],w=g['x']+g['w'],h=g['y']+g['h'],preshift=g['preshift'],yadjust=g['yadjust'],postshift=g['postshift']).items()})
 ET.indent(xml);descriptor=a.out/'Data/font_data.xml';descriptor.parent.mkdir(exist_ok=True)
 ET.ElementTree(xml).write(descriptor,encoding='utf-8',xml_declaration=True)
 # Independent artifact validation, including the actual DDS round trip.
 reopened=Image.open(texture);assert reopened.size==(size,size) and reopened.mode=='RGBA'
 assert reopened.tobytes()==atlas.tobytes()
 chars=ET.parse(descriptor).getroot().findall('.//character');codes=[int(g.get('code')) for g in chars]
 assert len(codes)==len(set(codes)) and not required-set(codes)
 bands={}
 for g in chars:
  u,v,w,h=(int(g.get(k)) for k in ('u','v','w','h'))
  assert 0<=u<w<=size and 0<=v<h<=size and g.get('page')=='0'
  # Row-by-row interval overlap detection is independent of the packing routine.
  for line in range(v,h):bands.setdefault(line,[]).append((u,w))
 for intervals in bands.values():
  intervals.sort();assert all(a[1]<=b[0] for a,b in zip(intervals,intervals[1:]))
 manifest=dict(status='experimental, no Warband/WSE2/OpenGL in-game rendering QA',font_name='ACAN Chinese Bitmap Candidate',font_size_pixels=40,baseline=ascent,padding_pixels=pad,outline_pixels=1,atlas=[size,size],dds_encoding='uncompressed 32-bit RGBA legacy DDS',glyph_count=len(codes),translated_codepoints=len({ord(c) for c in target if c.isprintable()}),translated_han=len({ord(c) for c in target if '\u4e00'<=c<='\u9fff'}),source_codepoints=len({ord(c) for c in source if c.isprintable()}),gb2312_codepoints=len(gb),missing_required=0,missing_gb2312=0,secondary_face_glyphs=[f'U+{g["code"]:04X}' for g in glyphs if g['face']==1],fonts=[dict(path=str(path),sha256=sha(path),family=f['name'].getDebugName(1),version=f['name'].getDebugName(5),copyright=f['name'].getDebugName(0)) for path,f in [(a.cjk_font,primary),(a.latin_font,secondary)]],versions=dict(pillow=PIL.__version__,fonttools=fontTools.__version__,freetype=features.version('freetype2')),inputs={str(f.relative_to(a.root)):sha(f) for f in files},output_sha256={str(f.relative_to(a.out)):sha(f) for f in (descriptor,texture)},qa=dict(bounds=True,no_overlaps=True,unique_codes=True,dds_roundtrip_exact=True,runtime_tested=False))
 (a.out/'font_report.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 # OFL.txt is a versioned companion file; copy it with every redistributed build.
 (a.out/'codepoints.txt').write_text(''.join(chr(c) for c in codes)+'\n')
 print(json.dumps({k:manifest[k] for k in ('glyph_count','translated_han','missing_required','gb2312_codepoints','secondary_face_glyphs','qa')},ensure_ascii=False))
if __name__=='__main__':main()
