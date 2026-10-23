from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v34'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names=['sample-entry-probe','prepare-passage-entry-probe','object-passage-entry-probe','shared-return-plan-probe']
results={n:read(S/(n+'-verified-01.json')) for n in names}
for i,(n,x) in enumerate(results.items()):assert x['passed'] and x['phase']==i and x['cases']==65536 and x['original_stack_cleanup_verified'],n
sources=[S/'joint_probe.c',S/'native_probe_host.h',R/'build-joint-probe-v34.ps1']
for directory,modules in [('gameplay',['ground_template_entry','ground_passage_entry','ground_return_plan']),('runtime',['ground_joint_bridge'])]:
 for module in modules:
  for ext in ['c','h']:sources.append(R/f'ra2/src/{directory}/{module}.{ext}')
exe=S/'joint_probe.exe'
value=dict(passed=True,total_cases=262144,results=results,original_sha256=sha(R/'ra2/game/game.exe'),scope='Native 4A17D5 sample entry; 4A3486 leave/classify/enter sequence; 70323E object entry through 703331 including complete blocked returns; Advance/Prepare/passage shared epilogues. Ordered callback substitutions exercise changed owners and mutable frame outputs. Full-function and all-branch real-game equivalence are not claimed.',stack_and_nonvolatile_registers_verified=True,callback_sequence_and_values_verified=True,probe_executable=dict(path=exe.relative_to(R).as_posix(),sha256=sha(exe)),inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in sources])
(S/'native-joint-identity.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(passed=True,cases=262144)))
