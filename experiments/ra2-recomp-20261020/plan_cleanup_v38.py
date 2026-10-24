"""Plan removal of inactive, untracked, reproducible native-probe objects only."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v38'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
tracked={x.decode('utf-8') for x in subprocess.check_output(['git','-c','core.fsmonitor=false','ls-files','-z'],cwd=P).split(b'\0') if x}
stems={p.stem for p in (R/'ra2/src').rglob('*.c')};files=[];protected=[]
for number in [36,37]:
 base=R/f'evidence/movement-state-v{number}';stems.update(p.stem for p in base.glob('*.c'))
 for p in sorted(base.iterdir()):
  assert not p.is_symlink()
  if not p.is_file():continue
  candidate=p.suffix=='.obj' and p.stem in stems and 'fixture' not in p.stem
  record=dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p))
  if candidate:
   assert p.relative_to(P).as_posix() not in tracked and p.resolve().parent==base.resolve()
   assert not (p.stat().st_file_attributes&0x400)
   files.append(record)
  else:protected.append(record)
assert files and all('/baseline/' not in e['path'] and '/runs/' not in e['path'] for e in files)
value=dict(passed=True,scope='Only root native-probe .obj in inactive v36/v37; excludes fixture link objects, source, executable, logs, traces, baselines and archives',files=files,protected_files=protected,total_files=len(files),total_bytes=sum(e['bytes'] for e in files),authorized_by_current_user_cleanup_request=True)
out=S/'cleanup-plan.json';assert not out.exists();out.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');print(dict(files=len(files),bytes=value['total_bytes']))
