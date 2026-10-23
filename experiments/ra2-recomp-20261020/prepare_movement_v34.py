"""Protect generation32 before creating any new source or evidence."""
from pathlib import Path
import hashlib,json,shutil,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;O=R/'evidence/movement-state-v33';S=R/'evidence/movement-state-v34'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not S.exists()
assert subprocess.check_output(['git','-c','core.fsmonitor=false','status','--porcelain'],cwd=P)==b'?? experiments/ra2-recomp-20261020/prepare_movement_v34.py\n'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip()=='30b30d2dd6ab088c78697fb904fc4ce3fdf74ce0'
manifest=json.loads((O/'source-manifest.json').read_text(encoding='utf-8'));assert len(manifest)==4684
assert sha(R/'ra2/build-original-c/ra2.exe')=='19bb89a2f7a69534848b40bdd474c0a44f5788a8b3bb536d8a8650285e8a2104'
for e in manifest:assert sha(R/e['path'])==sha(O/'final-source'/e['path'])==e['sha256'],e['path']
for e in manifest:
    d=S/'baseline'/e['path'];d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/e['path'],d)
shutil.copy2(O/'source-manifest.json',S/'baseline/source-manifest.json')
for rel in ['README.md','reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json','交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt','交接文档-单位移动第三十二批正式验收-20261023.txt','docs/单位移动第三十二批-四副本接续与北向移动交会及对象服务出口-20261023.txt']:
    d=S/'baseline/project'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/rel,d)
exclude=('prepare_','finalize_','integrate_','preflight_','normalize_','preserve-','polish_','verify_final_','audit_git_','resume_','audit_interruption_','preserve_startup_','run_final_audits_','audit_recipe_','finish_acceptance_','continue_','estimate_progress_','trial_','extend_','record_remaining_','record_round33_','audit_destination_')
for p in R.glob('*v33*'):
    if p.is_file() and p.suffix in ['.py','.ps1'] and not p.name.startswith(exclude):
        d=R/p.name.replace('v33','v34');assert not d.exists();d.write_text(p.read_text(encoding='utf-8-sig').replace('v33','v34'),encoding='utf-8',newline='\n')
for p in O.iterdir():
    if p.is_file() and p.suffix in ['.c','.h','.asm']:shutil.copy2(p,S/p.name)
shutil.copytree(O/'fixtures',S/'fixtures');shutil.copytree(O/'pending',S/'pending')
for e in manifest:assert sha(S/'baseline'/e['path'])==e['sha256']
(S/'baseline/receipt.json').write_text(json.dumps(dict(passed=True,files=len(manifest),code_commit='30b30d2dd6ab088c78697fb904fc4ce3fdf74ce0',formal_exe_sha256=sha(R/'ra2/build-original-c/ra2.exe')),indent=2)+'\n',encoding='utf-8')
extra=S/'baseline/extra';extra.mkdir();shutil.copy2(O/'internal-alias-sources.json',extra/'internal-alias-sources.json')
(extra/'receipt.json').write_text(json.dumps(dict(path='evidence/movement-state-v33/internal-alias-sources.json',sha256=sha(O/'internal-alias-sources.json')),indent=2)+'\n',encoding='utf-8')
(S/'vcs-context.json').write_text(json.dumps(dict(parent_commit='30b30d2dd6ab088c78697fb904fc4ce3fdf74ce0',config_sha256=sha(P/'.git/config'),remote_refs_sha256=hashlib.sha256(subprocess.check_output(['git','-c','core.fsmonitor=false','for-each-ref','--format=%(refname) %(objectname)','refs/remotes/'],cwd=P)).hexdigest()),indent=2)+'\n',encoding='utf-8')
(S/'startup-failures.json').write_text(json.dumps(dict(passed=True,attempts=[]),indent=2)+'\n',encoding='utf-8')
print('Protected',len(manifest),'files',flush=True)
