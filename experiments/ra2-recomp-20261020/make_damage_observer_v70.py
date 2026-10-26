"""Read-only entry/result observation; same native command adapter as the accepted parent."""
from combat_batch_v70 import *
import shlex
def extend(t):
    marker='static void *health_trampoline;';assert t.count(marker)==1
    code=r'''
static void *damage_trampoline,*damage_cap_trampoline,*damage_result_trampoline;
static float observed_float(uint32_t at){float v;memcpy(&v,(void *)(uintptr_t)at,4);return v;}
static void damage_entry(int32_t damage,uint32_t warhead,uint32_t stack)
{
    if(!state_file || !started)return;
    uint16_t control=g_fpu_cw;if(original_mode){__asm fnstcw control}
    uint32_t armor=U32(stack+4);double verse=0;
    if(warhead && armor<11)memcpy(&verse,(void *)(uintptr_t)(warhead+0xA0+armor*8),8);
    fprintf(state_file,"{\"kind\":\"fixture-damage-entry\",\"frame\":%u,\"incoming\":%d,\"distance\":%d,\"armor\":%u,\"warhead\":\"%.24s\",\"spread\":%.9g,\"edge\":%.9g,\"verse\":%.17g,\"maximum\":%d,\"control\":%u}\n",
        U32(FRAME_ADDRESS),damage,I32(stack+8),armor,warhead?(char *)(uintptr_t)(warhead+0x24):"",warhead?observed_float(warhead+0x124):0,warhead?observed_float(warhead+0x12C):0,verse,I32(U32(0x839848)+0x1330),control&0x1F3F);
}
static void damage_exit(int32_t damage)
{
    if(state_file && started)fprintf(state_file,"{\"kind\":\"fixture-damage-exit\",\"frame\":%u,\"damage\":%d}\n",U32(FRAME_ADDRESS),damage);
}
void observed_damage_original(void);
void sub_0047E1C0(void)
{
    damage_entry((int32_t)g_ecx,g_edx,g_esp);
    observed_damage_original();
    damage_exit((int32_t)g_eax);
}
static __declspec(naked) void damage_hook(void)
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
        push dword ptr [ebp+20]
        push dword ptr [ebp+24]
        call damage_entry
        add esp,12
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [damage_trampoline]
    }
}
static __declspec(naked) void damage_cap_hook(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push dword ptr [ebp+24]
        call damage_exit
        add esp,4
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [damage_cap_trampoline]
    }
}
static __declspec(naked) void damage_result_hook(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push dword ptr [ebp+28]
        call damage_exit
        add esp,4
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [damage_result_trampoline]
    }
}
'''
    t=t.replace(marker,code+'\n'+marker)
    marker='    original_mode = 1;';assert t.count(marker)==1
    t=t.replace(marker,marker+'''
    static const uint8_t damage_bytes[]={0x83,0xEC,0x0C,0x56,0x8B,0xF1};
    static const uint8_t cap_bytes[]={0x5F,0x8B,0xC1,0x5E,0x83,0xC4,0x0C};
    static const uint8_t result_bytes[]={0x5F,0x5E,0x83,0xC4,0x0C};
    install_hook(0x47E1C0,damage_bytes,sizeof(damage_bytes),damage_hook,&damage_trampoline);
    install_hook(0x47E299,cap_bytes,sizeof(cap_bytes),damage_cap_hook,&damage_cap_trampoline);
    install_hook(0x47E2A5,result_bytes,sizeof(result_bytes),damage_result_hook,&damage_result_trampoline);
''')
    return t
# Inherit the accepted command and health recorder construction without changing production tracing.
script=(R/'make_combat_observer_v69.py').read_text(encoding='utf-8').replace('from combat_batch_v69 import *','from combat_batch_v70 import *')
script=script.replace("p=S/'combat_observer.c'","t=extend(t)\np=S/'combat_observer.c'")
exec(compile(script,str(R/'make_combat_observer_v69.py'),'exec'),globals())
args=read(S/'observer-build-arguments.json')
chunk=R/'ra2/src/recomp/gen_game/recomp_0007.c';source=chunk.read_bytes();needle=b'void sub_0047E1C0(void) {';assert source.count(needle)==1
p=S/'observer-build/damage_generated.c';p.parent.mkdir(exist_ok=True)
if p.exists():assert '--relink' in sys.argv
p.write_bytes(source.replace(needle,b'void observed_damage_original(void) {'))
entry=next(x for x in read(R/'ra2/build-original-c/compile_commands.json') if Path(x['file']).name=='recomp_0007.c')
compile_args=[x.strip('"') for x in shlex.split(entry['command'],posix=False)][1:]
compile_args=[('/Fo'+str(S/'damage_generated.obj')) if a.startswith('/Fo') else ('/Fd'+str(S/'damage_generated.pdb')) if a.startswith('/Fd') else str(p) if a.replace('\\','/').endswith('/gen_game/recomp_0007.c') else a for a in compile_args]+['/I'+str(R/'ra2/src/recomp/gen_game'),'/utf-8']
args['compiles'].append(compile_args);target='CMakeFiles\\ra2.dir\\src\\recomp\\gen_game\\recomp_0007.c.obj';assert args['link'].count(target)==1
args['link']=[str(S/'damage_generated.obj') if a==target else a for a in args['link']]
(S/'observer-build-arguments.json').write_text(json.dumps(args,indent=2)+'\n',encoding='utf-8')
command_source=(O/'combat_command.c').read_bytes();p=S/'combat_command.c'
if p.exists():assert p.read_bytes()==command_source
else:p.write_bytes(command_source)
command_args=dict(compiles=[[a.replace('combat_observer','combat_command') for a in args['compiles'][0]]],link=[target if a==str(S/'damage_generated.obj') else a.replace('combat_observer','combat_command').replace('combat-observer','combat-command') for a in args['link']])
p=S/'command-build-arguments.json';p.write_text(json.dumps(command_args,indent=2)+'\n',encoding='utf-8')
for kind in ['observer','command']:
    text=(R/'build-combat-observer-v69.ps1').read_text(encoding='utf-8').replace('combat-state-v1','combat-state-v2').replace('observer-build-arguments',kind+'-build-arguments')
    p=R/f'build-combat-{kind}-v70.ps1'
    if p.exists():assert p.read_text(encoding='utf-8')==text
    else:p.write_text(text,encoding='utf-8',newline='\n')
    text=(R/'run_combat_observer_v69.py').read_text(encoding='utf-8').replace('combat-state-v1','combat-state-v2').replace('combat-observer.exe','combat-'+kind+'.exe')
    p=R/f'run_combat_{kind}_v70.py'
    if p.exists():assert p.read_text(encoding='utf-8')==text
    else:p.write_text(text,encoding='utf-8',newline='\n')
print(dict(passed=True,damage_entry_and_exit_observed=True,production_sources_changed=False))
