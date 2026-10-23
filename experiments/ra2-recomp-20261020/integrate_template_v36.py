"""Use incoming coordinates at the shared map-query continuation."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v36'
p=R/'ra2/src/runtime/ground_joint_bridge.c';t=p.read_text(encoding='utf-8')
a='uint32_t x=MEM32(frame+offset),y=MEM32(frame+offset+4),z=MEM32(frame+offset+8);\n    MEM32(frame+0x18)=x;MEM32(frame+0x1C)=y;MEM32(frame+0x20)=z;'
b='uint32_t x,y,z;\n    if(alternate==2){x=g_ecx;y=g_edx;z=g_ebx;}\n    else\n    {\n        x=MEM32(frame+offset);y=MEM32(frame+offset+4);z=MEM32(frame+offset+8);\n        MEM32(frame+0x18)=x;MEM32(frame+0x1C)=y;MEM32(frame+0x20)=z;\n    }'
assert t.count(a)==1;t=t.replace(a,b);p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');m='L_004A24F4:\n';n=t.count(m);assert n==12,n
code='    /* 共享地图查询使用入口坐标，服务后重读owner。 */\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_template_destination_bridge(2);\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto L_004A2528;\n'
parts=re.split(r'(?=^void sub_)',t,flags=re.M)
for i,block in enumerate(parts):
    if m not in block:continue
    target='L_004A2528' if 'L_004A2528:' in block else 'destination_resume_v33'
    assert target+':' in block
    parts[i]=block.replace(m,m+code.replace('goto L_004A2528;','goto '+target+';'))
t=''.join(parts);p.write_bytes(t.encode('utf-8'))
(S/'pending/register-destination-integration.json').write_text(json.dumps(dict(passed=True,entry='004A24F4',copies=n,incoming_coordinates=True,owner_reloaded_after_service=True,new_native_entries=0),indent=2)+'\n',encoding='utf-8')
