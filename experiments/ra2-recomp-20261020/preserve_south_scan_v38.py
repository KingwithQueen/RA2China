"""Keep the south initial-scan-only pair before replacing its ordinary lane recipe."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38';out=S/'investigations/south-initial-scan';assert not out.exists();out.mkdir(parents=True)
def move(src,dst):
    assert src.resolve().is_relative_to(S.resolve()) and dst.resolve().is_relative_to(S.resolve()) and src.exists() and not dst.exists();dst.parent.mkdir(parents=True,exist_ok=True);src.replace(dst)
for tag in ['op-south','oh-south']:
    assert json.loads((S/'runs'/tag/'comparison.json').read_text(encoding='utf-8'))['passed'];move(S/'runs'/tag,out/'runs'/tag);move(S/(tag+'.log'),out/(tag+'.log'))
move(S/'fixtures/bridge-occupied-south.MAP',out/'fixtures/bridge-occupied-south.MAP')
for n in ['bridge-occupied-fixtures.json','recipe-byte-audit.json']:move(S/n,out/n)
move(S/'investigations/recipe-replay-01',out/'recipe-replay-01')
for n in ['make_bridge_occupied_v38.py','audit_bridge_occupied_v38.py']:shutil.copy2(R/n,out/n)
paths=[p for p in out.rglob('*') if p.is_file() and (p.suffix in ['.json','.jsonl','.log','.py'] or p.name in ['SOV01T.MAP','RA2.INI','SAVE0029.SAV'])]
(out/'receipt.json').write_text(json.dumps(dict(passed=True,paired_frames=1802,formal_acceptance_frames=0,reason='South has actual exit wait but pair queries only in initial frame6. Keep separate until ordinary lane candidate passes full moving-query gate.',files=[dict(path=p.relative_to(out).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths]),indent=2)+'\n',encoding='utf-8')
