#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ground_path_search.h"
#include "ground_path_nodes.h"

/* 独立的三格有向图：起点可一步到目标，也可走入死路。方向序列先生成目标、后生成死路。 */
typedef struct World {
    Ra2SearchNode nodes[16];Ra2PathLink links[16];uint32_t used_nodes,used_links;
} World;
static const Ra2PathPoint points[4]={{0,0},{4,4},{5,4},{4,5}};
static uintptr_t neighbor(void *p,uintptr_t cell,unsigned direction)
{(void)p;return cell==1?(direction==2?2:direction==4?3:0):0;}
static int cell_view(void *p,uintptr_t cell,Ra2PathCell *out)
{(void)p;if(!cell || cell>3)return 0;*out=(Ra2PathCell){points[cell],0,0,0};return 1;}
static int32_t offset(void *p,unsigned direction)
{(void)p;static const int32_t table[8]={-16,-15,1,17,16,15,-1,-17};return table[direction];}
static int32_t region(void *p,const Ra2PathSearch *s){(void)p;(void)s;return 1;}
static int32_t passage(void *p,const Ra2PathSearch *s){(void)p;(void)s;return 0;}
static double cost(void *p,const Ra2PathSearch *s,int32_t pass){(void)p;(void)s;(void)pass;return 1.0;}
static Ra2SearchNode *create_node(void *opaque,const Ra2PathSearch *s)
{
    World *w=opaque;Ra2PathNodeStorage pool={w->nodes,&w->used_nodes,w->links,&w->used_links};
    Ra2PathNodeInput in={s->current,(void *)s->candidate_cell,0,0,0,0,0,s->step_cost};
    if(w->used_nodes>=16 || w->used_links>=16)exit(3);
    Ra2SearchNode *node=ra2_path_node_create(&pool,&in,0x037F);
    Ra2PathPoint q=points[s->candidate_cell];
    node->priority=node->accumulated_cost+(float)(abs(q.x-points[2].x)+abs(q.y-points[2].y));return node;
}
static int shortest_distance(void)
{
    unsigned queue[4]={1},head=0,tail=1;int distance[4]={-1,0,-1,-1};
    while(head<tail){unsigned u=queue[head++];if(u==2)return distance[u];
        for(unsigned d=0;d<8;++d){unsigned v=(unsigned)neighbor(NULL,u,d);if(v && distance[v]<0){distance[v]=distance[u]+1;queue[tail++]=v;}}}
    return -1;
}
static int search(unsigned capacity,int *path_length,float *goal_cost)
{
    World w={0};Ra2SearchNode *items[4]={0};Ra2PathHeap heap={0,capacity,items,0,UINT32_MAX};
    uint32_t stamps[2][256]={{0}},generation=1,connected[2]={0,1},cursor=0,last_point=0;
    float costs[2][256]={{0}},bias[8]={0},weight=1.0f;int32_t level=0,destination_level=0;uint8_t mode=0;uint16_t route[1]={0};
    Ra2PathNodeStorage pool={w.nodes,&w.used_nodes,w.links,&w.used_links};Ra2PathNodeInput input={0};input.cell_reference=(void *)1;
    Ra2SearchNode *root=ra2_path_node_create(&pool,&input,0x037F);root->priority=1;
    Ra2PathSearch s={0};s.current=root;s.destination=2;s.expansion_limit=16;s.current_level=&level;s.destination_level=&destination_level;
    s.search_weight=&weight;s.movement_mode=&mode;s.region_cursor=&cursor;s.last_region_point=&last_point;s.region_route=route;s.connected_regions=connected;
    s.cache=(Ra2PathNodeCache){{stamps[0],costs[0]},{stamps[1],costs[1]},&generation};s.open=&heap;s.grid_width=16;s.cache_epsilon=0.00001;s.direction_bias=bias;s.numeric_control=0x037F;
    ra2_path_cache_publish(&s.cache,68,1,0);
    Ra2PathSearchServices v={&w,neighbor,cell_view,offset,region,passage,cost,create_node};
    Ra2PathSearchStop stop=ra2_path_search_neighbors(&s,&v);
    if(heap.count>=heap.capacity || w.used_nodes>16 || w.used_links>16)exit(3);
    if(stop==RA2_SEARCH_REACHED_GOAL){*path_length=s.current->path_length;*goal_cost=s.current->accumulated_cost;return 1;}
    *path_length=0;*goal_cost=-1;return 0;
}
static int quality_cases(void)
{
    uint32_t rng=12345;
    for(unsigned n=0;n<65536;++n){
        Ra2SearchNode nodes[10]={{0}},*items[10];for(unsigned i=0;i<10;++i){nodes[i].priority=(float)i;items[i]=&nodes[i];}
        unsigned capacity=n%8+1,count=capacity-1;Ra2PathHeap h={count,capacity,items,91,17};
        rng=rng*1664525u+1013904223u;nodes[8].priority=(float)(rng%100);rng=rng*1664525u+1013904223u;nodes[9].priority=(float)(rng%100);
        Ra2SearchNode *before[10];memcpy(before,items,sizeof(items));
        Ra2SearchNode *chosen=ra2_path_heap_offer(&h,&nodes[8],&nodes[9]);
        if(chosen->priority>nodes[8].priority || chosen->priority>nodes[9].priority || h.count!=count || h.highest_node_address!=91 || h.lowest_node_address!=17 || memcmp(before,items,sizeof(items)))return 0;
        if(nodes[8].priority==nodes[9].priority && chosen!=&nodes[9])return 0;
    }
    return 1;
}
static int guards(void)
{
    Ra2SearchNode a={0},b={0},*items[2]={&a,&b};a.priority=1;b.priority=2;
    const uint32_t counts[3]={0,0,UINT32_MAX},capacities[3]={0,1,3};
    for(unsigned i=0;i<3;++i){Ra2PathHeap h={counts[i],capacities[i],items,91,17};
        if(ra2_path_heap_offer(&h,&a,&b)!=&a || h.count!=counts[i] || items[0]!=&a || items[1]!=&b || h.highest_node_address!=91 || h.lowest_node_address!=17)return 0;}
    return 1;
}
int main(int argc,char **argv)
{
    if(argc!=2)return 2;int improved=atoi(argv[1]),length=0;float score=-1;
    int found=search(1,&length,&score),distance=shortest_distance();
    if(distance!=1 || found!=improved || (found && (length!=distance+1 || score!=distance)))return 1;
    int other_length=0;float other_score=-1;if(!search(2,&other_length,&other_score) || other_length!=2 || other_score!=1)return 1;
    if(improved && (!quality_cases() || !guards()))return 1;
    printf("{\"passed\":true,\"expect_improvement\":%s,\"zero_slot_heap_reached_goal\":%s,\"goal_cost\":%g,\"bfs_distance\":%d,\"one_slot_heap_reached_goal\":true,\"quality_cases\":%u,\"guard_cases\":%u,\"graph_cases\":2,\"cases\":%u,\"synthetic_not_natural\":true}\n",improved?"true":"false",found?"true":"false",(double)score,distance,improved?65536u:0u,improved?3u:0u,improved?65541u:2u);return 0;
}
