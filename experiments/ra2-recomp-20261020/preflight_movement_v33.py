"""Concrete production identity, labels, byte styles and independent helper origins."""
from pathlib import Path
import hashlib, json, re
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v33'
read = lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt = read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count']==171 and len(receipt['inputs'])==292 and receipt['refreshed_count']==0
assert receipt['executable_sha256']==sha(R/'ra2/build-original-c/ra2.exe')
for path,digest in receipt['inputs'].items():
    assert sha(Path(path))==digest,path
for rel in ['run_fixture_comparison.py','run_state_comparison.py','ra2/src/runtime/state_trace.c']:
    assert (R/rel).read_bytes()==(S/'baseline'/rel).read_bytes(),rel
for filename,newline in [('recomp_0010.c','LF'),('recomp_0046.c','CRLF')]:
    path = R/'ra2/src/recomp/gen_game'/filename
    data = path.read_bytes()
    assert (b'\r\n' not in data) if newline=='LF' else data.count(b'\n')==data.count(b'\r\n')
    current = data.decode('utf-8')
    old = (S/'baseline/ra2/src/recomp/gen_game'/filename).read_text(encoding='utf-8')
    for pattern in [r'^L_[0-9A-F]+:',r'case (0x[0-9A-Fa-f]+u): goto',r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)']:
        assert re.findall(pattern,current,re.M)==re.findall(pattern,old,re.M),(filename,pattern)
for name in ['ground_template.c','ground_template_table.h','ground_objects.c','ground_building_flags.h','ground_sampling_shared.c','ground_sampling_shared.h','ground_enemy_kind.h','ground_allied.c','ground_moving_tail.h','ground_allied_relation.h','ground_enemy_contact.h']:
    text = (R/'ra2/src/gameplay'/name).read_text(encoding='utf-8')
    assert not any(s in text for s in ['MEM8(','MEM16(','MEM32('])
    assert not re.search(r'0x00[47][0-9A-Fa-f]{5}',text)
u = (R/'ra2/src/recomp/gen_game/recomp_0010.c').read_text(encoding='utf-8')
w = (R/'ra2/src/recomp/gen_game/recomp_0046.c').read_text(encoding='utf-8')
assert u.count('ra2_ground_template_table_bridge();')==7
assert w.count('ra2_ground_object_branch_bridge(5);')==2
exits = read(S/'pending/shared-exit-integration.json')
assert exits['unique_entries']==4 and exits['output_alias_order_preserved']
assert u.count('ra2_ground_prepare_written_return_bridge(')==1+exits['overlapping_copies']
assert read(S/'legal-overlap-sources.json')['passed']
assert u.count('ra2_ground_template_index_bridge();')==10
assert w.count('ra2_ground_object_branch_bridge(6);')==3
assert u.count('ra2_ground_prepare_service_return_bridge(')==27
assert u.count('ra2_ground_sample_anchor_bridge();')==12
assert w.count('ra2_ground_moving_tail_bridge();')==3
assert u.count('ra2_ground_advance_service_return_bridge(')==15
assert u.count('ra2_ground_template_destination_bridge(')==25
assert w.count('ra2_ground_allied_relation_bridge();')==3
assert u.count('ra2_ground_prepare_stop_return_bridge(')==1+sum(e['copies'] for e in read(S/'pending/prepare-stop-integration.json')['entries'])
args = read(S/'truck-actor-fixture-build-arguments.json')
objects = [Path(p) if Path(p).is_absolute() else R/'ra2/build-original-c'/p for p in args['link'] if p.endswith('.obj')]
assert len(objects)==171 and sum(p.name=='truck_actor_movement_fixture.obj' for p in objects)==1
(S/'truck-actor-fixture-receipt.json').write_text(json.dumps(dict(production_exe_sha256=receipt['executable_sha256'],
    fixture_exe_sha256=sha(S/'truck-actor-fixture-probe.exe'),fixture_source_sha256=sha(S/'truck_actor_movement_fixture.c'),
    changed_object='movement_fixture.c.obj',object_count=len(objects),objects=[dict(path=str(p),sha256=sha(p)) for p in objects]),indent=2)+'\n',encoding='utf-8')
value = dict(passed=True,production_c_sources=171,compile_inputs=292,template_table_entries=7,building_flags_entries=2,
             shared_exit_entries=4,shared_exit_copies=exits['overlapping_copies'],existing_tail_targets_preserved=True,
             state_trace_unchanged=True,comparators_unchanged=True,byte_styles_preserved=True,
             whole_object_passage_classifier_readable=False,full_original_equivalence_verified=False)
value.update(template_index_internal_entries=10,enemy_kind_internal_entries=3,service_exit_entries=3,service_exit_copies=26)
value.update(sample_anchor_internal_entries=12,moving_tail_internal_entries=3,advance_service_exit_entries=2,advance_service_exit_copies=14)
value.update(destination_internal_copies=24,allied_relation_internal_copies=3,prepare_stop_service_entries=2,prepare_stop_service_copies=sum(e['copies'] for e in read(S/'pending/prepare-stop-integration.json')['entries']))
value.update(remaining_destination_copies_connected=4,enemy_contact_internal_copies=3,following_service_entries=2,following_service_copies=sum(e['copies'] for e in read(S/'pending/following-service-integration.json')['entries']))
assert w.count('ra2_ground_object_branch_bridge(7);')==3
out = S/'refactor-structure.json'
assert not out.exists()
out.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(value))
