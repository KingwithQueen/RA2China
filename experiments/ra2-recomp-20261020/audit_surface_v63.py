"""Read-only surface classification from raw positions and per-map cell catalogues."""
from run_batch_v63 import *
profiles={}
for item in read(S/'traffic-fixtures.json')['fixtures']:
 assert sha(R/item['path'])==sha(Path(item['source']))==item['source_sha256']
 for tag in [item['baseline_tag'],item['tag']]:
  profiles[tag]={}
  for mode in ['original','generated-c']:
   folder=S/'runs'/tag/mode
   cells={tuple(c['cell']):c for c in read(folder/'cells.json')['cells']}
   observed={};ground_levels=set();zs=set()
   for line in (folder/'state.jsonl').open(encoding='utf-8'):
    r=json.loads(line)
    if r['kind']!='state':continue
    for o in r['objects']:
     if o['id'] not in item['actor_ids']:continue
     xy=tuple(v//256 for v in o['position'][:2]);c=cells[xy];z=o['position'][2];zs.add(z)
     if c['bridge']:
      assert c['level']==0 and z==416
      q=observed.setdefault(xy,dict(cell=list(xy),base_land=c['land'],base_level=c['level'],cell_bridge=c['bridge'],unit_z=z,first_frame=r['frame'],frames=0));q['frames']+=1
     else:
      assert c['land'] in [0,1,6,7] and c['level'] in [4,5]
      ground_levels.add(c['level'])
   assert observed and ground_levels=={4,5} and min(zs)==416 and max(zs)==520 and len(zs)>2
   profiles[tag][mode]=dict(bridge_cells=list(observed.values()),unbridged_ground_levels=sorted(ground_levels),unit_z_range=[min(zs),max(zs)],distinct_z_values=len(zs),state_sha256=sha(folder/'state.jsonl'),catalog_sha256=sha(folder/'cells.json'))
write(S/'bridge-surface-profile.json',dict(passed=True,scenes=profiles,ground_plane_helper=str(R/'ra2/src/gameplay/ground_bridge_plane.c'),ground_plane_helper_sha256=sha(R/'ra2/src/gameplay/ground_bridge_plane.c'),parent_land_proof=str(O/'channel-land-proof.json'),parent_land_proof_sha256=sha(O/'channel-land-proof.json'),checker_correction='The initial current traffic predicate omitted flagged bridge cells whose base terrain is Rock=3. Retained baseline original/C comparisons were strict. Classify only observed base-level0 flagged bridge cells at Z416 as bridge surface; unflagged land remains restricted to Clear/Road/Beach/Rough. No production, rule, map or raw trace changes and no duplicate game runs.',unit_upper_bridge_flag_transition_proved=False,scope='Cell bridge flag plus actual unit height is surface evidence; no claim of a newly instrumented per-unit upper-layer flag.'))
print(dict(passed=True,recipes=2,observed_ground_levels=[4,5],height_range=[416,520]))
