"""Retain scoped completion and unresolved work without a new percentage estimate."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v35'
paths=[S/'new-fragment-contract.json',S/'bridge-occupied-real-scenes.json',S/'alias-natural-scenes.json',S/'bridge-detour-real-scenes.json']
assert all(json.loads(p.read_text(encoding='utf-8'))['passed'] for p in paths)
v=dict(passed=True,cleanup_completed=True,cleanup_deleted_files=2428,historical_only=True,reestimated_this_round=False,previous_estimate=str(R/'evidence/movement-state-v34/progress-estimate.json'),remaining_destination_copies_from_generation31=0,loaded_sample_copies_connected=8,terrain_weapon_copies_connected=3,invalidate_service_copies_connected=11,bridge_meeting_occupied_scenes=2,nonprimary_natural_entry_proved=False,remaining=['Other internal template and register-sourced continuations.','More object, building, terrain, locomotor, crushing and bridge destruction combinations.','Other service, recursive and callback-writeback exits.','Legal natural sources for 28 nonprimary C aliases, including arbitrary computed targets and unrun routes.','Alternate saved-segment pointer; wider height, occupancy and traffic combinations.','Whole-game readable recovery, guards, campaigns, synchronization and performance.'],inputs=[dict(path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__)]+paths])
(S/'progress-estimate.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
