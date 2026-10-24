"""Ordinary scenario records and mission events; original terrain and rules retained."""
from run_batch_v52 import *
from map_codec_v52 import unpack
parent=read(O/'dynamic-fixtures.json')['fixtures'];items=[]
for old,tag in [(next(x for x in parent if x['tag']=='cw'),'ww'),(next(x for x in parent if x['tag']=='ca'),'js')]:
 t=(R/old['path']).read_text(encoding='ascii');orders=list(old['orders'])
 if tag=='ww':
  orders+=['700:1023362:16:0:0']
  ids=dict(carrier_id=1023362,cargo_id=1023363,ship_id=1023364,blocker_id=1023366,foot_id=1023367,other_id=1023368)
 else:
  assert 'DEST,256' in t and 'CLEG,256' in t
  t=t.replace('DEST,256','SUB,256').replace('CLEG,256','JUMPJET,256')
  # SUB does not create the destroyer's ASW child; pilot below confirms the ids.
  mapping={'1023365':'1023364','1023366':'1023365','1023367':'1023366'}
  orders=[':'.join(mapping.get(v,v) for v in o.split(':')) for o in orders]
  ids=dict(carrier_id=1023362,cargo_id=1023364,ship_id=1023363,foot_id=1023366,other_id=1023365)
 p=S/'fixtures'/('coast-'+tag+'.MAP');assert not p.exists();p.write_bytes(t.encode('ascii'))
 assert unpack(t)[1]==unpack((R/old['path']).read_text(encoding='ascii'))[1]
 items.append(dict(tag=tag,baseline_tag='b-'+tag,path=p.relative_to(R).as_posix(),sha256=sha(p),orders=orders,last=old['last'],capture_host=True,terrain_pack_sha256=hashlib.sha256(unpack(t)[1]).hexdigest(),**ids))
old=next(x for x in parent if x['tag']=='cm');p=S/'fixtures'/Path(old['path']).name;shutil.copy2(R/old['path'],p)
items.append(dict(**{k:v for k,v in old.items() if k not in ['path','sha256']},path=p.relative_to(R).as_posix(),sha256=sha(p)))
write(S/'dynamic-fixtures.json',dict(passed=True,fixtures=items,ordinary_events=True,terrain_pack_unchanged=True,no_rules_overrides=True,identity_pilot_required='js'))
write(S/'identity-pilot-fixture.json',dict(passed=True,path=items[1]['path'],sha256=items[1]['sha256'],orders=[],last=2,capture_host=True))
print(dict(passed=True,fixtures=[x['tag'] for x in items]))
