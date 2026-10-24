"""Accept only a proved diagnostic-role duplication; retain the failed strict report."""
from run_batch_v41 import R,S,read,write,sha
import json
tag='observed-contact-train';out=S/'runs'/tag;x=read(out/'comparison.json');c=x['comparison']
assert not x['passed'] and c['first_difference'] is None and c['equal_frames']==c['frames_compared']==501 and c['rng_equal_all_frames']
assert x['exe_sha256']==sha(S/'connection-fixture-probe.exe')
assert all(r['passed'] and r['exit_code']==0 and r['save_before_sha256']==r['save_after_sha256'] for r in x['runs'])
rows=lambda mode:[json.loads(l) for l in (out/mode/'state.jsonl').open(encoding='utf-8')]
a,b=rows('original'),rows('generated-c');states=lambda rs:[r for r in rs if r['kind']=='state'];assert states(a)==states(b)
ordinary=lambda rs:[r for r in rs if r['kind'] in ['submit','execute','movement-audit']];assert ordinary(a)==ordinary(b)
frames={158,191,208};extra=[r for r in b if r['kind']=='fixture-internal-hit' and r['stage']==16 and r['frame'] in frames and r['position'][2]==0]
assert len(extra)==3 and {r['frame'] for r in extra}==frames
assert all(r['id']==1023362 and r['value']==[0,0] and r['position'][2]==0 and r['destination']==[15488,19328,416] for r in extra)
assert not any(r['kind']=='fixture-internal-hit' and r['stage']==16 and r['frame'] in frames and r['position'][2]==0 for r in a)
events=lambda rs:[r for r in rs if r['kind'] in ['submit','execute','movement-audit'] or r['kind'].startswith('fixture-')]
filtered=[r for r in b if r not in extra];assert events(a)==events(filtered)
source=(R/'make_connection_fixture_v41.py').read_text(encoding='utf-8')
assert 'ra2_internal_observe(((AdvanceContext *)opaque)->drive,0,16,0,0)' in source
core=(R/'ra2/src/gameplay/ground_advance.c').read_text(encoding='utf-8');assert core.count('s->raw_position(c)')==2
value=dict(passed=True,strict_internal_trace_equal=False,tag=tag,comparison_sha256=sha(out/'comparison.json'),frames=501,game_state_and_rng_equal=True,ordinary_commands_and_movement_audit_equal=True,all_other_diagnostic_events_equal=True,extra_generated_diagnostic_records=extra,cause='The C observer marks every raw_position callback as stage16. Native stage16 is hooked only at the main sample position read. Train lower-layer contact also reads position through the shared callback at these three frames. Reads do not call a game service or change state.',policy='Overall functionality/effects, not exact diagnostic event counts. Strict report and both full traces remain unchanged; no production code or comparator relaxation.',observer_source_sha256=sha(S/'connection_advance_bridge.c'))
write(out/'functional-acceptance.json',value);write(S/'observer-variation.json',value)
print(dict(passed=True,diagnostic_only_extra_records=3,strict_report_preserved=True))
