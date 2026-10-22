from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v25'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names=['advance-interpolation-probe','prepare-shared-probe','cell-services-probe']
results={n:json.loads((S/(n+'-verified-01.json')).read_text(encoding='utf-8-sig')) for n in names}
assert all(v['passed'] and v['original_stack_cleanup_verified'] for v in results.values())
sources=[S/'ground_services_probe.c',S/'native_probe_host.h']
for module in ['ground_interpolation','ground_prepare_shared','ground_cell_services','unit_movement']:
 sources.extend(R/'ra2/src/gameplay'/(module+ext) for ext in ['.c','.h'])
sources.extend(R/'ra2/src/compat'/('x87_arithmetic'+ext) for ext in ['.c','.h'])
assert all((S/'ground_services_probe.exe').stat().st_mtime>=p.stat().st_mtime for p in sources)
value=dict(passed=True,scope='native original fragments and readable C, separate from real simulation gates',
 original_sha256=sha(R/'ra2/game/game.exe'),probe_sha256=sha(S/'ground_services_probe.exe'),
 inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in sources],results=results,
 precision_modes=3,rounding_modes=4,total_cases=sum(v['cases'] for v in results.values()))
(S/'native-services-identity.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,cases=value['total_cases'])))
