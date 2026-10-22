from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'ra2/src/recomp/gen_game/recomp_0046.c';t=p.read_text(encoding='utf-8');assert 'ground_objects_bridge.h' not in t
t='#include "ground_objects_bridge.h"\n'+t
branches={
    '0070346B':(0,[(0x7031B1,'007031B1'),(0x703A95,'00703A95'),(0x703536,'00703536'),(0x7038FD,'007038FD')],'00703693'),
    '007035AC':(1,[(0x703B5A,'00703B5A'),(0x7038FD,'007038FD')],'00703693'),
    '0070397C':(2,[(0x703B5A,'00703B5A')],'007038EF'),
    '0070394F':(3,[(0x703B5A,'00703B5A')],'007038EF')}
for label,(entry,options,default) in branches.items():
    needle='L_'+label+':\n';assert needle in t,label
    code='    /* 可读 C：对象/建筑过滤与敌我通行分类。 */\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();\n'
    code+=f'    uint32_t object_resume_v9_{entry} = ra2_ground_object_branch_bridge({entry});\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n'
    for address,target in options: code+=f'    if (object_resume_v9_{entry} == 0x{address:X}) goto L_{target};\n'
    code+='    goto L_'+default+';\n'
    t=t.replace(needle,needle+code)
p.write_text(t,encoding='utf-8',newline='\n')
p=ROOT/'ra2/CMakeLists.txt';t=p.read_text(encoding='utf-8').replace('  src/gameplay/ground_entry.c\n',
    '  src/gameplay/ground_entry.c\n  src/gameplay/ground_objects.c\n  src/runtime/ground_objects_bridge.c\n')
t+='\nset_source_files_properties(src/gameplay/ground_objects.c src/runtime/ground_objects_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
p.write_text(t,encoding='utf-8',newline='\n')
