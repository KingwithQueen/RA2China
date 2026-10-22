"""Check the concrete final production and diagnostic build, before acceptance."""
from pathlib import Path
import hashlib, json, re
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v27'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
receipt = read(R / 'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count'] == 171 and len(receipt['inputs']) == 285
assert receipt['refreshed_count'] == 0
assert receipt['executable_sha256'] == sha(R / 'ra2/build-original-c/ra2.exe')
for path, digest in receipt['inputs'].items():
    assert sha(Path(path)) == digest, path
for name in ['template', 'passage', 'returns']:
    assert read(S / (name + '-integration.json'))['existing_tail_targets_preserved']
for rel in ['run_fixture_comparison.py', 'run_state_comparison.py', 'ra2/src/runtime/state_trace.c']:
    assert (R / rel).read_bytes() == (S / 'baseline' / rel).read_bytes(), rel
for name in ['ground_template_transition', 'ground_object_chain']:
    for ext in ['c', 'h']:
        text = (R / f'ra2/src/gameplay/{name}.{ext}').read_text(encoding='utf-8')
        assert not any(token in text for token in ['MEM8(', 'MEM16(', 'MEM32('])
        assert not re.search(r'\(\s*(?:const\s+)?(?:void|u?int\w*)\s*\*\s*\)\s*0x', text)
u = (R / 'ra2/src/recomp/gen_game/recomp_0010.c').read_text(encoding='utf-8')
w = (R / 'ra2/src/recomp/gen_game/recomp_0046.c').read_text(encoding='utf-8')
assert u.count('ra2_ground_template_transition_bridge(0);') == 6
assert u.count('ra2_ground_template_transition_bridge(1);') == 2
assert w.count('ra2_ground_object_chain_bridge(0);') == 1
assert w.count('ra2_ground_object_chain_bridge(1);') == 4
counts = [w.count(f'ra2_ground_passage_return_bridge({i});') for i in range(5)]
assert all(counts)
assert 'ra2_ground_template_cells(' in (R / 'ra2/src/gameplay/ground_advance.c').read_text(encoding='utf-8')
assert 'ra2_ground_return_frame(c.frame, RA2_FRAME_PASSAGE, result);' in (R / 'ra2/src/runtime/ground_progress_bridge.c').read_text(encoding='utf-8')
args = read(S / 'truck-actor-fixture-build-arguments.json')
objects = [Path(p) if Path(p).is_absolute() else R / 'ra2/build-original-c' / p for p in args['link'] if p.endswith('.obj')]
assert len(objects) == 171 and sum(p.name == 'truck_actor_movement_fixture.obj' for p in objects) == 1
(S / 'truck-actor-fixture-receipt.json').write_text(json.dumps(dict(
    production_exe_sha256=sha(R / 'ra2/build-original-c/ra2.exe'), fixture_exe_sha256=sha(S / 'truck-actor-fixture-probe.exe'),
    fixture_source_sha256=sha(S / 'truck_actor_movement_fixture.c'), changed_object='movement_fixture.c.obj',
    object_count=len(objects), objects=[dict(path=str(p), sha256=sha(p)) for p in objects]), indent=2) + '\n', encoding='utf-8')
value = dict(passed=True, production_c_sources=171, compile_inputs=285, template_entries=[6, 2],
             object_chain_entries=[1, 4], passage_return_entries=counts,
             advance_primary_uses_same_cell_helper=True, passage_finish_uses_same_return_helper=True,
             state_trace_unchanged=True, comparators_unchanged=True, existing_tail_targets_preserved=True,
             whole_object_passage_classifier_readable=False, full_original_equivalence_verified=False)
(S / 'refactor-structure.json').write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
print(json.dumps(value))
