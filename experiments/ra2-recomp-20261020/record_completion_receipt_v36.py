from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v36'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
names=['advance-arrival-completion-probe','prepare-target-cleanup-probe','base-passage-probe','ground-height-entry-probe']
results={name:read(S/(name+'-verified-01.json')) for name in names}
assert all(v['passed'] and v['original_stack_cleanup_verified'] for v in results.values())
assert [v['cases'] for v in results.values()]==[65536,32768,32768,32768]
sources=[S/'arrival_complete_probe.c',S/'completion_services_probe.c',S/'native_probe_host.h']
for directory,modules in [('gameplay',['ground_completion','ground_passage','ground_cell_services','ground_arrival','unit_movement']),
 ('runtime',['ground_completion_bridge','ground_arrival_bridge']),('compat',['x87_arithmetic'])]:
 for module in modules:sources.extend(R/'ra2/src'/directory/(module+ext) for ext in ['.c','.h'])
exes=[S/'arrival_complete_probe.exe',S/'completion_services_probe.exe']
assert all(p.stat().st_mtime<=min(e.stat().st_mtime for e in exes) for p in sources)
value=dict(passed=True,scope='native original fragments and production C bridges; real simulation gates recorded separately',
 original_sha256=sha(R/'ra2/game/game.exe'),probe_executables=[dict(path=e.relative_to(R).as_posix(),sha256=sha(e)) for e in exes],
 inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in sources],results=results,
 arrival_precision_modes=3,arrival_rounding_modes=4,callback_owner_replacement_tested=True,total_cases=163840,
 retained_height_core='4706C0 slope plane initialization and arithmetic retained; 55A280 world lookup and delegation replaced')
(S/'native-completion-identity.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,cases=value['total_cases'])))
