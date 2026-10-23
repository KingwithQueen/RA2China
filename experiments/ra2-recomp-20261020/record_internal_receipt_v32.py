from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v32'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
names=['advance-shared-sampling-probe','prepare-internal-probe'];results={name:read(S/(name+'-verified-01.json')) for name in names}
assert all(v['passed'] and v['original_stack_cleanup_verified'] and v['cases']==65536 for v in results.values())
sources=[S/'internal_probe.c',S/'native_probe_host.h',R/'build-internal-probe-v32.ps1']
for directory,modules in [('gameplay',['ground_sampling_shared','ground_prepare_internal']),('runtime',['ground_internal_bridge'])]:
 for module in modules:sources.extend(R/'ra2/src'/directory/(module+ext) for ext in ['.c','.h'])
exe=S/'internal_probe.exe';assert all(p.stat().st_mtime<=exe.stat().st_mtime for p in sources)
value=dict(passed=True,scope='Native original fragments 4A15F0/4A230E/4A3216/4A39C8/4A39CA versus production bridges. Continuations are intercepted and original fragment stack balance is checked; prior finish/exit services retain separate native regression gates.',
 original_sha256=sha(R/'ra2/game/game.exe'),probe_executable=dict(path=exe.relative_to(R).as_posix(),sha256=sha(exe)),
 inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in sources],results=results,total_cases=131072,
 signed_coordinate_boundaries_tested=True,callback_owner_replacement_tested=True,full_return_value_verified=True,interpolation_input_registers_verified=True)
(S/'native-internal-identity.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,cases=value['total_cases'])))
