"""Record unsuccessful trigger setup separately from actual native enemy motion."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v34'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs=[Path(__file__)];records=[]
for tag,frames,moving in [('inv-enemy-ai-north',301,False),('inv-enemy-ai2-north',181,False),('inv-enemy-ai3-north',181,True)]:
    report=S/'runs'/tag/'comparison.json';x=json.loads(report.read_text(encoding='utf-8'));c=x['comparison']
    assert x['passed'] and c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==frames
    assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
    counts=[]
    for mode in ['original','generated-c']:
        p=report.parent/mode/'state.jsonl';rows=[json.loads(l) for l in p.open(encoding='utf-8')];states=[r for r in rows if r['kind']=='state']
        positions={tuple(o['position']) for r in states for o in r['objects'] if o['id']==1023363}
        assert (len(positions)>1)==moving
        assert not any(r['kind']=='submit' and r['id']==1023363 for r in rows)
        counts.append(len(positions));inputs += [p,report.parent/mode/'command.json']
    assert counts[0]==counts[1]
    fixture=Path(x['scenario_map']);fixture=fixture if fixture.is_absolute() else R/fixture
    assert sha(fixture)==x['scenario_sha256']
    assert ('[Tags]\n' in fixture.read_text(encoding='ascii'))==moving
    records.append(dict(tag=tag,frames=frames,setup_investigation_only=True,native_and_c_equal=True,enemy_positions=counts[0],enemy_moves=moving,enemy_player_order=False))
    inputs += [report,fixture]
value=dict(passed=True,accepted_production_scenes=0,records=records,
    conclusion='The first two setup trials lacked an instantiated Tags entry and produced no enemy motion. The third adds the normal tag instance: the original CreateTeam action recruits the placed enemy truck and script action3 drives it. These short trials are kept separate from the later 901-frame accepted scenes.',
    inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in inputs])
out=S/'native-team-setup-investigation.json';assert not out.exists();out.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,setup_trials=records)))
