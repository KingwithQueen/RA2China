"""Verify complete production/observer record parity before either production edit."""
from run_batch_v66 import *
from accept_traffic_v66 import records
from itertools import zip_longest
assert read(S/'traffic-baseline-scenes.json')['passed']
items=[]
for item in read(S/'traffic-fixtures.json')['fixtures']:
 tag=item['observer_baseline_tag'];plain=item['baseline_tag']
 for mode in ['original','generated-c']:
  a=records(S/'runs'/plain/mode/'state.jsonl');b=(r for r in records(S/'runs'/tag/mode/'state.jsonl') if not r['kind'].startswith('fixture-'));count=0
  for left,right in zip_longest(a,b):assert left==right,(tag,mode,count);count+=1
  items.append(dict(tag=tag,mode=mode,production_records=count,complete_production_record_parity=True))
write(S/'channel-observer-baseline-parity.json',dict(passed=True,production_exe_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'),observer_exe_sha256=sha(S/'baseline-channel-observer/channel-observer.exe'),records=items))
print(dict(passed=True,complete_per_mode_parity=len(items)))
