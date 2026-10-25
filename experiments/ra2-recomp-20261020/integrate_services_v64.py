"""Reversible bridge/segment phase followed by Tube entry-height handoff."""
from run_batch_v64 import *
assert read(S/'traffic-baseline-scenes.json')['passed']
if sys.argv[1]=='bridge':
 p=R/'ra2/src/gameplay/ground_bridge_plane.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R))
 p.write_text('''#include "ground_bridge_plane.h"

int ra2_ground_bridge_height_matches(int32_t upper_level, int32_t lower_level)
{ return (uint32_t)upper_level==(uint32_t)lower_level+4u; }

static void enter_upper_bridge(int32_t previous,int32_t next,void *context,
    uint32_t (*flags)(void *,unsigned),void (*set_layer)(void *,unsigned))
{
    if(ra2_ground_bridge_height_matches(previous,next) && (flags(context,1)&0x100u))
        set_layer(context,1);
}

static void leave_upper_bridge(void *context,uint32_t (*flags)(void *,unsigned),
    void (*set_layer)(void *,unsigned))
{
    /* 上层写回可以改变格标志；独立复核离桥条件，不能与入桥组成else。 */
    if(!(flags(context,1)&0x100u) && (flags(context,0)&0x100u))
        set_layer(context,0);
}

void ra2_ground_transition_bridge(void *context,
    int32_t (*level)(void *context, unsigned next),
    uint32_t (*flags)(void *context, unsigned next),
    void (*set_layer)(void *context, unsigned upper))
{
    int32_t previous=level(context,0);
    int32_t next=level(context,1);
    enter_upper_bridge(previous,next,context,flags,set_layer);
    leave_upper_bridge(context,flags,set_layer);
}
''',encoding='utf-8',newline='\n')
 p=R/'ra2/src/gameplay/ground_segment.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R))
 t=p.read_text(encoding='utf-8');head=t.index('Ra2SegmentPhase ra2_ground_prepare_segment(')
 a=t.index('    output->candidate =',head);b=t.index('    if (!services->query(context, RA2_SEGMENT_OWNER_PREDICATE_27C))',a);surface=t[a:b]
 c=t.index('    output->passage =',b);permission=t[b:c]
 t=t[:a]+'''    resolve_segment_surface(direction,output,services,context);
    if(wait_for_segment_permission(path_head,output,services,context))return RA2_SEGMENT_WAIT;
'''+t[c:]
 helpers='''/* 当前格、owner桥层、第二次候选点、下一格各自保持原查询时点。 */
static void resolve_segment_surface(unsigned direction,Ra2SegmentPreparation *output,
    const Ra2SegmentServices *services,void *context)
{
'''+surface+'''}

static int wait_for_segment_permission(int32_t path_head,Ra2SegmentPreparation *output,
    const Ra2SegmentServices *services,void *context)
{
'''+permission.replace('return RA2_SEGMENT_WAIT;','return 1;')+'''    return 0;
}

'''
 t=t[:head]+helpers+t[head:];p.write_text(t,encoding='utf-8',newline='\n')
elif sys.argv[1]=='channel':
 p=R/'ra2/src/gameplay/ground_tube_travel.c';assert sha(p)==sha(S/'baseline'/p.relative_to(R))
 t=p.read_text(encoding='utf-8');head=t.index('Ra2TubeEntryPreparation ra2_ground_tube_prepare_entry(')
 a=t.index('    /* 两端查询都有副作用',head);b=t.index('    return result;',a);height=t[a:b]
 height=height.replace('    result.rise=count ?','    return count ?')
 t=t[:a]+'    result.rise=resolve_tube_rise(s,c);\n'+t[b:]
 helper='''/* 路由及端点服务完成后才查询层高，保留入口、出口、段数的顺序。 */
static int32_t resolve_tube_rise(const Ra2TubeEntryServices *s,void *c)
{
'''+height+'''}

'''
 t=t[:head]+helper+t[head:];p.write_text(t,encoding='utf-8',newline='\n')
else:raise ValueError(sys.argv[1])
print(dict(passed=True,part=sys.argv[1]))
