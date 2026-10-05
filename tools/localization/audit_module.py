#!/usr/bin/env python3
"""Read-only static module asset checks; writes docs/localization/asset_audit.json."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[2];m=root/'Aut_Caesar_Aut_Nihil';files=[p for p in m.rglob('*') if p.is_file()]
r={'scope':'Static filesystem/text-reference audit; no installed Warband baseline or runtime launch','counts':{},'bytes':sum(p.stat().st_size for p in files)}
for name in ['Resource','Textures','SceneObj','Sounds','Music','Data','GLShaders','GLShadersOptimized','Optional']:
 a=[p for p in files if p.relative_to(m).parts[0]==name];r['counts'][name]={'files':len(a),'bytes':sum(p.stat().st_size for p in a)}
r['lfs_pointers']=[];r['empty_files']=[]
for p in files:
 if p.stat().st_size==0:r['empty_files'].append(str(p.relative_to(m)))
 if p.stat().st_size<1024 and p.read_bytes().startswith(b'version https://git-lfs.github.com/spec/v1'):r['lfs_pointers'].append(str(p.relative_to(m)))
mods=[];base=[];odd=[]
for n,l in enumerate((m/'module.ini').read_text().splitlines(),1):
 l=l.split('#',1)[0].strip()
 if not l:continue
 if '=' not in l:odd.append({'line':n,'text':l});continue
 k,v=map(str.strip,l.split('=',1))
 if k=='load_mod_resource':mods.append(v+'.brf')
 if k=='load_resource':base.append(v+'.brf')
r['module_resources']={'count':len(mods),'missing':[v for v in mods if not(m/'Resource'/v).is_file()],'base_game_required':base,'invalid_ini_lines':odd}
for cat,folder in [('sounds','Sounds'),('music','Music')]:
 ls=(m/(cat+'.txt')).read_text().splitlines();n=int(ls[1] if cat=='sounds' else ls[0]);ls=ls[2:2+n] if cat=='sounds' else ls[1:1+n];names=[l.split()[0] for l in ls];local={p.name.casefold():p.name for p in (m/folder).iterdir()};missing=[x for x in names if not(m/folder/x).is_file()]
 r[cat]={'references':n,'local_exact':n-len(missing),'case_only_matches':[{'reference':x,'file':local[x.casefold()]} for x in missing if x.casefold() in local],'not_bundled':[x for x in missing if x.casefold() not in local]}
scenes=[l.split() for l in (m/'scenes.txt').read_text().splitlines() if l.startswith('scn_')];r['scenes']={'references':len(scenes),'local_exact':sum((m/'SceneObj'/(s[0]+'.sco')).is_file() for s in scenes),'without_local_sco':[{'id':s[0],'flags':int(s[2]),'mesh':s[3],'body':s[4],'terrain':s[-1]} for s in scenes if not(m/'SceneObj'/(s[0]+'.sco')).is_file()]}
req='actions conversation factions game_variables info_pages item_kinds1 map map_icons menus meshes mission_templates music particle_systems parties party_templates postfx presentations quests quick_strings scene_props scenes scripts simple_triggers skills skins skyboxes sounds strings tableau_materials triggers troops'.split();r['compiled_tables']={'checked':[x+'.txt' for x in req],'missing':[x+'.txt' for x in req if not(m/(x+'.txt')).is_file()]}
# Only declared texture sections: material names ending in .tga are not filenames.
import struct
refs={}
for name in ['x_texture_all.brf','x_textures_engine.brf']:
 b=(m/'Resource'/name).read_bytes();pos=0
 def uint():
  global pos
  n=struct.unpack_from('<I',b,pos)[0];pos+=4;return n
 def string():
  global pos
  n=uint();v=b[pos:pos+n].decode();pos+=n;return v
 assert string()=='rfver ';version=uint();assert string()=='texture';n=uint()
 for _ in range(n):
  name_value=string();flags=uint();refs.setdefault(name_value,[]).append(name)
 assert string()=='end'
local={p.name.casefold():p.name for p in (m/'Textures').iterdir()}
r['declared_texture_sections']={'archives':['x_texture_all.brf','x_textures_engine.brf'],'unique_references':len(refs),'not_exact_local':[{'name':k,'archives':v,'case_match':local.get(k.casefold())} for k,v in refs.items() if not(m/'Textures'/k).is_file()],'method':'Parsed complete declared texture sections in the two module texture archives; not a full BRF material/mesh graph audit.'}
r['unknown_external_sounds']=r['sounds']['not_bundled']
r['scope_notes']=['load_resource archives require installed Warband CommonRes; not module-missing files.','Sound names absent locally are unresolved external dependencies, not verified Native assets.','Absent SCO does not establish missing required scene; generated scenes and marker scenes need no authored SCO.','waterbump is an extensionless engine-resource candidate; not proven missing DDS.','Case-only texture mismatches may fail on case-sensitive platforms; no filenames modified.']
(root/'docs/localization/asset_audit.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'module_brf_missing':r['module_resources']['missing'],'unresolved_sound_files':r['unknown_external_sounds'],'texture_not_exact_local':len(r['declared_texture_sections']['not_exact_local']),'lfs_pointers':r['lfs_pointers'],'report':'docs/localization/asset_audit.json'},indent=2))
