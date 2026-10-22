"""Reproduce category-entry cases and deliberately changing category callbacks."""
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v28'
p=S/'objects_probe.c';t=p.read_text(encoding='utf-8')
for old,new in [
    ('0x70397C,0x70394F};','0x70397C,0x70394F,0x7034BF};'),
    ('if(phase>3)','if(phase>4)'),
    ('static unsigned outcomes[7];','static unsigned outcomes[7],kind_reads;'),
    ('return kinds[(fixture>>5)&3];','return kinds[((fixture>>5)+(phase==4 ? kind_reads++ : 0))&3];'),
    ('count=weapon_reads=native_resume=0;','count=weapon_reads=native_resume=kind_reads=0;')]:
    assert t.count(old)==1,old
    t=t.replace(old,new)
p.write_text(t,encoding='utf-8',newline='\n')
p=R/'run_lifecycle_part_v28.py';t=p.read_text(encoding='utf-8')
old="'object-chain-probe-verified-01.json'"
assert t.count(old)==1
p.write_text(t.replace(old,old+",'object-kind-probe-verified-01.json'"),encoding='utf-8',newline='\n')
print('Added independent category-only native boundary and mutable callbacks')
