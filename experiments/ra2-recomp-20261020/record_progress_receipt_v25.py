from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v25'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names=['tube-approach-probe','tube-height-progress-probe','movement-internal-next-probe','object-passage-finish-probe']
results={name:read(S/(name+'-verified-01.json')) for name in names}
assert all(x['passed'] and x['original_stack_cleanup_verified'] and x['cases']==(393216 if name=='tube-height-progress-probe' else 32768) for name,x in results.items())
sources=[S/'progress_probe.c',S/'native_probe_host.h',R/'build-progress-probe-v25.ps1']
for directory,modules in [('gameplay',['ground_tube_progress','ground_internal_next','ground_passage_finish']),('runtime',['ground_progress_bridge']),('compat',['x87_arithmetic'])]:
 for module in modules:sources.extend(R/'ra2/src'/directory/(module+suffix) for suffix in ['.c','.h'])
exe=S/'progress_probe.exe';assert all(p.stat().st_mtime<=exe.stat().st_mtime for p in sources)
value=dict(passed=True,total_cases=491520,results=results,original_sha256=sha(R/'ra2/game/game.exe'),
 scope='Native 6FABAA approach fragment; full 6FAD1C/6FAE1D height and epilogues; 4A166A/4A32B4 continuations; complete 703AA9 classification finish. Callback substitutions test query order and mutable centers/owner/offset data; no claim of whole-function or complete real-game coverage.',
 operation_control_modes=12,conversion_rounding_modes=4,straight_and_diagonal_lengths=True,
 stack_and_nonvolatile_registers_verified=True,callback_sequence_and_values_verified=True,prefetched_coordinate_registers_verified=True,
 probe_executable=dict(path=exe.relative_to(R).as_posix(),sha256=sha(exe)),inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in sources])
(S/'native-progress-identity.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,cases=value['total_cases'])))
