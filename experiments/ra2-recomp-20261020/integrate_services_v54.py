"""Two reversible stages in the existing path-preparation unit."""
from run_batch_v54 import *
p=R/'ra2/src/gameplay/ground_path_prepare.c';name=sys.argv[1];t=p.read_text(encoding='utf-8')
if name=='levels':
 assert sha(p)==sha(S/'baseline/ra2/src/gameplay/ground_path_prepare.c')
 a=t.index('    int32_t kind = v->owner_kind');b=t.index('    type = v->owner_type(v->context);\n    *p->movement_zone',a);c=t.index('\n    if (p->start->x',b)
 level=t[a:b].replace('v->cell(v->context, p->target_reference, &target)','v->cell(v->context, p->target_reference, target)').replace('v->cell(v->context, p->start_reference, &start)','v->cell(v->context, p->start_reference, start)').replace('target.ground_level','target->ground_level').replace('target.has_bridge','target->has_bridge').replace('start.ground_level','start->ground_level').replace('start.has_bridge','start->has_bridge')
 root=t[b:c].replace('    type = v->owner_type(v->context);','    Ra2PathOwnerType type = v->owner_type(v->context);',1)
 helpers='''static void resolve_bridge_levels(Ra2PathPreparation *p,
    const Ra2PathPreparationServices *v, Ra2PathCell *start, Ra2PathCell *target)
{
    /* 保留校验时的格数据；后续重复读取的返回值原来就不作分支判断。 */
'''+level+'''}

static void create_root_state(Ra2PathPreparation *p, const Ra2PathPreparationServices *v)
{
    /* 第二次类型查询与区域快照必须先于根节点服务；同格判断仍在创建根之后。 */
'''+root+'''
}

'''
 t=t[:a]+'''    resolve_bridge_levels(p, v, &start, &target);
    create_root_state(p, v);
'''+t[c:]
 t=t.replace('Ra2PathPreparationResult ra2_path_prepare(',helpers+'Ra2PathPreparationResult ra2_path_prepare(',1)
 # The trailing owner-kind query retains its independent local after the split.
 t=t.replace('    kind = v->owner_kind(v->context);\n    p->continue_at_blocked_goal','    int32_t kind = v->owner_kind(v->context);\n    p->continue_at_blocked_goal')
 t=t.replace('    type = v->owner_type(v->context);\n    p->ignore_soft_obstacles','    Ra2PathOwnerType type = v->owner_type(v->context);\n    p->ignore_soft_obstacles')
elif name=='exclusions':
 assert 'resolve_bridge_levels' in t and 'seed_start_exclusions' not in t
 a=t.index('    if (*p->obstacle_mode)');b=t.index('    int32_t kind = v->owner_kind(v->context);\n    p->continue_at_blocked_goal',a)
 block=t[a:b].replace('v->cell(v->context, p->start_reference, &start)','v->cell(v->context, p->start_reference, start)').replace('exclude_cell(p, &start, start.ground_level)','exclude_cell(p, start, start->ground_level)')
 helper='''static void seed_start_exclusions(Ra2PathPreparation *p,
    const Ra2PathPreparationServices *v, Ra2PathCell *start)
{
    /* 根节点回调之后才读取障碍模式、类型和朝向；每次仍读取实时context。 */
'''+block+'''}

'''
 t=t[:a]+'    seed_start_exclusions(p, v, &start);\n'+t[b:]
 t=t.replace('Ra2PathPreparationResult ra2_path_prepare(',helper+'Ra2PathPreparationResult ra2_path_prepare(',1)
else:raise ValueError(name)
eol=b'\r\n' if b'\r\n' in p.read_bytes() else b'\n';p.write_bytes(t.encode('utf-8').replace(b'\n',eol))
print(dict(passed=True,part=name,sha256=sha(p)))
