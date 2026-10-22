"""Two diagnostic object replacements; production recorder, comparator and binary unchanged."""
from pathlib import Path
import hashlib,json,shlex
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v22'
t=(R/'ra2/src/runtime/movement_fixture.c').read_text(encoding='utf-8')
marker='void ra2_movement_fixture_tick(uint32_t frame, FILE *output, int original_mode)\n{'
assert t.count(marker)==1
t=t.replace(marker,(S/'connection_observer.c').read_text(encoding='utf-8')+'\n'+marker+'\n    connection_tick(output,original_mode);')
(S/'connection_movement_fixture.c').write_text(t,encoding='utf-8',newline='\n')
t=(R/'ra2/src/runtime/ground_remainder_bridge.c').read_text(encoding='utf-8')
t='extern void __cdecl ra2_connection_observe(unsigned drive, unsigned stage);\n'+t
marker='MEM8(owner(c) + 0x575) = 0;';assert t.count(marker)==1
t=t.replace(marker,marker+' ra2_connection_observe(c->drive,0);')
marker='MEM8(c->drive + 0x63) = 1;';assert t.count(marker)==1
t=t.replace(marker,marker+' ra2_connection_observe(c->drive,1);')
(S/'connection_remainder_bridge.c').write_text(t,encoding='utf-8',newline='\n')
commands=json.loads((R/'ra2/build-original-c/compile_commands.json').read_text(encoding='utf-8'))
compiles=[];replacements={}
for original,helper in [('movement_fixture','connection_movement_fixture'),('ground_remainder_bridge','connection_remainder_bridge')]:
 entry=next(e for e in commands if e['file'].replace('\\','/').endswith('/'+original+'.c'))
 args=[a.strip('"') for a in shlex.split(entry['command'],posix=False)][1:]
 args=[('/Fo'+str(S/(helper+'.obj'))) if a.startswith('/Fo') else ('/Fd'+str(S/(helper+'.pdb'))) if a.startswith('/Fd') else str(S/(helper+'.c')) if a.replace('\\','/').endswith('/src/runtime/'+original+'.c') else a for a in args]
 compiles.append(args);replacements['CMakeFiles\\ra2.dir\\src\\runtime\\'+original+'.c.obj']=str(S/(helper+'.obj'))
ninja=(R/'ra2/build-original-c/build.ninja').read_text(encoding='utf-8')
objects=next(l for l in ninja.splitlines() if l.startswith('build ra2.exe:')).split('Release ',1)[1].split(' || ',1)[0].split()
assert all(objects.count(o)==1 for o in replacements)
libs=next(l for l in ninja.splitlines() if l.startswith('  LINK_LIBRARIES =')).split(' = ',1)[1].split()
links=['/nologo','/machine:X86','/subsystem:console','/INCREMENTAL:NO','/BASE:0x60000000','/FIXED:NO','/DYNAMICBASE:NO','/NXCOMPAT','/LARGEADDRESSAWARE','/STACK:0x1000000','/MANIFESTUAC:NO','/out:'+str(S/'connection-fixture-probe.exe')]+[replacements.get(o,o) for o in objects]+libs
(S/'connection-fixture-build-arguments.json').write_text(json.dumps(dict(compiles=compiles,link=links),indent=2),encoding='utf-8')
t=(R/'build-truck-actor-fixture-v22.ps1').read_text(encoding='utf-8').replace('truck-actor-fixture-build-arguments.json','connection-fixture-build-arguments.json')
t=t.replace('$taskCompile=@($taskArguments.compile);& cl @taskCompile\n    if($LASTEXITCODE){throw \'TRUCKA fixture compile failed\'}',"foreach($taskC in $taskArguments.compiles){$taskCompile=@($taskC);& cl @taskCompile;if($LASTEXITCODE){throw 'Connection observer compile failed'}}")
(R/'build-connection-fixture-v22.ps1').write_text(t,encoding='utf-8',newline='\n')
print('Connection observer replaces exactly two diagnostic objects; production sha256',hashlib.sha256((R/'ra2/build-original-c/ra2.exe').read_bytes()).hexdigest())
