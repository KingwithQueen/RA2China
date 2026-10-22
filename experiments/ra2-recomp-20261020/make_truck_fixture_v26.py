"""Standalone default-rule scene helper. Production executable/objects stay intact."""
from pathlib import Path
import hashlib,json,shlex
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v26'
t=(R/'ra2/src/runtime/movement_fixture.c').read_text(encoding='utf-8')
old='uint32_t enemy_house = U32(U32(0xA3229C) + 4);'
assert t.count(old)==1
t=t.replace(old,old+'\n            if (enemy_house == house) enemy_house = U32(U32(0xA3229C));')
old='uint32_t unit_type = U32(actor + 0x5AC), size = 0x7D0;'
new='''uint32_t unit_type = 0, size = 0x7D0;
            uint32_t type_count = U32(0xA35D58), type_data = U32(0xA35D4C);
            if (type_count > 4096) fixture_fail("invalid UnitType vector");
            for (uint32_t ti = 0; ti < type_count; ++ti)
            {
                uint32_t candidate = U32(type_data + ti * 4);
                if (candidate && U32(candidate) == 0x7AE328
                    && !strcmp((const char *)(uintptr_t)(candidate + 0x24), "TRUCKA")) unit_type = candidate;
            }
            if (!unit_type) fixture_fail("default TRUCKA type not found");'''
assert t.count(old)==1;t=t.replace(old,new)
old='''            if (!cell || U32(cell + 0x44) != UINT32_MAX || U32(cell + 0xE4) || U32(cell + 0xE8))
                fixture_fail("ring cell is not empty");'''
new='''            if (!cell) fixture_fail("missing ring cell");
            if (U32(cell + 0xE4) || U32(cell + 0xE8))
            {
                fprintf(output, "{\\"kind\\":\\"fixture-occupied\\",\\"frame\\":%u,\\"id\\":%u,\\"cell\\":[%d,%d]}\\n", frame, fixture_id, cx, cy);
                continue;
            }'''
assert t.count(old)==1;t=t.replace(old,new)
src=S/'truck_movement_fixture.c';src.write_text(t,encoding='utf-8')
commands=json.loads((R/'ra2/build-original-c/compile_commands.json').read_text(encoding='utf-8'))
entry=next(e for e in commands if e['file'].endswith('movement_fixture.c'))
args=[a.strip('"') for a in shlex.split(entry['command'],posix=False)][1:]
args=[('/Fo'+str(S/'truck_movement_fixture.obj')) if a.startswith('/Fo') else ('/Fd'+str(S/'truck_fixture.pdb')) if a.startswith('/Fd') else str(src) if a.replace('\\','/').endswith('/src/runtime/movement_fixture.c') else a for a in args]
assert args[-1]==str(src)
ninja=(R/'ra2/build-original-c/build.ninja').read_text(encoding='utf-8')
objects=next(l for l in ninja.splitlines() if l.startswith('build ra2.exe:')).split('Release ',1)[1].split(' || ',1)[0].split()
libs=next(l for l in ninja.splitlines() if l.startswith('  LINK_LIBRARIES =')).split(' = ',1)[1].split()
oldobj='CMakeFiles\\ra2.dir\\src\\runtime\\movement_fixture.c.obj';assert objects.count(oldobj)==1
objects=[str(S/'truck_movement_fixture.obj') if x==oldobj else x for x in objects]
links=['/nologo','/machine:X86','/subsystem:console','/INCREMENTAL:NO','/BASE:0x60000000','/FIXED:NO','/DYNAMICBASE:NO','/NXCOMPAT','/LARGEADDRESSAWARE','/STACK:0x1000000','/MANIFESTUAC:NO','/out:'+str(S/'truck-fixture-probe.exe'),'/pdb:'+str(S/'truck-fixture-probe.pdb')]+objects+libs
(S/'truck-fixture-build-arguments.json').write_text(json.dumps(dict(compile=args,link=links),ensure_ascii=False,indent=2),encoding='utf-8')
(S/'truck-fixture-recipe.json').write_text(json.dumps(dict(production_sha256=hashlib.sha256((R/'ra2/build-original-c/ra2.exe').read_bytes()).hexdigest(),changed_object=oldobj,source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),default_rules=True,blocker_type='TRUCKA',occupied_cells='preserve and report',explicit_rebuild_for_radius_2_or_3=False),indent=2),encoding='utf-8')
print('Independent TRUCKA fixture recipe created',len(objects),'objects')
