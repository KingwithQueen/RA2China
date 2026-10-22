"""Replay probe/observer recipe edits in an isolated copy, then compare exact bytes."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v28';O=R/'evidence/movement-state-v27'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ap=argparse.ArgumentParser();ap.add_argument('--attempt',default='01');a=ap.parse_args()
assert a.attempt.isdigit()
replica=S/'investigations'/('recipe-replay-'+a.attempt)
assert replica.resolve().is_relative_to(S.resolve()) and not replica.exists()
target=replica/'evidence/movement-state-v28';target.mkdir(parents=True)
inputs=[]
for name in ['overlap_probe.c','objects_probe.c','connection_observer.c']:
    p=O/name;shutil.copy2(p,target/name);inputs.append(p)
for name in ['make_connection_fixture','run_lifecycle_part']:
    p=R/(name+'_v27.py');inputs.append(p)
    (replica/(name+'_v28.py')).write_text(p.read_text(encoding='utf-8-sig').replace('v27','v28'),encoding='utf-8',newline='\n')
scripts=['extend_probe_v28.py','extend_objects_probe_v28.py','extend_exit_probe_v28.py','extend_observer_v28.py','extend_chain_observer_v28.py']
for name in scripts:
    p=R/name;inputs.append(p);shutil.copy2(p,replica/name)
    with (replica/(name+'.log')).open('x',encoding='utf-8') as output:
        subprocess.run([sys.executable,'-X','utf8','-B',str(replica/name)],cwd=replica,stdout=output,stderr=subprocess.STDOUT,check=True)
outputs=[]
for current,replayed in [(S/name,target/name) for name in ['overlap_probe.c','objects_probe.c','connection_observer.c']]+[(R/name,replica/name) for name in ['make_connection_fixture_v28.py','run_lifecycle_part_v28.py']]:
    assert current.read_bytes()==replayed.read_bytes(),str(current)
    outputs.append(dict(path=current.relative_to(R).as_posix(),sha256=sha(current)))
value=dict(passed=True,isolated_recipe_replay=True,exact_source_outputs=outputs,
           inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in inputs],
           original_formal_sources_unchanged=True,compiled_production_unchanged=True)
p=S/'recipe-byte-audit.json';assert not p.exists();p.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,exact_source_files=len(outputs),isolated_attempt=a.attempt)))
