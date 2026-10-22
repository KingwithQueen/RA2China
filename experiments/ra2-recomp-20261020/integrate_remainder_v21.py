from pathlib import Path
import argparse,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v21'
ap=argparse.ArgumentParser();ap.add_argument('part',choices=['landing','failure','slope']);a=ap.parse_args()
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');counts={}
if a.part=='landing':
 t='#include "ground_remainder_bridge.h"\n'+t
 for label,entry in [('004A1388',0),('004A22F9',1),('004A263A',2)]:
  body='    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();\n'
  if entry==0:
   body+='    uint32_t landing_resume=ra2_ground_landing_bridge(0);\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n    if (landing_resume==0x4A15F0) goto L_004A15F0;\n    return;\n'
  else:body+=f'    ra2_ground_landing_bridge({entry}); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n'
  t,n=re.subn(r'^L_'+label+r':\n',lambda m:m.group()+body,t,flags=re.M);assert n>0,(label,n);counts[label]=n
 c=R/'ra2/CMakeLists.txt';raw=c.read_bytes();nl='\r\n' if b'\r\n' in raw else '\n'
 files='src/gameplay/ground_landing.c src/gameplay/ground_failure.c src/gameplay/ground_slope.c src/runtime/ground_remainder_bridge.c'
 c.write_bytes(raw+f'\ntarget_sources(ra2 PRIVATE {files})\nset_source_files_properties({files} PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'.replace('\n',nl).encode())
elif a.part=='failure':
 assert json.loads((S/'parts/landing-verified/validation.json').read_text())['passed']
 for label,entry in [('004A3BFD',1),('004A3985',2),('004A3C34',3),('004A3A38',4),('004A39AF',5),('004A3C5D',6)]:
  body=f'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_failure_bridge({entry}); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n'
  t,n=re.subn(r'^L_'+label+r':\n',lambda m:m.group()+body,t,flags=re.M);assert n>0,(label,n);counts[label]=n
 marker='    SET_LO8(eax, MEM8(esp + 0x64)); /* 0x004A395A:'
 body='    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_failure_bridge(0); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n'
 t,n=re.subn(r'(?='+re.escape(marker)+')',lambda m:body,t);assert n>0;counts['revealed_retry']=n
else:
 assert json.loads((S/'parts/failure-verified/validation.json').read_text())['passed']
 p=R/'ra2/src/recomp/gen_game/recomp_0007.c';t=p.read_text(encoding='utf-8');t='#include "ground_remainder_bridge.h"\n'+t
 pattern=r'void (\w+)\(void\) \{(?:(?!\n\}).)*?RECOMP_ENTER\(0x004706C0u\);(?:(?!\n\}).)*?\n\}'
 matches=list(re.finditer(pattern,t,re.S));assert len(matches)==1
 m=matches[0];name=m.group(1)
 t=t[:m.start()]+f'void {name}(void) {{\n    uint32_t _flag_k=FK_NONE,_flag_a=0,_flag_b=0,_cf=0;\n    RECOMP_ENTER(0x004706C0u);\n    ra2_ground_slope_bridge();\n}}'+t[m.end():];counts[name]=1
for f in re.findall(r'void \w+\(void\) \{.*?\n\}',t,re.S):
 missing=set(re.findall(r'goto (L_[0-9A-F]+)',f))-set(re.findall(r'^\s*(L_[0-9A-F]+):',f,re.M))
 assert not missing,(f.splitlines()[0],missing)
p.write_text(t,encoding='utf-8',newline='\n')
(S/(a.part+'-integration.json')).write_text(json.dumps(dict(passed=True,part=a.part,entries=counts,existing_tail_targets_preserved=True),indent=2),encoding='utf-8')
print('Integrated',a.part,counts)
