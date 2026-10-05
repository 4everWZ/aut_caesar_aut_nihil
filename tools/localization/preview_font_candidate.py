#!/usr/bin/env python3
"""Offline illustrative XML/DDS decoding; not a screenshot or engine emulation."""
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont,ImageChops
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root',type=Path,required=True)
parser.add_argument('--descriptor',type=Path,required=True)
parser.add_argument('--texture',type=Path,required=True)
parser.add_argument('--out',type=Path,required=True)
parser.add_argument('--label-font',type=Path,required=True)
args=parser.parse_args();root=args.root/'Aut_Caesar_Aut_Nihil';out=args.out;out.mkdir(parents=True,exist_ok=True)
canvas=Image.new('RGB',(1600,780),(34,37,43));d=ImageDraw.Draw(canvas)
label=ImageFont.truetype(str(args.label_font),22)
small=ImageFont.truetype(str(args.label_font),17)
d.text((24,18),'OFFLINE FONT CANDIDATE REVIEW - not an in-game screenshot',font=label,fill='white')
d.text((24,53),'Both panels decode DDS rectangles. Baseline/advance arithmetic is illustrative; actual engine layout remains untested.',font=small,fill='#c0c0c0')
samples=['Roma invicta! Legion XVII - 1,234 denarii','凯撒万岁！第十七军团已抵达罗马。','元老院支持：75%。粮食储备还可维持30天。','“愿诸神赐福。”【任务】返回亚历山大里亚。','AaGgjpqy 0123456789 % / {} [] ḥ']
for col,(name,xmlp,ddsp) in enumerate([('BUNDLED ORIGINAL - no Chinese glyphs',root/'Data/font_data.xml',root/'Textures/font.dds'),('OFL CANDIDATE - 7,560 glyphs',args.descriptor,args.texture)]):
 xstart=24+col*790;d.text((xstart,110),name,font=label,fill='#ffffff');font=ET.parse(xmlp).getroot();chars={int(c.get('code')):c.attrib for c in font.findall('.//character')};atlas=Image.open(ddsp).convert('RGBA');sx=atlas.width/int(font.get('width'));sy=atlas.height/int(font.get('height'));scale=34/int(font.get('font_size'))
 for row,text in enumerate(samples):
  pen=xstart;baseline=220+row*100
  d.line((xstart,baseline,xstart+760,baseline),fill='#444852')
  for ch in text:
   g=chars.get(ord(ch))
   if g is None:
    d.rectangle((pen,baseline-25,pen+23,baseline-2),outline='#de7777',width=1);pen+=26;continue
   u,v,w,h=(int(g[k]) for k in ('u','v','w','h'));patch=atlas.crop((round(u*sx),round(v*sy),round(w*sx),round(h*sy)))
   if patch.width==0 or patch.height==0:continue
   targetsize=(max(1,round((w-u)*scale)),max(1,round((h-v)*scale)))
   r,_,_,a=patch.split();r=r.resize(targetsize,Image.Resampling.LANCZOS);a=a.resize(targetsize,Image.Resampling.LANCZOS); opacity=ImageChops.add(ImageChops.invert(r),a);shade=ImageChops.add(a,Image.new('L',a.size,13));ink=Image.merge('RGBA',(shade,shade,shade,opacity))
   canvas.paste(ink,(round(pen+int(g['preshift'])*scale),round(baseline-int(g['yadjust'])*scale)),ink)
   pen+=int(g['postshift'])*scale
 d.text((xstart,735),'Red boxes = absent descriptor entries. White text approximates HLSL outline.',font=small,fill='#b8b8b8')
canvas.save(out/'comparison.png')
# Candidate-only glyph closeup avoids including any pre-existing font imagery.
f=ET.parse(args.descriptor).getroot();entries={int(c.get('code')):c.attrib for c in f.findall('.//character')};atlas=Image.open(args.texture);im=Image.new('RGB',(720,240),(238,236,226));d=ImageDraw.Draw(im);d.text((12,12),'Candidate channel inspection: alpha (top) / inverse red (bottom)',font=small,fill='black')
for i,ch in enumerate('羅罗鬱郁鹰凯'):
 g=entries.get(ord(ch))
 if not g:continue
 patch=atlas.crop(tuple(int(g[k]) for k in ('u','v','w','h')));r,_,_,a=patch.split()
 for j,p in enumerate([a,ImageChops.invert(r)]):im.paste(p.resize((90,90)),(12+i*115,45+j*94))
im.save(out/'channels.png')
