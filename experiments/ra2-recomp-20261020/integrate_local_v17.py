from pathlib import Path
import argparse,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v17'
ap=argparse.ArgumentParser();ap.add_argument('part',choices=['turn','segment','completion']);a=ap.parse_args()
p=R/'ra2/src/recomp/gen_game/recomp_0003.c';t=p.read_text(encoding='utf-8')
if a.part!='turn':
 previous='turn' if a.part=='segment' else 'segment'
 assert json.loads((S/f'parts/{previous}-verified/validation.json').read_text(encoding='utf-8'))['passed']
else:t='#include "ground_path_local_bridge.h"\n'+t
original_text=t
def replace_entry(entry,bridge):
 global t
 replacement=f'''void sub_{entry}(void) {{
    uint32_t _flag_k=FK_NONE,_flag_a=0,_flag_b=0,_cf=0;
    RECOMP_ENTER(0x{entry}u);
    {bridge}();
}}'''
 t,n=re.subn(r'void sub_'+entry+r'\(void\) \{.*?\n\}',replacement,t,flags=re.S);assert n==1,n
 return n
if a.part=='turn':
 n=replace_entry('00428CF0','ra2_path_turn_rewrite_bridge')+replace_entry('00429570','ra2_path_anchor_bridge')
 cm=R/'ra2/CMakeLists.txt';c=cm.read_text(encoding='utf-8')
 files='src/gameplay/ground_path_local.c src/gameplay/ground_path_completion.c src/runtime/ground_path_local_bridge.c'
 c+=f'\ntarget_sources(ra2 PRIVATE {files})\nset_source_files_properties({files} PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n';cm.write_text(c,encoding='utf-8')
elif a.part=='segment':n=replace_entry('004296F0','ra2_path_segment_rewrite_bridge')
else:
 def finish(mode):
  return '    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_path_completion_bridge('+str(mode)+'); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n'
 replacement='L_00427CBB:\n'+finish(3)+'L_00427D1B:\nL_00427D1F:\n'+finish(2)+'L_00427D2E:\n'+finish(0)
 def replace_tail(match):
  # 生成器把跨片段跳转标签附在ret之后；它们仍被前半段引用，必须保留。
  tails=''.join(line+'\n' for line in match.group(0).splitlines() if 'RECOMP_ITAIL(' in line)
  return replacement+tails
 t,n=re.subn(r'L_00427CBB:\n.*?(?=    RECOMP_REGS_OUT\(\);\n\})',replace_tail,t,flags=re.S)
 assert n==16,n
p.write_text(t,encoding='utf-8')
metadata=dict(passed=True,part=a.part,entries=n)
if a.part=='completion':
 def continuations(text):
  return {f.splitlines()[0]:sorted(re.findall(r'^\s*(L_[0-9A-F]+): RECOMP_ITAIL\([^\n]+',f,re.M)) for f in re.findall(r'void sub_[0-9A-F]+\(void\) \{.*?\n\}',text,re.S)}
 assert continuations(original_text)==continuations(t)
 for f in re.findall(r'void sub_[0-9A-F]+\(void\) \{.*?\n\}',t,re.S):
  targets=set(re.findall(r'goto (L_[0-9A-F]+)',f));labels=set(re.findall(r'^\s*(L_[0-9A-F]+):',f,re.M));assert not targets-labels
 metadata.update(internal_tail_labels_preserved=True,undefined_goto_labels=0)
(S/(a.part+'-integration.json')).write_text(json.dumps(metadata,indent=2),encoding='utf-8')
print('Integrated',a.part,n,'entries')
