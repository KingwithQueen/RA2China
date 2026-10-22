from pathlib import Path
import re,json,shutil
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v14'
p=R/'ra2/src/recomp/gen_game/recomp_0003.c';t=p.read_text(encoding='utf-8')
t='#include "ground_path_distance_bridge.h"\n'+t
call=lambda name:'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); '+name+'(); RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n'
t,n=re.subn(r'L_00427E2A:.*?(?=    RECOMP_CALL\(sub_004BA410)', 'L_00427E2A:\n'+call('ra2_path_node_distance_bridge'),t,flags=re.S)
assert n==1,n
t,m=re.subn(r'L_00427880:.*?(?=L_004278C7:)', 'L_00427880:\n'+call('ra2_path_connection_distance_bridge'),t,flags=re.S);assert m==6,m
p.write_text(t,encoding='utf-8')
p=R/'ra2/CMakeLists.txt';t=p.read_text(encoding='utf-8');t+='\ntarget_sources(ra2 PRIVATE src/gameplay/ground_path_distance.c src/runtime/ground_path_distance_bridge.c)\nset_source_files_properties(src/gameplay/ground_path_distance.c src/runtime/ground_path_distance_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n';p.write_text(t,encoding='utf-8')
for p in R.glob('*v13*'):
    if p.is_file() and p.suffix in ('.ps1','.py') and not p.name.startswith(('prepare_','finalize_','integrate_')):
        dest=R/p.name.replace('v13','v14');assert not dest.exists();dest.write_text(p.read_text(encoding='utf-8-sig').replace('v13','v14'),encoding='utf-8')
for p in (R/'evidence/movement-state-v13').iterdir():
    if p.is_file() and p.suffix in ('.c','.h'):shutil.copy2(p,S/p.name)
shutil.copytree(R/'evidence/movement-state-v13/fixtures',S/'fixtures')
(S/'pending').mkdir(exist_ok=True)
(S/'distance-integration.json').write_text(json.dumps(dict(node=n,connection=m),indent=2),encoding='utf-8')
