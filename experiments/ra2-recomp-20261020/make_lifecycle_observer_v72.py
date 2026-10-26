"""Independent readonly health-result and Tag event observation; no product instrumentation."""
from combat_batch_v72 import *
import shlex
def previous_extend(t):
    marker='static void *health_trampoline;'
    assert t.count(marker)==1
    t=t.replace(marker,'''static unsigned death_depth;
static uint32_t death_ids[128],death_returns[128],death_return_target;
static void *tag_event_trampoline;
static void health_return_hook(void);
'''+marker)
    marker='    int32_t health=I32(actor+0x6C);';assert t.count(marker)==1
    t=t.replace(marker,'''    if(death_depth>=128)fail("health observer nesting");
    death_ids[death_depth]=U32(actor+0x10);death_returns[death_depth]=U32(stack);++death_depth;
    if(original_mode)*(uint32_t *)(uintptr_t)stack=(uint32_t)(uintptr_t)health_return_hook;
    int infantry=U32(actor)==0x7A3540;
    fprintf(state_file,"{\\"kind\\":\\"fixture-death-entry\\",\\"frame\\":%u,\\"id\\":%u,\\"health\\":%d,\\"active\\":%u,\\"has_tag\\":%u,\\"special_kind\\":%d,\\"special_applied\\":%d}\\n",U32(FRAME_ADDRESS),U32(actor+0x10),I32(actor+0x6C),U8(actor+0x7D),U32(actor+0x34)!=0,infantry?U8(U32(actor+0x5A8)+0xC00):-1,infantry?U8(actor+0x5C3):-1);
'''+marker)
    marker='static void health_trace(uint32_t va)';assert t.count(marker)==1
    code=r'''
static uint32_t health_end(uint32_t result)
{
    if(!death_depth)return 0;
    --death_depth;uint32_t id=death_ids[death_depth],p=find_object(id);int infantry=p && U32(p)==0x7A3540;
    fprintf(state_file,"{\"kind\":\"fixture-death-result\",\"frame\":%u,\"id\":%u,\"result\":%u,\"present\":%u,\"health\":%d,\"active\":%u,\"special_applied\":%d}\n",U32(FRAME_ADDRESS),id,result,p!=0,p?I32(p+0x6C):0,p?U8(p+0x7D):0,infantry?U8(p+0x5C3):-1);
    return death_returns[death_depth];
}
static void event_entry(uint32_t stack)
{
    if(!state_file || !started)return;
    uint32_t actor=U32(stack+8),source=U32(stack+20);
    fprintf(state_file,"{\"kind\":\"fixture-tag-event\",\"frame\":%u,\"event\":%u,\"id\":%u,\"source\":%u}\n",U32(FRAME_ADDRESS),U32(stack+4),actor?U32(actor+0x10):0,source?U32(source+0x10):0);
}
void observed_health_original(void);
void WaveClass__virtual_86(void){observed_health_original();health_end(g_eax);}
static __declspec(naked) void health_return_hook(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push dword ptr [ebp+28]
        call health_end
        add esp,4
        mov death_return_target,eax
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [death_return_target]
    }
}
static __declspec(naked) void tag_event_hook(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        lea eax,[ebp+36]
        push eax
        call event_entry
        add esp,4
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [tag_event_trampoline]
    }
}
'''
    t=t.replace(marker,code+'\n'+marker)
    marker='    if(!original_mode && va==0x5D3D20)health_entry(g_ecx,g_esp);';assert t.count(marker)==1
    t=t.replace(marker,marker+'\n    if(!original_mode && va==0x6B3DF0)event_entry(g_esp);')
    marker='    original_mode = 1;';assert t.count(marker)==1
    t=t.replace(marker,marker+'\n    static const uint8_t tag_event_bytes[]={0x51,0x53,0x55,0x8B,0xE9};\n    install_hook(0x6B3DF0,tag_event_bytes,sizeof(tag_event_bytes),tag_event_hook,&tag_event_trampoline);')
    return t
