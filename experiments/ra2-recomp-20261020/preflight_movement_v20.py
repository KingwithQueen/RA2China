from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v20'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):
 p=S/name;assert not p.exists(),p;p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
args=read(S/'truck-actor-fixture-build-arguments.json')
objects=[Path(x) if Path(x).is_absolute() else R/'ra2/build-original-c'/x for x in args['link'] if x.lower().endswith('.obj')]
assert len(objects)==143 and sum(p.name=='truck_actor_movement_fixture.obj' for p in objects)==1
assert not any(p.name=='movement_fixture.c.obj' for p in objects)
write('truck-actor-fixture-receipt.json',dict(production_exe_sha256=sha(R/'ra2/build-original-c/ra2.exe'),
 fixture_exe_sha256=sha(S/'truck-actor-fixture-probe.exe'),fixture_source_sha256=sha(S/'truck_actor_movement_fixture.c'),
 changed_object='movement_fixture.c.obj',object_count=143,objects=[dict(path=str(p),sha256=sha(p)) for p in objects]))
t=(R/'ra2/src/recomp/gen_game/recomp_0003.c').read_text(encoding='utf-8')
for call,count in [('ra2_path_prepare_bridge',1),('ra2_region_route_publish_bridge',4),('ra2_path_rebuild_bridge',1),
 ('ra2_path_search_neighbors_bridge',2),('ra2_region_search_bridge',1),('ra2_path_smooth_bridge',1),('ra2_path_postprocess_bridge',1),
 ('ra2_path_turn_rewrite_bridge',1),('ra2_path_anchor_bridge',1),('ra2_path_segment_rewrite_bridge',1)]:
 assert t.count(call+'();')==count,(call,t.count(call+'();'))
assert read(S/'arrival-integration.json')['all_existing_labels_retained']
for mode in [0,2,3]:assert t.count(f'ra2_path_completion_bridge({mode});')==16
for module in ['ground_sampling','ground_prepare_exit','ground_object_services','ground_completion','ground_passage']:
 for suffix in ['.c','.h']:
  text=(R/'ra2/src/gameplay'/(module+suffix)).read_text(encoding='utf-8')
  assert not any(s in text for s in ['MEM32(','MEM16(','MEM8(']),module
  assert not re.search(r'\(\s*(?:const\s+)?(?:void|u?int\w*)\s*\*\s*\)\s*0x',text),module
assert (R/'ra2/src/runtime/state_trace.c').read_bytes()==(S/'baseline/ra2/src/runtime/state_trace.c').read_bytes()
for rel in ['run_fixture_comparison.py','run_state_comparison.py']:
 assert (R/rel).read_bytes()==(S/'baseline'/rel).read_bytes()
u=(R/'ra2/src/recomp/gen_game/recomp_0010.c').read_text(encoding='utf-8')
assert u.count('ra2_ground_interpolation_bridge();')==10
assert u.count('ra2_ground_prepare_shared_bridge(1);')==2
assert u.count('ra2_ground_prepare_shared_bridge(0);')==2
w=(R/'ra2/src/recomp/gen_game/recomp_0022.c').read_text(encoding='utf-8')
for i in range(4):assert w.count(f'ra2_cell_service_bridge({i});')==1
for i,count in [(0,3),(1,9),(2,10)]:assert u.count(f'ra2_ground_sampling_bridge({i});')==count
for i,count in [(0,10),(1,6),(2,8),(3,4)]:assert u.count(f'ra2_ground_prepare_exit_bridge({i});')==count
for filename,entries in [('recomp_0007.c',range(4)),('recomp_0029.c',range(4,6))]:
 text=(R/'ra2/src/recomp/gen_game'/filename).read_text(encoding='utf-8')
 for i in entries:assert text.count(f'ra2_ground_object_service_bridge({i});')==1

for name in ['arrival','cleanup','passage']:assert read(S/(name+'-integration.json'))['all_existing_labels_retained']
assert u.count('ra2_ground_arrival_complete_bridge();')==6
for i,count in [(0,2),(1,10),(2,7),(3,9),(4,14),(5,7),(6,8),(7,2)]:
 assert u.count(f'ra2_ground_prepare_finish_bridge({i});')==count,(i,count)
for filename,entries in [('recomp_0012.c',[0,1]),('recomp_0023.c',[2])]:
 text=(R/'ra2/src/recomp/gen_game'/filename).read_text(encoding='utf-8')
 for i in entries:assert text.count(f'ra2_ground_passage_bridge({i});')==1

write('refactor-structure.json',dict(passed=True,two_run_local_rewrite=1,reverse_anchor_search=1,
 collision_segment_rewrite=1,search_completion_tails=16,early_return_tails=16,empty_root_cleanup_tails=16,internal_tail_labels_preserved=True,
 state_trace_unchanged=True,comparators_unchanged=True,primary_427370_flow_readable=True,
 advance_interpolation_entries=10,prepare_shared_success_entries=2,cell_lookup_services=3,threat_read_service=1,whole_owner_passage_classifier_readable=False,base_passage_functions=2,ground_height_entry_readable=True,slope_height_core_readable=False,arrival_complete_entries=6,prepare_finish_entries=59,advance_sampling_entries=[3,9,10],prepare_exit_entries=[10,6,8,4],object_and_height_services=6,whole_search_readable=False))
print(json.dumps(dict(passed=True,objects=143,exe_sha256=sha(R/'ra2/build-original-c/ra2.exe'))))
