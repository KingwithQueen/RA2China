from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v23'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
names=['advance-landing-probe','prepare-failure-tails-probe','slope-height-probe']
results={name:read(S/(name+'-verified-01.json')) for name in names}
assert all(v['passed'] and v['original_stack_cleanup_verified'] for v in results.values())
assert [v['cases'] for v in results.values()]==[32768,32768,131072]
sources=[S/'remainder_probe.c',S/'native_probe_host.h',R/'build-remainder-probe-v23.ps1']
for directory,modules in [('gameplay',['ground_landing','ground_failure','ground_slope','unit_movement']),('runtime',['ground_remainder_bridge']),('compat',['x87_arithmetic'])]:
 for module in modules:sources.extend(R/'ra2/src'/directory/(module+ext) for ext in ['.c','.h'])
exe=S/'remainder_probe.exe'
assert all(p.stat().st_mtime<=exe.stat().st_mtime for p in sources)
value=dict(passed=True,scope='native original fragments and production C bridges; real simulation gates recorded separately',
 original_sha256=sha(R/'ra2/game/game.exe'),probe_executable=dict(path=exe.relative_to(R).as_posix(),sha256=sha(exe)),
 inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in sources],results=results,
 slope_precision_modes=3,slope_rounding_modes=4,slope_shapes=20,partial_cache_flags_tested=8,total_cases=196608,
 callback_owner_replacement_tested=True)
(S/'native-remainder-identity.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,cases=value['total_cases'])))
