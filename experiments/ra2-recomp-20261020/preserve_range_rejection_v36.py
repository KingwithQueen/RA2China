"""Keep the invalid short-trial configuration and its zero-frame rejection."""
from pathlib import Path
import argparse,hashlib,json
ap=argparse.ArgumentParser();ap.add_argument('--tag',default='trial-os4');ap.add_argument('--directory',default='range-rejection');a=ap.parse_args()
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v36';root=S/'investigations/south-subcells';out=root/a.directory;assert out.resolve().is_relative_to(root.resolve()) and not out.exists();out.mkdir()
src=S/'runs'/a.tag;dst=out/'run';v=json.loads((src/'comparison.json').read_text(encoding='utf-8'));assert not v['passed'] and all(x['exit_code']==7 and x['state_sha256'] is None and x['failures']==['[state-error] order outside trace range'] for x in v['runs'])
assert src.resolve().is_relative_to(S.resolve()) and dst.resolve().is_relative_to(S.resolve());src.replace(dst)
(root/(a.tag+'.log')).replace(out/(a.tag+'.log'))
paths=[p for p in out.rglob('*') if p.is_file() and p.suffix in ['.json','.log']]
(out/'receipt.json').write_text(json.dumps(dict(passed=True,simulation_frames=0,reason='Short trial0:300 included an order at or beyond its final boundary. Both hosts refused before simulation. Short trial retains only orders strictly before300; formal0:900 orders unchanged.',files=[dict(path=p.relative_to(out).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths]),indent=2)+'\n',encoding='utf-8')
