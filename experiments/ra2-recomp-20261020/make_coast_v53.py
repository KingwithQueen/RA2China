"""Natural coast fixtures: fully occupied adjacent cells and mixed multiple passengers."""
from run_batch_v53 import *
from map_codec_v53 import unpack
import re
source=(O/'fixtures/coast-ww.MAP').read_text(encoding='ascii');items=[]
unit=lambda kind,x,y:f'Player House,{kind},256,{x},{y},0,Guard,None,0,-1,0,-1,1,1'
foot=lambda kind,x,y:f'Player House,{kind},256,{x},{y},2,Guard,0,None,0,-1,0,1,1'
def section(t,name,lines):
 replacement='['+name+']\n'+'\n'.join(str(i)+'='+v for i,v in enumerate(lines))+'\n\n'
 return re.sub(r'^\['+name+r'\]\n.*?(?=^\[|\Z)',lambda m:replacement,t,flags=re.M|re.S)
for tag,last in [('aw',3200),('mp',3000)]:
 units=[unit('LCRF',138,102),unit('TRUCKA',139,102),unit('DEST',130,99)]
 if tag=='aw':
  starts=[(135,103),(136,103),(137,105),(138,105),(139,105),(140,103),(140,102),(140,101)]
  targets=[(137,101),(138,101),(139,101),(137,102),(139,102),(137,103),(138,103),(139,103)]
  units += [unit('TRUCKA',*c) for c in starts]
  orders=['50:1023363:7:1023362:0','400:1023362:2:129:103','900:1023362:2:138:102','1700:1023362:16:0:0','2300:1023370:2:144:102','2700:1023363:2:144:104','200:1023364:2:130:106','1200:1023364:2:130:94','2500:1023364:2:130:106','700:1023374:2:141:100','300:1023375:2:139:96','1500:1023375:2:140:100']
  orders += [f'1300:{1023366+i}:2:{x}:{y}' for i,(x,y) in enumerate(targets)]
  extra=dict(carrier_id=1023362,cargo_ids=[1023363],ship_id=1023364,foot_id=1023374,other_id=1023375,blockers=[dict(id=1023366+i,start=list(start),target=list(target)) for i,(start,target) in enumerate(zip(starts,targets))],release_id=1023370,release_order=2300,unload_order=1700)
 else:
  units += [unit('TRUCKA',139,103),unit('TRUCKA',138,101)]
  orders=['50:1023363:7:1023362:0','100:1023366:7:1023362:0','150:1023368:7:1023362:0','800:1023362:2:129:103','1400:1023362:2:138:102','2000:1023362:16:0:0','2400:1023363:2:139:104','2400:1023366:2:140:104','2400:1023368:2:141:104','200:1023364:2:130:106','1400:1023364:2:130:94','2400:1023364:2:130:106','2500:1023367:2:138:104','300:1023369:2:139:96','1500:1023369:2:138:105']
  extra=dict(carrier_id=1023362,cargo_ids=[1023363,1023366,1023368],ship_id=1023364,other_id=1023369,blockers=[dict(id=1023367,start=[138,101],target=[138,101])],unload_order=2000)
 t=section(source,'Units',units);p=S/'fixtures'/('coast-'+tag+'.MAP');p.write_bytes(t.encode('ascii'));assert unpack(t)[1]==unpack(source)[1]
 items.append(dict(tag=tag,baseline_tag='b-'+tag,path=p.relative_to(R).as_posix(),sha256=sha(p),last=last,orders=orders,capture_host=True,terrain_pack_sha256=hashlib.sha256(unpack(t)[1]).hexdigest(),**extra))
old=next(x for x in read(O/'dynamic-fixtures.json')['fixtures'] if x['tag']=='js');p=S/'fixtures/coast-js.MAP';shutil.copy2(R/old['path'],p)
items.append(dict(**{k:v for k,v in old.items() if k not in ['path','sha256','baseline_tag']},path=p.relative_to(R).as_posix(),sha256=sha(p),baseline_tag='js',baseline_stage=O.name))
write(S/'dynamic-fixtures.json',dict(passed=True,fixtures=items,ordinary_events=True,terrain_pack_unchanged=True,no_rules_overrides=True,inherited_js_baseline=True))
print(dict(passed=True,fixtures=[x['tag'] for x in items]))
