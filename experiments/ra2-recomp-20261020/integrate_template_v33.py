"""Connect the four raw copies using a local continuation at the existing instruction."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v33'
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');assert b'\r\n' not in p.read_bytes()
parts=re.split(r'(?=^void sub_)',t,flags=re.M);records=[]
for i,b in enumerate(parts):
    if 'L_004A24C6:' not in b or 'L_004A2528:' in b:continue
    name=re.search(r'void (\w+)\(void\)',b)[1]
    assert name in ['sub_004A1F8D','sub_004A1FA1','sub_004A230E','sub_004A2311']
    assert 'destination_resume_v33:' not in b
    start=b.index('L_004A24C6:');end=b.index('    eax = MEM32(ecx + 0x88); /* 0x004A2528:')
    before=b[start:end]
    # Every original instruction remains in place. The new label is local C flow.
    b=b[:end]+'destination_resume_v33:\n'+b[end:]
    for n,a in enumerate(['004A24C6','004A24DC']):
        m='L_'+a+':\n';assert b.count(m)==1
        b=b.replace(m,m+f'''    /* 复用已验证的目标坐标服务，接回本副本原有的2528指令。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_template_destination_bridge({n});
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto destination_resume_v33;
''')
    parts[i]=b;records.append(dict(function=name,entries=['004A24C6','004A24DC'],continuation='004A2528',
        original_fragment_sha256=hashlib.sha256(before.encode()).hexdigest(),new_native_dispatch_entries=0))
assert len(records)==4
p.write_bytes(''.join(parts).encode('utf-8'))
(S/'pending/destination-copy-integration.json').write_text(json.dumps(dict(passed=True,parent_copies=4,entry_copies=8,local_labels=4,old_labels_preserved=True,new_native_dispatch_entries=0,copies=records),indent=2)+'\n',encoding='utf-8')
print('Integrated remaining four destination copies')
