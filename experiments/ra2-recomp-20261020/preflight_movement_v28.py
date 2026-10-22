"""Concrete production identity, labels, byte styles and independent helper origins."""
from pathlib import Path
import hashlib, json, re
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v28'
read = lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt = read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count']==171 and len(receipt['inputs'])==286 and receipt['refreshed_count']==0
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
for name in ['ground_template_transition.c','ground_object_kind.h','ground_objects.c']:
    text = (R/'ra2/src/gameplay'/name).read_text(encoding='utf-8')
    assert not any(s in text for s in ['MEM8(','MEM16(','MEM32('])
    assert not re.search(r'0x00[47][0-9A-Fa-f]{5}',text)
u = (R/'ra2/src/recomp/gen_game/recomp_0010.c').read_text(encoding='utf-8')
w = (R/'ra2/src/recomp/gen_game/recomp_0046.c').read_text(encoding='utf-8')
assert u.count('ra2_ground_template_layer_bridge();')==6
assert w.count('ra2_ground_object_branch_bridge(4);')==2
exits = read(S/'pending/shared-exit-integration.json')
assert exits['unique_entries']==27 and exits['original_labels_retained']
assert u.count('ra2_ground_return_frame(g_esp, RA2_FRAME_PREPARE,')==sum(e['copies'] for e in exits['entries'] if e['kind']=='RA2_FRAME_PREPARE')
assert read(S/'legal-overlap-sources.json')['passed']
args = read(S/'truck-actor-fixture-build-arguments.json')
objects = [Path(p) if Path(p).is_absolute() else R/'ra2/build-original-c'/p for p in args['link'] if p.endswith('.obj')]
assert len(objects)==171 and sum(p.name=='truck_actor_movement_fixture.obj' for p in objects)==1
(S/'truck-actor-fixture-receipt.json').write_text(json.dumps(dict(production_exe_sha256=receipt['executable_sha256'],
    fixture_exe_sha256=sha(S/'truck-actor-fixture-probe.exe'),fixture_source_sha256=sha(S/'truck_actor_movement_fixture.c'),
    changed_object='movement_fixture.c.obj',object_count=len(objects),objects=[dict(path=str(p),sha256=sha(p)) for p in objects]),indent=2)+'\n',encoding='utf-8')
value = dict(passed=True,production_c_sources=171,compile_inputs=286,template_layer_entries=6,object_kind_entries=2,
             shared_exit_entries=27,shared_exit_copies=exits['overlapping_copies'],existing_tail_targets_preserved=True,
             state_trace_unchanged=True,comparators_unchanged=True,byte_styles_preserved=True,
             whole_object_passage_classifier_readable=False,full_original_equivalence_verified=False)
out = S/'refactor-structure.json'
assert not out.exists()
out.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(value))
