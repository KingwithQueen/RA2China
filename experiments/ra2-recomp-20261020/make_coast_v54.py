"""One vehicle and one infantry passenger, at two unmodified original shoreline sectors."""
from run_batch_v54 import *
from map_codec_v54 import unpack
parent=read(O/'dynamic-fixtures.json')['fixtures'];source=next(x for x in parent if x['tag']=='mp');items=[]
for tag,last,shore in [('mi',3000,[138,102]),('sc',3400,[138,107])]:
 p=S/'fixtures'/('coast-'+tag+'.MAP');shutil.copy2(R/source['path'],p)
 common=['50:1023363:7:1023362:0','100:1023368:7:1023362:0','800:1023362:2:129:103','200:1023364:2:130:106','1400:1023364:2:130:94','2600:1023364:2:130:106','300:1023369:2:139:96']
 if tag=='mi':
  orders=common+['300:1023366:2:141:104','1400:1023362:2:138:102','2000:1023362:16:0:0','2400:1023363:2:139:104','2400:1023368:2:140:104','2500:1023367:2:138:104','1500:1023369:2:138:105']
  goals={1023362:[138,102],1023363:[139,104],1023364:[130,106],1023366:[141,104],1023367:[138,104],1023368:[140,104],1023369:[138,105]}
 else:
  orders=common+['300:1023366:2:140:106','1900:1023366:2:139:106','2500:1023366:2:141:104','1700:1023367:2:137:106','1400:1023362:2:138:107','2200:1023362:16:0:0','2600:1023363:2:139:104','2600:1023368:2:140:104','1700:1023369:2:139:105','2900:1023369:2:138:99']
  goals={1023362:[138,107],1023363:[139,104],1023364:[130,106],1023366:[141,104],1023367:[137,106],1023368:[140,104],1023369:[138,99]}
 items.append(dict(tag=tag,baseline_tag='b-'+tag,path=p.relative_to(R).as_posix(),sha256=sha(p),last=last,orders=orders,capture_host=True,terrain_pack_sha256=hashlib.sha256(unpack(p.read_text(encoding='ascii'))[1]).hexdigest(),carrier_id=1023362,cargo_ids=[1023363,1023368],ship_id=1023364,other_id=1023369,traffic_ids=[1023366,1023367],shore=shore,unload_order=2000 if tag=='mi' else 2200,goals=goals))
old=next(x for x in parent if x['tag']=='aw3');p=S/'fixtures/coast-aw3.MAP';shutil.copy2(R/old['path'],p)
items.append(dict(**{k:v for k,v in old.items() if k not in ['path','sha256','baseline_tag']},path=p.relative_to(R).as_posix(),sha256=sha(p),baseline_tag='aw3',baseline_stage=O.name))
write(S/'dynamic-fixtures.json',dict(passed=True,fixtures=items,ordinary_events=True,no_rules_overrides=True,terrain_pack_unchanged=True,alternate_original_southern_shore=True,aw3_baseline_inherited=True))
print(dict(passed=True,fixtures=[x['tag'] for x in items]))
