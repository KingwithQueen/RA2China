from pathlib import Path
import argparse,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v19'
ap=argparse.ArgumentParser();ap.add_argument('part',choices=['sampling','exits','objects']);a=ap.parse_args()
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');counts={}
def dispatch(entry):
 return f'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_prepare_exit_bridge({entry}); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n'
if a.part=='sampling':
 t='#include "ground_dispatch_bridge.h"\n'+t
 for label,mode,expected in [('004A15ED',0,3),('004A1F8D',1,9),('004A1FA1',2,10)]:
  if mode==0:route='    if (sampling_resume_0==0x4A22F9) goto L_004A22F9;\n'
  elif mode==1:route=''
  else:route='    if (sampling_resume_2==0x4A263A) goto L_004A263A;\n    goto L_004A237D;\n'
  if mode<2:route+=f'    if (sampling_resume_{mode}==0x4A166A) goto L_004A166A;\n    goto L_004A1FA1;\n'
  body=f'L_{label}:\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();\n    uint32_t sampling_resume_{mode}=ra2_ground_sampling_bridge({mode});\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n'+route
  t,n=re.subn(r'^L_'+label+r':\n',lambda m:body,t,flags=re.M);assert n==expected,(label,n);counts[label]=n
 def interpolation_entry(m):
  f=m.group(0)
  if re.search(r'^L_004A1FA1:',f,re.M) and 'L_004A237D:' not in f:
   marker='    eax = esp + 0x34; /* 0x004A237D:'
   assert f.count(marker)==1
   f=f.replace(marker,'L_004A237D:\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_interpolation_bridge(); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n'+marker)
  return f
 t=re.sub(r'void \w+\(void\) \{.*?\n\}',interpolation_entry,t,flags=re.S)
 cm=R/'ra2/CMakeLists.txt';c=(S/'baseline/ra2/CMakeLists.txt').read_bytes();files='src/gameplay/ground_sampling.c src/gameplay/ground_prepare_exit.c src/gameplay/ground_object_services.c src/runtime/ground_dispatch_bridge.c'
 nl='\r\n' if b'\r\n' in c else '\n'
 cm.write_bytes(c+f'\ntarget_sources(ra2 PRIVATE {files})\nset_source_files_properties({files} PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'.replace('\n',nl).encode())
elif a.part=='exits':
 assert json.loads((S/'parts/sampling-verified/validation.json').read_text())['passed']
 t,n=re.subn(r'(?=    ecx = MEM32\(ebp \+ 0xC\); /\* 0x004A3A0A:)',lambda m:dispatch(0),t);assert n==5,n;counts['after_rebuild']=n
 for label,entry,expected in [('004A3A24',0,5),('004A3A50',1,6),('004A3C75',2,8),('004A3A44',3,4)]:
  t,n=re.subn(r'^L_'+label+r':\n',lambda m:m.group()+dispatch(entry),t,flags=re.M);assert n==expected,(label,n);counts[label]=n
else:
 assert json.loads((S/'parts/exits-verified/validation.json').read_text())['passed']
 for filename,functions in [('recomp_0007.c',[('sub_004717B0',0,'004717B0'),('sub_004717E0',1,'004717E0'),('sub_00471830',2,'00471830'),('sub_0047A130',3,'0047A130')]),
  ('recomp_0029.c',[('sub_005D47D0',4,'005D47D0'),('WaveClass__virtual_108',5,'005D4810')])]:
  p=R/'ra2/src/recomp/gen_game'/filename;t=p.read_text(encoding='utf-8');t='#include "ground_dispatch_bridge.h"\n'+t
  for name,entry,address in functions:
   body=f'void {name}(void) {{\n    uint32_t _flag_k=FK_NONE,_flag_a=0,_flag_b=0,_cf=0;\n    RECOMP_ENTER(0x{address}u);\n    ra2_ground_object_service_bridge({entry});\n}}'
   t,n=re.subn(r'void '+name+r'\(void\) \{.*?\n\}',lambda m:body,t,flags=re.S);assert n==1,(name,n);counts[name]=n
  p.write_text(t,encoding='utf-8',newline='\n')
 t=None
if t is not None:
 for f in re.findall(r'void \w+\(void\) \{.*?\n\}',t,re.S):
  missing=set(re.findall(r'goto (L_[0-9A-F]+)',f))-set(re.findall(r'^\s*(L_[0-9A-F]+):',f,re.M))
  assert not missing,(f.splitlines()[0],missing)
 p.write_text(t,encoding='utf-8',newline='\n')
(S/(a.part+'-integration.json')).write_text(json.dumps(dict(passed=True,part=a.part,entries=counts,all_existing_labels_retained=True),indent=2),encoding='utf-8')
print('Integrated',a.part,counts)
