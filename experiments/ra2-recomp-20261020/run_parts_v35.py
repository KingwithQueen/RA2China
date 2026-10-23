"""Integrate and validate one part at a time; both game lanes belong to that part."""
from pathlib import Path
import argparse,json,os,subprocess,sys
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v35'
ap=argparse.ArgumentParser();ap.add_argument('--resume-template',action='store_true');a=ap.parse_args()
def run(args,log):
    print('Starting '+log,flush=True)
    with (S/log).open('x',encoding='utf-8') as f:p=subprocess.run(args,cwd=R,stdout=f,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
    if p.returncode:print((S/log).read_text(encoding='utf-8',errors='replace')[-6000:],flush=True);raise RuntimeError(log)
for part,extension,build,exe,phase,name in [('template','register','tube-state','tube_state',5,'loaded-sample'),('passage','objects','objects','objects',9,'terrain-weapon'),('returns','exit','overlap','overlap',16,'invalidate-service')]:
    if a.resume_template and part=='template':
        run([sys.executable,'-X','utf8','-B',str(R/'run_lifecycle_part_v35.py'),part,'--resume'],'part-template-resume-01.log')
        print('Completed resumed template',flush=True);continue
    run([sys.executable,'-X','utf8','-B',str(R/('integrate_'+('objects' if part=='passage' else part)+'_v35.py'))],'integrate-'+part+'.log')
    run([sys.executable,'-X','utf8','-B',str(R/('extend_'+extension+'_probe_v35.py'))],'extend-'+part+'.log')
    run(['pwsh','-NoProfile','-File',str(R/'build-faithful.ps1')],'build-'+part+'.log')
    run(['pwsh','-NoProfile','-File',str(R/('build-'+build+'-probe-v35.ps1'))],'build-probe-'+part+'.log')
    run([str(S/(exe+'_probe.exe')),str(R/'ra2/game/game.exe'),str(phase)],name+'-probe-verified-01.json')
    v=json.loads((S/(name+'-probe-verified-01.json')).read_text(encoding='utf-8'));assert v['passed'] and v.get('cases',v.get('object_cases'))==65536
    run([sys.executable,'-X','utf8','-B',str(R/'run_lifecycle_part_v35.py'),part],'part-'+part+'.log')
    print('Completed '+part,flush=True)
print('All three part checkpoints passed',flush=True)
