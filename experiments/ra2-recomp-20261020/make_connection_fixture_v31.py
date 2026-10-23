"""Ten diagnostic object replacements; production recorder and comparator unchanged."""
from pathlib import Path
import hashlib,json,shlex
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v31'
t=(R/'ra2/src/runtime/movement_fixture.c').read_text(encoding='utf-8')
marker='void ra2_movement_fixture_tick(uint32_t frame, FILE *output, int original_mode)\n{'
assert t.count(marker)==1
t=t.replace(marker,(S/'connection_observer.c').read_text(encoding='utf-8')+'\n'+marker+'\n    connection_tick(output,original_mode);')
(S/'connection_movement_fixture.c').write_text(t,encoding='utf-8',newline='\n')
t=(R/'ra2/src/runtime/ground_remainder_bridge.c').read_text(encoding='utf-8')
t='extern void __cdecl ra2_internal_observe(unsigned drive,unsigned unit,unsigned stage,int x,int y);\nextern void __cdecl ra2_connection_observe(unsigned drive, unsigned stage);\n'+t
marker='MEM8(owner(c) + 0x575) = 0;';assert t.count(marker)==1
t=t.replace(marker,marker+' ra2_connection_observe(c->drive,0);')
marker='MEM8(c->drive + 0x63) = 1;';assert t.count(marker)==1
t=t.replace(marker,marker+' ra2_connection_observe(c->drive,1);')
marker='c.result = (int32_t)g_eax;';assert t.count(marker)==1
t=t.replace(marker,marker+' if(entry==2)ra2_internal_observe(c.drive,0,15,0,0);')
(S/'connection_remainder_bridge.c').write_text(t,encoding='utf-8',newline='\n')
t=(R/'ra2/src/runtime/ground_tube_state_bridge.c').read_text(encoding='utf-8')
t='extern void __cdecl ra2_internal_observe(unsigned drive,unsigned unit,unsigned stage,int x,int y);\nextern void __cdecl ra2_connection_observe(unsigned drive, unsigned stage);\n'+t
for name,stage in [('place_exit',2),('begin',3)]:
 marker='static void '+name+'(void *opaque)\n{TubeContext *c=opaque;';assert t.count(marker)==1
 t=t.replace(marker,marker+f'ra2_connection_observe(MEM32(c->unit+0x564)-4,{stage});')
(S/'connection_tube_state_bridge.c').write_text(t,encoding='utf-8',newline='\n')
t=(R/'ra2/src/runtime/ground_progress_bridge.c').read_text(encoding='utf-8')
t='extern void __cdecl ra2_internal_observe(unsigned drive,unsigned unit,unsigned stage,int x,int y);\nextern void __cdecl ra2_connection_observe(unsigned drive, unsigned stage);\n'+t
marker='ProgressContext c={0};c.frame=g_esp;c.unit=g_esi;c.approach=g_edi;';assert t.count(marker)==1
t=t.replace(marker,marker+'ra2_connection_observe(MEM32(c.unit+0x564)-4,entry==0?4:entry==1?5:6);')
(S/'connection_progress_bridge.c').write_text(t,encoding='utf-8',newline='\n')
t=(R/'ra2/src/runtime/ground_travel_bridge.c').read_text(encoding='utf-8')
t='extern void __cdecl ra2_internal_observe(unsigned drive,unsigned unit,unsigned stage,int x,int y);\nextern void __cdecl ra2_connection_observe(unsigned drive, unsigned stage);\n'+t
marker='c.frame=g_esp;c.unit=g_esi;c.route=g_ebp;c.approach=g_edi;';assert t.count(marker)==1
t=t.replace(marker,marker+'ra2_connection_observe(MEM32(c.unit+0x564)-4,entry==0?7:entry==1?8:9);')
marker='c.frame=g_esp;c.drive=g_ebp;g_esp=c.frame-0x100;';assert t.count(marker)==1
t=t.replace(marker,'c.frame=g_esp;c.drive=g_ebp;if(entry==0)ra2_internal_observe(c.drive,0,10,0,0);g_esp=c.frame-0x100;')
(S/'connection_travel_bridge.c').write_text(t,encoding='utf-8',newline='\n')

