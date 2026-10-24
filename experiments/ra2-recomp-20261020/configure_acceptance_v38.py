"""Adapt this batch's gates and scene recipes before any final identities are sealed."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38'
def edit(name,pairs):
 p=R/name;t=p.read_text(encoding='utf-8')
 for a,b in pairs:
  assert a in t,(name,a);t=t.replace(a,b)
 compile(t,str(p),'exec');p.write_text(t,encoding='utf-8',newline='\n')
for name in ['audit_inherited_fixtures_v38.py','record_remaining_v38.py']:
 edit(name,[('movement-state-v36','movement-state-v37')])
edit('run_native_gates_v38.py',[('len(receipts) == 123','len(receipts) == 126')])
edit('audit_movement_v38.py',[('len(probes)==123','len(probes)==126')])
edit('record_remaining_v38.py',[("['groups']==123","['groups']==126")])
edit('run_native_gates_v38.py',[("'record_round37_receipt']","'record_round37_receipt','record_round38_receipt']"),('groups=123','groups=126')])
t=(R/'record_round37_receipt_v38.py').read_text(encoding='utf-8').replace("19,'loaded-destination'","21,'late-layer'").replace("11,'loaded-warhead'","12,'loaded-weapon'").replace("20,'mark-enter'","22,'leave-place-mark'").replace('if phase==11:','if phase==12:').replace('native-round37-identity','native-round38-identity').replace('destination_height_written_before_service=True,loaded_warhead_zero_service_calls=True,mark_enter_callback_saved_slots=True','late_layer_repeated_reads_and_alias_writes=True,loaded_weapon_zero_service_calls=True,leave_place_mark_callback_saved_slots=True')
(R/'record_round38_receipt_v38.py').write_text(t,encoding='utf-8',newline='\n')
edit('audit_internal_alias_sources_v38.py',[("'004A25E8'","'004A25E8','004A25A0','004A2586'"),("'00703A53'","'00703A53','00703A45'")])
for name in ['preflight_movement_v38.py','audit_fragment_contract_v38.py']:
 p=R/name;t=p.read_text(encoding='utf-8');marker="out = S/'refactor-structure.json'" if name.startswith('preflight') else "(S/'new-fragment-contract.json').write_text"
 i=t.index(marker);var='value' if name.startswith('preflight') else 'v'
 t=t[:i]+"assert u.count('ra2_ground_late_layer_bridge();')==13 and w.count('ra2_ground_object_branch_bridge(12);')==3 and u.count('ra2_ground_advance_leave_place_return_bridge();')==13\n"+var+".update(late_layer_internal_copies=13,loaded_weapon_internal_copies=3,leave_place_mark_service_copies=13)\n"+t[i:];p.write_text(t,encoding='utf-8',newline='\n')
# New ordinary-order combination: neighbor leaves early, main lane stays occupied longer.
t=(R/'make_bridge_lane_release_v38.py').read_text(encoding='utf-8').replace('bridge-lane-release','bridge-neighbor-release').replace('(210,300) if','(210,420) if').replace('(226,316)','(226,436)').replace("old['blocker_ids'][1]):first,str(old['blocker_ids'][0]):second","old['blocker_ids'][0]):first,str(old['blocker_ids'][1]):second")
(R/'make_bridge_neighbor_release_v38.py').write_text(t,encoding='utf-8',newline='\n')
t=(R/'run_bridge_lane_release_v38.py').read_text(encoding='utf-8').replace('bridge-lane-release','bridge-neighbor-release').replace("'lh-'","'nh-'").replace("'lp-'","'nr-'")
(R/'run_bridge_neighbor_release_v38.py').write_text(t,encoding='utf-8',newline='\n')
t=(R/'audit_bridge_lane_release_v38.py').read_text(encoding='utf-8').replace('bridge-lane-release','bridge-neighbor-release').replace('make_bridge_lane_release','make_bridge_neighbor_release').replace('run_bridge_lane_release','run_bridge_neighbor_release').replace("'lh-'","'nh-'").replace("'lp-'","'nr-'").replace('ordinary main-lane departure while the adjacent blocker remains held','ordinary adjacent-lane departure while the main-lane blocker remains held')
(R/'audit_bridge_neighbor_release_v38.py').write_text(t,encoding='utf-8',newline='\n')
t=(R/'audit_bridge_release_motion_v38.py').read_text(encoding='utf-8').replace('bridge-lane-release','bridge-neighbor-release').replace("'lp-'","'nr-'").replace("assert all(e['held_through_vehicle_crossing'] for e in rows) and rows[0]['first_actual_motion_frame']>cross","assert not rows[0]['held_through_vehicle_crossing'] and rows[0]['first_actual_motion_frame']<cross\n  assert rows[1]['held_through_vehicle_crossing'] and rows[1]['first_actual_motion_frame']>cross").replace('In this pair the main car crosses while both blockers still retain their wait positions; the earlier release request does not immediately clear the lane.','In this pair the main car crosses after the neighboring blocker starts moving and before the main-lane blocker leaves. The two lane-release orders and actual movement times are measured separately.')
(R/'audit_bridge_neighbor_motion_v38.py').write_text(t,encoding='utf-8',newline='\n')
edit('audit_recipe_replay_v38.py',[("make_bridge_lane_release","make_bridge_neighbor_release"),('bridge-lane-release-','bridge-neighbor-release-'),('production_sources_changed=6','production_sources_changed=4')])
edit('prepare_final_v38.py',[("for n in ['audit_legal_sources'","run([sys.executable,'-X','utf8','-B',str(R/'make_bridge_neighbor_release_v38.py')],'make-new-bridge-final.log')\nfor n in ['audit_legal_sources'")])
edit('run_final_scenes_v38.py',[("jobs=[['run_bridge_lane_release_v38.py'","jobs=[['run_bridge_neighbor_release_v38.py','production'],['run_bridge_neighbor_release_v38.py','observer'],['audit_bridge_neighbor_release_v38.py'],['audit_bridge_neighbor_motion_v38.py'],['run_bridge_lane_release_v38.py'")])
edit('audit_scene_totals_v38.py',[("('main_lane_release','bridge-lane-release-fixtures.json','lp-')","('main_lane_release','bridge-lane-release-fixtures.json','lp-'),('neighbor_lane_release','bridge-neighbor-release-fixtures.json','nr-')"),('==69','==71'),('==47439','==49241')])
edit('run_occupied_alias_scenes_v38.py',[('bridge-lane-release-fixtures','bridge-neighbor-release-fixtures'),('main-lane-release','neighbor-lane-release')])
edit('audit_occupied_alias_v38.py',[("base='lh-'","base='nh-'"),('main-lane-release','neighbor-lane-release')])
edit('record_remaining_v38.py',[("'production_scenes']==69","'production_scenes']==71"),("['004A24F0','00703A53','004A25E8']","['004A25A0','00703A45','004A2586']"),('沿用第三十五批的历史工程估算','沿用此前批次的历史工程估算'),('本轮已整理4A24F0、703A53、4A25E8','本轮已整理4A25A0、703A45、4A2586'),('及桥层写回','及其他桥层接续')])
# Two game lanes only, with late work moved after the core lane has actually finished.
(S/'observer-lane-assignment.json').write_text(json.dumps(dict(delegated_jobs=['combined-scenes'],free_bridge_jobs=False,free_core_jobs=['combined-scenes'],required_before=['core-scenes-complete.json','alias-occupied-natural-scenes.json'],max_scene_lanes=2,max_game_processes=4),indent=2)+'\n',encoding='utf-8')
print('Final native and scene recipes configured')
