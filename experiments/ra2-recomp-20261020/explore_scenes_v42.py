from run_batch_v42 import *
x=[a for a in read(S/'representative-acceptance-fixtures.json')['fixtures'] if a['name'].startswith('bridge-')]
values=scenes([fixture_job('baseline-04-'+a['name'],a,a['last']) for a in x])
write(S/'baseline-representative-matrix-04.json',dict(passed=True,results=values))
