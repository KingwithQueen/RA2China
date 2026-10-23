"""Normal map headings and mirrored actor placement; no runtime movement-state writes."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v35';records=[]
def adjust(text,key,mirror,sub_override):
    m=re.search(r'(?ms)^\['+key+r'\]\n(.*?)(?=^\[|\Z)',text);assert m;lines=[]
    for row in m[1].splitlines():
        if not row.strip():continue
        index,body=row.split('=',1);v=body.split(',');inf=key=='Infantry'
        if mirror:
            v[4]=str(133-int(v[4]))
            if inf:v[5]=str({0:0,1:3,2:4,3:1,4:2}[int(v[5])])
        v[7 if inf else 5]=str((128-int(v[7 if inf else 5]))&255)
        if inf and int(index)==2 and sub_override is not None:v[5]=str(sub_override)
        lines.append(index+'='+','.join(v))
    return text[:m.start(1)]+'\n'.join(lines)+'\n\n'+text[m.end(1):]
for name,mirror,sub in [('nmirror',True,None),('nface',False,None),('nsub',False,4)]:
    source=S/('fixtures/bridge-infantry-meeting-'+('south' if mirror else 'north')+'.MAP');text=source.read_text(encoding='ascii')
    for key in ['Units','Infantry']:text=adjust(text,key,mirror,sub)
    p=S/f'fixtures/bridge-north-lane-{name}.MAP';p.write_text(text,encoding='ascii',newline='\n')
    records.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),query_after_frame=5,
        orders=['5:1023362:2:60:72','5:1023367:2:60:61',f'1:1023364:2:60:{58 if mirror else 75}'],
        actor_ids=[1023362,1023367],vehicle_id=1023362,infantry_id=1023367,goals={'1023362':[60,72],'1023367':[60,61]},
        mirrored_actors=mirror,normal_map_headings=True,source=source.relative_to(R).as_posix()))
(S/'north-query-candidates.json').write_text(json.dumps(dict(passed=True,fixtures=records,ordinary_move_orders=True,raw_state_writes=False),indent=2)+'\n',encoding='utf-8')
print('Created three normal heading and actor-mirror candidates')
