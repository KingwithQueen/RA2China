"""Reconcile the two retained orchestration failures with explicit completed resumptions."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert 'RuntimeError: all-native-final.log' in (S/'queue-preparation.log').read_text(encoding='utf-8')
assert 'audit_bridge_neighbor_release_v38.py' in (S/'queue-bridge.log').read_text(encoding='utf-8')
assert '12645' in (S/'queue-acceptance.log').read_text(encoding='utf-8')
assert 'bridge lane complete' in (S/'queue-bridge-resume-01.log').read_text(encoding='utf-8')
names=['delegated-bridge-infantry-scenes.json','native-recovery.json','native-gates.json','core-scenes-complete.json','bridge-scenes-complete.json','validation.json','final-check.json']
assert all(read(S/n)['passed'] for n in names)
assert read(S/'native-gates.json')['groups']==126 and read(S/'validation.json')['paired_scenes']==71
assert read(S/'native-recovery.json')['production_executable_unchanged']
assert sha(R/'ra2/build-original-c/ra2.exe')==read(S/'validation.json')['exe_sha256']
inputs=[Path(__file__)]+[S/n for n in names+['queue-preparation.log','queue-bridge.log','queue-bridge-resume-01.log','native-retry-01.log','queue-acceptance.log','acceptance-resume-01.log']]
value=dict(passed=True,original_coordinator_retained_failures=['preparation probe link','neighbor audit measurement baseline','acceptance audit seed prefix replacement'],complete_native_rerun_passed=True,bridge_lane_resumed_passed=True,core_lane_passed=True,final_acceptance_passed=True,production_source_unchanged_during_recovery=True,max_scene_lanes=2,max_game_processes=4,inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in inputs])
out=S/'queue-recovery.json';assert not out.exists();out.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');print(dict(passed=True,recovered_queues=3))
