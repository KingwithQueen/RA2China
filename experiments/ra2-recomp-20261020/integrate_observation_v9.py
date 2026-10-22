from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'ra2/src/runtime/state_trace.c';t=p.read_text(encoding='utf-8')
assert 'continuation_classified_trampoline' not in t
t=t.replace('static void *advance_sample_trampoline;','static void *advance_sample_trampoline;\nstatic void *continuation_classified_trampoline,*followup_candidate_trampoline,*followup_search_trampoline;')
t=t.replace('\\"schema\\":10','\\"schema\\":11').replace('stage <= 20','stage <= 23')
old='value = stage==16 || stage==19 || stage==20 ? (int32_t)object : stage==17 ? I32(actor+0x4D4) : 0;'
assert old in t
t=t.replace(old,'value = stage==16 || stage==19 || stage==20 || stage==21 || stage==23 ? (int32_t)object : stage==17 || stage==22 ? I32(actor+0x4D4) : 0;')
t=t.replace('stage==16 || stage==17 || stage==20 ?','stage==16 || stage==17 || stage==20 || stage==21 ?')
start=t.index('static __declspec(naked) void advance_sample_audit_hook')
hooks=''
for name,stage,use_eax in [('continuation_classified',21,True),('followup_candidate',22,False),('followup_search',23,True)]:
    object_line='push dword ptr [ebp + 28]' if use_eax else 'push 0'
    hooks+=f'''static __declspec(naked) void {name}_audit_hook(void)
{{
    __asm
    {{
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        {object_line}
        push 0
        push dword ptr [ebp + 8]
        push {stage}
        call ra2_state_movement_audit
        add esp,16
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [{name}_trampoline]
    }}
}}

'''
t=t[:start]+hooks+t[start:]
needle='        static const uint8_t advance_sample_bytes[]'
assert needle in t
t=t.replace(needle,'''        /* 仅搬移完整且不含相对转移的指令；分类处是原版绝对地址间接跳转。 */
        static const uint8_t continuation_classified_bytes[] = {0xFF,0x24,0x85,0x4C,0x26,0x4A,0x00};
        install_hook(0x4A1CA8,continuation_classified_bytes,sizeof(continuation_classified_bytes),continuation_classified_audit_hook,&continuation_classified_trampoline);
        static const uint8_t followup_candidate_bytes[] = {0x8B,0x4D,0x0C,0x8B,0xB1,0xD4,0x04,0x00,0x00};
        install_hook(0x4A3E79,followup_candidate_bytes,sizeof(followup_candidate_bytes),followup_candidate_audit_hook,&followup_candidate_trampoline);
        static const uint8_t followup_search_bytes[] = {0x8B,0x4D,0x0C,0x8B,0x11};
        install_hook(0x4A3EFB,followup_search_bytes,sizeof(followup_search_bytes),followup_search_audit_hook,&followup_search_trampoline);
'''+needle)
p.write_text(t,encoding='utf-8',newline='\n')
p=ROOT/'ra2/src/runtime/ground_continuation_bridge.c';t=p.read_text(encoding='utf-8')
t=t.replace('#include "ground_continuation_bridge.h"','#include "ground_continuation_bridge.h"\n#include "state_trace.h"')
t=t.replace('static void classified(void *opaque,int32_t result) { (void)opaque;(void)result; }',
    'static void classified(void *opaque,int32_t result)\n{ ContinuationContext *c=opaque;write_state(c);if((uint32_t)result<=6) ra2_state_movement_audit(21,c->drive,0,(uint32_t)result); }')
p.write_text(t,encoding='utf-8',newline='\n')
p=ROOT/'ra2/src/runtime/ground_followup_bridge.c';t=p.read_text(encoding='utf-8')
needle='    Ra2GroundPrepareState state;\n';assert needle in t
t=t.replace(needle,needle+'    int32_t last_followup_distance;\n',1)
needle='    owner_call(context, 0x4B8, arguments, 2);'
assert needle in t
t=t.replace(needle,needle+'\n    ra2_state_movement_audit(22,context->drive,0,0);',1)
needle='    return (int32_t)engine_call(context, 0x41B780, scratch, NULL, 0);'
assert needle in t
t=t.replace(needle,'    context->last_followup_distance=(int32_t)engine_call(context, 0x41B780, scratch, NULL, 0);\n    return context->last_followup_distance;',1)
needle='static int followup_train(void *opaque)\n{\n    FollowupContext *context = opaque;'
assert needle in t
t=t.replace(needle,needle+'\n    ra2_state_movement_audit(23,context->drive,0,(uint32_t)context->last_followup_distance);')
p.write_text(t,encoding='utf-8',newline='\n')
p=ROOT/'evidence/movement-state-v9/continuation_probe.c';t=p.read_text(encoding='utf-8')
t+='\nvoid ra2_state_movement_audit(uint32_t a,uint32_t b,uint32_t c,uint32_t d) { (void)a;(void)b;(void)c;(void)d; }\n'
p.write_text(t,encoding='utf-8',newline='\n')