t=(R/'ra2/src/runtime/ground_advance_bridge.c').read_text(encoding='utf-8');t='extern void __cdecl ra2_internal_observe(unsigned drive,unsigned unit,unsigned stage,int x,int y);\n'+t
marker='    Ra2WorldPoint result=read_point(engine_call(0x4A4740,c->drive,args,3));';assert t.count(marker)==1
t=t.replace(marker,'    ra2_internal_observe(c->drive,0,previous?11:10,0,0);\n'+marker+'\n    if(!previous)ra2_internal_observe(c->drive,0,12,result.x,result.y);')
marker='static Ra2WorldPoint raw_position(void *opaque)\n{ return read_point(owner(opaque)+0x88); }';assert t.count(marker)==1
t=t.replace(marker,'static Ra2WorldPoint raw_position(void *opaque)\n{ ra2_internal_observe(((AdvanceContext *)opaque)->drive,0,16,0,0); return read_point(owner(opaque)+0x88); }')
(S/'connection_advance_bridge.c').write_text(t,encoding='utf-8',newline='\n')
t=(R/'ra2/src/runtime/ground_joint_bridge.c').read_text(encoding='utf-8');t='extern void __cdecl ra2_internal_observe(unsigned drive,unsigned unit,unsigned stage,int x,int y);\n'+t
marker='    if(!entry){';assert t.count(marker)==1
t=t.replace(marker,marker+'ra2_internal_observe(c.drive,0,12,(int)g_ecx,(int)g_edi);')
marker='    Ra2TemplatePassageServices s=';assert t.count(marker)==1
t=t.replace(marker,'    ra2_internal_observe(c.drive,0,13,0,0);\n'+marker)
marker='    Ra2PassageEntryServices s=';assert t.count(marker)==1
t=t.replace(marker,'    ra2_internal_observe(0,c.unit,14,0,0);\n'+marker)
(S/'connection_joint_bridge.c').write_text(t,encoding='utf-8',newline='\n')

t=(R/'ra2/src/runtime/ground_entry_bridge.c').read_text(encoding='utf-8');t='extern void __cdecl ra2_internal_observe(unsigned drive,unsigned unit,unsigned stage,int x,int y);\n'+t
marker='    EntryContext *c=opaque; write_state(c,s);';assert t.count(marker)==2
# Only check_placement is the native 70323E boundary, not base_passage.
start=t.index('static int32_t check_placement(');end=t.index('static int32_t query(',start)
piece=t[start:end].replace(marker,'    EntryContext *c=opaque; ra2_internal_observe(0,c->owner,14,0,0); write_state(c,s);')
t=t[:start]+piece+t[end:];(S/'connection_entry_bridge.c').write_text(t,encoding='utf-8',newline='\n')
t=(R/'ra2/src/runtime/ground_prepare_bridge.c').read_text(encoding='utf-8');t='extern void __cdecl ra2_internal_observe(unsigned drive,unsigned unit,unsigned stage,int x,int y);\n'+t
marker='static int32_t segment_classify_cell(void *opaque, Ra2GroundCell cell, int32_t direction, int32_t reference_level)\n{\n    PrepareContext *context = opaque;';assert t.count(marker)==1
t=t.replace(marker,marker+'\n    ra2_internal_observe(context->drive,0,13,0,0);')
start=t.index('static int32_t segment_classify_cell(');end=t.index('uint32_t ra2_ground_prepare_segment_bridge',start)
piece=t[start:end];marker='    return passage;';assert piece.count(marker)==1
piece=piece.replace(marker,'    ra2_internal_observe(context->drive,0,17,0,0);\n'+marker)
t=t[:start]+piece+t[end:]
(S/'connection_prepare_bridge.c').write_text(t,encoding='utf-8',newline='\n')
t=(R/'ra2/src/runtime/ground_overlap_bridge.c').read_text(encoding='utf-8')
t='#include <intrin.h>\nextern void __cdecl ra2_internal_observe(unsigned drive,unsigned unit,unsigned stage,int x,int y);\nextern void __cdecl ra2_overlap_route(unsigned site,unsigned entry);\nextern void __cdecl ra2_chain_observe(unsigned unit,unsigned cell,unsigned frame);\n'+t
marker='    uint32_t frame = g_esp;';assert t.count(marker)==2
start=t.index('uint32_t ra2_ground_template_transition_bridge(');end=t.index('uint32_t ra2_ground_object_chain_bridge(',start)
piece=t[start:end].replace(marker,marker+'\n    ra2_internal_observe(g_ebp,0,entry?17:16,0,0); ra2_overlap_route(entry?17:16,(unsigned)(uintptr_t)_ReturnAddress());')
t=t[:start]+piece+t[end:]
start=t.index('uint32_t ra2_ground_object_chain_bridge(');end=t.index('void ra2_ground_passage_return_bridge(',start)
piece=t[start:end].replace(marker,marker+'\n    if(entry)ra2_internal_observe(0,g_ebp,19,0,0);else ra2_chain_observe(g_ebp,g_ebx,frame); ra2_overlap_route(entry?19:18,(unsigned)(uintptr_t)_ReturnAddress());')
t=t[:start]+piece+t[end:]
(S/'connection_overlap_bridge.c').write_text(t,encoding='utf-8',newline='\n')

