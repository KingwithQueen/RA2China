"""Stage only this batch's allowlisted files, preserving the accepted source bytes."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v37'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=read(S/'validation.json');assert v['passed'] and v['formal_baseline_generation']==36 and v['verification_round']==37
assert read(P/'reports/latest-recovery.json')['validation']==str(S/'validation.json')
assert sha(R/'ra2/build-original-c/ra2.exe')==v['exe_sha256']
for e in read(S/'source-manifest.json'):assert sha(R/e['path'])==e['sha256'],e['path']
root_files={'README.md','reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json',
            '交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt',
            '交接文档-单位移动第三十六批正式验收-20261024.txt','docs/单位移动第三十六批-4A24F0与弹头门槛及桥上主车道先放行组合-20261024.txt'}
sources={'ra2/src/gameplay/'+name for name in ['ground_sampling_shared.c','ground_sampling_shared.h','ground_enemy_kind.h','ground_template.c','ground_template_table.h','ground_objects.c','ground_building_flags.h','ground_allied.c','ground_moving_tail.h','ground_allied_relation.h','ground_enemy_contact.h','ground_enemy_kind.h','阅读说明-单位移动.txt']}
sources|={'ra2/src/runtime/'+name for name in ['ground_objects_bridge.c','ground_overlap_bridge.c','ground_joint_bridge.c','ground_allied_bridge.c','ground_tube_state_bridge.c']}
sources|={'ra2/src/recomp/gen_game/'+name for name in ['recomp_0010.c','recomp_0046.c']}
prefix=R.relative_to(P).as_posix()+'/'
raw=subprocess.check_output(['git','-c','core.fsmonitor=false','status','--porcelain','-z','--untracked-files=all'],cwd=P)
names=[]
for row in raw.split(b'\0'):
    if not row:continue
    status=row[:2].decode('ascii');name=row[3:].decode('utf-8')
    assert not any(c in status for c in 'RCDU'),(status,name)
    allowed=name in root_files
    if name.startswith(prefix):
        rel=name[len(prefix):];p=Path(rel)
        allowed |= rel in sources
        allowed |= '/' not in rel and 'v37' in p.name and p.suffix in ['.py','.ps1']
        if rel.startswith('evidence/movement-state-v37/'):
            tail=Path(rel).parts[2:]
            allowed |= len(tail)==1 and p.suffix in ['.json','.c','.h','.asm']
            allowed |= len(tail)==2 and tail[0]=='fixtures' and p.suffix.lower() in ['.map','.ini']
    assert allowed,('Outside batch staging scope',name)
    assert (P/name).resolve().is_relative_to(P.resolve()) and (P/name).is_file(),name
    names.append(name)
for start in range(0,len(names),40):
    subprocess.run(['git','-c','core.fsmonitor=false','-c','core.autocrlf=false','add','--',*names[start:start+40]],cwd=P,check=True)
out=S/'git-staging-scope.json'
out.write_text(json.dumps(dict(passed=True,allowlist_verified=True,selected_files=len(names),source_bytes_prechecked=True,
    baselines_parts_runs_resources_excluded=True,remote_actions=False),indent=2)+'\n',encoding='utf-8')
subprocess.run(['git','-c','core.fsmonitor=false','-c','core.autocrlf=false','add','--',out.relative_to(P).as_posix()],cwd=P,check=True)
print(json.dumps(dict(passed=True,selected_files=len(names),scope_verified=True)))