LIFECYCLE_CODE='\nstatic void lifecycle_entry(uint32_t va,uint32_t actor)\n{\n    if(!state_file || !started)return;\n    if(va==0x6ECF10){if(!U32(0xAC0CE8))return;actor=0;}\n    fprintf(state_file,"{\\"kind\\":\\"fixture-lifecycle\\",\\"frame\\":%u,\\"address\\":%u,\\"id\\":%u,\\"health\\":%d,\\"active\\":%u,\\"queued\\":%u}\\n",U32(FRAME_ADDRESS),va,actor?U32(actor+0x10):0,actor?I32(actor+0x6C):0,actor?U8(actor+0x7D):0,U32(0xAC0CE8));\n}\nstatic void *life_unit_trampoline;\nstatic __declspec(naked) void life_unit_hook(void)\n{\n    __asm {\n        pushfd\n        pushad\n        mov ebp,esp\n        sub esp,528\n        and esp,-16\n        fxsave [esp]\n        push dword ptr [ebp+24]\n        push 06FCA30h\n        call lifecycle_entry\n        add esp,8\n        fxrstor [esp]\n        mov esp,ebp\n        popad\n        popfd\n        jmp dword ptr [life_unit_trampoline]\n    }\n}\nstatic void *life_infantry_trampoline;\nstatic __declspec(naked) void life_infantry_hook(void)\n{\n    __asm {\n        pushfd\n        pushad\n        mov ebp,esp\n        sub esp,528\n        and esp,-16\n        fxsave [esp]\n        push dword ptr [ebp+24]\n        push 04FFB70h\n        call lifecycle_entry\n        add esp,8\n        fxrstor [esp]\n        mov esp,ebp\n        popad\n        popfd\n        jmp dword ptr [life_infantry_trampoline]\n    }\n}\nstatic void *life_foot_trampoline;\nstatic __declspec(naked) void life_foot_hook(void)\n{\n    __asm {\n        pushfd\n        pushad\n        mov ebp,esp\n        sub esp,528\n        and esp,-16\n        fxsave [esp]\n        push dword ptr [ebp+24]\n        push 04CCE40h\n        call lifecycle_entry\n        add esp,8\n        fxrstor [esp]\n        mov esp,ebp\n        popad\n        popfd\n        jmp dword ptr [life_foot_trampoline]\n    }\n}\nstatic void *life_object_trampoline;\nstatic __declspec(naked) void life_object_hook(void)\n{\n    __asm {\n        pushfd\n        pushad\n        mov ebp,esp\n        sub esp,528\n        and esp,-16\n        fxsave [esp]\n        push dword ptr [ebp+24]\n        push 05D4E90h\n        call lifecycle_entry\n        add esp,8\n        fxrstor [esp]\n        mov esp,ebp\n        popad\n        popfd\n        jmp dword ptr [life_object_trampoline]\n    }\n}\nstatic void *life_drain_trampoline;\nstatic __declspec(naked) void life_drain_hook(void)\n{\n    __asm {\n        pushfd\n        pushad\n        mov ebp,esp\n        sub esp,528\n        and esp,-16\n        fxsave [esp]\n        push dword ptr [ebp+24]\n        push 06ECF10h\n        call lifecycle_entry\n        add esp,8\n        fxrstor [esp]\n        mov esp,ebp\n        popad\n        popfd\n        jmp dword ptr [life_drain_trampoline]\n    }\n}\nstatic void *life_unitdelete_trampoline;\nstatic __declspec(naked) void life_unitdelete_hook(void)\n{\n    __asm {\n        pushfd\n        pushad\n        mov ebp,esp\n        sub esp,528\n        and esp,-16\n        fxsave [esp]\n        push dword ptr [ebp+24]\n        push 070A330h\n        call lifecycle_entry\n        add esp,8\n        fxrstor [esp]\n        mov esp,ebp\n        popad\n        popfd\n        jmp dword ptr [life_unitdelete_trampoline]\n    }\n}\nstatic void *life_infdelete_trampoline;\nstatic __declspec(naked) void life_infdelete_hook(void)\n{\n    __asm {\n        pushfd\n        pushad\n        mov ebp,esp\n        sub esp,528\n        and esp,-16\n        fxsave [esp]\n        push dword ptr [ebp+24]\n        push 0509810h\n        call lifecycle_entry\n        add esp,8\n        fxrstor [esp]\n        mov esp,ebp\n        popad\n        popfd\n        jmp dword ptr [life_infdelete_trampoline]\n    }\n}\n'
LIFECYCLE_INSTALL='\n    static const uint8_t life_unit_bytes[]={0x83,0xEC,0x28,0x53,0x55};\n    install_hook(0x6FCA30,life_unit_bytes,sizeof(life_unit_bytes),life_unit_hook,&life_unit_trampoline);\n    static const uint8_t life_infantry_bytes[]={0x83,0xEC,0x3C,0x53,0x55};\n    install_hook(0x4FFB70,life_infantry_bytes,sizeof(life_infantry_bytes),life_infantry_hook,&life_infantry_trampoline);\n    static const uint8_t life_foot_bytes[]={0x56,0x8B,0xF1,0x8B,0x8E,0x30,0x02,0x00,0x00};\n    install_hook(0x4CCE40,life_foot_bytes,sizeof(life_foot_bytes),life_foot_hook,&life_foot_trampoline);\n    static const uint8_t life_object_bytes[]={0x56,0x8B,0xF1,0x8B,0x4E,0x38};\n    install_hook(0x5D4E90,life_object_bytes,sizeof(life_object_bytes),life_object_hook,&life_object_trampoline);\n    static const uint8_t life_drain_bytes[]={0x51,0xA1,0xE8,0x0C,0xAC,0x00};\n    install_hook(0x6ECF10,life_drain_bytes,sizeof(life_drain_bytes),life_drain_hook,&life_drain_trampoline);\n    if(U32(0x7ADE18)!=0x70A330)fail("destructor vtable signature");\n    life_unitdelete_trampoline=(void *)0x70A330;*(uint32_t *)(uintptr_t)0x7ADE18=(uint32_t)(uintptr_t)life_unitdelete_hook;\n    if(U32(0x7A3560)!=0x509810)fail("destructor vtable signature");\n    life_infdelete_trampoline=(void *)0x509810;*(uint32_t *)(uintptr_t)0x7A3560=(uint32_t)(uintptr_t)life_infdelete_hook;'
LIFECYCLE_POINTS=[7326256, 5241712, 5033536, 6114960, 7261968, 7381808, 5281808]
def extend(t):
    t=previous_extend(t)
    marker='static void health_trace(uint32_t va)';assert t.count(marker)==1
    t=t.replace(marker,LIFECYCLE_CODE+'\n'+marker)
    marker='    if(!original_mode && va==0x5D3D20)health_entry(g_ecx,g_esp);';assert t.count(marker)==1
    t=t.replace(marker,marker+'\n    if(!original_mode && ('+' || '.join('va==0x%X'%a for a in LIFECYCLE_POINTS)+'))lifecycle_entry(va,g_ecx);')
    marker='    original_mode = 1;';assert t.count(marker)==1
    t=t.replace(marker,marker+LIFECYCLE_INSTALL)
    return t

