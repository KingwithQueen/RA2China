"""One finite affected matrix, plus six ordinary alias-observation scenes."""
from run_batch_v39 import R,S,read,write,run,py,scenes,fixture_job,sha
import argparse
def build():
 run(py('make_connection_fixture_v39.py'),'prepare-connection-observer')
 run(['pwsh','-NoProfile','-File',R/'build-connection-fixture-v39.ps1'],'build-connection-observer')
 run(py('audit_legal_sources_v39.py'),'audit-legal-sources')
 run(py('audit_internal_alias_sources_v39.py'),'audit-internal-alias-sources')
 write(S/'final-build-ready.json',dict(passed=True,production_sha256=sha(R/'ra2/build-original-c/ra2.exe'),observer_sha256=sha(S/'connection-fixture-probe.exe')))
def matrix():
 assert read(S/'final-build-ready.json')['passed']
 jobs=[]
 for x in read(S/'bridge-cross-release-fixtures.json')['fixtures']:
  jobs.append(fixture_job('cross-'+x['name'],x))
  jobs.append(fixture_job('observed-cross-'+x['name'],x,runner='run_connection_v39.py'))
 for x in read(S/'bridge-infantry-fixtures.json')['fixtures']:
  if x['meeting']:jobs.append(fixture_job(x['name'],x))
 x=next(x for x in read(S/'bridge-hostile-fixtures.json')['fixtures'] if x['name']=='enemy-traffic-ai3-north')
 jobs.append(fixture_job('enemy-traffic-north',x))
 for tag,filename,goal in [('curve-up','tube-curved-elevated-east.MAP',80),('curve-tall-down','tube-curved-tall-west.MAP',66)]:
  x=dict(path=(S/'fixtures'/filename).relative_to(R).as_posix(),orders=[f'5:1022581:2:{goal}:114'])
  jobs.append(fixture_job(tag,x,600))
 x=dict(path=(S/'fixtures/tube-east.MAP').relative_to(R).as_posix(),orders=['5:1022581:2:80:114'])
 tag,args=fixture_job('blocked-tube',x);jobs.append((tag,args+['--unit-ring','170:1022581:2']))
 x=dict(path=(S/'fixtures/dynamic-far-base.MAP').relative_to(R).as_posix(),orders=['5:1022579:2:100:114']+[f'{f}:1022579:2:100:114' for f in range(450,1111,60)])
 tag,args=fixture_job('repeat-failure',x,1250);jobs.append((tag,args+['--unit-ring','398:1022579:2']))
 for group in range(6):
  x=read(S/'bridge-cross-release-fixtures.json')['fixtures'][group%2]
  jobs.append(fixture_job('alias-'+str(group),x,runner='run_occupied_alias_probe_v39.py'))
 values=scenes(jobs)
 write(S/'final-scene-matrix.json',dict(passed=True,results=values,production_scenes=9,production_frames=sum(x['frames'] for x in values if not x['tag'].startswith(('observed-','alias-'))),observer_scenes=8,observer_frames=4008,alias_scenes=6,alias_frames=3006,scope='Two bridge crossing/release combinations, two unobstructed opposing infantry scenes, hostile traffic, two curved height anomalies, controlled blocked exit, repeated failure. Existing broad historical matrices are retained in v38, not claimed as rerun.'))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['build','scenes']);a=ap.parse_args()
 build() if a.action=='build' else matrix()
