from run_batch_v42 import *
a=next(a for a in read(S/'representative-acceptance-fixtures.json')['fixtures'] if a['name']=='bridge-collapse')
tag,args=fixture_job('bridge-collapse',a,a['last'])
print(scenes([(tag,args+['--cell-catalog'])]))
