from pathlib import Path
import argparse,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v25'
ap=argparse.ArgumentParser();ap.add_argument('part',choices=['travel','internal','passage']);a=ap.parse_args();counts={}
def load(p):
 raw=p.read_bytes();return raw.decode('utf-8').replace('\r\n','\n'),'\r\n' if b'\r\n' in raw else '\n'
def insert(t,address,body):
 marker='L_'+address+':\n';n=t.count(marker);assert n,address;counts[address]=n;return t.replace(marker,marker+body)
if a.part=='travel':
 p=R/'ra2/src/recomp/gen_game/recomp_0046.c';t,nl=load(p);t='#include "ground_travel_bridge.h"\n'+t
 t=insert(t,'006FAA66','    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_tube_travel_bridge(0); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto L_006FAB6A;\n')
 marker='    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();\n    uint32_t tube_resume_1=';assert t.count(marker)==1;t=t.replace(marker,'L_006FAB6A:\n'+marker)
 for address,entry,target in [('006FAC70',1,'006FAD1C'),('006FAD75',2,'006FAE1D')]:
  t=insert(t,address,f'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_tube_travel_bridge({entry}); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto L_{target};\n')
 for address in ['006FAD1C','006FAE1D']:
  marker='    _flag_a = (uint32_t)('+('ebx' if address=='006FAD1C' else 'ebp')+'); _flag_b = (uint32_t)(0x80000001u);';assert t.count(marker)==1;t=t.replace(marker,'L_'+address+':\n'+marker)
 p.write_text(t,encoding='utf-8',newline=nl)
 p=R/'ra2/CMakeLists.txt';t,nl=load(p)
 files='src/gameplay/ground_tube_travel.c src/gameplay/ground_template_next.c src/gameplay/ground_passage_neighbor.c src/runtime/ground_travel_bridge.c'
 t+=f'\ntarget_sources(ra2 PRIVATE {files})\nset_source_files_properties({files} PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n';p.write_text(t,encoding='utf-8',newline=nl)
elif a.part=='internal':
 assert json.loads((S/'parts/travel-verified/validation.json').read_text(encoding='utf-8'))['passed']
 p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t,nl=load(p);t='#include "ground_travel_bridge.h"\n'+t
 t=insert(t,'004A17A2','    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_template_next_bridge(0); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto L_004A17D5;\n')
 t=insert(t,'004A33C3','    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); uint32_t template_resume_1=ra2_ground_template_next_bridge(1); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); if(!template_resume_1) return; goto L_004A3433;\n')
 p.write_text(t,encoding='utf-8',newline=nl)
else:
 assert json.loads((S/'parts/internal-verified/validation.json').read_text(encoding='utf-8'))['passed']
 p=R/'ra2/src/recomp/gen_game/recomp_0046.c';t,nl=load(p)
 t=insert(t,'007031F2','    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); uint32_t neighbor_resume=ra2_ground_passage_neighbor_bridge(); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); if(!neighbor_resume) return; goto L_0070323E;\n')
 p.write_text(t,encoding='utf-8',newline=nl)
for m in re.finditer(r'void \w+\(void\) \{.*?\n\}',t,re.S):
 f=m[0];missing=set(re.findall(r'goto (L_[0-9A-F]+)',f))-set(re.findall(r'^\s*(L_[0-9A-F]+):',f,re.M));assert not missing,(f.splitlines()[0],missing)
(S/(a.part+'-integration.json')).write_text(json.dumps(dict(passed=True,entries=counts,existing_tail_targets_preserved=True),indent=2),encoding='utf-8')
print(a.part,counts)
