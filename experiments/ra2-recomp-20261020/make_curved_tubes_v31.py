"""Keep endpoints and ordinary orders; use legal cardinal/diagonal TubeClass segments."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v31'
route=[2,1,1,2,3,3,2,1,3,2];reverse=[(d+4)%8 for d in reversed(route)]
# Original initializer 4916D0 builds this table in BSS; it is not PE file data.
offsets=[(0,-256),(256,-256),(256,0),(256,256),(0,256),(-256,256),(-256,0),(-256,-256)]
assert sum(offsets[d][0] for d in route)==2560 and sum(offsets[d][1] for d in route)==0
records=[]
for name in ['east','west']:
 source=S/'fixtures'/('tube-'+name+'.MAP');text=source.read_text(encoding='ascii');m=re.search(r'(?ms)^\[Tubes\]\n.*\Z',text);assert m
 rows='[Tubes]\n0=68,114,2,78,114,'+','.join(map(str,route))+',-1\n1=78,114,6,68,114,'+','.join(map(str,reverse))+',-1\n'
 out=S/'fixtures'/('tube-curved-'+name+'.MAP');assert not out.exists();out.write_text(text[:m.start()]+rows,encoding='ascii',newline='\n')
 records.append(dict(path=out.relative_to(R).as_posix(),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
value=dict(passed=True,forward=route,reverse=reverse,endpoints_unchanged=True,diagonal_segments=6,raw_runtime_writes=False,fixtures=records,offset_initializer='4916D0',route_waypoints=[[68+sum(offsets[d][0]//256 for d in route[:i]),114+sum(offsets[d][1]//256 for d in route[:i])] for i in range(11)])
(S/'curved-tube-fixtures.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print('Created legal curved tubes; runtime validation pending')
