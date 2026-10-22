from pathlib import Path
import argparse,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v23'
ap=argparse.ArgumentParser();ap.add_argument('part',choices=['tube','handoff','surface']);a=ap.parse_args();counts={}
if a.part=='tube':
 p=R/'ra2/src/recomp/gen_game/recomp_0046.c';t=p.read_text(encoding='utf-8');t='#include "ground_tube_state_bridge.h"\n'+t
 for address,entry,targets in [('006FAA45',2,['006FAE76','006FAA66']),('006FAB6A',1,['006FAE76','006FABAA','006FAD75'])]:
  marker='    '+('eax = (int32_t)(int8_t)MEM8(esi + 0x574);' if entry==2 else 'eax = MEM32(esp + 0x28);')+' /* 0x'+address+':'
  assert t.count(marker)==1
  body=f'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();\n    uint32_t tube_resume_{entry}=ra2_ground_tube_state_bridge({entry});\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n'
  for target in targets[:-1]:body+=f'    if (tube_resume_{entry}==0x{target}) goto L_{target};\n'
  body+=f'    goto L_{targets[-1]};\n';t=t.replace(marker,body+marker);counts[address]=1
 marker='L_006FAE76:\n';assert t.count(marker)==1;t=t.replace(marker,marker+'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_tube_state_bridge(0); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n');counts['006FAE76']=1
 p.write_text(t,encoding='utf-8',newline='\r\n')
 cm=R/'ra2/CMakeLists.txt';raw=cm.read_bytes();nl='\r\n' if b'\r\n' in raw else '\n'
 files='src/gameplay/ground_tube_state.c src/gameplay/ground_handoff.c src/gameplay/ground_surface_class.c src/runtime/ground_tube_state_bridge.c'
 cm.write_bytes(raw+f'\ntarget_sources(ra2 PRIVATE {files})\nset_source_files_properties({files} PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'.replace('\n',nl).encode())
elif a.part=='handoff':
 assert json.loads((S/'parts/tube-verified/validation.json').read_text(encoding='utf-8'))['passed']
 p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');t='#include "ground_tube_state_bridge.h"\n'+t
 for address,entry,targets in [('004A3257',0,['004A32B4']),('004A2311',1,['004A263A','004A237D']),('004A1F90',2,['004A166A','004A1FA1'])]:
  marker='L_'+address+':\n';expected=t.count(marker);assert expected
  body=f'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();\n    uint32_t handoff_resume_{entry}=ra2_ground_internal_handoff_bridge({entry});\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n'
  if len(targets)>1:body+=f'    if (handoff_resume_{entry}==0x{targets[0]}) goto L_{targets[0]};\n'
  body+=f'    goto L_{targets[-1]};\n';t=t.replace(marker,marker+body);counts[address]=expected
 # Standalone overlapping entry 4A2311 lacks the label retained by 4A230E.
 def interpolation_label(m):
  f=m[0]
  if 'handoff_resume_1' in f and 'L_004A237D:' not in f:
   marker='    eax = esp + 0x34; /* 0x004A237D:';assert f.count(marker)==1
   f=f.replace(marker,'L_004A237D:\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_interpolation_bridge(); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n'+marker)
  return f
 t=re.sub(r'void \w+\(void\) \{.*?\n\}',interpolation_label,t,flags=re.S)
 for m in re.finditer(r'void \w+\(void\) \{.*?\n\}',t,re.S):
  f=m[0];missing=set(re.findall(r'goto (L_[0-9A-F]+)',f))-set(re.findall(r'^\s*(L_[0-9A-F]+):',f,re.M));assert not missing,(f.splitlines()[0],missing)
 p.write_text(t,encoding='utf-8',newline='\n')
else:
 assert json.loads((S/'parts/handoff-verified/validation.json').read_text(encoding='utf-8'))['passed']
 p=R/'ra2/src/recomp/gen_game/recomp_0007.c';raw=p.read_bytes();nl='\r\n' if b'\r\n' in raw else '\n';t=raw.decode('utf-8').replace('\r\n','\n');t='#include "ground_tube_state_bridge.h"\n'+t
 for name,entry,address in [('sub_00479CC0',0,'00479CC0'),('sub_0047A270',1,'0047A270'),('sub_0047A290',2,'0047A290')]:
  body=f'void {name}(void) {{\n    uint32_t _flag_k=FK_NONE,_flag_a=0,_flag_b=0,_cf=0;\n    RECOMP_ENTER(0x{address}u);\n    ra2_ground_surface_class_bridge({entry});\n}}'
  t,n=re.subn(r'void '+name+r'\(void\) \{.*?\n\}',lambda m:body,t,flags=re.S);assert n==1;counts[name]=n
 p.write_text(t,encoding='utf-8',newline=nl)
(S/(a.part+'-integration.json')).write_text(json.dumps(dict(passed=True,entries=counts,existing_tail_targets_preserved=True),indent=2),encoding='utf-8')
print(a.part,counts)
