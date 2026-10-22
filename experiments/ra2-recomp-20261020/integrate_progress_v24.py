from pathlib import Path
import argparse,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v24'
ap=argparse.ArgumentParser();ap.add_argument('part',choices=['travel','internal','passage']);a=ap.parse_args();counts={}
def load(p):
 raw=p.read_bytes();return raw.decode('utf-8').replace('\r\n','\n'),'\r\n' if b'\r\n' in raw else '\n'
if a.part=='travel':
 p=R/'ra2/src/recomp/gen_game/recomp_0046.c';t,nl=load(p);t='#include "ground_progress_bridge.h"\n'+t
 marker='L_006FABAA:\n';assert t.count(marker)==1
 t=t.replace(marker,marker+'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_tube_progress_bridge(0); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto L_006FAC70;\n');counts['006FABAA']=1
 marker='    ecx = esi + 0x88; /* 0x006FAC70:';assert t.count(marker)==1;t=t.replace(marker,'L_006FAC70:\n'+marker)
 for address,entry,register in [('006FAD1C',1,'ebx'),('006FAE1D',2,'ebp')]:
  marker=f'    {register} = {register} & 0x80000001u; /* 0x{address}:';assert t.count(marker)==1
  t=t.replace(marker,f'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_tube_progress_bridge({entry}); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n'+marker);counts[address]=1
 p.write_text(t,encoding='utf-8',newline=nl)
 p=R/'ra2/CMakeLists.txt';t,nl=load(p)
 files='src/gameplay/ground_tube_progress.c src/gameplay/ground_internal_next.c src/gameplay/ground_passage_finish.c src/runtime/ground_progress_bridge.c'
 t+=f'\ntarget_sources(ra2 PRIVATE {files})\nset_source_files_properties({files} PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n';p.write_text(t,encoding='utf-8',newline=nl)
elif a.part=='internal':
 assert json.loads((S/'parts/travel-verified/validation.json').read_text(encoding='utf-8'))['passed']
 p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t,nl=load(p);t='#include "ground_progress_bridge.h"\n'+t
 for address,entry,targets in [('004A166A',0,['004A1FDC','004A16A6']),('004A32B4',1,['004A3A44','004A33C3'])]:
  marker='L_'+address+':\n';count=t.count(marker);assert count
  body=f'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); uint32_t next_resume_{entry}=ra2_ground_internal_next_bridge({entry}); RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n    if(next_resume_{entry}==0x{targets[0]}) goto L_{targets[0]};\n    goto L_{targets[1]};\n'
  t=t.replace(marker,marker+body);counts[address]=count
 for m in re.finditer(r'void \w+\(void\) \{.*?\n\}',t,re.S):
  f=m[0];missing=set(re.findall(r'goto (L_[0-9A-F]+)',f))-set(re.findall(r'^\s*(L_[0-9A-F]+):',f,re.M));assert not missing,(f.splitlines()[0],missing)
 p.write_text(t,encoding='utf-8',newline=nl)
else:
 assert json.loads((S/'parts/internal-verified/validation.json').read_text(encoding='utf-8'))['passed']
 p=R/'ra2/src/recomp/gen_game/recomp_0046.c';t,nl=load(p);marker='L_00703AA9:\n';count=t.count(marker);assert count
 t=t.replace(marker,marker+'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_passage_finish_bridge(); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n');counts['00703AA9']=count
 p.write_text(t,encoding='utf-8',newline=nl)
(S/(a.part+'-integration.json')).write_text(json.dumps(dict(passed=True,entries=counts,existing_tail_targets_preserved=True),indent=2),encoding='utf-8')
print(a.part,counts)