source=(R/'make_combat_observer_v69.py').read_text(encoding='utf-8').replace('from combat_batch_v69 import *','from combat_batch_v72 import *').replace("p=S/'combat_observer.c'","t=extend(t)\np=S/'combat_observer.c'")
exec(compile(source,str(R/'make_combat_observer_v69.py'),'exec'),globals())
args=read(S/'observer-build-arguments.json');chunk=R/'ra2/src/recomp/gen_game/recomp_0029.c';body=chunk.read_bytes();needle=b'void WaveClass__virtual_86(void) {';assert body.count(needle)==1
p=S/'observer-build/death_generated.c';p.parent.mkdir(exist_ok=True)
if p.exists():assert '--relink' in sys.argv
p.write_bytes(body.replace(needle,b'void observed_health_original(void) {'))
entry=next(e for e in read(R/'ra2/build-original-c/compile_commands.json') if Path(e['file']).name=='recomp_0029.c')
a=[x.strip('"') for x in shlex.split(entry['command'],posix=False)][1:]
a=[('/Fo'+str(S/'death_generated.obj')) if x.startswith('/Fo') else ('/Fd'+str(S/'death_generated.pdb')) if x.startswith('/Fd') else str(p) if x.replace('\\','/').endswith('/gen_game/recomp_0029.c') else x for x in a]+['/I'+str(R/'ra2/src/recomp/gen_game'),'/utf-8']
args['compiles'].append(a);target='CMakeFiles\\ra2.dir\\src\\recomp\\gen_game\\recomp_0029.c.obj';assert args['link'].count(target)==1
args['link']=[str(S/'death_generated.obj') if x==target else x for x in args['link']]
(S/'observer-build-arguments.json').write_text(json.dumps(args,indent=2)+'\n',encoding='utf-8')
original=R/'evidence/combat-state-v1/combat_command.c';p=S/'combat_command.c'
if p.exists():assert p.read_bytes()==original.read_bytes()
else:p.write_bytes(original.read_bytes())
ca=dict(compiles=[[x.replace('combat_observer','combat_command') for x in args['compiles'][0]]],link=[target if x==str(S/'death_generated.obj') else x.replace('combat_observer','combat_command').replace('combat-observer','combat-command') for x in args['link']])
(S/'command-build-arguments.json').write_text(json.dumps(ca,indent=2)+'\n',encoding='utf-8')
for kind in ['observer','command']:
    t=(R/'build-combat-observer-v69.ps1').read_text(encoding='utf-8').replace('combat-state-v1','combat-state-v4').replace('observer-build-arguments',kind+'-build-arguments')
    p=R/f'build-combat-{kind}-v72.ps1'
    if p.exists():assert p.read_text(encoding='utf-8')==t
    else:p.write_text(t,encoding='utf-8',newline='\n')
    t=(R/'run_combat_observer_v69.py').read_text(encoding='utf-8').replace('combat-state-v1','combat-state-v4').replace('combat-observer.exe','combat-'+kind+'.exe')
    t=t.replace("source=(R/'run_fixture_comparison.py').read_text(encoding='utf-8')","from lifecycle_fixture_v72 import fixture_source\nsource=fixture_source()")
    p=R/f'run_combat_{kind}_v72.py'
    if p.exists():assert p.read_text(encoding='utf-8')==t
    else:p.write_text(t,encoding='utf-8',newline='\n')
print(dict(passed=True,health_result_and_tag_event_observed=True,production_sources_changed=False))
