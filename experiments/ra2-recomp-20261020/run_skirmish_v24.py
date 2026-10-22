"""经原版遭遇战菜单进入游戏；固定 seed，不改预算、队列、目标或会话内存。"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,importlib.util,json,os,subprocess,sys
from run_fixture_comparison import compare_traces
R=Path(__file__).resolve().parent; S=R/'evidence/movement-state-v24'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
ap=argparse.ArgumentParser();ap.add_argument('--tag',required=True);ap.add_argument('--range',default='0:900');ap.add_argument('--order',action='append',default=[]);ap.add_argument('--unit-ring');ap.add_argument('--host-exe',type=Path);ap.add_argument('--starting-units',type=int);ap.add_argument('--scenario-rules',type=Path);a=ap.parse_args()
out=S/'runs'/a.tag;assert out.resolve().parent==(S/'runs').resolve();out.mkdir(parents=True,exist_ok=False)
os.environ['RA2_TARGET']='game'
spec=importlib.util.spec_from_file_location('playtest',R/'ra2/tools/playtest.py');test=importlib.util.module_from_spec(spec);spec.loader.exec_module(test)
exe=a.host_exe.resolve() if a.host_exe else R/'ra2/build-original-c/ra2.exe';fingerprint=sha(exe)
script=test.SP().press(test.SINGLE,'Skirmish',test.SKIRMISH).press(test.SKIRMISH,'StartGame').waitlog(test.INGAME)
def run(original):
    mode='original' if original else 'generated-c';folder=out/mode;folder.mkdir()
    settings={'Skirmish':{'UnitCount':a.starting_units}} if a.starting_units is not None else None
    game=Path(test.farm(str(folder/'game'),settings))
    if a.scenario_rules:
        temporary=game/'rules-skirmish-new.tmp';temporary.write_bytes(a.scenario_rules.read_bytes());temporary.replace(game/'RULES.INI')
    save=game/'SAVE0029.SAV';before=sha(save);assert save.stat().st_nlink==1
    ini=game/'RA2.INI';ini_before=sha(ini)
    cmd=[str(exe),'--headless','--run','--mute','--debuglog','--watchdog','240','--exe',str(game/'game.exe'),'--game',str(game),'--mod','none','--seed','12345','--state-log',str(folder/'state.jsonl'),'--state-range',a.range,'--state-movement-audit']+script.args
    for order in a.order:cmd+=['--frame-order',order]
    if a.unit_ring:cmd+=['--state-unit-ring',a.unit_ring]
    if original:cmd+=['--original']
    (folder/'command.json').write_text(json.dumps(cmd,ensure_ascii=False,indent=2),encoding='utf-8')
    with (folder/'run.log').open('w',encoding='utf-8') as f:code=subprocess.run(cmd,cwd=R/'ra2',stdout=f,stderr=subprocess.STDOUT,timeout=270).returncode
    return dict(mode=mode,exit_code=code,passed=code==0,save_before=before,save_after=sha(save),ini_before=ini_before)
with ThreadPoolExecutor(max_workers=2) as pool:runs=list(pool.map(run,[True,False]))
x=dict(exe_sha256=fingerprint,seed=12345,entry='original skirmish menu and map',starting_units=a.starting_units,scenario_rules_sha256=sha(a.scenario_rules) if a.scenario_rules else None,save_loaded=False,memory_state_injection=False,runs=runs)
if all(r['passed'] for r in runs):
    first,last=map(int,a.range.split(':'));x['comparison']=compare_traces(out/'original/state.jsonl',out/'generated-c/state.jsonl',first,last)
x['passed']=all(r['passed'] and r['save_before']==r['save_after'] for r in runs) and x.get('comparison',{}).get('passed',False) and sha(exe)==fingerprint
(out/'comparison.json').write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in x.items() if k!='comparison'},ensure_ascii=False));sys.exit(0 if x['passed'] else 1)
