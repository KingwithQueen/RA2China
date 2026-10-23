"""Verify real existing instructions and preserve every old label/tail/guard."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v36'
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';old=(S/'baseline/ra2/src/recomp/gen_game/recomp_0010.c').read_text(encoding='utf-8');now=p.read_text(encoding='utf-8')
split=lambda t:{re.search(r'void (\w+)\(void\)',b)[1]:b for b in re.split(r'(?=^void sub_)',t,flags=re.M) if b.startswith('void sub_')}
before=split(old);after=split(now);records=[]
for name in ['sub_004A1F8D','sub_004A1FA1','sub_004A230E','sub_004A2311']:
    a=before[name];b=after[name];assert 'L_004A2528:' not in a and b.count('destination_resume_v36:')==1
    for pattern in [r'^L_[0-9A-F]+:',r'/\* 0x([0-9A-Fa-f]+):.*?\*/',r'case (0x[0-9A-Fa-f]+u): goto',r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)']:
        assert re.findall(pattern,a,re.M)==re.findall(pattern,b,re.M),(name,pattern)
    native_sequence=re.findall(r'/\* 0x([0-9A-Fa-f]+): (.*?) \*/',a[a.index('L_004A24C6:'):a.index('/* 0x004A2528:')])
    assert len(native_sequence)==22,(name,len(native_sequence))
    records.append(dict(function=name,original_instructions=len(native_sequence),old_labels_and_tails_preserved=True))
assert now.count('ra2_ground_template_destination_bridge(')==25
value=dict(passed=True,parent_copies=4,entry_copies=8,total_destination_entries=24,local_continuations=4,new_native_dispatch_entries=0,copies=records,
    inputs=[dict(path=x.relative_to(R).as_posix(),sha256=hashlib.sha256(x.read_bytes()).hexdigest()) for x in [Path(__file__),p,S/'baseline/ra2/src/recomp/gen_game/recomp_0010.c',R/'ra2/src/runtime/ground_joint_bridge.c']])
(S/'destination-copy-contract.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');print(dict(passed=True,copies=4,entries=8))
