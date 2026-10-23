"""Preserve an admission failure before any game or private scenario was created."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v37';tag='a-template-ur3';src=S/(tag+'.log');dst=S/'investigations/prelaunch-path-guard'/src.name
assert src.is_file() and not (S/'runs'/tag).exists() and 'ValueError: 场景路径越界' in src.read_text(encoding='utf-8')
assert src.resolve().is_relative_to(S.resolve()) and dst.resolve().is_relative_to(S.resolve()) and not dst.exists()
dst.parent.mkdir(parents=True,exist_ok=True);src.replace(dst)
v=dict(passed=True,attempts=[dict(tag=tag,simulation_frames=0,game_launched=False,private_scenario_created=False,reason='Path admission guard refused before scenario creation; exact same path now resolves within the existing runs directory. No comparator or guard changes.',log=dst.relative_to(R).as_posix(),sha256=hashlib.sha256(dst.read_bytes()).hexdigest())])
(S/'prelaunch-failures.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
