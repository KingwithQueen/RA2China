"""Allowlist only ignored, reproducible root-level compiler objects after all builds."""
from run_batch_v39 import R,P,S,O,read,write,sha
import subprocess
roots=[O,S];candidates=[];protected=[]
def ordinary(p):
 for q in [p,*p.parents]:
  if q==R.parent:break
  assert not (q.lstat().st_file_attributes&0x400),q
for root in roots:
 ordinary(root)
 for p in sorted(root.iterdir()):
  if not p.is_file():continue
  ordinary(p)
  row=dict(path=str(p.resolve()),bytes=p.stat().st_size,sha256=sha(p))
  if p.suffix.lower()=='.obj':
   assert not subprocess.check_output(['git','-c','core.fsmonitor=false','ls-files','--',str(p.relative_to(P))],cwd=P)
   candidates.append(row)
  elif p.name not in ['cleanup-plan.json','cleanup.json']:protected.append(row)
assert candidates
write(S/'cleanup-plan.json',dict(passed=True,authorized_by_current_user=True,roots=[str(p.resolve()) for p in roots],candidates=candidates,protected=protected,files=len(candidates),bytes=sum(x['bytes'] for x in candidates),scope='Only untracked root .obj, all probes/builds already complete. No recursion or force, no game copies, traces, EXE, source, baseline, checkpoints or archive deletion.'))
print(dict(passed=True,files=len(candidates),bytes=sum(x['bytes'] for x in candidates)),flush=True)
