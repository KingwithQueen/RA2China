"""Bind reused scenario bytes to generation31's protected accepted archive."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v37'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base=S/'baseline/evidence/movement-state-v36/fixtures';records=[]
for p in sorted(base.iterdir()):
    if not p.is_file():continue
    live=S/'fixtures'/p.name;assert sha(live)==sha(p),p.name
    records.append(dict(path=live.relative_to(R).as_posix(),baseline_path=p.relative_to(R).as_posix(),sha256=sha(live)))
for e in read(S/'bridge-fixtures.json')['inputs']:assert sha(R/e['path'])==e['sha256'],e['path']
v=dict(passed=True,reused_fixture_files=len(records),fixtures=records,scenario_bytes_preserved=True,
    producer_recipe_policy='Old accepted maps are reused byte-for-byte. Original producer identities in bridge-fixtures.json remain prior accepted verification recipes, and are verified rather than renamed.',
    inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [Path(__file__),S/'bridge-fixtures.json',S/'bridge-mixed-fixtures.json',S/'bridge-hostile-fixtures.json']])
(S/'inherited-fixtures.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8');print(dict(passed=True,reused_fixture_files=len(records)))
