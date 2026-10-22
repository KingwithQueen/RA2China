"""Save an immutable checkpoint only after its named strict scene and probe gates pass."""
from pathlib import Path
import argparse,hashlib,json,shutil
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v27'
ap=argparse.ArgumentParser();ap.add_argument('--name',required=True);ap.add_argument('--scene',action='append',required=True);ap.add_argument('--probe',action='append',required=True);a=ap.parse_args()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
digest=sha(R/'ra2/build-original-c/ra2.exe');cases=[]
for tag in a.scene:
    x=read(S/'runs'/tag/'comparison.json');c=x['comparison'];assert x['passed'] and c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
    assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']
    assert x['exe_sha256']==(sha(S/'truck-actor-fixture-probe.exe') if 'budget' in tag else digest)
    if 'budget' in tag:
        for mode in ['original','generated-c']:
            rs=[json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
            assert [r['value'] for r in rs if r.get('kind')=='movement-audit' and r.get('stage')==3]==list(range(10,-1,-1))
    cases.append(dict(tag=tag,frames=c['frames_compared'],exe_sha256=x['exe_sha256']))
for name in a.probe:assert read(S/name)['passed'],name
paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(Path(name).relative_to(R).as_posix() for name in read(R/'ra2/build-original-c/source-content-receipt.json')['inputs'])
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ('.c','.h','.txt'))
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v27*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and (p.suffix in ('.c','.h') or p.name in ('truck-actor-fixture-probe.exe','truck-actor-fixture-build-arguments.json')))
paths.update(p.relative_to(R).as_posix() for p in (S/'pending').glob('*') if p.is_file())
out=S/'parts'/a.name;assert not out.exists();manifest=[]
for rel in sorted(paths):
    dest=out/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,dest);manifest.append(dict(path=rel,sha256=sha(dest)))
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'validation.json').write_text(json.dumps(dict(passed=True,exe_sha256=digest,scenes=cases,probes=a.probe,files=len(manifest)),indent=2),encoding='utf-8')
print('Saved',a.name,len(manifest),'files')
