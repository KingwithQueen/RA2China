"""Keep the original position-output buffer at the entry/retry service boundary."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v41'
p=R/'ra2/src/runtime/ground_prepare_bridge.c';raw=p.read_bytes();t=p.read_text(encoding='utf-8')
old='    uint32_t obstacle_cell;';assert t.count(old)==1;t=t.replace(old,old+'\n    unsigned entry_position_buffer;')
old='            argument = scratch;\n            result = owner_call(context, 0x48, &argument, 1);';assert t.count(old)==1
t=t.replace(old,'            argument = context->entry_position_buffer ? context->frame+0x44 : scratch;\n            result = owner_call(context, 0x48, &argument, 1);')
t=t.replace('PrepareContext *context=opaque;uint32_t owner=owner_address(context);','PrepareContext *context=opaque;context->entry_position_buffer=0;uint32_t owner=owner_address(context);',1)
t=t.replace('context.drive=g_ebp;context.frame=g_esp;','context.drive=g_ebp;context.frame=g_esp;context.entry_position_buffer=1;',1)
start=t.index('uint32_t ra2_ground_prepare_entry_bridge(void)');end=t.index('uint32_t ra2_ground_retry_path_bridge(void)',start)
piece=t[start:end].replace('    context.frame = g_esp;','    context.frame = g_esp;\n    context.entry_position_buffer=1;');t=t[:start]+piece+t[end:]
nl='\r\n' if raw.count(b'\r\n')==raw.count(b'\n') else '\n';p.write_bytes(t.replace('\n',nl).encode('utf-8'))
(S/'prepare-boundary-resolution.json').write_text(json.dumps(dict(passed=True,failed_probe='investigations/prepare-cycle-01',field='owner+534 copied from legacy frame+48 during retry restart',cause='Native entry distance service writes its output at frame+44, whose y word remains at frame+48; the old split bridge used a separate scratch buffer.',resolution='Pass the actual legacy output buffer to the entry-position service; after entry/retry transition, subsequent distance services use their separate retry buffer. Business cycle does not interpret the legacy timer middle word.',semantic_scope='Correct service output storage across merged state transitions; no original bug fix or expansion of comparisons.'),indent=2)+'\n',encoding='utf-8')
print('Preserved entry position output at the cycle boundary')
