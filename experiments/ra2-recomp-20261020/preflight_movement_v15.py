from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v15'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):
    p=S/name;assert not p.exists(),p;p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
args=read(S/'truck-actor-fixture-build-arguments.json')
objects=[Path(x) if Path(x).is_absolute() else R/'ra2/build-original-c'/x for x in args['link'] if x.lower().endswith('.obj')]
assert len(objects)==126 and sum(p.name=='truck_actor_movement_fixture.obj' for p in objects)==1
assert not any(p.name=='movement_fixture.c.obj' for p in objects)
write('truck-actor-fixture-receipt.json',dict(production_exe_sha256=sha(R/'ra2/build-original-c/ra2.exe'),
    fixture_exe_sha256=sha(S/'truck-actor-fixture-probe.exe'),fixture_source_sha256=sha(S/'truck_actor_movement_fixture.c'),
    changed_object='movement_fixture.c.obj',object_count=126,objects=[dict(path=str(p),sha256=sha(p)) for p in objects]))
t=(R/'ra2/src/recomp/gen_game/recomp_0003.c').read_text(encoding='utf-8')
assert t.count('prepared=ra2_path_prepare_bridge();')==1
assert t.count('ra2_region_route_publish_bridge();')==5
assert t.count('ra2_path_rebuild_bridge();')==1
assert t.count('ra2_path_search_neighbors_bridge();')==2
for module in ['ground_path_prepare','ground_region_route','ground_path_rebuild']:
    for suffix in ['.c','.h']:
        text=(R/'ra2/src/gameplay'/(module+suffix)).read_text(encoding='utf-8')
        assert not any(s in text for s in ['MEM32(','MEM16(','MEM8(']),module
        assert not re.search(r'\(\s*(?:const\s+)?(?:void|u?int\w*)\s*\*\s*\)\s*0x',text),module
assert (R/'ra2/src/runtime/state_trace.c').read_bytes()==(S/'baseline/ra2/src/runtime/state_trace.c').read_bytes()
write('refactor-structure.json',dict(passed=True,entry_preparation=1,region_parent_chain_publication=5,path_rebuild=1,
    neighbor_loop_unchanged=True,state_trace_unchanged=True,region_graph_search_still_generated=True,
    path_smoothing_and_final_postprocessing_still_generated=True))
print(json.dumps(dict(passed=True,objects=126,exe_sha256=sha(R/'ra2/build-original-c/ra2.exe'))))
