"""Hash-checked cache/scratch cleanup after all native and scene work has completed."""
from run_batch_v62 import R,P,S,read,write,sha
from pathlib import Path
import subprocess
assert read(S/'final-scene-matrix.json')['passed'] and read(S/'native-gates.json')['passed'] and read(S/'effects.json')['passed']
tracked={n.decode('utf-8') for n in subprocess.check_output(['git','-c','core.fsmonitor=false','ls-files','-z'],cwd=P).split(b'\0') if n}
def ordinary(p):
 for q in [p,*p.parents]:
  if q==R.parent:break
  assert not (q.lstat().st_file_attributes&0x400),q
candidates={}
def add(p,kind):
 ordinary(p);assert p.resolve().is_relative_to(R.resolve()) and p.relative_to(P).as_posix() not in tracked
 candidates[str(p.resolve())]=dict(path=str(p.resolve()),bytes=p.stat().st_size,sha256=sha(p),kind=kind)
for root in (R/'evidence').iterdir():
 if root.is_dir() and root.name.startswith('movement-state-v'):
  ordinary(root)
  for p in root.glob('*.obj'):add(p,'reproducible-root-probe-object')
empty_dirs=[]
for root in [R/'__pycache__',R/'ra2/tools/__pycache__']:
 if root.exists():
  ordinary(root)
  for p in root.glob('*.pyc'):
   if (root.parent/(p.name.split('.cpython-')[0]+'.py')).exists():add(p,'python-bytecode-cache')
  if all(str(p.resolve()) in candidates for p in root.iterdir()):empty_dirs.append(str(root.resolve()))
for root in (R/'temp').glob('difftest-*'):
 if root.is_dir() and (root/'difftest.c').is_file() and (root/'difftest.exe').is_file():add(root/'difftest.exe','scratch-difftest-with-retained-source')
p=R/'temp/storage-probe-copy.sav'
if p.exists():
 assert p.stat().st_nlink==1 and sha(p)==sha(R/'ra2/game/SAVE0029.SAV');add(p,'redundant-private-copy-of-preserved-original-save')
assert candidates is not None
roots={str(Path(p).parent) for p in candidates};protected=[]
for name in sorted(roots):
 for p in sorted(Path(name).iterdir()):
  if p.is_file() and str(p.resolve()) not in candidates and p.name not in ['cleanup-plan.json','cleanup.json']:
   ordinary(p);protected.append(dict(path=str(p.resolve()),sha256=sha(p)))
write(S/'cleanup-plan.json',dict(passed=True,authorized_by_current_user=True,workspace=str(R.resolve()),roots=sorted(roots),candidates=list(candidates.values()),files=len(candidates),bytes=sum(x['bytes'] for x in candidates.values()),protected=protected,empty_cache_directories=empty_dirs,scope='Only ignored, inactive probe .obj, reproducible Python cache, scratch difftest EXE with retained C, and one hash-identical private save copy. No sources, accepted executable, original assets, traces, baseline or rollback deletion.'))
print(dict(passed=True,files=len(candidates),bytes=sum(x['bytes'] for x in candidates.values())))
