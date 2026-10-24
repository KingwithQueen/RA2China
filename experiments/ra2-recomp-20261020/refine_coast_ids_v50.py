"""DEST normally creates an ASW aircraft before following actors receive IDs."""
from run_batch_v50 import *
p=S/'coast-fixtures.json';data=read(p);write(S/'initial-coast-fixtures.json',data)
for item in data['fixtures']:
 old=item['tag'];item['tag']='w2' if old=='wa' else 'a2';item['baseline_tag']='b-'+item['tag']
 threshold=1023365 if old=='wa' else 1023364;orders=[]
 for order in item['orders']:
  parts=order.split(':');uid=int(parts[1]);parts[1]=str(uid+1 if uid>=threshold else uid);orders.append(':'.join(parts))
 item['orders']=orders
 item['identity_refinement']=dict(natural_ASW_aircraft_created=True,aircraft_id=threshold,following_actors_shifted_by=1,frame0_original=str(S/'runs'/('b-'+old)/'original/state.jsonl'))
data['identity_refined']=True;p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
