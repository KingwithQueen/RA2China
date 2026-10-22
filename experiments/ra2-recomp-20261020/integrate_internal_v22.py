from pathlib import Path
import argparse,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v22'
ap=argparse.ArgumentParser();ap.add_argument('part',choices=['sampling','prepare']);a=ap.parse_args()
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');counts={}
if a.part=='sampling':
 t='#include "ground_internal_bridge.h"\n'+t
 for label,entry,expected in [('004A15F0',0,3),('004A230E',1,11)]:
  body=f'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();\n    uint32_t internal_sampling_{entry}=ra2_ground_sampling_shared_bridge({entry});\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n'
  targets=['004A1FA1','004A22F9','004A166A'] if entry==0 else ['004A263A','004A237D']
  for target in targets[:-1]:body+=f'    if (internal_sampling_{entry}==0x{target}) goto L_{target};\n'
  body+=f'    goto L_{targets[-1]};\n'
  t,n=re.subn(r'^L_'+label+r':\n',lambda m:m.group()+body,t,flags=re.M);assert n==expected,(label,n);counts[label]=n
 cm=R/'ra2/CMakeLists.txt';raw=cm.read_bytes();nl='\r\n' if b'\r\n' in raw else '\n'
 files='src/gameplay/ground_sampling_shared.c src/gameplay/ground_prepare_internal.c src/runtime/ground_internal_bridge.c'
 cm.write_bytes(raw+f'\ntarget_sources(ra2 PRIVATE {files})\nset_source_files_properties({files} PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'.replace('\n',nl).encode())
else:
 assert json.loads((S/'parts/sampling-verified/validation.json').read_text(encoding='utf-8'))['passed']
 for label,entry,expected in [('004A3216',2,1),('004A39C8',0,4),('004A39CA',1,5)]:
  body=f'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_prepare_internal_bridge({entry}); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n'
  t,n=re.subn(r'^L_'+label+r':\n',lambda m:m.group()+body,t,flags=re.M);assert n==expected,(label,n);counts[label]=n
def add_interpolation_entry(m):
 f=m.group(0)
 if re.search(r'^L_004A230E:',f,re.M) and not re.search(r'^L_004A237D:',f,re.M):
  marker='    eax = esp + 0x34; /* 0x004A237D:'
  assert f.count(marker)==1
  f=f.replace(marker,'L_004A237D:\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_interpolation_bridge(); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n'+marker)
 return f
if a.part=='sampling':t=re.sub(r'void \w+\(void\) \{.*?\n\}',add_interpolation_entry,t,flags=re.S)
for f in re.findall(r'void \w+\(void\) \{.*?\n\}',t,re.S):
 missing=set(re.findall(r'goto (L_[0-9A-F]+)',f))-set(re.findall(r'^\s*(L_[0-9A-F]+):',f,re.M));assert not missing,(f.splitlines()[0],missing)
p.write_text(t,encoding='utf-8',newline='\n')
(S/(a.part+'-integration.json')).write_text(json.dumps(dict(passed=True,entries=counts,existing_tail_targets_preserved=True),indent=2),encoding='utf-8')
print(a.part,counts)
