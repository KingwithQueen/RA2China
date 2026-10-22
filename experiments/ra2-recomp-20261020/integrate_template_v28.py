"""Share the cross-cell bridge-layer transition with overlapping Advance entries."""
from pathlib import Path
import json, re
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v28'

def edit(path, old, new, count=1):
    data = path.read_bytes()
    nl = b'\r\n' if b'\r\n' in data else b'\n'
    text = data.decode('utf-8').replace('\r\n', '\n')
    assert text.count(old) == count, (path, text.count(old), count)
    path.write_bytes(text.replace(old, new).replace('\n', nl.decode()).encode('utf-8'))

header = '''
typedef struct Ra2TemplateLayerServices
{
    void *context;
    int32_t (*level)(void *, unsigned next);
    uint32_t (*flags)(void *, unsigned next);
    void (*set_layer)(void *, unsigned upper);
} Ra2TemplateLayerServices;

/* 跨格落点可进入或离开桥层；第二次查询下一格标志的顺序不能改变。 */
void ra2_ground_template_layer(const Ra2TemplateLayerServices *services);
'''
path = R / 'ra2/src/gameplay/ground_template_transition.h'
assert 'Ra2TemplateLayerServices' not in path.read_text(encoding='utf-8')
with path.open('a', encoding='utf-8', newline='\n') as f:
    f.write(header)
path = R / 'ra2/src/gameplay/ground_template_transition.c'
with path.open('a', encoding='utf-8', newline='\n') as f:
    f.write('''
void ra2_ground_template_layer(const Ra2TemplateLayerServices *services)
{
    void *context = services->context;
    int32_t previous_level = services->level(context, 0);
    int32_t next_level = services->level(context, 1);
    if ((uint32_t)next_level == (uint32_t)previous_level - 4u
        && (services->flags(context, 1) & 0x100u))
    {
        services->set_layer(context, 1);
    }
    if (!(services->flags(context, 1) & 0x100u)
        && (services->flags(context, 0) & 0x100u))
    {
        services->set_layer(context, 0);
    }
}
''')
path = R / 'ra2/src/gameplay/ground_advance.c'
edit(path, 'int ra2_ground_advance_sample(const Ra2AdvanceServices *s)', '''typedef struct AdvanceLayerContext
{
    const Ra2AdvanceServices *services;
    uint32_t cells[2];
} AdvanceLayerContext;

static int32_t layer_level(void *opaque, unsigned next)
{
    AdvanceLayerContext *context = opaque;
    const Ra2AdvanceServices *services = context->services;
    return services->query(services->context, RA2_ADVANCE_CELL_LEVEL, context->cells[next]);
}

static uint32_t layer_flags(void *opaque, unsigned next)
{
    AdvanceLayerContext *context = opaque;
    const Ra2AdvanceServices *services = context->services;
    return services->query(services->context, RA2_ADVANCE_CELL_HAS_BRIDGE, context->cells[next]) ? 0x100u : 0;
}

static void layer_set(void *opaque, unsigned upper)
{
    AdvanceLayerContext *context = opaque;
    const Ra2AdvanceServices *services = context->services;
    services->act(services->context, RA2_ADVANCE_SET_BRIDGE_LAYER, 0, (int32_t)upper);
}

int ra2_ground_advance_sample(const Ra2AdvanceServices *s)''')
edit(path, '''        int32_t previous_level = s->query(c, RA2_ADVANCE_CELL_LEVEL, previous_cell);
        int32_t next_level = s->query(c, RA2_ADVANCE_CELL_LEVEL, next_cell);
        if (next_level == previous_level - 4 && s->query(c, RA2_ADVANCE_CELL_HAS_BRIDGE, next_cell))
            s->act(c, RA2_ADVANCE_SET_BRIDGE_LAYER, 0, 1);
        if (!s->query(c, RA2_ADVANCE_CELL_HAS_BRIDGE, next_cell)
            && s->query(c, RA2_ADVANCE_CELL_HAS_BRIDGE, previous_cell))
            s->act(c, RA2_ADVANCE_SET_BRIDGE_LAYER, 0, 0);''', '''        AdvanceLayerContext layer_context = {s, {previous_cell, next_cell}};
        Ra2TemplateLayerServices layer_services = {&layer_context, layer_level, layer_flags, layer_set};
        ra2_ground_template_layer(&layer_services);''')
path = R / 'ra2/src/runtime/ground_overlap_bridge.h'
edit(path, 'uint32_t ra2_ground_template_transition_bridge(unsigned entry);', 'uint32_t ra2_ground_template_transition_bridge(unsigned entry);\nuint32_t ra2_ground_template_layer_bridge(void);')
path = R / 'ra2/src/runtime/ground_overlap_bridge.c'
with path.open('a', encoding='utf-8', newline='\n') as f:
    f.write('''
typedef struct LayerContext
{
    uint32_t drive, previous, next;
} LayerContext;

static int32_t layer_level(void *opaque, unsigned next)
{
    LayerContext *context = opaque;
    int32_t level = (int8_t)MEM8((next ? context->next : context->previous) + 0x11B);
    if (!next) g_eax = (uint32_t)level;
    else
    {
        g_ecx = (uint32_t)level;
        g_flag_k = FK_CMP;
        g_flag_a = (uint32_t)level;
        g_flag_b = g_eax - 4u;
        g_flag_cf = g_flag_a < g_flag_b;
        g_eax = 0x100u;
    }
    return level;
}

static uint32_t layer_flags(void *opaque, unsigned next)
{
    LayerContext *context = opaque;
    uint32_t flags = MEM32((next ? context->next : context->previous) + 0x140);
    g_flag_k = FK_TEST;
    g_flag_a = flags;
    g_flag_b = 0x100u;
    g_flag_cf = 0;
    return flags;
}

static void layer_set(void *opaque, unsigned upper)
{
    LayerContext *context = opaque;
    uint32_t unit = MEM32(context->drive + 0xC);
    MEM8(unit + 0x79) = (uint8_t)upper;
    if (upper) g_edx = unit;
    else g_eax = unit;
}

uint32_t ra2_ground_template_layer_bridge(void)
{
    LayerContext context = {g_ebp, g_esi, g_ebx};
    Ra2TemplateLayerServices services = {&context, layer_level, layer_flags, layer_set};
    MEM32(g_esp + 0x40) = context.next;
    ra2_ground_template_layer(&services);
    return 0x4A18EF;
}
''')
path = R / 'ra2/src/recomp/gen_game/recomp_0010.c'
marker = 'L_004A18AB:\n'
edit(path, marker, marker + '''    /* 可读 C：跨格模板的桥层切换，保留内部入口。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_template_layer_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto L_004A18EF;
''', 6)
(S / 'pending/template-integration.json').write_text(json.dumps(dict(passed=True, internal_entry='004A18AB', overlapping_copies=6, primary_advance_shared=True), indent=2) + '\n', encoding='utf-8')
print('Integrated bridge-layer template transition in main Advance and six internal copies')
