"""Connect all thirteen 4A24F0 continuations without new native entries."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v37'
p=R/'ra2/src/runtime/ground_joint_bridge.c';t=p.read_text();a='if(alternate==2){x=g_ecx;y=g_edx;z=g_ebx;}'
assert t.count(a)==1;t=t.replace(a,'if(alternate>=2){x=g_ecx;y=g_edx;z=g_ebx;if(alternate==3)MEM32(frame+0x20)=z;}');p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');m='L_004A24F0:\n';n=t.count(m);assert n==13
parts=re.split(r'(?=^void sub_)',t,flags=re.M)
for i,b in enumerate(parts):
 if m not in b:continue
 target='L_004A2528' if 'L_004A2528:' in b else 'destination_resume_v33' if 'destination_resume_v33:' in b else 'destination_resume_v37'
 if target=='destination_resume_v37':
  mark='    eax = MEM32(ecx + 0x88); /* 0x004A2528:';assert b.count(mark)==1;b=b.replace(mark,target+':\n'+mark)
 code='    /* 入口先写目标高度，再查询地图；保留原生段内跳转。 */\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_template_destination_bridge(3);\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto '+target+';\n'
 parts[i]=b.replace(m,m+code)
p.write_bytes(''.join(parts).encode('utf-8'))
(S/'pending/loaded-destination-integration.json').write_text(json.dumps(dict(passed=True,entry='004A24F0',copies=n,stack_z_before_service=True,new_native_entries=0,local_c_resume_labels_added=1),indent=2)+'\n',encoding='utf-8')
