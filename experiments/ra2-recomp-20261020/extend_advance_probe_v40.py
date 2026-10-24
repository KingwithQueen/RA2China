"""Record useful native-oracle coverage for chain removal and entering suppression."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v40/advance_probe.c';t=p.read_text(encoding='utf-8')
t=t.replace('damage_cases,same_cell_cases;','damage_cases,same_cell_cases,multi_damage_cases,removed_before_enter_cases;')
marker='        ++counts[resume==boundaries[1]];';assert t.count(marker)==1
t=t.replace(marker,marker+'''
        unsigned damage_in_case=0,entered=0;
        for(unsigned i=0;i<count;++i) {
            if(records[i][0]==DAMAGE) ++damage_in_case;
            if(records[i][0]==OCCUPATION&&records[i][2]) entered=1;
        }
        if(damage_in_case>=4) ++multi_damage_cases;
        if(damage_in_case&&!entered&&(fixture&(1u<<24))) ++removed_before_enter_cases;
''')
t=t.replace('if(!counts[0]||!counts[1]||!damage_cases||!same_cell_cases)', 'if(!counts[0]||!counts[1]||!damage_cases||!same_cell_cases||!multi_damage_cases||!removed_before_enter_cases)')
marker='    printf("{\\"passed\\":true,\\"advance_cases';a=t.index(marker);b=t.index('\n    return 0;',a)
t=t[:a]+'''    printf("{\\"passed\\":true,\\"advance_cases\\":65536,\\"continue_cases\\":%u,\\"removed_cases\\":%u,\\"damage_calls\\":%u,\\"same_cell_calls\\":%u,\\"multiple_chain_target_cases\\":%u,\\"removed_before_enter_cases\\":%u,\\"state_calls_live_locals_verified\\":true}\\n",counts[0],counts[1],damage_cases,same_cell_cases,multi_damage_cases,removed_before_enter_cases);'''+t[b:]
p.write_text(t,encoding='utf-8',newline='\n')
print('Added native effect coverage counters')
