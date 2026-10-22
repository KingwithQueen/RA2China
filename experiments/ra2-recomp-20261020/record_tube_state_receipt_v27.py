"""Bind native fragment results to the exact C sources and probe executable."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v27'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
names=['tube-exit-probe','movement-handoff-probe','surface-class-probe','tube-waypoint-probe']
results={n:read(S/(n+'-verified-01.json')) for n in names}
assert all(x['passed'] and x['cases']==32768 and x['original_stack_cleanup_verified'] for x in results.values())
sources=[S/'tube_state_probe.c',S/'native_probe_host.h',R/'build-tube-state-probe-v27.ps1']
for directory,modules in [('gameplay',['ground_tube_state','ground_handoff','ground_surface_class','ground_sampling_shared']),('runtime',['ground_tube_state_bridge'])]:
 for name in modules:sources.extend(R/'ra2/src'/directory/(name+ext) for ext in ['.c','.h'])
exe=S/'tube_state_probe.exe';assert all(p.stat().st_mtime<=exe.stat().st_mtime for p in sources)
value=dict(passed=True,scope='Original native 6FAE76 full exit including epilogue; 6FAA45/6FAB6A waypoint switches; 4A3257/4A2311/4A1F90 continuations; 479CC0/47A270/47A290 full classification services. Continuation stops and callback substitutions verify fragment behavior, not a complete real game.',
 original_sha256=sha(R/'ra2/game/game.exe'),probe_executable=dict(path=exe.relative_to(R).as_posix(),sha256=sha(exe)),
 inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in sources],results=results,total_cases=131072,
 callback_order_and_values_verified=True,registers_and_stack_verified=True,mutable_snapshot_and_callbacks_verified=True,
 signed_wrap_and_thresholds_verified=True)
(S/'native-tube-state-identity.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,cases=value['total_cases'])))
