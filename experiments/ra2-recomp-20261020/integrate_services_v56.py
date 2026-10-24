"""Two reversible internal phases in the existing regional-search unit."""
from run_batch_v56 import *
p=R/'ra2/src/gameplay/ground_region_search.c';part=sys.argv[1]
t=p.read_text(encoding='utf-8')
if part=='layers':
 assert sha(p)==sha(S/'baseline/ra2/src/gameplay/ground_region_search.c')
 a=t.index('        for(uint32_t i=0;i<=heap->count;++i)');b=t.index('        uint32_t next_node=1;',a)
 helper='''static Ra2RegionLayer *prepare_layer(Ra2RegionSearch *s,const Ra2RegionSearchServices *v,
    const Ra2PathPoint *start,const Ra2PathPoint *goal,unsigned layer,Ra2RegionHeap *heap,
    uint32_t *first,uint32_t *target)
{
    /* 堆在查询前取快照；地址上下界是历史记录，只清条目与计数。 */
    for(uint32_t i=0;i<=heap->count;++i)heap->items[i]=NULL;
    heap->count=0;
    *first=(uint32_t)v->region_at(v->context,start,layer);
    *target=(uint32_t)v->region_at(v->context,goal,layer);
    /* 两次区域查询之后才选取本层缓存，并分别发布起点与终点的连通代次。 */
    Ra2RegionLayer *cache=&s->layers[layer];
    cache->connected[*first]=*s->generation;cache->connected[*target]=*s->generation;
    return cache;
}

static void publish_same_region(Ra2RegionSearch *s,Ra2RegionLayer *cache,unsigned layer,uint32_t first)
{
    /* 同区域只写原先的字段，不清节点其余内容，也不查询禁行边。 */
    if(!layer){s->nodes[0].region=first;s->nodes[0].depth=0;}
    cache->route[0]=(uint16_t)first;*cache->route_count=1;
}

static void seed_layer_frontier(Ra2RegionSearch *s,Ra2RegionHeap *heap,
    Ra2RegionLayer *cache,uint32_t first)
{
    s->nodes[0]=(Ra2RegionRouteNode){-1,first,0.0f,0};offer(heap,s->nodes);
    cache->visited[first]=*s->generation;cache->costs[first]=0.0f;
}

'''
 t=t[:a]+'''        uint32_t first,target;
        Ra2RegionLayer *cache=prepare_layer(s,v,start,goal,(unsigned)layer,heap,&first,&target);
        if(first==target) {
            publish_same_region(s,cache,(unsigned)layer,first);continue;
        }
        seed_layer_frontier(s,heap,cache,first);
'''+t[b:]
 t=t.replace('int ra2_region_search(',helper+'int ra2_region_search(',1)
elif part=='edges':
 assert 'prepare_layer' in t and 'proposed_edge_cost' not in t
 a=t.index('                int32_t penalty=0;',t.index('int ra2_region_search('))
 b=t.index('                Ra2RegionRouteNode *node=',a)
 helper='''static float proposed_edge_cost(Ra2RegionSearch *s,const Ra2RegionSearchServices *v,
    unsigned layer,uint32_t house,const Ra2RegionRouteNode *current,const Ra2RegionView *adjacent,
    const Ra2RegionEdge *edge,int use_penalty,double factor)
{
    int32_t penalty=0;
    if(use_penalty) {
        penalty=v->edge_penalty(v->context,house,layer,current->region,edge->destination);
        Ra2LegacyReal weighted=ra2_real_multiply(ra2_real_from_i32(penalty),ra2_real_from_f64(factor),*s->numeric_control);
        /* 先按当时的控制字乘权重，再切换整数转换控制；后续代价沿用该控制。 */
        *s->numeric_control=s->integer_conversion_control;
        penalty=ra2_real_round_i32(weighted,*s->numeric_control);
    }
    /* 罚分服务之后才读取父代价；即使边随后被限制，也先完成代价计算。 */
    return cost(s,current->cost,adjacent->terrain,penalty,edge->surcharge);
}

static int edge_is_eligible(Ra2RegionSearch *s,const Ra2RegionSearchServices *v,
    int layer,Ra2RegionLayer *cache,const Ra2RegionRouteNode *current,
    const Ra2RegionView *adjacent,const Ra2RegionEdge *edge,float proposed,int initially_unblocked)
{
    if(cache->visited[edge->destination]==*s->generation && cache->costs[edge->destination]<=proposed)return 0;
    if(layer!=2 && s->layers[layer+1].connected[adjacent->parent_region]!=*s->generation && adjacent->terrain!=1)return 0;
    if(s->terrain_allowed[adjacent->terrain]!=1)return 0;
    /* 每层首次禁行列表为空时免查；否则仅在前面限制均通过后重读列表。 */
    if(!initially_unblocked && blocked(v->blocked_edges(v->context,(unsigned)layer),current->region,edge->destination))return 0;
    return 1;
}

'''
 t=t[:a]+'''                float proposed=proposed_edge_cost(s,v,(unsigned)layer,house,current,&adjacent,&edge,use_penalty,factor);
                if(!edge_is_eligible(s,v,layer,cache,current,&adjacent,&edge,proposed,initially_unblocked))continue;
'''+t[b:]
 t=t.replace('int ra2_region_search(',helper+'int ra2_region_search(',1)
else:raise ValueError(part)
eol=b'\r\n' if b'\r\n' in p.read_bytes() else b'\n';p.write_bytes(t.encode('utf-8').replace(b'\n',eol))
print(dict(passed=True,part=part,source_sha256=sha(p)))
