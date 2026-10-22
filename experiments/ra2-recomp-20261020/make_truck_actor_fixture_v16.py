"""Default-rule AI TRUCKA actor, created and ordered through original services."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v16'
t=(S/'truck_movement_fixture.c').read_text(encoding='utf-8')
needle='    uint32_t locomotion = U32(actor + 0x564);'
insert='''    /* Independent scene setup: a real unarmed AI truck avoids combat overriding
       the blocked move. Only constructor/placement/mission/destination services run. */
    uint32_t reference = actor, source_drive = U32(actor + 0x564) - 4;
    int32_t goal_x = (int32_t)U32(source_drive + 0x34) / 256;
    int32_t goal_y = (int32_t)U32(source_drive + 0x38) / 256;
    if (!goal_x || !goal_y) fixture_fail("reference has no accepted move");
    uint32_t truck_type=0, tc=U32(0xA35D58), td=U32(0xA35D4C);
    if (tc>4096) fixture_fail("invalid type vector");
    for(uint32_t ti=0;ti<tc;++ti) {
        uint32_t candidate=U32(td+ti*4);
        if(candidate && U32(candidate)==0x7AE328 && !strcmp((const char *)(uintptr_t)(candidate+0x24),"TRUCKA")) truck_type=candidate;
    }
    if(!truck_type) fixture_fail("TRUCKA type missing");
    int32_t px=(int32_t)U32(reference+0x88)/256+12, py=(int32_t)U32(reference+0x8C)/256;
    uint32_t actor_size=0x7D0;
    actor=fixture_call(original_mode,0x782017,0,&actor_size,1);
    if(!actor) fixture_fail("truck allocation failed");
    uint32_t ctor[2]={truck_type,U32(reference+0x1B4)};
    fixture_call(original_mode,0x6FA400,actor,ctor,2);
    int32_t actor_point[3]={px*256+128,py*256+128,(int32_t)U32(reference+0x90)};
    uint32_t placement[2]={(uint32_t)(uintptr_t)actor_point,0};
    if(!(fixture_call(original_mode,U32(U32(actor)+0xD4),actor,placement,2)&255u)) fixture_fail("truck placement failed");
    fixture_id=U32(actor+0x10);
    uint32_t mission[2]={2,0};
    fixture_call(original_mode,U32(U32(actor)+0x1D0),actor,mission,2);
    uint32_t target_cell=U32(U32(0x832618)+(goal_y*512+goal_x)*4);
    uint32_t dest[2]={target_cell,1};
    fixture_call(original_mode,U32(U32(actor)+0x410),actor,dest,2);
    fprintf(output,"{\\"kind\\":\\"fixture-actor\\",\\"frame\\":%u,\\"id\\":%u,\\"reference_id\\":%u,\\"type\\":\\"TRUCKA\\",\\"cell\\":[%d,%d],\\"ordered_goal\\":[%d,%d]}\\n",frame,fixture_id,U32(reference+0x10),px,py,goal_x,goal_y);
'''
assert t.count(needle)==1;t=t.replace(needle,insert+needle)
src=S/'truck_actor_movement_fixture.c';src.write_text(t,encoding='utf-8')
x=json.loads((S/'truck-fixture-build-arguments.json').read_text(encoding='utf-8'))
for k in ['compile','link']:x[k]=[a.replace('truck_movement_fixture','truck_actor_movement_fixture').replace('truck_fixture.pdb','truck_actor_fixture.pdb').replace('truck-fixture-probe','truck-actor-fixture-probe') for a in x[k]]
(S/'truck-actor-fixture-build-arguments.json').write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
build=(R/'build-truck-fixture-v16.ps1').read_text(encoding='utf-8').replace('truck-fixture-build-arguments.json','truck-actor-fixture-build-arguments.json')
(R/'build-truck-actor-fixture-v16.ps1').write_text(build,encoding='utf-8')
print('Created independent actor fixture, engine mission and destination setup only')
