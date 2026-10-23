"""Prepare current-round orchestration and keep prior-round producers intact."""
from pathlib import Path
R=Path(__file__).resolve().parent
def edit(name,pairs):
    p=R/name;t=p.read_text(encoding='utf-8')
    for old,new in pairs:assert old in t,(name,old);t=t.replace(old,new)
    p.write_text(t,encoding='utf-8',newline='\n')
edit('extend_observer_v34.py',[('movement-state-v32','movement-state-v33')])
edit('run_native_gates_v34.py',[("'record_round33_receipt']","'record_round33_receipt','record_round34_receipt']"),('== 111','== 114'),('groups=111','groups=114')])
edit('audit_movement_v34.py',[('==111','==114')])
edit('audit_internal_alias_sources_v34.py',[("'004A46BD'}","'004A46BD','004A2314','004A449B'}"),("{'0070399A'}","{'0070399A','007039EC'}")])
edit('audit_inherited_fixtures_v34.py',[('movement-state-v32','movement-state-v33')])
edit('audit_scene_totals_v34.py',[("('north_query','north-query-fixtures.json','np-')","('north_query','north-query-fixtures.json','np-'),('occupied_bridge','bridge-occupied-fixtures.json','op-')"),('==61','==63'),('==40231','==42033')])
edit('preflight_movement_v34.py',[("out = S/'refactor-structure.json'","assert u.count('ra2_ground_internal_handoff_bridge(3);')==8\nassert w.count('ra2_ground_object_branch_bridge(8);')==3\nassert u.count('ra2_ground_prepare_owner_stop_return_bridge();')==8\nvalue.update(register_sample_internal_copies=8,enemy_weapon_internal_copies=3,owner_stop_service_copies=7)\nout = S/'refactor-structure.json'")])
print('Configured round34')
