"""Preserve the original ownership rejection as a control, never as acceptance."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v35'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
inputs=[Path(__file__)];records=[]
for tag in ['ep-enemy-traffic-north','eh-enemy-traffic-north']:
    p=S/'runs'/tag/'comparison.json';x=read(p)
    assert not x['passed'] and 'comparison' not in x
    assert all(r['exit_code']==7 and not r['passed'] and r['failures']==['[state-error] order was not submitted and executed'] and r['save_before_sha256']==r['save_after_sha256'] for r in x['runs'])
    sets=[]
    for mode in ['original','generated-c']:
        folder=p.parent/mode;rows=[json.loads(l) for l in (folder/'state.jsonl').open(encoding='utf-8')]
        states=[r for r in rows if r['kind']=='state'];assert [r['frame'] for r in states]==list(range(901))
        assert any(r['kind']=='submit' and r['id']==1023363 for r in rows)
        assert not any(r['kind']=='execute' and r['id']==1023363 for r in rows)
        assert any(r['kind']=='execute' and r['id']==1023362 for r in rows)
        assert len({tuple(o['position']) for r in states for o in r['objects'] if o['id']==1023363})==1
        sets.append(rows);inputs += [folder/n for n in ['state.jsonl','run.log','command.json']]
    assert sets[0]==sets[1]
    inputs += [p,Path(x['scenario_map'])]
    records.append(dict(tag=tag,control_only=True,frames_recorded=901,enemy_player_submit_executed=False,own_player_order_executed=True,
        native_and_c_rows_identical=True,scenario_sha256=x['scenario_sha256']))
value=dict(passed=True,accepted_production_scenes=0,accepted_frames=0,controls=records,
    conclusion='Both original and C reject execution of the player order to the enemy-owned unit. These failed acceptance attempts remain in their original run directories; they are not retries, success receipts, or evidence of moving enemy traffic.',
    inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in inputs])
out=S/'rejected-enemy-order-control.json';assert not out.exists();out.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,controls=2,accepted_frames=0)))
