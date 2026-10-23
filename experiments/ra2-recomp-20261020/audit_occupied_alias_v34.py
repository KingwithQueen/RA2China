"""Separate observed original internal boundaries from independent C alias dispatch."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v34';read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=lambda t,m:[json.loads(l) for l in (S/'runs'/t/m/'state.jsonl').open(encoding='utf-8')]
ordered=lambda rs:[r for r in rs if r['kind'] in ['submit','execute','movement-audit'] or r['kind'].startswith('fixture-')]
seen=set();records=[];candidates=[];inputs=[Path(__file__),R/'run_occupied_alias_probe_v34.py',R/'run_occupied_alias_scenes_v34.py',S/'internal-alias-sources.json']
for group in range(6):
    tag='ao-'+str(group);base='oh-'+('north' if group%2==0 else 'south');v=read(S/'runs'/tag/'comparison.json');c=v['comparison'];bv=read(S/'runs'/base/'comparison.json')
    assert v['passed'] and v['exe_sha256']==sha(S/'connection-fixture-probe.exe') and v['scenario_sha256']==bv['scenario_sha256'] and v['seed']==bv['seed']==12345
    assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901 and c['rng_equal_all_frames'] and c['first_difference'] is None and c['command_difference'] is None
    assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
    assert all(x['passed'] and x['exit_code']==0 and x['save_is_private_copy'] and x['save_before_sha256']==x['save_after_sha256'] for x in v['runs'])
    a,b=rows(tag,'original'),rows(tag,'generated-c');assert ordered(a)==ordered(b)
    for mode,observed in [('original',a),('generated-c',b)]:
        plain=rows(base,mode);assert [r for r in observed if r['kind']=='state']==[r for r in plain if r['kind']=='state'] and ordered(observed)==ordered(plain)
    cmd=read(S/'runs'/tag/'generated-c/command.json');configured={f'{int(cmd[i+1],0):08X}' for i,x in enumerate(cmd) if x=='--probe'}
    counts=Counter(re.findall(r'^\[probe\] sub_([0-9A-F]{8}) from ',(S/'runs'/tag/'generated-c/run.log').read_text(encoding='utf-8',errors='replace'),re.M));assert all(counts[p]>0 for p in ['004A1000','004A2670','00703040'])
    aliases=configured-{'004A1000','004A2670','00703040'};seen.update(aliases);candidates.extend(dict(tag=tag,entry=p,records=counts[p]) for p in sorted(aliases) if counts[p])
    records.append(dict(tag=tag,frames=901,configured_aliases=sorted(aliases),first_call_record_counts={p:counts[p] for p in sorted(configured)}))
    inputs.extend([S/'runs'/tag/'comparison.json',S/'runs'/tag/'generated-c/command.json',S/'runs'/tag/'generated-c/run.log'])
assert len(seen)==28 and seen=={e['entry'] for e in read(S/'internal-alias-sources.json')['entries'] if e['entry_kind']=='alias'}
value=dict(passed=not candidates,scenes=6,frames=5406,aliases=28,records=records,natural_entry_candidates=candidates,nonprimary_natural_entry_proved=False,production_observer_state_identity=True,limits='All28 configured candidates across six alternating north/south occupied-exit scenes; not every candidate in every scene. Primary positive controls are present. Fixed-frame first-call observation is not an exclusion of arbitrary computed targets or unrun routes.',inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in inputs])
(S/'alias-occupied-natural-scenes.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');assert not candidates,candidates;print(dict(passed=True,aliases=28,frames=5406))
