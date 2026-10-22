from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v26'
O=R/'evidence/movement-state-v22'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
failures=[]
for tag,frame in [('k-tube-production-west',42),('p-tube-hook-west',59),('s-tube-production-west',59)]:
 p=O/'runs'/tag/'comparison.json';x=read(p);difference=x['comparison']['first_difference']
 assert not x['passed'] and difference['frame']==frame and difference['path']=='state.objects[id=1022581].position[1]'
 failures.append(dict(tag=tag,exe_sha256=x['exe_sha256'],first_difference=difference,comparison_sha256=sha(p)))
x=read(S/'runs/c-final-tube-west/comparison.json');assert x['passed']
write=dict(passed=True,original_failures_retained=failures,accepted_scene='c-final-tube-west',accepted_sha256=x['exe_sha256'],
 final_frames=x['comparison']['frames_compared'],first_difference=x['comparison']['first_difference'],
 reproduction='Legal tube-west.MAP, seed 12345, ordinary move order 5:1022581:2:66:114; no raw movement-state injection.',
 fixes=['Apply original x87 precision and rounding to each coordinate multiply/add/subtract.',
 'Preserve angle conversion and table-index arithmetic locally.',
 'Apply the same numeric services to both ordinary progression and remaining-distance progression across a tube waypoint.'],
 pre_fix_programs_retained=[str(O/'parts/prepare-verified/ra2/build-original-c/ra2.exe'),str(O/'parts/numeric-verified/ra2/build-original-c/ra2.exe')])
(S/'connection-regression-origin.json').write_text(json.dumps(write,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Preserved three failed traces and confirmed repaired 501-frame westbound scene')
