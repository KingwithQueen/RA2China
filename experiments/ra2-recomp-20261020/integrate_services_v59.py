"""Reversible bounded-capacity heap improvement, then node allocation/publication phases."""
from run_batch_v59 import *
if sys.argv[1]=='heap':
 p=R/'ra2/src/gameplay/ground_path_heap.c';assert sha(p)==sha(S/'baseline/ra2/src/gameplay/ground_path_heap.c')
 t=p.read_text(encoding='utf-8')
 t=t.replace('static void push(Ra2PathHeap *heap,Ra2SearchNode *node)','''static int has_free_slot(const Ra2PathHeap *heap)
{
    /* capacity包含闲置的0号槽；先比较再加一，零容量和计数回绕均不能发布。 */
    return heap->capacity>0 && heap->count<heap->capacity-1u;
}

static int try_push(Ra2PathHeap *heap,Ra2SearchNode *node)''',1)
 t=t.replace('    uint32_t slot=heap->count+1;\n    if(slot>=heap->capacity)return;','    if(!has_free_slot(heap))return 0;\n    uint32_t slot=heap->count+1;',1)
 t=t.replace('    ra2_path_heap_finish_offer(heap,node,slot);\n}', '    ra2_path_heap_finish_offer(heap,node,slot);\n    return 1;\n}',1)
 a=t.index('    /* INC 后的零标志');b=t.index('\n}',a)
 t=t[:a]+'''    if(try_push(heap,pending))return candidate;
    /* 用户允许寻路改进：满堆不增加内存，保留两候选中分数较低者；同分仍选新的。 */
    return pending->priority<candidate->priority?pending:candidate;'''+t[b:]
 p.write_text(t,encoding='utf-8',newline='\r\n')
 p=R/'ra2/src/gameplay/ground_path_heap.h';t=p.read_text(encoding='utf-8')
 a=t.index('/* pending 表示');b=t.index('Ra2SearchNode *ra2_path_heap_offer',a)
 t=t[:a]+'''/* pending是独立暂存的候选。有空槽时把旧候选入堆、暂存新候选。
 * 满堆时在两候选间保留较低priority者，同分仍选新候选；不增加容量或内存。
 * 这是经授权的局部路径选择改进，不保证受限预算下的全局最优。 */
'''+t[b:]
 p.write_text(t,encoding='utf-8',newline='\r\n')
elif sys.argv[1]=='nodes':
 p=R/'ra2/src/gameplay/ground_path_nodes.c';assert sha(p)==sha(S/'baseline/ra2/src/gameplay/ground_path_nodes.c')
 t=p.read_text(encoding='utf-8')
 a=t.index('    if(!input->parent) {');b=t.index('    node->path_link=link;',a)
 init=t[a:b]
 helper='''static void initialize_node_state(Ra2SearchNode *node,Ra2PathLink *link,
    const Ra2PathNodeInput *input,uint16_t control)
{
'''+init+'''}

'''
 t=t[:a]+'    initialize_node_state(node,link,input,control);\n'+t[b:]
 t=t.replace('Ra2SearchNode *ra2_path_node_create(',helper+'Ra2SearchNode *ra2_path_node_create(',1)
 t=t.replace('    Ra2SearchNode *node=&storage->nodes[(*storage->used_nodes)++];','    /* 容量由搜索上下文保证；节点先于链分配，各计数仍在取址时递增。 */\n    Ra2SearchNode *node=&storage->nodes[(*storage->used_nodes)++];',1)
 t=t.replace('    node->path_link=link;','    /* 链与节点状态就绪后再发布关联；priority仍留待距离服务生成。 */\n    node->path_link=link;',1)
 a=t.index('    for(uint32_t i=0;i<cell_count;++i)');b=t.index('    ++*cache->generation;',a)
 clear=t[a:b]
 helper='''static void clear_wrapped_generation(Ra2PathNodeCache *cache,uint32_t cell_count,
    Ra2PathRegionCache regions[3])
{
    /* 只清代次标记，不清代价、节点旧内容或历史堆地址界限。 */
'''+clear+'''}

'''
 t=t[:a]+'    clear_wrapped_generation(cache,cell_count,regions);\n'+t[b:]
 t=t.replace('void ra2_path_search_reset(',helper+'void ra2_path_search_reset(',1)
 p.write_text(t,encoding='utf-8',newline='\n')
else:raise ValueError(sys.argv[1])
print(dict(passed=True,part=sys.argv[1]))
