"""Fixture host: native capture input and readonly bridge snapshots; no repair/path/result calls."""
from run_batch_v46 import *
import shlex
p=R/'ra2/src/runtime/state_trace.c';t=p.read_text(encoding='utf-8')
old='if ((order->mission != 2 && order->mission != 13) || order->x >= 1000 || order->y >= 1000) fail("unsupported mission or cell");'
assert t.count(old)==1
t=t.replace(old,'if ((order->mission != 2 && order->mission != 13 && order->mission != 8 && order->mission != 7 && order->mission != 16) || ((order->mission == 8 || order->mission == 7) ? (!order->x || order->y) : (order->x >= 1000 || order->y >= 1000))) fail("unsupported mission or target");')
marker='    memcpy((void *)(uintptr_t)(0xA32344 + slot * 111), event, sizeof(event));';assert t.count(marker)==1
t=t.replace(marker,'''    if (order->mission == 8 || order->mission == 7)
    {
        uint32_t target = find_object(order->x);
        if (!target || U32(object) != 0x7A3540 || U32(target) != (order->mission == 8 ? 0x79CBBCu : 0x7ADDF8u)) fail("invalid capture/transport target");
        uint32_t offset = order->mission == 7 ? 0x13u : 0x0Eu;
        memcpy(event + offset, &order->x, 4);
        event[offset + 4] = 0x34;
    }
'''+marker)
t=t.replace('if (!cell_catalog_path[0] || cell_catalog_written) return;','if (frame < 900 || !cell_catalog_path[0] || cell_catalog_written) return;')
marker='    write_cell_catalog(frame);';assert t.count(marker)==1
t=t.replace(marker,marker+'''
    if (frame == 200 || frame == 900 || frame == 1800)
    {
        uint32_t cells = U32(0x8324E0 + 0x138);
        uint32_t left = U32(cells + (66 * 512 + 60) * 4);
        uint32_t right = U32(cells + (66 * 512 + 61) * 4);
        fprintf(state_file, "{\\\"kind\\\":\\\"fixture-bridge-state\\\",\\\"frame\\\":%u,\\\"bridge\\\":[%u,%u]}\\n", frame,
            (U32(left + 0x140) & 0x100) != 0, (U32(right + 0x140) & 0x100) != 0);
    }
''')
t=t.replace('    write_cell_catalog(frame);', '    write_cell_catalog(frame);'+'\n    for (uint32_t index=0; index<U32(0xA40C30); ++index)\n    {\n        uint32_t object=U32(U32(0xA40C24)+index*4), kind=U32(object);\n        if(kind==0x7A3540)\n            fprintf(state_file,"{\\"kind\\":\\"fixture-object-flags\\",\\"frame\\":%u,\\"id\\":%u,\\"bytes_74_75_76_79_7a_7d\\":[%u,%u,%u,%u,%u,%u]}\\n",frame,U32(object+0x10),U8(object+0x74),U8(object+0x75),U8(object+0x76),U8(object+0x79),U8(object+0x7A),U8(object+0x7D));\n    }\n')
q=S/'bridge_catalog_observer.c'
if q.exists():
 assert '--relink' in sys.argv and q.read_bytes()==t.encode('utf-8')
else:q.write_text(t,encoding='utf-8',newline='\n')
commands=read(R/'ra2/build-original-c/compile_commands.json');entry=next(e for e in commands if e['file'].replace('\\','/').endswith('/runtime/state_trace.c'))
args=[a.strip('"') for a in shlex.split(entry['command'],posix=False)][1:]
args=[('/Fo'+str(S/'bridge_catalog_observer.obj')) if a.startswith('/Fo') else ('/Fd'+str(S/'bridge_catalog_observer.pdb')) if a.startswith('/Fd') else str(q) if a.replace('\\','/').endswith('/runtime/state_trace.c') else a for a in args]
args+=['/I'+str(R/'ra2/src/runtime')]
ninja=(R/'ra2/build-original-c/build.ninja').read_text(encoding='utf-8');objects=next(l for l in ninja.splitlines() if l.startswith('build ra2.exe:')).split('Release ',1)[1].split(' || ',1)[0].split();target='CMakeFiles\\ra2.dir\\src\\runtime\\state_trace.c.obj';assert objects.count(target)==1
libs=next(l for l in ninja.splitlines() if l.startswith('  LINK_LIBRARIES =')).split(' = ',1)[1].split()
link=['/nologo','/machine:X86','/subsystem:console','/INCREMENTAL:NO','/BASE:0x60000000','/FIXED:NO','/DYNAMICBASE:NO','/NXCOMPAT','/LARGEADDRESSAWARE','/STACK:0x1000000','/MANIFESTUAC:NO','/MAP:'+str(S/'bridge-catalog-observer.map'),'/out:'+str(S/'bridge-catalog-observer.exe')]+[str(S/'bridge_catalog_observer.obj') if o==target else o for o in objects]+libs
data=dict(compiles=[args],link=link);destination=S/'bridge-catalog-build-arguments.json'
if destination.exists():
 assert '--relink' in sys.argv;destination.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
else:write(destination,data)
print(dict(passed=True,production_sha256=sha(R/'ra2/build-original-c/ra2.exe'),observer_change='Normal capture target packet plus readonly bridge flags at200/900/1800 and catalog900; production game logic and recorder unchanged.'))
