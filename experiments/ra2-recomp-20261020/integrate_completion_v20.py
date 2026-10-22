from pathlib import Path
import argparse,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v20'
ap=argparse.ArgumentParser();ap.add_argument('part',choices=['arrival','cleanup','passage']);a=ap.parse_args()
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');counts={}
if a.part=='arrival':
 t='#include "ground_completion_bridge.h"\n'+t
 body='    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();\n    uint32_t completion_resume=ra2_ground_arrival_complete_bridge();\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n    if (!completion_resume) return;\n    goto L_004A1FA1;\n'
 t,n=re.subn(r'^L_004A1FDC:\n',lambda m:m.group()+body,t,flags=re.M);assert n==6,n;counts['arrival_entries']=n
 c=R/'ra2/CMakeLists.txt';raw=c.read_bytes();nl='\r\n' if b'\r\n' in raw else '\n'
 files='src/gameplay/ground_completion.c src/gameplay/ground_passage.c src/runtime/ground_completion_bridge.c'
 c.write_bytes(raw+f'\ntarget_sources(ra2 PRIVATE {files})\nset_source_files_properties({files} PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'.replace('\n',nl).encode())
elif a.part=='cleanup':
 assert json.loads((S/'parts/arrival-verified/validation.json').read_text())['passed']
 for label,entry in [('004A322E',0),('004A44B3',1),('004A4450',2),('004A4522',3),('004A4502',4),('004A44D1',6),('004A322A',7)]:
  route='    if (cleanup_resume==0x4A4174) goto L_004A4174;\n' if entry==6 else ''
  call=f'uint32_t cleanup_resume=ra2_ground_prepare_finish_bridge({entry});' if entry==6 else f'ra2_ground_prepare_finish_bridge({entry});'
  body='    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();\n    '+call+'\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n'+route+'    return;\n'
  t,n=re.subn(r'^L_'+label+r':\n',lambda m:m.group()+body,t,flags=re.M);assert n>0,(label,n);counts[label]=n
 # This recursion also has a standalone entry with no label at its start.
 marker='    ecx = MEM32(ebp + 0xC); /* 0x004A4429:'
 body='    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_prepare_finish_bridge(5); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n'
 t,n=re.subn(r'(?='+re.escape(marker)+')',lambda m:body,t);assert n>0;n0=n;counts['recursive_clear_path']=n0
else:
 assert json.loads((S/'parts/cleanup-verified/validation.json').read_text())['passed']
 for filename,functions in [('recomp_0012.c',[('FootClass__virtual_171',0,'004C86E0'),('sub_004C8730',1,'004C8730')]),('recomp_0023.c',[('sub_0055A280',2,'0055A280')])]:
  p=R/'ra2/src/recomp/gen_game'/filename;t=p.read_text(encoding='utf-8');t='#include "ground_completion_bridge.h"\n'+t
  for name,entry,address in functions:
   # Resolve the known address, since generated virtual names depend on the original vtable.
   matches=list(re.finditer(r'void (\w+)\(void\) \{(?:(?!\n\}).)*?RECOMP_ENTER\(0x'+address+r'u\);(?:(?!\n\}).)*?\n\}',t,re.S));assert len(matches)==1,(address,len(matches))
   m=matches[0];name=m.group(1)
   body=f'void {name}(void) {{\n    uint32_t _flag_k=FK_NONE,_flag_a=0,_flag_b=0,_cf=0;\n    RECOMP_ENTER(0x{address}u);\n    ra2_ground_passage_bridge({entry});\n}}'
   t=t[:m.start()]+body+t[m.end():];counts[name]=1
  p.write_text(t,encoding='utf-8',newline='\n')
 t=None
if t is not None:
 for f in re.findall(r'void \w+\(void\) \{.*?\n\}',t,re.S):
  missing=set(re.findall(r'goto (L_[0-9A-F]+)',f))-set(re.findall(r'^\s*(L_[0-9A-F]+):',f,re.M))
  assert not missing,(f.splitlines()[0],missing)
 p.write_text(t,encoding='utf-8',newline='\n')
(S/(a.part+'-integration.json')).write_text(json.dumps(dict(passed=True,part=a.part,entries=counts,all_existing_labels_retained=True),indent=2),encoding='utf-8')
print('Integrated',a.part,counts)
