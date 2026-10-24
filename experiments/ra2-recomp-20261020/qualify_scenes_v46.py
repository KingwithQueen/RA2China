from run_batch_v46 import *
log=run([S/'transport_packet_probe.exe',R/'ra2/game/game.exe'],'transport-native-constructor')
x=read(log);assert x['passed'] and x['native_transport_constructor_cases']==128
write(S/'transport-native-validation.json',dict(**x,source_sha256=sha(S/'transport_packet_probe.c'),probe_sha256=sha(S/'transport_packet_probe.exe'),original_sha256=sha(R/'ra2/game/game.exe')))
out=S/'baseline-observer';out.mkdir();entries=[]
for p in [S/n for n in ['bridge_catalog_observer.c','bridge-catalog-observer.exe','bridge-catalog-build-arguments.json']]+[R/n for n in ['make_bridge_catalog_v46.py','build-bridge-catalog-v46.ps1','run_bridge_catalog_v46.py']]:
 d=out/p.name;shutil.copy2(p,d);entries.append(dict(path=p.name,sha256=sha(d)))
write(out/'manifest.json',entries)
values=[]
for x in read(S/'dynamic-fixtures.json')['fixtures']:
 tag,args=fixture_job(x['baseline_tag'],x,x['last']);run(args,'scene-'+tag,allowed_codes=(0,1))
 q=read(S/'runs'/tag/'comparison.json');assert all(r['passed'] for r in q['runs'])
 if not q['passed']:
  assert tag=='b-hv'
  from accept_hover_v46 import accept
  assert accept(tag)['passed']
 values.append(dict(tag=tag,strict_passed=q['passed'],frames=q['comparison']['frames_compared'],comparison_sha256=sha(S/'runs'/tag/'comparison.json')))
write(S/'baseline-scene-matrix.json',dict(passed=True,results=values,excluded_from_final_acceptance_count=True))
