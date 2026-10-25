"""Ordinary rule-defined locomotors, without forcing unused engine interfaces."""
from run_batch_v68 import *
import re
ground=len(sys.argv)>2 and sys.argv[2]=='ground'
record='other-movement-ground' if ground else 'other-movement'
tagpart='gtypes' if ground else 'types'
def section(t,key,rows):
    pat=rf'(?ms)^\[{key}\]\n.*?(?=^\[|\Z)';value='['+key+']\n'+rows+'\n'
    return re.sub(pat,lambda _:value,t) if re.search(pat,t) else t+'\n'+value
if sys.argv[1]=='correct':
    x=read(S/'other-movement-pending.json');src=R/x['path'];t=src.read_text(encoding='ascii')
    # Accepted map schema: Tag,Veterancy,Group,OnBridge,Autocreate,Deletable.
    old='Guard,0,None,-1,0,-1,1,1';new='Guard,0,None,0,-1,0,1,1'
    assert t.count(old)==3;out=t.replace(old,new);p=S/'fixtures/move-types-ground.MAP';assert not p.exists();p.write_text(out,encoding='ascii',newline='\n')
    x.update(path=p.relative_to(R).as_posix(),map_sha256=sha(p),initial_invalid_bridge_flag=-1,corrected_bridge_flag=0)
    write(S/'other-movement-ground-pending.json',x)
    write(S/'other-movement-input-review.json',dict(passed=True,initial_map=str(src),initial_sha256=sha(src),initial_comparison_sha256=sha(S/'runs/b-types/comparison.json'),excluded_from_positive_acceptance=True,reason='Infantry row fields were shifted after Tag, yielding OnBridge=-1 and artificial upper-layer starts; initial traces kept, no production change to imitate this input.',corrected_map=str(p),corrected_sha256=sha(p),schema_reference=str(R/'evidence/movement-state-v38/fixtures/bridge-detour-north.MAP')))
    print(dict(passed=True,only_three_infantry_row_suffixes_corrected=True))
elif sys.argv[1]=='prepare':
    src=O/'fixtures/traffic-bm.MAP';text=src.read_text(encoding='ascii')
    units=[('HTNK',[77,76],[70,76]),('SAPC',[46,64],[56,64]),('DEST',[46,63],[56,63])]
    infantry=[('E1',[77,80],[70,80]),('JUMPJET',[78,80],[72,80]),('CLEG',[78,78],[74,80])]
    catalog=O/'runs/traffic-bm/original/cells.json';cells={tuple(c['cell']):c for c in read(catalog)['cells']}
    rules=Path(read(S/'scene-recipes-pending.json')['rules_original']);rt=rules.read_text(encoding='cp936');checks=[]
    for name,start,goal in units+infantry:
        m=re.search(r'(?ms)^\['+name+r'\]\s*\n(.*?)(?=^\[|\Z)',rt);assert m
        loc=re.search(r'(?m)^Locomotor=(.*)$',m[1]);assert loc
        points=[cells[tuple(p)] for p in [start,goal]]
        if name=='SAPC':assert points[0]['land']==2 and points[1]['land'] in [0,1,6,7],(name,points)
        elif name=='DEST':assert all(c['land']==2 for c in points),(name,points)
        else:assert all(c['land'] in [0,1,6,7] for c in points),(name,points)
        checks.append(dict(type=name,start=start,goal=goal,locomotor=loc[1],terrain=points))
    ur=''.join(f'{i}=Player House,{n},256,{p[0]},{p[1]},0,Guard,None,0,-1,0,-1,1,1\n' for i,(n,p,g) in enumerate(units))
    ir=''.join(f'{i}=Player House,{n},256,{p[0]},{p[1]},0,Guard,0,None,-1,0,-1,1,1\n' for i,(n,p,g) in enumerate(infantry))
    out=section(section(section(text,'Units',ur),'Infantry',ir),'Aircraft','');dest=S/'fixtures/move-types.MAP';assert not dest.exists();dest.write_text(out,encoding='ascii',newline='\n')
    write(S/'other-movement-pending.json',dict(passed=True,path=dest.relative_to(R).as_posix(),checks=checks,source=str(src),source_sha256=sha(src),map_sha256=sha(dest),rules_sha256=sha(rules),catalog_sha256=sha(catalog)))
    source=(R/'run_fixture_comparison.py').read_text(encoding='utf-8');marker="exe = ROOT / 'ra2/build-original-c/ra2.exe'";assert source.count(marker)==1
    source=source.replace(marker,"exe = ROOT / 'evidence/movement-state-v68/baseline/ra2/build-original-c/ra2.exe'")
    (R/'run_baseline_fixture_v68.py').write_text('from pathlib import Path\nR=Path(__file__).resolve().parent\nsource='+repr(source)+"\nexec(compile(source,str(R/'run_fixture_comparison.py'),'exec'),dict(__file__=str(R/'run_fixture_comparison.py'),__name__='__main__'))\n",encoding='utf-8')
    print(dict(passed=True,types=6))
elif sys.argv[1]=='baseline':
    x=read(S/(record+'-pending.json'));_,args=fixture('id-'+tagpart,x,1);args[4]=R/'run_baseline_fixture_v68.py'
    if not (S/'runs'/('id-'+tagpart)/'comparison.json').exists():run(args,'scene-id-'+tagpart)
    p=S/'runs'/('id-'+tagpart)/'comparison.json';assert read(p)['passed']
    state=next(json.loads(l) for l in (p.parent/'original/state.jsonl').open(encoding='utf-8') if json.loads(l)['kind']=='state')
    by_cell={tuple(v//256 for v in a['position'][:2]):a for a in state['objects']};orders=[]
    for c in x['checks']:
        a=by_cell[tuple(c['start'])];c['id']=a['id'];c['initial_locomotor_vtable']=a.get('locomotor_vtable');orders.append(f"5:{a['id']}:2:{c['goal'][0]}:{c['goal'][1]}")
    x['orders']=orders;write(S/(record+'-recipe.json'),x)
    _,args=fixture('b-'+tagpart,x,1800);args[4]=R/'run_baseline_fixture_v68.py';run(args,'scene-b-'+tagpart,codes=(0,1));d=read(S/'runs'/('b-'+tagpart)/'comparison.json')
    assert all(z['passed'] and z['exit_code']==0 for z in d['runs']);write(S/(record+'-baseline.json'),dict(passed=True,strict=d['passed'],comparison_sha256=sha(S/'runs'/('b-'+tagpart)/'comparison.json'),scope='Before-change executable and locked original; unknown differences stay explicit.'))
else:
    x=read(S/(record+'-recipe.json'));_,args=fixture('f-'+tagpart,x,1800);run(args,'scene-f-'+tagpart,codes=(0,1));d=read(S/'runs'/('f-'+tagpart)/'comparison.json')
    assert all(z['passed'] and z['exit_code']==0 for z in d['runs']);write(S/(record+'-final.json'),dict(passed=True,strict=d['passed'],comparison_sha256=sha(S/'runs'/('f-'+tagpart)/'comparison.json')))
