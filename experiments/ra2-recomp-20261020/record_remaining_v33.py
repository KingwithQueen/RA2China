"""Record completed scopes and remaining work without inventing a new percentage."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v33';read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
assert read(S/'destination-copy-contract.json')['parent_copies']==4 and read(S/'north-query-real-scenes.json')['north_meeting_dynamic_relation_query_verified']
v=dict(passed=True,reestimated_this_round=False,historical_only=True,previous_estimate=str(R/'evidence/movement-state-v32/progress-estimate.json'),
    remaining_destination_copies_from_generation31=0,north_moving_meeting_relationship_query_completed=True,
    remaining=['Other template/Advance/Prepare continuations and service exits; callback and recursive side effects.',
    'More concrete object/locomotor/building/terrain/crush/bridge-destruction and traffic combinations.',
    'Legal natural entry sources for 28 nonprimary C aliases; computed pointers and unrun routes remain unresolved.',
    'Alternate saved-segment pointer and broader curved height/occupied exit scenarios.',
    'Whole-game readable recovery, unsupported guard classification, campaigns, network synchronization and performance acceptance.'],
    inputs=[dict(path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),S/'destination-copy-contract.json',S/'north-query-real-scenes.json']])
(S/'progress-estimate.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
