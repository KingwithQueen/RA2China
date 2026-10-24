from run_batch_v48 import *
out=S/'baseline-observer';out.mkdir();entries=[]
for p in [S/n for n in ['bridge_catalog_observer.c','bridge-catalog-observer.exe','bridge-catalog-build-arguments.json']]+[R/n for n in ['make_bridge_catalog_v48.py','build-bridge-catalog-v48.ps1','run_bridge_catalog_v48.py']]:
 d=out/p.name;shutil.copy2(p,d);entries.append(dict(path=p.name,sha256=sha(d)))
write(out/'manifest.json',entries)
values=[]
for item in read(S/'collapse-transport-fixtures.json')['fixtures']:
 tag,args=fixture_job(item['baseline_tag'],item,item['last']);run(args,'scene-'+tag,allowed_codes=(0,1))
 p=S/'runs'/tag/'comparison.json';q=read(p);assert all(x['passed'] for x in q['runs'])
 values.append(dict(tag=tag,strict_passed=q['passed'],frames=q['comparison']['frames_compared'],comparison_sha256=sha(p)))
write(S/'transport-baseline-scenes.json',dict(passed=True,results=values,functional_effect_qualification_required=True,excluded_from_final_acceptance_count=True))
