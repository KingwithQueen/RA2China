"""Extract search services in two content-checked, reversible phases."""
from run_batch_v55 import *
p=R/'ra2/src/gameplay/ground_path_search.c';part=sys.argv[1]
t=p.read_text(encoding='utf-8')
if part=='neighbors':
 assert sha(p)==sha(S/'baseline/ra2/src/gameplay/ground_path_search.c')
 a=t.index('            s->candidate_cell=v->neighbor');b=t.index('            if(cached_candidate_is_cheaper(s))continue;',a)
 old=t[a:b]
 helper='''static int resolve_neighbor(Ra2PathSearch *s,const Ra2PathSearchServices *v,
    Ra2PathCell *candidate)
{
    /* 第九项是特殊连接，按实际落格计算索引；普通八邻格使用原偏移表。 */
    s->candidate_cell=v->neighbor(v->context,s->current_cell,s->direction);
    if(!v->cell(v->context,s->candidate_cell,candidate))return 0;
    s->candidate_point=candidate->point;
    s->candidate_grid_index=s->direction==8?
        (uint32_t)candidate->point.y*s->grid_width+(uint32_t)(int32_t)candidate->point.x:
        s->current_grid_index+(uint32_t)v->neighbor_grid_offset(v->context,s->direction);
    s->lower_surface=!candidate->has_bridge || level_difference(*s->current_level,candidate->ground_level)<=1;
    return 1;
}

static int candidate_region_allows(Ra2PathSearch *s,const Ra2PathSearchServices *v,
    Ra2PathCell *candidate)
{
    s->candidate_region=v->region(v->context,s);
    /* 区域服务可能改变连接标记，必须重读同一格；沿用原本忽略返回值的语义。 */
    v->cell(v->context,s->candidate_cell,candidate);
    return ra2_path_region_allows(s->connected_regions[s->candidate_region],*s->cache.generation,
        s->lower_surface,candidate->has_region_connection,s->restrict_to_connected_regions);
}

'''
 t=t[:a]+'''            Ra2PathCell candidate;
            if(!resolve_neighbor(s,v,&candidate))continue;
            if(!candidate_region_allows(s,v,&candidate))continue;
'''+t[b:]
 t=t.replace('Ra2PathSearchStop ra2_path_search_neighbors(',helper+'Ra2PathSearchStop ra2_path_search_neighbors(',1)
 assert 'v->neighbor(v->context,s->current_cell,s->direction)' in old
elif part=='frontier':
 assert 'candidate_region_allows' in t and 'score_candidate_step' not in t
 a=t.index('            if(s->direction==8) {',t.index('Ra2PathSearchStop ra2_path_search_neighbors'))
 b=t.index('            if(passage<7) {',a)
 block=t[a:b]
 helper='''static void score_candidate_step(Ra2PathSearch *s,const Ra2PathSearchServices *v,
    int32_t passage,Ra2PathCell *current,Ra2PathCell *candidate)
{
    /* 通行服务之后才计算代价，保留实时权重、朝向与数值控制的读取。 */
'''+block.replace('            ','    ').replace('&current','current').replace('&candidate','candidate').replace('current.point','current->point').replace('candidate.point','candidate->point')+'''}

static int advance_frontier(Ra2PathSearch *s)
{
    /* 先合并待选节点并取堆，再发布新层高，最后增加展开计数（空堆也计数）。 */
    s->current=ra2_path_heap_take(s->open,s->pending);
    if(s->current)*s->current_level=((Ra2PathLink *)s->current->path_link)->surface_level;
    ++s->expanded;
    return s->current!=NULL;
}

'''
 t=t[:a]+'            score_candidate_step(s,v,passage,&current,&candidate);\n'+t[b:]
 old='''        s->current=ra2_path_heap_take(s->open,s->pending);
        if(s->current)*s->current_level=((Ra2PathLink *)s->current->path_link)->surface_level;
        ++s->expanded;
        if(!s->current)return RA2_SEARCH_EMPTY;'''
 assert t.count(old)==1
 t=t.replace(old,'        if(!advance_frontier(s))return RA2_SEARCH_EMPTY;')
 t=t.replace('Ra2PathSearchStop ra2_path_search_neighbors(',helper+'Ra2PathSearchStop ra2_path_search_neighbors(',1)
 t=t.replace('    Ra2SearchNode *node=v->create_node', '    /* 建节点回调后才提交堆与缓存，随后按当时的区域游标推进路线。 */\n    Ra2SearchNode *node=v->create_node',1)
else:raise ValueError(part)
eol=b'\r\n' if b'\r\n' in p.read_bytes() else b'\n'
p.write_bytes(t.encode('utf-8').replace(b'\n',eol))
print(dict(passed=True,part=part,source_sha256=sha(p)))
