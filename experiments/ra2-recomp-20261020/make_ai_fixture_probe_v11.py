"""独立实景工具：只替换测试摆放器对象，保留正式 EXE、源码及构建对象。"""
from pathlib import Path
import json,shlex
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v11'
t=(R/'ra2/src/runtime/movement_fixture.c').read_text(encoding='utf-8')
old='uint32_t enemy_house = U32(U32(0xA3229C) + 4);'
new='uint32_t enemy_house = U32(U32(0xA3229C) + 4);\n            if (enemy_house == house) enemy_house = U32(U32(0xA3229C));'
assert t.count(old)==1;t=t.replace(old,new)
(S/'ai_movement_fixture.c').write_text(t,encoding='utf-8')
commands=json.loads((R/'ra2/build-original-c/compile_commands.json').read_text(encoding='utf-8'))
entry=next(e for e in commands if e['file'].endswith('movement_fixture.c'))
args=[a.strip('"') for a in shlex.split(entry['command'],posix=False)][1:]
args=[('/Fo'+str(S/'ai_movement_fixture.obj')) if a.startswith('/Fo') else ('/Fd'+str(S/'ai_fixture.pdb')) if a.startswith('/Fd') else str(S/'ai_movement_fixture.c') if a.replace('\\','/').endswith('/src/runtime/movement_fixture.c') else a for a in args]
assert args[-1]==str(S/'ai_movement_fixture.c')
link=(S/'production-link-command.txt').read_text(encoding='utf-8');link=link.split(' /nologo ',1)[1].rsplit(' && cd ."',1)[0]
links=['/nologo']+link.split()
oldobj='CMakeFiles\\ra2.dir\\src\\runtime\\movement_fixture.c.obj';assert links.count(oldobj)==1
links=[str(S/'ai_movement_fixture.obj') if a==oldobj else '/out:'+str(S/'ai-fixture-probe.exe') if a.startswith('/out:') else '/implib:'+str(S/'ai-fixture-probe.lib') if a.startswith('/implib:') else '/pdb:'+str(S/'ai-fixture-probe.pdb') if a.startswith('/pdb:') else a for a in links]
(S/'ai-fixture-build-arguments.json').write_text(json.dumps(dict(compile=args,link=links),ensure_ascii=False,indent=2),encoding='utf-8')
print('standalone fixture recipe created; production files untouched')
