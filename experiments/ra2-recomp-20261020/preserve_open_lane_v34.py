"""Keep matching but nonqualifying trials separate from formal coverage."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v34';out=S/'investigations/occupied-open-lane';assert not out.exists();out.mkdir(parents=True)
def move(src,dst):
    assert src.resolve().is_relative_to(S.resolve()) and dst.resolve().is_relative_to(S.resolve()) and src.exists() and not dst.exists()
    dst.parent.mkdir(parents=True,exist_ok=True);src.replace(dst)
for tag in ['op-north','op-south','oh-north','oh-south']:
    assert json.loads((S/'runs'/tag/'comparison.json').read_text(encoding='utf-8'))['passed']
    move(S/'runs'/tag,out/'runs'/tag);move(S/(tag+'.log'),out/(tag+'.log'))
for n in ['bridge-occupied-north.MAP','bridge-occupied-south.MAP']:move(S/'fixtures'/n,out/'fixtures'/n)
for n in ['bridge-occupied-fixtures.json','recipe-byte-audit.json']:move(S/n,out/n)
move(S/'investigations/recipe-replay-01',out/'recipe-replay-01')
for n in ['make_bridge_occupied_v34.py','audit_bridge_occupied_v34.py']:shutil.copy2(R/n,out/n)
files=[p for p in out.rglob('*') if p.is_file() and (p.suffix in ['.json','.jsonl','.log','.py'] or p.name in ['SOV01T.MAP','RA2.INI','SAVE0029.SAV'] or p.parent.name=='fixtures')]
v=dict(passed=True,paired_runs=4,paired_frames=3604,formal_acceptance_frames=0,reason='All four comparisons match. North primary vehicle arrived before release; only initial blocker queries and no opposite-motion pair queries. Near-goal rest was not an occupied-exit wait.',files=[dict(path=p.relative_to(out).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files])
(out/'receipt.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8');print(dict(preserved=True,paired_frames=3604,formal_acceptance_frames=0))
