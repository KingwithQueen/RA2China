"""Bounded call provenance; retain divergence instead of resynchronizing RNG."""
from run_batch_v49 import *
def rows(p):return [json.loads(l) for l in p.open(encoding='utf-8')]
data={m:rows(S/'runs/rng2'/m/'state.jsonl.rng.jsonl') for m in ['original','generated-c']}
prefixes={}
for mode in data:
 current=rows(S/'runs/rng2'/mode/'state.jsonl');old=rows(O/'runs/b3-dc'/mode/'state.jsonl')
 # Only the last-frame declaration and future commands differ; all actual records match.
 a=[q for q in current if q['kind'] not in ['header','complete']];b=[q for q in old if q['kind']!='header']
 # Stop occurs at the entry snapshot1046, before that frame's AI callbacks.
 assert a==b[:len(a)],(mode,'Diagnostic changed gameplay prefix')
 assert current==rows(S/'runs/rng1'/mode/'state.jsonl')
 prefixes[mode]=dict(diagnostic_trace_sha256=sha(S/'runs/rng2'/mode/'state.jsonl'),parent_trace_sha256=sha(O/'runs/b3-dc'/mode/'state.jsonl'),complete_records_equal_through=1045,last_equal_entry_snapshot=1046)
draws={m:[q for q in rs if q['kind'] in [0,2]] for m,rs in data.items()};n=min(map(len,draws.values()))
assert n>300
assert [(q['indices'],q['word']) for q in draws['original'][:n]]==[(q['indices'],q['word']) for q in draws['generated-c'][:n]]
assert len(draws['original'])==len(draws['generated-c'])+1
interesting={m:[q for q in rs if q['kind']==1 and q['bounds']==[0,2]] for m,rs in data.items()}
a=interesting['original'][0];b=interesting['generated-c'][0]
assert a['frame']==1028 and a['caller']==0x4C394A and a['object_ids'][0]==1023362
assert b['frame']==1029 and b['caller']==0x4C4660 and b['object_ids'][0]==1023362
# The raw native caller is return VA 4C394A (call at3945); lifted C reports entry4C38D0.
states={m:{q['frame']:{o['id']:o for o in q['objects']} for q in rows(S/'runs/rng2'/m/'state.jsonl') if q['kind']=='state'} for m in data}
assert states['original'][1028][1023362]['mission'][0]==states['generated-c'][1028][1023362]['mission'][0]==2
assert states['original'][1029][1023362]['mission'][0]==2 and states['generated-c'][1029][1023362]['mission'][0]==5
rng={m:{q['frame']:q['rng'] for q in rows(S/'runs/rng2'/m/'state.jsonl') if q['kind']=='state'} for m in data}
first=next(f for f in rng['original'] if rng['original'][f]!=rng['generated-c'][f])
assert first==1029
for tag in ['rng1','rng2']:
 q=read(S/'runs'/tag/'comparison.json');assert not q['passed'] and all(r['passed'] for r in q['runs']) and not q['comparison']['rng_equal_all_frames']
result=dict(passed=True,scope='First RNG divergence of inherited timed-clear recipe, finite frames1027..1046 only; not full-game RNG proof.',first_divergent_snapshot=first,first_different_interval_calls=interesting,raw_draw_counts={m:len(v) for m,v in draws.items()},sequential_draws_with_same_indices_and_words=n,complete_prechange_prefixes=prefixes,arrival_state_original=states['original'][1029][1023362]['mission'],arrival_state_C=states['generated-c'][1029][1023362]['mission'],finding='Same LCRF consumes Move interval jitter at original call4C3945 in frame1028, while C next uses Guard interval jitter in Foot virtual129 at frame1029. Arrival/mission scheduling changes draw timing and later assignment; sampled raw generator sequence is identical.',root_cause_limit='First split traced to arrival/mission service scheduling. The earlier Hover numerical arrival difference is retained, not corrected; later full-tail random assignments are not proved equivalent.',strict_false_retained=True,production_rng_and_comparator_unchanged=True,not_promoted_as_strict_transport_pass=True,production_input_before=read(S/'rng-diagnostic-inputs.json'),diagnostic_executable_sha256=sha(S/'rng-attribution.exe'),attribution_sources=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [S/'rng_attribution_observer.c',S/'rng_attribution_recomp.c',S/'rng-attribution-build-arguments.json']])
write(S/'rng-provenance.json',result);print(dict(passed=True,first_snapshot=first,draws=n,calls=interesting))
