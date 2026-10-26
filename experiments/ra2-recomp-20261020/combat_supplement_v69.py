"""One overheal-cap case and command-only/readonly-observer parity."""
from combat_batch_v69 import *
if sys.argv[1]=='prepare':
    x=dict(next(x for x in read(S/'scene-recipes.json')['fixtures'] if x['tag']=='repair'))
    src=R/x['path'];text=src.read_text(encoding='ascii');old='Player House,MTNK,128,85,112';assert text.count(old)==1
    p=S/'fixtures/cap.MAP';p.write_text(text.replace(old,'Player House,MTNK,200,85,112'),encoding='ascii',newline='\n')
    x.update(tag='cap',path=p.relative_to(R).as_posix(),map_sha256=sha(p),kind='ordinary-repair-cap',source=str(src),source_sha256=sha(src))
    write(S/'extra-scene.json',dict(passed=True,fixture=x,only_initial_health_fraction_changed=True))
    run(fixture('b-cap',x),'scene-b-cap',codes=(0,1));d=read(S/'runs/b-cap/comparison.json');assert all(a['passed'] and a['exit_code']==0 for a in d['runs'])
    write(S/'extra-baseline-contract.json',dict(passed=True,result=dict(tag='b-cap',frames=1501,strict=d['passed'],comparison_sha256=sha(S/'runs/b-cap/comparison.json'),exe_sha256=d['exe_sha256']),traces=[dict(tag='b-cap',mode=m,path=str(S/'runs/b-cap'/m/'state.jsonl'),sha256=sha(S/'runs/b-cap'/m/'state.jsonl')) for m in ['original','generated-c']]))
elif sys.argv[1]=='host':
    t=(S/'combat_observer.c').read_text(encoding='utf-8');a=t.index('static void *health_trampoline;');b=t.index('void ra2_state_tick(void)',a);t=t[:a]+t[b:]
    t=t.replace('    if(recomp_trace_extra && recomp_trace_extra!=health_trace)fail("unexpected trace observer");\n    recomp_trace_extra=health_trace;\n','')
    t=t.replace('    static const uint8_t health_bytes[]={0x83,0xEC,0x14,0x53,0x55};\n    install_hook(0x5D3D20,health_bytes,sizeof(health_bytes),health_hook,&health_trampoline);\n','')
    assert 'health_trace' not in t and 'health_hook' not in t
    p=S/'combat_command.c'
    if p.exists():assert p.read_text(encoding='utf-8')==t
    else:p.write_text(t,encoding='utf-8')
    args=read(S/'observer-build-arguments.json');serialized=json.dumps(args).replace('combat_observer','combat_command').replace('combat-observer','combat-command');out=S/'command-build-arguments.json'
    if out.exists():out.write_text(json.dumps(json.loads(serialized),indent=2)+'\n',encoding='utf-8')
    else:write(out,json.loads(serialized))
    for src,dest in [('build-combat-observer-v69.ps1','build-combat-command-v69.ps1'),('run_combat_observer_v69.py','run_combat_command_v69.py')]:
        t=(R/src).read_text(encoding='utf-8').replace('observer-build-arguments','command-build-arguments').replace('combat-observer.exe','combat-command.exe');(R/dest).write_text(t,encoding='utf-8')
    run(['pwsh','-NoProfile','-File',R/'build-combat-command-v69.ps1'],'build-command-'+sys.argv[2])
elif sys.argv[1] in ['baseline','final']:
    label='b' if sys.argv[1]=='baseline' else 'f';x=next(x for x in read(S/'scene-recipes.json')['fixtures'] if x['tag']=='tank')
    args=fixture(label+'-tank-cmd',x);args[4]=R/'run_combat_command_v69.py';run(args,'scene-'+label+'-tank-cmd',codes=(0,1))
    d=read(S/'runs'/(label+'-tank-cmd')/'comparison.json');assert d['passed']
    write(S/(label+'-command-scenes.json'),dict(passed=True,result=dict(tag=label+'-tank-cmd',frames=1501,strict=True,comparison_sha256=sha(S/'runs'/(label+'-tank-cmd')/'comparison.json'),exe_sha256=d['exe_sha256'])))
else:raise ValueError(sys.argv[1])
