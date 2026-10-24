"""Separate issued release orders from actual original movement of each blocker."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base=read(S/'bridge-neighbor-release-real-scenes.json');assert base['passed']
records={};inputs=[Path(__file__),S/'bridge-neighbor-release-real-scenes.json',S/'bridge-neighbor-release-fixtures.json']
for item in read(S/'bridge-neighbor-release-fixtures.json')['fixtures']:
 modes={};name=item['name'];car=item['actor_ids'][0]
 for mode in ['original','generated-c']:
  p=S/'runs'/('nr-'+name)/mode/'state.jsonl';rs=[json.loads(l) for l in p.open(encoding='utf-8')];inputs.append(p)
  h={r['frame']:{o['id']:o for o in r['objects']} for r in rs if r['kind']=='state'}
  cross=base['scenes'][name]['modes'][mode]['crossed_exit_frame'];wait=base['scenes'][name]['modes'][mode]['wait_range'][0]
  rows=[]
  for u in sorted(item['blocker_ids'],key=lambda u:item['release_frames'][str(u)]):
   command=item['release_frames'][str(u)];motion=next(f for f in range(command,901) if h[f][u]['position']!=h[f-1][u]['position'])
   held_through_cross=all(h[f][u]['position']==h[wait][u]['position'] for f in range(wait,cross+1))
   rows.append(dict(id=u,normal_release_order_frame=command,first_actual_motion_frame=motion,order_to_motion_delay_frames=motion-command,held_through_vehicle_crossing=held_through_cross,position_at_cross=h[cross][u]['position']))
  assert not rows[0]['held_through_vehicle_crossing'] and rows[0]['first_actual_motion_frame']<cross
  assert rows[1]['held_through_vehicle_crossing'] and rows[1]['first_actual_motion_frame']>cross
  assert all(e['order_to_motion_delay_frames']>=0 for e in rows)
  early,late=[e['id'] for e in rows];simultaneous=[]
  for f in range(rows[0]['normal_release_order_frame']+1,rows[1]['normal_release_order_frame']):
   a,b=h[f][car]['position'],h[f][early]['position']
   if a[2]==b[2]==416 and a!=h[f-1][car]['position'] and b!=h[f-1][early]['position'] and a[0]//256 not in [60,61] and abs(a[1]-b[1])<=1024 and h[f][late]['position']==h[wait][late]['position']:simultaneous.append(f)
  assert simultaneous,(name,mode,'No simultaneous deck detour and adjacent traffic with held main lane')
  modes[mode]=dict(vehicle_crossed_exit_frame=cross,blockers=rows,simultaneous_near_exit_detour_frames=simultaneous,simultaneous_near_exit_detour_frame_count=len(simultaneous))
 assert modes['original']==modes['generated-c'];records[name]=modes
value=dict(passed=True,scenes=records,scope='Release orders are ordinary submitted commands. Actual blocker motion is measured independently. In this pair the main car crosses after the neighboring blocker starts moving and before the main-lane blocker leaves. The two lane-release orders and actual movement times are measured separately. No anomaly is corrected.',inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in inputs])
out=S/'bridge-neighbor-release-motion.json';assert not out.exists();out.write_text(json.dumps(value,indent=2)+chr(10),encoding='utf-8');print(json.dumps(dict(passed=True,scenes=records)))
