"""Serial build boundaries, independent scene pairs, and immutable receipts."""
from run_batch_v68 import *
from concurrent.futures import ThreadPoolExecutor
import argparse
def observer(label):
    run(py('make_bridge_catalog_v68.py',*(['--relink'] if (S/'bridge_catalog_observer.c').exists() else [])),'make-observer-'+label)
    run(['pwsh','-NoProfile','-File',R/'build-bridge-catalog-v68.ps1'],'build-observer-'+label)
def one(job):
    tag,args=job
    run(args,'scene-'+tag,codes=(0,1))
    p=S/'runs'/tag/'comparison.json';d=read(p)
    assert all(x['passed'] and x['exit_code']==0 for x in d['runs']),tag
    assert d['comparison']['negative_control']['passed']
    # Unknown differences are not automatically converted to successful functional cases.
    assert d['passed'],(tag,d['comparison'].get('first_difference'))
    return dict(tag=tag,frames=d['comparison']['frames_compared'],exe_sha256=d['exe_sha256'],comparison_sha256=sha(p),strict=True)
def calibrate():
    items=read(S/'scene-recipes-pending.json')['fixtures'];proofs=[]
    for x in items:
        if not x.get('calibrate'):continue
        tag='id-occ' if x['occupied'] else 'id-free';one(fixture(tag,x,1))
        p=S/'runs'/tag/'original/state.jsonl'
        state=next(json.loads(l) for l in p.open(encoding='utf-8') if json.loads(l)['kind']=='state')
        by_cell={tuple(v//256 for v in a['position'][:2]):a['id'] for a in state['objects'] if a.get('ground_drive')}
        actor=by_cell[(77,76)];x.update(actor_ids=[actor],goals={str(actor):[57,76]},orders=[f'5:{actor}:2:57:76'],request_frames={str(actor):5})
        if x['occupied']:
            blocker=by_cell[(57,76)];x['blocker_ids']=[blocker];x['orders']+=[f'1000:{blocker}:2:58:74',f'1200:{actor}:2:57:76']
        proofs.append(dict(tag=tag,sha256=sha(S/'runs'/tag/'comparison.json'),setup_only=True))
    write(S/'scene-recipes.json',dict(passed=True,fixtures=items,identity_calibration=proofs))
def scene_group(label):
    items=read(S/'scene-recipes.json')['fixtures'];jobs=[]
    for x in items:
        jobs.append(fixture(label+'-'+x['tag'],x,x['last'],observer=True))
    # Production parity for the corrected queue, including all standard state/audit records.
    x=next(x for x in items if x['tag']=='rq-valid');jobs.append(fixture(label+'-rq-prod',x,x['last']))
    with ThreadPoolExecutor(max_workers=2) as pool:values=list(pool.map(one,jobs))
    write(S/(label+'-scenes.json'),dict(passed=True,results=values,pairs=len(values),frames=sum(x['frames'] for x in values)))
def native(label):
    receipts=[]
    for kind,probe,args in [('prepare','prepare',[]),('obstacle','obstacle',[]),('arrival','arrival',[]),('ground-services','ground_services',['2'])]:
        run(['pwsh','-NoProfile','-File',R/f'build-{kind}-probe-v68.ps1'],'build-native-'+label+'-'+kind)
        p=run([S/(probe+'_probe.exe'),R/'ra2/game/game.exe',*args],'native-'+label+'-'+kind)
        d=read(p);assert d['passed'];receipts.append(dict(probe=kind,exe_sha256=sha(S/(probe+'_probe.exe')),result=d))
    if label=='final':
        for kind in ['collision','map-area']:
            run(['pwsh','-NoProfile','-File',R/f'build-{kind}-probe-v68.ps1'],'build-native-final-'+kind)
            exe=S/(kind.replace('-','_')+'_probe.exe')
            p=run([exe,R/'ra2/game/game.exe'],'native-final-'+kind);d=read(p);assert d['passed']
            receipts.append(dict(probe=kind,exe_sha256=sha(exe),result=d))
    write(S/(label+'-native.json'),dict(passed=True,probes=receipts,original_sha256=sha(R/'ra2/game/game.exe')))
def checkpoint():
    receipt=read(R/'ra2/build-original-c/source-content-receipt.json');out=S/'parts/closeout';assert not out.exists();entries=[]
    paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']};paths.update(['ra2/CMakeLists.txt','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json'])
    for rel in sorted(paths):
        p=out/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,p);entries.append(dict(path=rel,sha256=sha(p)))
    write(out/'manifest.json',entries)
    write(out/'validation.json',dict(passed=True,exe_sha256=sha(R/'ra2/build-original-c/ra2.exe'),files=len(entries),scene_receipt_sha256=sha(S/'final-scenes.json'),native_receipt_sha256=sha(S/'final-native.json')))
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('action',choices=['baseline','final','regression']);x=a.parse_args()
    if x.action=='baseline':
        native('baseline');observer('baseline');calibrate();scene_group('b')
        dst=S/'baseline-observer';dst.mkdir()
        for n in ['bridge-catalog-observer.exe','bridge_catalog_observer.c']:shutil.copy2(S/n,dst/n)
        write(S/'baseline-observer.json',dict(passed=True,exe_sha256=sha(dst/'bridge-catalog-observer.exe'),source_sha256=sha(dst/'bridge_catalog_observer.c')))
    elif x.action=='final':
        native('final');observer('final');scene_group('f');shutil.copy2(S/'f-scenes.json',S/'final-scenes.json');checkpoint()
    else:
        jobs=[('default',py('run_skirmish_v68.py','--tag','default','--range','0:300'))]
        old=read(O/'bridge-cross-release-fixtures.json')['fixtures']
        jobs.extend(fixture('cross-'+z['name'],z,500) for z in old)
        collision=read(O/'collision-acceptance-fixtures.json')['fixtures']
        jobs.extend(fixture('contact-'+z['name'],z,500) for z in collision if 'control' not in z['name'])
        z=dict(path=(S/'fixtures/dynamic-far-base.MAP').relative_to(R).as_posix(),orders=['5:1022579:2:100:114']+[f'{f}:1022579:2:100:114' for f in range(450,1111,60)])
        tag,args=fixture('repeat-failure',z,1250);jobs.append((tag,args+['--unit-ring','398:1022579:2']))
        with ThreadPoolExecutor(max_workers=2) as pool:values=list(pool.map(one,jobs))
        write(S/'regressions.json',dict(passed=True,results=values,pairs=len(values),frames=sum(v['frames'] for v in values)))
