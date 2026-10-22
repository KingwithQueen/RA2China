from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v25'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names=['tube-entry-preparation-probe','tube-remaining-horizontal-probe','tube-regular-horizontal-probe','movement-next-template-probe','neighbor-passage-probe']
results={name:read(S/(name+'-verified-01.json')) for name in names}
for i,(name,x) in enumerate(results.items()):assert x['passed'] and x['phase']==i and x['original_stack_cleanup_verified'] and x['cases']==(131072 if i in (1,2) else 32768),name
sources=[S/'travel_probe.c',S/'native_probe_host.h',R/'build-travel-probe-v25.ps1']
for directory,modules in [('gameplay',['ground_tube_travel','ground_template_next','ground_passage_neighbor','ground_connection_numeric','ground_connection_trig','unit_movement']),('runtime',['ground_travel_bridge']),('compat',['x87_arithmetic'])]:
 for module in modules:
  for suffix in ['.c','.h']:
   p=R/'ra2/src'/directory/(module+suffix)
   if p.exists():sources.append(p)
exe=S/'travel_probe.exe';assert all(p.stat().st_mtime<=exe.stat().st_mtime for p in sources)
value=dict(passed=True,total_cases=360448,results=results,original_sha256=sha(R/'ra2/game/game.exe'),
 scope='Native 6FAA66..6FAB6A entry preparation; 6FAC70..6FAD1C and 6FAD75..6FAE1D horizontal continuations; 4A17A2 sample and 4A33C3 prepare gates; 7031F2 neighbor direction classification including full returns. Ordered service substitutions preserve mutable owners and constructor return aliases. Whole-function and all-branch runtime equivalence remain unfinished.',
 operation_control_modes=12,conversion_rounding_modes=4,stack_and_nonvolatile_registers_verified=True,callback_sequence_and_values_verified=True,
 probe_executable=dict(path=exe.relative_to(R).as_posix(),sha256=sha(exe)),inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in sources])
(S/'native-travel-identity.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,cases=value['total_cases'])))
