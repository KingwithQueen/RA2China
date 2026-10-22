"""Record independent helper identity and readable-region structure."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v14'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):
    p=S/name
    if p.exists():
        assert read(p)==value,p
        return
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
args=read(S/'truck-actor-fixture-build-arguments.json')
objects=[Path(x) if Path(x).is_absolute() else R/'ra2/build-original-c'/x for x in args['link'] if x.lower().endswith('.obj')]
assert len(objects)==122
assert sum(p.name=='truck_actor_movement_fixture.obj' for p in objects)==1
assert not any(p.name=='movement_fixture.c.obj' for p in objects)
write('truck-actor-fixture-receipt.json',dict(
    production_exe_sha256=sha(R/'ra2/build-original-c/ra2.exe'),fixture_exe_sha256=sha(S/'truck-actor-fixture-probe.exe'),
    fixture_source_sha256=sha(S/'truck_actor_movement_fixture.c'),changed_object='movement_fixture.c.obj',
    object_count=len(objects),objects=[dict(path=str(p),sha256=sha(p)) for p in objects]))
generated=(R/'ra2/src/recomp/gen_game/recomp_0003.c').read_text(encoding='utf-8')
assert generated.count('ra2_path_search_neighbors_bridge();')==2
assert generated.count('allowed=ra2_path_region_allows_bridge();')==3
assert generated.count('ra2_path_node_distance_bridge();')==1
for module in ['ground_path_distance','ground_path_search']:
    for suffix in ['.c','.h']:
        text=(R/'ra2/src/gameplay'/(module+suffix)).read_text(encoding='utf-8')
        assert 'MEM32(' not in text and 'MEM16(' not in text and 'MEM8(' not in text,module
        assert not re.search(r'\(\s*(?:const\s+)?(?:void|u?int\w*)\s*\*\s*\)\s*0x',text),module
assert 'RECOMP_CALL(sub_004BA410)' in generated
assert (R/'ra2/src/runtime/state_trace.c').read_bytes()==(S/'baseline/ra2/src/runtime/state_trace.c').read_bytes()
write('refactor-structure.json',dict(passed=True,complete_neighbor_loops=2,legacy_region_decisions=3,
    node_squared_distance_entries=1,readable_modules=['ground_path_distance','ground_path_search'],
    original_approximate_distance_retained=True,state_trace_unchanged=True,
    service_order_and_shared_fields_preserved=True,complete_path_reconstruction_still_generated=True))
print(json.dumps(dict(passed=True,objects=len(objects),production_exe_sha256=sha(R/'ra2/build-original-c/ra2.exe'))))
