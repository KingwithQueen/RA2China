"""Keep native labels, instruction annotations, tails and guarded entries unchanged."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v36';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();files=[]
for n in ['recomp_0010.c','recomp_0046.c']:
    p=R/'ra2/src/recomp/gen_game'/n;old=S/'baseline/ra2/src/recomp/gen_game'/n;a=old.read_text(encoding='utf-8');b=p.read_text(encoding='utf-8')
    for pattern in [r'^L_[0-9A-F]+:',r'/\* 0x[0-9A-F]+: [^\n]*?\*/',r'case (0x[0-9A-Fa-f]+u): goto',r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)']:
        assert re.findall(pattern,a,re.M)==re.findall(pattern,b,re.M),(n,pattern)
    files.extend([p,old])
u=files[0].read_text(encoding='utf-8');w=files[2].read_text(encoding='utf-8')
assert u.count('ra2_ground_internal_handoff_bridge(3);')==8 and w.count('ra2_ground_object_branch_bridge(8);')==3 and u.count('ra2_ground_prepare_owner_stop_return_bridge();')==7
assert u.count('destination_resume_v33:')==4 and u.count('ra2_ground_template_destination_bridge(')==37
assert u.count('ra2_ground_internal_handoff_bridge(4);')==8 and w.count('ra2_ground_object_branch_bridge(9);')==3 and u.count('ra2_ground_prepare_invalidate_return_bridge();')==11
assert u.count('ra2_ground_template_destination_bridge(2);')==12 and w.count('ra2_ground_object_branch_bridge(10);')==3 and u.count('ra2_ground_advance_place_return_bridge();')==13
v=dict(passed=True,register_destination_copies=12,confirmed_building_copies=3,placement_restore_service_copies=13,loaded_sample_copies=8,terrain_weapon_copies=3,invalidate_service_copies=11,register_sample_copies=8,enemy_weapon_copies=3,owner_stop_copies=7,new_native_entries=0,prior_four_destination_copies_preserved=True,old_labels_instructions_tails_guards_preserved=True,natural_nonprimary_entry_proved=False,inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [Path(__file__)]+files])
(S/'new-fragment-contract.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8');print({k:v for k,v in v.items() if k!='inputs'})
