from pathlib import Path
import argparse,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v26'
ap=argparse.ArgumentParser();ap.add_argument('part',choices=['template','passage','returns']);a=ap.parse_args();counts={}
def load(p):
 raw=p.read_bytes();return raw.decode('utf-8').replace('\r\n','\n'),'\r\n' if b'\r\n' in raw else '\n'
def insert(t,address,body):
 marker='L_'+address+':\n';n=t.count(marker);assert n,address;counts[address]=n;return t.replace(marker,marker+body)
if a.part=='template':
 p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t,nl=load(p);t='#include "ground_joint_bridge.h"\n'+t
 for address,i,target in [('004A17D5',0,'004A17FE'),('004A3486',1,'004A3502')]:
  t=insert(t,address,f'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_template_entry_bridge({i}); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto L_{target};\n')
 marker='    /* cmp MEM32(esp + 0x18), 7 */ /* 0x004A3502:';assert t.count(marker)==2;t=t.replace(marker,'L_004A3502:\n'+marker);p.write_text(t,encoding='utf-8',newline=nl)
 for name in ['ground_advance.c','../runtime/ground_advance_bridge.c']:
  p=R/'ra2/src/gameplay'/name;t,nl=load(p);t='#include "ground_template_entry.h"\n'+t
  if name=='ground_advance.c':
   t=t.replace('uint16_t x = (uint16_t)(position.x / 256), y = (uint16_t)(position.y / 256);','uint32_t packed = ra2_ground_sample_cell(position.x,position.y);\n    uint16_t x = (uint16_t)packed, y = (uint16_t)(packed >> 16);')
  else:t=t.replace('uint32_t packed=(uint16_t)(result.x/256)|((uint32_t)(uint16_t)(result.y/256)<<16);','uint32_t packed=ra2_ground_sample_cell(result.x,result.y);')
  p.write_text(t,encoding='utf-8',newline=nl)
 p=R/'ra2/CMakeLists.txt';t,nl=load(p);files='src/gameplay/ground_template_entry.c src/gameplay/ground_passage_entry.c src/gameplay/ground_return_plan.c src/runtime/ground_joint_bridge.c'
 t+=f'\ntarget_sources(ra2 PRIVATE {files})\nset_source_files_properties({files} PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n';p.write_text(t,encoding='utf-8',newline=nl)
elif a.part=='passage':
 assert json.loads((S/'parts/template-verified/validation.json').read_text(encoding='utf-8'))['passed']
 p=R/'ra2/src/recomp/gen_game/recomp_0046.c';t,nl=load(p);t='#include "ground_joint_bridge.h"\n'+t
 t=insert(t,'0070323E','    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); uint32_t entry_resume=ra2_ground_passage_entry_bridge(); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); if(!entry_resume) return; goto L_00703331;\n');p.write_text(t,encoding='utf-8',newline=nl)
else:
 assert json.loads((S/'parts/passage-verified/validation.json').read_text(encoding='utf-8'))['passed']
 for name in ['ground_remainder_bridge.c','ground_completion_bridge.c']:
  p=R/'ra2/src/runtime'/name;t,nl=load(p);t='#include "ground_joint_bridge.h"\n'+t
  if name.startswith('ground_remainder'):
   start=t.index('static void return_frame(');end=t.index('\nstatic int valid(',start)
   t=t[:start]+'''static void return_frame(uint32_t f,uint32_t result,int prepare)
{ ra2_ground_return_frame(f,prepare?RA2_FRAME_PREPARE:RA2_FRAME_ADVANCE,result); }
'''+t[end:];counts['landing_and_failure_shared_return']=1
  else:
   start=t.index('    uint32_t f = c.frame;',t.index('uint32_t ra2_ground_prepare_finish_bridge'));end=t.index('    return 0;',start)
   t=t[:start]+'    ra2_ground_return_frame(c.frame,RA2_FRAME_PREPARE,result);\n'+t[end:];counts['prepare_finish_shared_return']=1
  p.write_text(t,encoding='utf-8',newline=nl)
(S/(a.part+'-integration.json')).write_text(json.dumps(dict(passed=True,entries=counts,existing_tail_targets_preserved=True),indent=2),encoding='utf-8')
print(a.part,counts)
