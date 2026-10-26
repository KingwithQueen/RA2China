"""Separate fixture/readonly recorder. The production recorder and comparator stay unchanged."""
from combat_batch_v69 import *
import shlex
t=(R/'ra2/src/runtime/state_trace.c').read_text(encoding='utf-8')
t=t.replace('#include "recomp_target.h"','#include "recomp_target.h"\n#include "recomp_types.h"\n#include "recomp_trace.h"')
old='if ((order->mission != 2 && order->mission != 13) || order->x >= 1000 || order->y >= 1000) fail("unsupported mission or cell");';assert t.count(old)==1
t=t.replace(old,'if ((order->mission != 2 && order->mission != 13 && order->mission != 1 && order->mission != 7) || ((order->mission == 1 || order->mission == 7) ? (!order->x || order->y) : (order->x >= 1000 || order->y >= 1000))) fail("unsupported mission or target");')
marker='    memcpy((void *)(uintptr_t)(0xA32344 + slot * 111), event, sizeof(event));';assert t.count(marker)==1
t=t.replace(marker,'''    if(order->mission==1 || order->mission==7) {
        uint32_t target=find_object(order->x);if(!target)fail("attack/enter target absent");
        uint32_t offset=order->mission==1?0x0E:0x13;
        memcpy(event+offset,&order->x,4);event[offset+4]=0x34;
    }
'''+marker)
marker='void ra2_state_tick(void)';assert t.count(marker)==1
code=r'''
static void *health_trampoline;
static void health_entry(uint32_t actor,uint32_t stack)
{
    if(!state_file || !started || !actor)return;
    int32_t health=I32(actor+0x6C);uint32_t damage=U32(stack+4),warhead=U32(stack+12),attacker=U32(stack+16),kind=U32(actor),type=0;
    if(kind==0x7ADDF8)type=U32(actor+0x5AC);
    else if(kind==0x7A3540)type=U32(actor+0x5A8);
    uint16_t control=g_fpu_cw;
    if(original_mode){__asm fnstcw control}
    fprintf(state_file,"{\"kind\":\"fixture-health-entry\",\"frame\":%u,\"id\":%u,\"health\":%d,\"incoming\":%d,\"distance\":%d,\"warhead\":\"%.24s\",\"attacker\":%u,\"ignore_defenses\":%u,\"type_flag_203\":%d,\"control\":%u}\n",
        U32(FRAME_ADDRESS),U32(actor+0x10),health,health>0 && damage?I32(damage):0,I32(stack+8),warhead?(char *)(uintptr_t)(warhead+0x24):"",attacker?U32(attacker+0x10):0,U8(stack+20),type?U8(type+0x203):-1,control&0x1F3Fu);
}
static void health_trace(uint32_t va)
{
    if(!original_mode && va==0x5D3D20)health_entry(g_ecx,g_esp);
}
static __declspec(naked) void health_hook(void)
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
        push dword ptr [ebp+24]
        call health_entry
        add esp,8
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [health_trampoline]
    }
}
'''
t=t.replace(marker,code+'\n'+marker)
marker='    started = 1;';assert t.count(marker)==1;t=t.replace(marker,marker+'\n    if(recomp_trace_extra && recomp_trace_extra!=health_trace)fail("unexpected trace observer");\n    recomp_trace_extra=health_trace;')
marker='    original_mode = 1;';assert t.count(marker)==1
t=t.replace(marker,marker+'\n    static const uint8_t health_bytes[]={0x83,0xEC,0x14,0x53,0x55};\n    install_hook(0x5D3D20,health_bytes,sizeof(health_bytes),health_hook,&health_trampoline);')
p=S/'combat_observer.c'
if p.exists():assert '--relink' in sys.argv and p.read_bytes()==t.encode('utf-8')
else:p.write_text(t,encoding='utf-8',newline='\n')
entry=next(x for x in read(R/'ra2/build-original-c/compile_commands.json') if x['file'].replace('\\','/').endswith('/runtime/state_trace.c'))
args=[x.strip('"') for x in shlex.split(entry['command'],posix=False)][1:]
args=[('/Fo'+str(S/'combat_observer.obj')) if a.startswith('/Fo') else ('/Fd'+str(S/'combat_observer.pdb')) if a.startswith('/Fd') else str(p) if a.replace('\\','/').endswith('/runtime/state_trace.c') else a for a in args]+['/I'+str(R/'ra2/src/runtime'),'/utf-8']
ninja=(R/'ra2/build-original-c/build.ninja').read_text(encoding='utf-8');objects=next(l for l in ninja.splitlines() if l.startswith('build ra2.exe:')).split('Release ',1)[1].split(' || ',1)[0].split();target='CMakeFiles\\ra2.dir\\src\\runtime\\state_trace.c.obj';assert objects.count(target)==1
libs=next(l for l in ninja.splitlines() if l.startswith('  LINK_LIBRARIES =')).split(' = ',1)[1].split()
link=['/nologo','/machine:X86','/subsystem:console','/INCREMENTAL:NO','/BASE:0x60000000','/FIXED:NO','/DYNAMICBASE:NO','/NXCOMPAT','/LARGEADDRESSAWARE','/STACK:0x1000000','/MANIFESTUAC:NO','/MAP:'+str(S/'combat-observer.map'),'/out:'+str(S/'combat-observer.exe')]+[str(S/'combat_observer.obj') if x==target else x for x in objects]+libs
out=S/'observer-build-arguments.json'
if out.exists():assert '--relink' in sys.argv;out.write_text(json.dumps(dict(compiles=[args],link=link),indent=2)+'\n',encoding='utf-8')
else:write(out,dict(compiles=[args],link=link))
print(dict(passed=True,source_sha256=sha(p),production_recorder_changed=False,extra_trace_existing_hook_only=True))
