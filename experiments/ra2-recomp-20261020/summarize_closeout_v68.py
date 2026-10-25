"""Count executed evidence once; preserve diagnostic inputs and finite limits."""
from run_batch_v68 import *
required=['source-preservation.json','movement-code-inventory.json','record-parity.json','reachability-fairness.json','occupation-stop-rules.json','other-movement-acceptance.json','stop-command-acceptance.json','regressions.json','final-native.json']
for name in required:assert read(S/name)['passed'],name
rows=[]
for name in ['b-scenes.json','f-scenes.json','regressions.json']:
    rows.extend(read(S/name)['results'])
for tag in ['b-gtypes','f-gtypes','f-gtypes-obs','b-stopcmd','f-stopcmd']:
    p=S/'runs'/tag/'comparison.json';d=read(p);assert all(v['passed'] and v['exit_code']==0 for v in d['runs'])
    assert d['comparison']['negative_control']['passed']
    rows.append(dict(tag=tag,frames=d['comparison']['frames_compared'],strict=d['passed'],comparison_sha256=sha(p),exe_sha256=d['exe_sha256']))
native=read(S/'final-native.json');keys={'prepare':['entry_cases','retry_cases'],'obstacle':['failed_rebuild_cases','rebuilt_cases'],'arrival':['native_arrival_cases'],'ground-services':['cases'],'collision':['native_occupation_cases','native_bridge_layer_cases'],'map-area':['map_area_cases']}
count=0;fragments=0
for q in native['probes']:
    assert q['result']['passed'];count+=sum(q['result'][k] for k in keys[q['probe']]);fragments+=len(keys[q['probe']])
assert count==630784 and fragments==9
traces=[]
for q in rows:
    p=S/'runs'/q['tag']/'comparison.json';d=read(p);assert q['comparison_sha256']==sha(p)
    for mode in ['original','generated-c']:
        t=p.parent/mode/'state.jsonl';traces.append(dict(tag=q['tag'],mode=mode,path=str(t),sha256=sha(t)))
    assert q['strict'] or q['tag'] in ['b-gtypes','f-gtypes','f-gtypes-obs']
for p in [R/n for n in ['run_fixture_comparison.py','run_state_comparison.py','build-faithful.ps1']]:assert p.exists()
helper_hashes=[dict(path=str(p),sha256=sha(p)) for p in sorted(R.glob('*v68*')) if p.is_file()]
probe_hashes=[dict(path=str(p),sha256=sha(p)) for p in sorted(S.iterdir()) if p.is_file() and p.suffix in ['.c','.h','.exe','.py']]
write(S/'evidence-rollup.json',dict(passed=True,formal_generation=67,verification_round=68,accepted_pairs=len(rows),accepted_frames=sum(v['frames'] for v in rows),strict_pairs=sum(v['strict'] for v in rows),functional_pairs=sum(not v['strict'] for v in rows),native_cases=count,native_programs=len(native['probes']),native_fragments=fragments,pairs=rows,traces=traces,helper_hashes_before_finalization=helper_hashes,probe_and_observer_hashes=probe_hashes,excluded=['id-free','id-occ','id-types','id-gtypes','b-types (invalid infantry OnBridge input)'],repeated_native_runs_counted_again=False,whole_game_equivalence_verified=False,fifo_guarantee=False,unbounded_starvation_freedom_proved=False,all_locomotors_readably_rewritten=False))
print(dict(passed=True,pairs=len(rows),frames=sum(v['frames'] for v in rows),strict=sum(v['strict'] for v in rows),functional=sum(not v['strict'] for v in rows),native_cases=count))
