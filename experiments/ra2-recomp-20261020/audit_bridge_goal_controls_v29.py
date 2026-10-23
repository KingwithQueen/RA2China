"""Preserve the original upper-surface goal selection, without claiming lower-chain coverage."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v29'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
scenes={}
for name in ['lower-north','lower-south']:
 modes={}
 for prefix in ['b-','h3-']:
  report=read(S/'runs'/(prefix+name)/'comparison.json');assert report['passed'] and report['comparison']['frames_compared']==901
  for mode in ['original','generated-c']:
   rows=[json.loads(l) for l in (S/'runs'/(prefix+name)/mode/'state.jsonl').open(encoding='utf-8')]
   states=[(r['frame'],next(o for o in r['objects'] if o['id']==1023362)) for r in rows if r['kind']=='state']
   assert len({tuple(o['position']) for _,o in states})==1 and states[0][1]['position'][2]==0
   elevated=[frame for frame,o in states if o['ground_drive']['destination'][2]==416]
   assert elevated and states[-1][1]['ground_drive']['destination']==[0,0,0]
   assert not any(r.get('kind')=='fixture-internal-hit' and r['id']==1023362 and r['stage'] in [18,22] for r in rows)
   modes[prefix+mode]=dict(upper_goal_frames=elevated,initial_position=states[0][1]['position'],
    final_position=states[-1][1]['position'],no_chain_entry=True)
 scenes[name]=dict(passed=True,modes=modes,counted_as_bridge_chain_coverage=False)
value=dict(passed=True,scenes=scenes,paired_frames=1802,independent_frames=1802,
 scope='Ordinary move orders targeting bridge cells select Z416 although actor starts below at Z0; the original clears the goal without movement or object-chain entry. Original/C equality is preserved separately from the four qualified bridge-chain scenes.')
(S/'bridge-goal-controls.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,control_scenes=2,qualified_chain_coverage=False)))
