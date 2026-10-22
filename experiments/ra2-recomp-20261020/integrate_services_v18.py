from pathlib import Path
import argparse,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v18'
ap=argparse.ArgumentParser();ap.add_argument('part',choices=['interpolation','prepare','services']);a=ap.parse_args()
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8')
if a.part=='interpolation':
 t='#include "ground_services_bridge.h"\n'+t
 # Keep original labels reachable for other generated shared entries; dispatch at the exact boundary.
 t,n=re.subn(r'(L_004A237D:\n)',r'\1    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_interpolation_bridge(); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n',t)
 assert n==8,n
 cm=R/'ra2/CMakeLists.txt';c=cm.read_text(encoding='utf-8')
 files='src/gameplay/ground_interpolation.c src/gameplay/ground_prepare_shared.c src/gameplay/ground_cell_services.c src/runtime/ground_services_bridge.c'
 c+=f'\ntarget_sources(ra2 PRIVATE {files})\nset_source_files_properties({files} PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
 cm.write_text(c,encoding='utf-8')
elif a.part=='prepare':
 assert json.loads((S/'parts/interpolation-verified/validation.json').read_text())['passed']
 def shared(m):
  return 'L_004A32B4:\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();\n    uint32_t shared_prepare_resume = ra2_ground_prepare_shared_bridge(1);\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n    if (!shared_prepare_resume) return;\n    goto L_004A3550;\n'+('L_004A32CA:\n' if 'L_004A32CA:' in m.group(0) else '')
 t,n=re.subn(r'(L_004A32B4:\n).*?(?=    /\* 可读 C：路径下一格)',shared,t,flags=re.S)
 assert n==2,n
 # Both cached-queue and reset-budget paths now use the named dispatch function.
 t=t.replace('uint32_t segment_prepare_resume = ra2_ground_prepare_segment_bridge();','uint32_t segment_prepare_resume = ra2_ground_prepare_shared_bridge(0);')
 assert t.count('ra2_ground_prepare_shared_bridge(0);')==2
else:
 assert json.loads((S/'parts/prepare-verified/validation.json').read_text())['passed']
 p=R/'ra2/src/recomp/gen_game/recomp_0022.c';t=p.read_text(encoding='utf-8');t='#include "ground_services_bridge.h"\n'+t;n=0
 for i,entry in enumerate(['00548000','00548070','005480B0','0054E3A0']):
  body=f'''void sub_{entry}(void) {{
    uint32_t _flag_k=FK_NONE,_flag_a=0,_flag_b=0,_cf=0;
    RECOMP_ENTER(0x{entry}u);
    ra2_cell_service_bridge({i});
}}'''
  t,cnt=re.subn(r'void sub_'+entry+r'\(void\) \{.*?\n\}',lambda m:body,t,flags=re.S);assert cnt==1;n+=cnt
for f in re.findall(r'void sub_[0-9A-F]+\(void\) \{.*?\n\}',t,re.S):
 assert not set(re.findall(r'goto (L_[0-9A-F]+)',f))-set(re.findall(r'^\s*(L_[0-9A-F]+):',f,re.M))
p.write_text(t,encoding='utf-8',newline='\n')
(S/(a.part+'-integration.json')).write_text(json.dumps(dict(passed=True,part=a.part,entries=n),indent=2),encoding='utf-8')
print('Integrated',a.part,n)
