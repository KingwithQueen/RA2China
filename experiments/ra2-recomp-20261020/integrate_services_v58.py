"""Two reversible local-path service phases; original service expressions retained."""
from run_batch_v58 import *
import re
p=R/'ra2/src/gameplay/ground_path_local.c';part=sys.argv[1];t=p.read_text(encoding='utf-8')
if part=='turns':
 assert sha(p)==sha(S/'baseline/ra2/src/gameplay/ground_path_local.c')
 a=t.index('void ra2_path_find_anchor(');b=t.index('int32_t ra2_path_shorten_turn(',a)
 block=t[a:b]
 for old,new in [('displacement','reverse_delta'),('point','candidate_anchor'),('maximum','maximum_extent'),('retreated','passed_peak'),('backward','reverse_direction')]:
  block=re.sub(r'\b'+old+r'\b',new,block)
 block=block.replace('    Ra2PathPoint reverse_delta=', '    /* 反扫跳过删除槽；方向8在这里仍按低三位回退，不查询特殊连接。 */\n    Ra2PathPoint reverse_delta=',1)
 block=block.replace('                *anchor_index=i+1;', '                /* 先发布索引，再读取偏移并发布上一格锚点，保留原写入顺序。 */\n                *anchor_index=i+1;',1)
 t=t[:a]+block+t[b:]
 a=t.index('        int32_t remaining=pairs*2,level=levels[first_count-pairs];int blocked=0;')
 b=t.index('        if(!blocked) {',a)
 t=t[:a]+'''        if(can_shorten_run(&origin,middle,pairs*2,levels[first_count-pairs],factor,house,v)) {
'''+t[b+len('        if(!blocked) {\n'):]
 helper='''static int can_shorten_run(const Ra2PathPoint *origin,int32_t direction,int32_t remaining,
    int32_t level,double factor,uint32_t house,const Ra2LocalPathServices *v)
{
    int blocked=0;
    Ra2PathPoint point=add(*origin,v->offsets[direction&7]);
    uintptr_t cell=v->cell_at(v->context,&point);
    while(remaining>0 && !blocked) {
        blocked=v->passage(v->context,cell,direction,level)!=0;
        if(!blocked)blocked=(v->cell_properties(v->context,cell).flags&0x40000u)!=0;
        /* 缩短转弯查询候选段起点的威胁；不要换成正在推进的格点。 */
        if(!blocked)blocked=scaled_at_least(v->threat(v->context,origin,house),factor,1.0,*v->numeric_control);
        --remaining;
        /* 已阻挡或刚到段尾仍探测下一格，并按通行服务之后的桥层信息更新高度。 */
        point=add(point,v->offsets[direction&7]);cell=v->cell_at(v->context,&point);
        level=next_level(level,v->cell_properties(v->context,cell));
    }
    return !blocked;
}

'''
 t=t.replace('int32_t ra2_path_shorten_turn(',helper+'int32_t ra2_path_shorten_turn(',1)
elif part=='segments':
 assert 'can_shorten_run' in t and 'segment_is_passable' not in t
 a=t.index('int ra2_path_rewrite_segment(')
 t=t[:a]+'''typedef struct Ra2SegmentRewritePlan {
    int32_t first,second,first_count,second_count;
    double factor;
    uint32_t house;
    int use_threat;
} Ra2SegmentRewritePlan;

static int segment_is_passable(const Ra2SegmentRewritePlan *plan,const Ra2PathPoint *anchor,
    int32_t level,int final_segment,const Ra2LocalPathServices *v)
{
    int blocked=plan->first_count==0;
    Ra2PathPoint point=*anchor;int32_t current_level=level,high_threat=0;
    for(unsigned run=0;run<2 && !blocked;++run) {
        int32_t direction=run?plan->second:plan->first,steps=run?plan->second_count:plan->first_count;
        for(int32_t i=0;i<steps && !blocked;++i) {
            point=add(point,v->offsets[direction&7]);uintptr_t cell=v->cell_at(v->context,&point);
            if(plan->use_threat && scaled_at_least(v->threat(v->context,&point,plan->house),plan->factor,0.01,*v->numeric_control))++high_threat;
            /* 段改写先查当前点威胁，再查通行；即使通行受阻也读取格属性并更新层高。 */
            blocked=v->passage(v->context,cell,direction,current_level)!=0;
            Ra2LocalPathCell properties=v->cell_properties(v->context,cell);
            if(!blocked)blocked=(properties.flags&0x40000u)!=0 || high_threat>3 || (!(final_segment&255) && high_threat>0);
            current_level=next_level(current_level,properties);
        }
    }
    return !blocked;
}

static void publish_segment_directions(int32_t *directions,int32_t count,const Ra2SegmentRewritePlan *plan)
{
    /* 完整候选通过后才发布；失败候选不改方向，成功后的剩余旧槽标为删除。 */
    int32_t written=0;
    for(int32_t i=0;i<plan->first_count;++i)directions[written++]=plan->first;
    for(int32_t i=0;i<plan->second_count;++i)directions[written++]=plan->second;
    while(written<count)directions[written++]=-2;
}

int ra2_path_rewrite_segment(int32_t *directions,int32_t count,const Ra2PathPoint *anchor,
    const Ra2PathPoint *delta,int32_t level,int final_segment,const Ra2LocalPathServices *v)
{
    Ra2SegmentRewritePlan plan;
    plan.first=delta->x<0?(delta->y<0?7:5):(delta->y<0?1:3);
    plan.second=delta->x-delta->y>0?(delta->x+delta->y>0?2:0):(delta->x+delta->y>0?4:6);
    int32_t x=abs(delta->x),y=abs(delta->y);
    plan.first_count=x<y?x:y;plan.second_count=abs(x-y);
    plan.factor=v->owner_factor(v->context);plan.house=v->owner_house(v->context);
    plan.use_threat=plan.factor>0.00001;
    for(unsigned attempt=0;attempt<2;++attempt) {
        if(segment_is_passable(&plan,anchor,level,final_segment,v)) {
            publish_segment_directions(directions,count,&plan);return 1;
        }
        /* 交换两段再试；下一次从原锚点/层高开始，威胁累计重新置零。 */
        int32_t temporary=plan.first;plan.first=plan.second;plan.second=temporary;
        temporary=plan.first_count;plan.first_count=plan.second_count;plan.second_count=temporary;
    }
    return 0;
}
'''
else:raise ValueError(part)
eol=b'\r\n' if b'\r\n' in p.read_bytes() else b'\n';p.write_bytes(t.encode('utf-8').replace(b'\n',eol))
print(dict(passed=True,part=part,source_sha256=sha(p)))
