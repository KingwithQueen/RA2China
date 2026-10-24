"""Readonly observer: defer the existing cell catalog to frame200; no game services/writes."""
from run_batch_v42 import *
import shlex
p=R/'ra2/src/runtime/state_trace.c';t=p.read_text(encoding='utf-8');marker='if (!cell_catalog_path[0] || cell_catalog_written) return;';assert t.count(marker)==1
q=S/'bridge_catalog_observer.c';assert not q.exists();q.write_text(t.replace(marker,'if (frame < 200 || !cell_catalog_path[0] || cell_catalog_written) return;'),encoding='utf-8',newline='\n')
commands=read(R/'ra2/build-original-c/compile_commands.json');entry=next(e for e in commands if e['file'].replace('\\','/').endswith('/runtime/state_trace.c'))
args=[a.strip('"') for a in shlex.split(entry['command'],posix=False)][1:]
args=[('/Fo'+str(S/'bridge_catalog_observer.obj')) if a.startswith('/Fo') else ('/Fd'+str(S/'bridge_catalog_observer.pdb')) if a.startswith('/Fd') else str(q) if a.replace('\\','/').endswith('/runtime/state_trace.c') else a for a in args]
args+=['/I'+str(R/'ra2/src/runtime')]
ninja=(R/'ra2/build-original-c/build.ninja').read_text(encoding='utf-8');objects=next(l for l in ninja.splitlines() if l.startswith('build ra2.exe:')).split('Release ',1)[1].split(' || ',1)[0].split();target='CMakeFiles\\ra2.dir\\src\\runtime\\state_trace.c.obj';assert objects.count(target)==1
libs=next(l for l in ninja.splitlines() if l.startswith('  LINK_LIBRARIES =')).split(' = ',1)[1].split()
link=['/nologo','/machine:X86','/subsystem:console','/INCREMENTAL:NO','/BASE:0x60000000','/FIXED:NO','/DYNAMICBASE:NO','/NXCOMPAT','/LARGEADDRESSAWARE','/STACK:0x1000000','/MANIFESTUAC:NO','/MAP:'+str(S/'bridge-catalog-observer.map'),'/out:'+str(S/'bridge-catalog-observer.exe')]+[str(S/'bridge_catalog_observer.obj') if o==target else o for o in objects]+libs
write(S/'bridge-catalog-build-arguments.json',dict(compiles=[args],link=link))
print(dict(passed=True,production_sha256=sha(R/'ra2/build-original-c/ra2.exe'),observer_change='Existing read-only catalog snapshot postponed to frame200; no game logic/state/schema changes.'))
