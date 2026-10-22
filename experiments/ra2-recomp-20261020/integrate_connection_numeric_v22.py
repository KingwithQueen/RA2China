from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v22'
assert json.loads((S/'parts/prepare-verified/validation.json').read_text(encoding='utf-8'))['passed']
p=R/'ra2/src/recomp/gen_game/recomp_0046.c';t=(S/'baseline/ra2/src/recomp/gen_game/recomp_0046.c').read_text(encoding='utf-8')
t='#include "ground_connection_numeric_bridge.h"\n'+t
for address,end,axis in [('006FADD5','006FADE2',0),('006FADF1','006FAE01',1)]:
 marker='    _st[0] *= *(double*)ADDR(esp + '+('0x30' if not axis else '0x38')+'); /* 0x'+address+':'
 assert t.count(marker)==1
 body=f'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_connection_numeric_bridge({axis}); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto L_{end};\n'
 t=t.replace(marker,body+marker)
 marker='    '+('ecx = MEM32(esp + 0x48);' if not axis else 'edx = MEM32(esp + 0x30);')+' /* 0x'+end+':'
 assert t.count(marker)==1;t=t.replace(marker,'L_'+end+':\n'+marker)
marker='    fp_push((double)(int32_t)MEM32(esp + 0x30)); /* 0x006FADA5:';assert t.count(marker)==1
t=t.replace(marker,'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_connection_numeric_bridge(2); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto L_006FADB3;\n'+marker)
marker='    fp_push((double)(int32_t)MEM32(esp + 0x18)); /* 0x006FADB3:';assert t.count(marker)==1;t=t.replace(marker,'L_006FADB3:\n'+marker)
for name,address,mode in [('004BA480','006FADD0',3),('004BA4D0','006FADEC',4)]:
 marker='    RECOMP_CALL(sub_'+name+'); /* 0x'+address+':';assert t.count(marker)==1
 t=t.replace(marker,'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_connection_numeric_bridge('+str(mode)+'); RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n    /* original table call replaced locally */ //'+marker)
for address,end,mode,offset in [('006FACD4','006FACE1',5,'0x20'),('006FACF0','006FAD00',6,'0x28')]:
 marker='    _st[0] *= *(double*)ADDR(esp + '+offset+'); /* 0x'+address+':';assert t.count(marker)==1
 t=t.replace(marker,f'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_connection_numeric_bridge({mode}); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto L_{end};\n'+marker)
 marker='    '+('edx = MEM32(esp + 0x48);' if mode==5 else 'ecx = MEM32(esp + 0x28);')+' /* 0x'+end+':';assert t.count(marker)==1;t=t.replace(marker,'L_'+end+':\n'+marker)
marker='    fp_push((double)(int32_t)MEM32(esp + 0x28)); /* 0x006FACA0:';assert t.count(marker)==1
t=t.replace(marker,'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_connection_numeric_bridge(7); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto L_006FACB2;\n'+marker)
marker='    fp_push((double)(int32_t)MEM32(esp + 0x18)); /* 0x006FACB2:';assert t.count(marker)==1;t=t.replace(marker,'L_006FACB2:\n'+marker)
for name,address,mode in [('004BA480','006FACCF',3),('004BA4D0','006FACEB',4)]:
 marker='    RECOMP_CALL(sub_'+name+'); /* 0x'+address+':';assert t.count(marker)==1
 t=t.replace(marker,'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_connection_numeric_bridge('+str(mode)+'); RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n    /* original table call replaced locally */ //'+marker)
p.write_text(t,encoding='utf-8',newline='\r\n')
p=R/'ra2/CMakeLists.txt';t=(S/'parts/prepare-verified/ra2/CMakeLists.txt').read_bytes();nl='\r\n' if b'\r\n' in t else '\n'
files='src/gameplay/ground_connection_numeric.c src/runtime/ground_connection_numeric_bridge.c'
p.write_bytes(t+f'\ntarget_sources(ra2 PRIVATE {files})\nset_source_files_properties({files} PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'.replace('\n',nl).encode())
(S/'connection-numeric-integration.json').write_text(json.dumps(dict(passed=True,entries=['6FACA0','6FACCF','6FACD4','6FACEB','6FACF0','6FADA5','6FADD0','6FADD5','6FADEC','6FADF1'],original_labels_retained=True),indent=2),encoding='utf-8')
