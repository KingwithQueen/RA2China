"""Use ordinary placed exit vehicles and delayed ordinary departure orders."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38';items=[]
for direction,source,block_y,clear_y in [('north','bridge-north-lane-nsub.MAP',70,79),('south','bridge-infantry-meeting-south.MAP',63,57)]:
    p=S/'fixtures'/source;t=p.read_text(encoding='utf-8');section=None;out=[];changed=0
    for line in t.splitlines():
        if line.startswith('['):section=line
        if section=='[Units]' and line.startswith(('1=','2=')):
            k,v=line.split('=',1);fields=v.split(',');assert fields[1]=='TRUCKA';fields[3]='61' if k=='1' else '60';fields[4]='66';fields[10]='1';line=k+'='+','.join(fields);changed+=1
        if direction=='south' and section=='[Infantry]' and line.startswith('2='):
            k,v=line.split('=',1);fields=v.split(',');assert fields[1]=='E2';fields[3:6]=['61','64','4'];line=k+'='+','.join(fields)
        out.append(line)
    assert changed==2
    dest=S/'fixtures'/('bridge-occupied-'+direction+'.MAP');dest.write_text('\n'.join(out)+'\n\n',encoding='utf-8',newline='\n')
    north=direction=='north';goals={'1023362':[60,75 if north else 58],'1023367':[60 if north else 61,61 if north else 72]}
    orders=[f'1:1023364:2:60:{block_y}',f'1:1023363:2:61:{block_y}',f'5:1023362:2:60:{goals["1023362"][1]}',f'5:1023367:2:{goals["1023367"][0]}:{goals["1023367"][1]}',f'300:1023364:2:60:{clear_y}',f'300:1023363:2:61:{clear_y}',f'320:1023362:2:60:{goals["1023362"][1]}']
    items.append(dict(name=direction,path=dest.relative_to(R).as_posix(),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),actor_ids=[1023362,1023367],blocker_id=1023364,blocker_ids=[1023363,1023364],blocker_cell=[60,block_y],release_frame=300,reissue_frame=320,goals=goals,orders=orders,source=p.relative_to(R).as_posix(),ordinary_map_and_orders=True,raw_state_writes=False))
(S/'bridge-occupied-fixtures.json').write_text(json.dumps(dict(passed=True,fixtures=items),indent=2)+'\n',encoding='utf-8')
