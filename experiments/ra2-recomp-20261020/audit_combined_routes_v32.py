"""Require occupied exit, waiting, ordinary recovery and independent observer parity."""
from pathlib import Path
import hashlib, json
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v32'
sha = lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def rows(tag,mode):
    return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def ordered(rs):
    return [r for r in rs if r['kind'] in ['submit','execute','movement-audit'] or r['kind'].startswith('fixture-')]
production = sha(R/'ra2/build-original-c/ra2.exe')
helper = sha(S/'connection-fixture-probe.exe')
scenes = {}
for name,goal,height,exit_cell in [('ub',80,728,[78,114]),('db',66,416,[68,114]),('mu',80,728,[78,114]),('md',66,416,[68,114])]:
    tags = ['k-'+name,'x-'+name]
    fixture = S/'fixtures'/dict(ub='tube-curved-tall-east.MAP',db='tube-curved-elevated-west.MAP',mu='tube-mirror-east.MAP',md='tube-mirror-west.MAP')[name]
    for tag in tags:
        r = read(S/'runs'/tag/'comparison.json');c = r['comparison']
        assert r['passed'] and r['exe_sha256'] == (helper if tag[0]=='k' else production)
        assert r['scenario_sha256']==sha(fixture) and r['input_exe_sha256']==sha(R/'ra2/game/game.exe')
        assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==601
        assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
        assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
        assert all(x['passed'] and x['exit_code']==0 and x['save_is_private_copy'] and x['save_before_sha256']==x['save_after_sha256'] for x in r['runs'])
        assert ordered(rows(tag,'original'))==ordered(rows(tag,'generated-c'))
    modes = {}
    for mode in ['original','generated-c']:
        observed,plain = (rows(tag,mode) for tag in tags)
        assert [r for r in observed if r['kind']=='state']==[r for r in plain if r['kind']=='state']
        assert [r for r in ordered(observed) if r['kind'] not in ['fixture-internal-hit','fixture-connection-hit']]==ordered(plain)
        hits = [r for r in observed if r['kind']=='fixture-connection-hit']
        assert all(any(h['stage']==stage for h in hits) for stage in [0,1,2,3,4,5,6,7,8,9])
        waiting = [h for h in hits if h['stage']==3]
        exits = [h for h in hits if h['stage']==2]
        assert len(waiting)>=20 and len(exits)==1
        assert [h['frame'] for h in waiting] == list(range(waiting[0]['frame'],exits[0]['frame']))
        assert len({tuple(h['position']) for h in waiting})==1
        progress = [h for h in hits if h['stage']>=4]
        assert any(h['position'][1]!=29312 for h in progress)
        assert len({h['flags'][1] for h in progress})>=8
        heights = [h['position'][2] for h in progress]
        assert max(heights)-min(heights)>100
        units = [r for r in plain if r['kind']=='fixture-unit']
        assert len(units)==16 and all(r['frame']==217 for r in units)
        assert exit_cell in [r['cell'] for r in units]
        constraints = [r for r in plain if r['kind']=='fixture-constraints']
        assert len(constraints)==1 and constraints[0]['explicit_rebuild_result']==4294967295
        last = next(o for r in reversed(plain) if r['kind']=='state' for o in r['objects'] if o['id']==1022581)
        assert last['position']==[goal*256+128,29312,height] and last['ground_drive']['destination']==[0,0,0]
        modes[mode] = dict(wait_frames=[h['frame'] for h in waiting],exit_frame=exits[0]['frame'],height_range=[min(heights),max(heights)],
                           final_position=last['position'],destination_cleared=True,actual_exit_cell_occupied=True,
                           independent_observer_and_production_identical=True)
    scenes[name] = dict(passed=True,frames=601,production_tag=tags[1],observer_tag=tags[0],fixture_sha256=sha(fixture),modes=modes)
out = S/'combined-real-scenes.json'
assert not out.exists()
out.write_text(json.dumps(dict(passed=True,production_scenes=4,production_frames=2404,independent_observer_frames=2404,
    production_executable_sha256=production,observer_executable_sha256=helper,scenes=scenes,
    scope='Four curved height/occupied-exit combinations, including mirrored curvature. Legal map Tubes/height records and ordinary constructor/placement services; no motion/path/budget injection or explicit rebuilding.'),indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,scenes=4,frames=2404,waits={k:len(v['modes']['original']['wait_frames']) for k,v in scenes.items()})))
