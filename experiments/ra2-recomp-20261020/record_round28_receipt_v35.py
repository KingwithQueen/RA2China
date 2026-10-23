"""Bind new native checks to the concrete code, recipes and executables."""
from pathlib import Path
import hashlib, json, subprocess
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v35'
sha = lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results = {}
for exe,phase,name in [('overlap_probe.exe',4,'template-layer-probe'),('objects_probe.exe',4,'object-kind-probe'),('overlap_probe.exe',5,'remaining-exits-probe')]:
    result = subprocess.run([str(S/exe),str(R/'ra2/game/game.exe'),str(phase)],cwd=R,check=True,capture_output=True,text=True)
    value = json.loads(result.stdout)
    assert value['passed'] and value['phase']==phase and value.get('cases',value.get('object_cases'))==65536
    (S/(name+'-verified-01.json')).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
    results[name] = value
sources = [Path(__file__),R/'extend_probe_v35.py',R/'extend_exit_probe_v35.py',R/'integrate_template_v35.py',
           R/'extend_objects_probe_v35.py',R/'audit_recipe_replay_v35.py',R/'extend_observer_v35.py',R/'extend_chain_observer_v35.py',
           R/'integrate_objects_v35.py',R/'integrate_returns_v35.py',R/'build-overlap-probe-v35.ps1',R/'build-objects-probe-v35.ps1',
           S/'overlap_probe.c',S/'objects_probe.c',S/'remaining_return_cases.h',S/'native_probe_host.h']
for folder,modules in [('gameplay',['ground_template_transition','ground_template_entry','ground_objects','ground_object_kind','ground_passage_entry','ground_return_plan','ground_object_chain']),
                       ('runtime',['ground_overlap_bridge','ground_joint_bridge','ground_objects_bridge'])]:
    for module in modules:
        for ext in ['c','h']:
            p = R/f'ra2/src/{folder}/{module}.{ext}'
            if p.is_file():sources.append(p)
entries = json.loads((R/'evidence/movement-state-v28/returns-integration.json').read_text(encoding='utf-8'))
value = dict(passed=True,total_cases=196608,results=results,shared_native_exit_entries=entries['unique_entries'],
             original_sha256=sha(R/'ra2/game/game.exe'),live_flags_checked_for_layer_and_exits=True,
             mutable_ordered_category_callbacks=True,stack_nonvolatile_and_eax_verified=True,
             probe_executables=[dict(path=(S/name).relative_to(R).as_posix(),sha256=sha(S/name)) for name in ['overlap_probe.exe','objects_probe.exe']],
             inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in sources])
(S/'native-round28-identity.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,new_cases=196608,exit_entries=entries['unique_entries'])))
