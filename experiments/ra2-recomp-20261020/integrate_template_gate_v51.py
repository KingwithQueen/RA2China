"""Separate the first type gate from the later overlay gate; do not cache live classification."""
from pathlib import Path
p=Path(__file__).resolve().parent/'ra2/src/gameplay/ground_template_transition.c';t=p.read_text(encoding='utf-8')
a=t.index('void ra2_ground_template_gate(');b=t.index('\nvoid ra2_ground_template_layer',a)
t=t[:a]+'''static int clear_type_gate(const Ra2TemplateGateServices *services, void *context)
{
    if (services->classification(context) >= 7) return 0;
    if (!services->type_flag(context, 0)) return 0;
    services->clear_classification(context);
    return 1;
}

static void clear_overlay_gate(const Ra2TemplateGateServices *services, void *context)
{
    /* 第一阶段的类型查询可能改变分类；第二阶段必须重新读取。 */
    int32_t classification = services->classification(context);
    if (classification != 5 && classification != 4) return;
    if (!services->type_flag(context, 1)) return;
    if (services->overlay(context) != 0) return;
    services->clear_classification(context);
}

void ra2_ground_template_gate(const Ra2TemplateGateServices *services)
{
    void *context = services->context;
    if (!clear_type_gate(services, context)) clear_overlay_gate(services, context);
}
''' + t[b:]
p.write_text(t,encoding='utf-8',newline='\n')
