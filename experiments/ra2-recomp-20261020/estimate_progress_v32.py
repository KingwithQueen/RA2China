"""Explicit engineering estimates; never report instruction coverage as game completion."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v32';P=R.parent.parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert read(S/'native-gates.json')['passed'] and read(S/'bridge-infantry-real-scenes.json')['passed']
groups=[dict(scope='ground_movement_and_pathfinding',estimate_percent=70,range_percent=[60,75],
    denominator='Readable recovery and controlled conformance of the currently investigated ground movement/pathfinding subsystem; includes remaining internal copies, concrete objects, connections and legal-entry verification.',
    weighted_milestones=[dict(name='path_search_region_heap_cache_and_path_rewrite',weight=25,credit=.90),dict(name='advance_prepare_template_state_machines',weight=30,credit=.75),dict(name='object_passage_services_bridge_and_tube',weight=25,credit=.65),dict(name='rare_routes_natural_entries_and_integration_acceptance',weight=20,credit=.45)]),
    dict(scope='whole_readable_independent_C17_engine',estimate_percent=20,range_percent=[15,25],
    denominator='A readable, maintainable complete C17 game engine with broad original conformance, rather than the existing executable static translation.',
    weighted_milestones=[dict(name='repeatable_static_C_runtime_and_baseline_environment',weight=20,credit=.85),dict(name='readable_gameplay_AI_combat_economy_UI_render_audio_save_network_subsystems',weight=40,credit=.075),dict(name='controlled_campaign_skirmish_multiplayer_and_whole_world_acceptance',weight=25,credit=.04),dict(name='independent_layout_ABI_portability_and_performance_acceptance',weight=15,credit=0)])]
for g in groups:
    assert sum(x['weight'] for x in g['weighted_milestones'])==100
    g['weighted_evidence_credit_percent']=round(sum(x['weight']*x['credit'] for x in g['weighted_milestones']),2)
remaining=[
    'Complete Advance/Prepare internal template continuations and unify copies only after proving their frame and continuation contracts.',
    'Broaden concrete object, locomotor, allied/enemy, building/terrain, crush, bridge destruction and dynamic occupancy classifications.',
    'Recover remaining service-bearing exits with callback mutation, output aliases, recursion and original return order.',
    'Prove legal natural entry sources for nonprimary C copies; computed pointers and unrun scenes remain unresolved.',
    'Broaden moving infantry/vehicle and hostile traffic, especially a northbound meeting query during simultaneous motion rather than its initial scan, curved height plus occupied exit, alternate saved-segment pointer and other rare-route scenes.',
    'Classify the 37 unsupported-instruction guards and audit global termination/tail targets; recover other full-game subsystems and complete campaign/network/performance acceptance.'
]
unintercepted=[]
t=(R/'ra2/src/recomp/gen_game/recomp_0010.c').read_text(encoding='utf-8')
for body in re.split(r'(?=^void sub_)',t,flags=re.M):
    if 'L_004A24C6:' in body and 'L_004A2528:' not in body:
        m=re.search(r'void (\w+)\(void\)',body);unintercepted.append(m[1])
assert len(unintercepted)==4
v=dict(passed=True,kind='subjective_weighted_engineering_estimate',estimates=groups,remaining=remaining,
    excluded_destination_copies=unintercepted,source_of_uncertainty='Milestone weights and credits are engineering judgments, not measured behavioral coverage or remaining effort; estimates can move after discovering hidden branches.',
    not_completion_metrics=['generated_C_line_count','disassembly_interval_coverage','number_of_passed_probes','number_of_batches'],
    full_original_equivalence_verified=False,
    inputs=[dict(path=p.relative_to(R).as_posix() if p.is_relative_to(R) else str(p),sha256=sha(p)) for p in [Path(__file__),S/'native-gates.json',S/'bridge-infantry-real-scenes.json',R/'ra2/src/recomp/gen_game/recomp_0010.c',S/'baseline/project/交接文档-原版逆向与C重编译-20261020.txt']])
(S/'progress-estimate.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8');print([(g['scope'],g['estimate_percent'],g['range_percent']) for g in groups])
