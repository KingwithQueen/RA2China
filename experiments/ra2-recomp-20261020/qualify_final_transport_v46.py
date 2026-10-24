"""Finite final traffic recipe: move the opposing infantry to the bridge approach."""
from run_batch_v46 import *
for item in read(S/'dynamic-fixtures.json')['fixtures'][:2]:
 tag,args=fixture_job(item['baseline_tag'],item,item['last']);run(args,'scene-'+tag)
 q=read(S/'runs'/tag/'comparison.json');assert q['passed']
print('Final loaded/unloaded bridge traffic qualification complete')