# Main Advance's new layer service observes before the first level query.
t=(S/'connection_advance_bridge.c').read_text(encoding='utf-8')
t+='\nvoid __cdecl ra2_layer_from_context(void *opaque)\n{ ra2_internal_observe(((AdvanceContext *)opaque)->drive,0,20,0,0); }\n'
(S/'connection_advance_bridge.c').write_text(t,encoding='utf-8',newline='\n')
t=(R/'ra2/src/gameplay/ground_advance.c').read_text(encoding='utf-8')
t='extern void __cdecl ra2_layer_from_context(void *opaque);\n'+t
marker='    return services->query(services->context, RA2_ADVANCE_CELL_LEVEL, context->cells[next]);'
assert t.count(marker)==1
t=t.replace(marker,'    if(!next)ra2_layer_from_context(services->context);\n'+marker)
(S/'connection_advance.c').write_text(t,encoding='utf-8',newline='\n')
t=(R/'ra2/src/runtime/ground_objects_bridge.c').read_text(encoding='utf-8')
t='extern void __cdecl ra2_internal_observe(unsigned drive,unsigned unit,unsigned stage,int x,int y);\n'+t
marker='        case RA2_OBJECT_OWNER_ACCEPTS_LINK:'
assert t.count(marker)==1
t=t.replace(marker,marker+'\n            ra2_internal_observe(0,c->owner,21,0,0);')
t='extern void __cdecl ra2_enemy_visit(unsigned unit,unsigned object);\nextern void __cdecl ra2_object_visit(unsigned unit,unsigned object);\n'+t
t=t.replace('    if(entry==0 && c.owner!=c.object) ra2_state_movement_audit', '    if(entry==0 && c.owner!=c.object) ra2_object_visit(c.owner,c.object);\n    if(entry==0 && c.owner!=c.object) ra2_state_movement_audit')
t=t.replace('    if(entry==0 && c.owner!=c.object) ra2_object_visit','    if(entry==2)ra2_enemy_visit(c.owner,c.object);\n    if(entry==0 && c.owner!=c.object) ra2_object_visit')
(S/'connection_objects_bridge.c').write_text(t,encoding='utf-8',newline='\n')

commands=json.loads((R/'ra2/build-original-c/compile_commands.json').read_text(encoding='utf-8'))
compiles=[];replacements={}
for original,helper in [('movement_fixture','connection_movement_fixture'),('ground_remainder_bridge','connection_remainder_bridge'),('ground_tube_state_bridge','connection_tube_state_bridge'),('ground_progress_bridge','connection_progress_bridge'),('ground_travel_bridge','connection_travel_bridge'),('ground_advance_bridge','connection_advance_bridge'),('ground_joint_bridge','connection_joint_bridge'),('ground_entry_bridge','connection_entry_bridge'),('ground_prepare_bridge','connection_prepare_bridge'),('ground_overlap_bridge','connection_overlap_bridge'),('ground_advance','connection_advance'),('ground_objects_bridge','connection_objects_bridge')]:
 entry=next(e for e in commands if e['file'].replace('\\','/').endswith('/'+original+'.c'))
 args=[a.strip('"') for a in shlex.split(entry['command'],posix=False)][1:]
 args=[('/Fo'+str(S/(helper+'.obj'))) if a.startswith('/Fo') else ('/Fd'+str(S/(helper+'.pdb'))) if a.startswith('/Fd') else str(S/(helper+'.c')) if a.replace('\\','/').endswith('/src/'+('gameplay' if original=='ground_advance' else 'runtime')+'/'+original+'.c') else a for a in args]
 compiles.append(args);replacements['CMakeFiles\\ra2.dir\\src\\'+('gameplay' if original=='ground_advance' else 'runtime')+'\\'+original+'.c.obj']=str(S/(helper+'.obj'))
ninja=(R/'ra2/build-original-c/build.ninja').read_text(encoding='utf-8')
objects=next(l for l in ninja.splitlines() if l.startswith('build ra2.exe:')).split('Release ',1)[1].split(' || ',1)[0].split()
assert all(objects.count(o)==1 for o in replacements)
libs=next(l for l in ninja.splitlines() if l.startswith('  LINK_LIBRARIES =')).split(' = ',1)[1].split()
links=['/nologo','/machine:X86','/subsystem:console','/INCREMENTAL:NO','/BASE:0x60000000','/FIXED:NO','/DYNAMICBASE:NO','/NXCOMPAT','/LARGEADDRESSAWARE','/STACK:0x1000000','/MANIFESTUAC:NO','/MAP:'+str(S/'connection-fixture.map'),'/out:'+str(S/'connection-fixture-probe.exe')]+[replacements.get(o,o) for o in objects]+libs
(S/'connection-fixture-build-arguments.json').write_text(json.dumps(dict(compiles=compiles,link=links),indent=2),encoding='utf-8')
t=(R/'build-truck-actor-fixture-v31.ps1').read_text(encoding='utf-8').replace('truck-actor-fixture-build-arguments.json','connection-fixture-build-arguments.json')
t=t.replace('$taskCompile=@($taskArguments.compile);& cl @taskCompile\n    if($LASTEXITCODE){throw \'TRUCKA fixture compile failed\'}',"foreach($taskC in $taskArguments.compiles){$taskCompile=@($taskC);& cl @taskCompile;if($LASTEXITCODE){throw 'Connection observer compile failed'}}")
(R/'build-connection-fixture-v31.ps1').write_text(t,encoding='utf-8',newline='\n')
print('Connection observer replaces exactly twelve diagnostic objects; production sha256',hashlib.sha256((R/'ra2/build-original-c/ra2.exe').read_bytes()).hexdigest())
