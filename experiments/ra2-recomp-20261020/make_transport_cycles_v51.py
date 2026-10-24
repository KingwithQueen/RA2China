"""Ordinary coast traffic: occupied shore, repeated loading/unloading, and an aircraft route."""
from run_batch_v51 import *
from map_codec_v51 import unpack
import hashlib
old=read(O/'coast-fixtures.json')['fixtures'];items=[]
for original,tag,last in [(old[0],'cw',3500),(old[1],'ca',4000)]:
 t=(R/original['path']).read_text(encoding='ascii')
 if tag=='cw':
  assert t.count('TRUCKA,256,138,104')==1;t=t.replace('TRUCKA,256,138,104','TRUCKA,256,138,101')
  orders=['50:1023363:7:1023362:0','200:1023364:2:130:106','1200:1023364:2:130:94','2200:1023364:2:130:106','400:1023362:2:129:103','900:1023362:2:138:102','1400:1023362:16:0:0','1500:1023366:2:140:102','1600:1023363:2:139:104','1800:1023363:7:1023362:0','2100:1023362:2:130:103','2500:1023362:2:138:102','3000:1023362:16:0:0','3200:1023363:2:139:104','2250:1023366:2:138:104','900:1023367:2:140:100','300:1023368:2:139:96','1500:1023368:2:138:105']
 else:
  orders=[x for x in original['orders'] if not x.startswith('2300:')]+['2300:1023365:7:1023362:0','2500:1023362:2:129:103','3000:1023362:2:139:102','3500:1023362:16:0:0','3700:1023365:2:140:104','2400:1023363:2:130:106','3300:1023363:2:130:96','3300:1023366:2:140:102','3800:1023366:2:138:105']
 p=S/'fixtures'/('coast-cycle-'+tag+'.MAP');p.write_bytes(t.encode('ascii'));assert unpack(t)[1]==unpack((R/original['path']).read_text(encoding='ascii'))[1]
 items.append(dict(tag=tag,baseline_tag='b-'+tag,path=p.relative_to(R).as_posix(),sha256=sha(p),orders=orders,last=last,capture_host=True,terrain_pack_sha256=hashlib.sha256(unpack(t)[1]).hexdigest(),cargo_id=1023363 if tag=='cw' else 1023365,carrier_id=1023362))
pilot=read(S/'aircraft-pilot-fixture.json');items.append(dict(tag='oc',baseline_tag='b-oc',path=pilot['path'],sha256=pilot['sha256'],orders=['200:1023364:2:129:103','800:1023364:2:140:104','1200:1023364:2:130:105','1700:1023364:2:138:102','200:1023362:2:130:106','1200:1023362:2:130:94','1000:1023365:2:140:100'],last=2200,capture_host=True,aircraft_id=1023364,ship_id=1023362,foot_id=1023365))
write(S/'transport-cycle-fixtures.json',dict(passed=True,fixtures=items,ordinary_events=True,water_beach_land_unchanged=True,aircraft_identity_pilot_sha256=sha(S/'runs/pilot/comparison.json')))
