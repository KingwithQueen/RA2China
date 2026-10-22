#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ground_path_search.h"
#include "ground_path_cost.h"
#include "native_probe_host.h"
/* Complete original loop, with four engine services stubbed identically.
 * Verify ordered service arguments plus all nodes, links, heap and caches. */
#define GRID (512*20)
#define N 256
#define U(a) (*(uint32_t *)(uintptr_t)(a))
static uint32_t host_stack,guest_stack,context_address;
static __declspec(naked) void original_loop(void){__asm {
 pushad
 mov host_stack,esp
 mov esi,context_address
 mov esp,guest_stack
 lea eax,returned
 mov [esp],eax
 mov eax,42764Ah
 jmp eax
returned:
 mov esp,host_stack
 popad
 ret
}}
static unsigned char cells[81][0x148],context[512],connection[64];
static uint32_t refs[GRID],stamps[2][GRID],regions[16],frame_space[16384];
static float costs[2][GRID];
static Ra2SearchNode nodes[N],*items[N];
static Ra2PathLink links[N];
static Ra2PathHeap heap;
static uint32_t region_table[40],connection_items[1],vtable[128],owner[1],*frame;
static unsigned test_case,node_count,event_count;
static uint16_t control;
static uint32_t rng;
typedef struct Event {uint32_t kind,a,b,c,d,e;} Event;
static Event events[2048];
typedef struct Result {
 uint32_t current,expanded,pending,direction,node_count,event_count;
 unsigned char context[512]; Ra2PathHeap heap; Ra2SearchNode *items[N];
 Ra2SearchNode nodes[N]; Ra2PathLink links[N];
 uint32_t stamps[2][GRID]; float costs[2][GRID]; Event events[2048];
} Result;
static Result expected,actual;
static uint32_t random_u32(void){rng=rng*1664525u+1013904223u;return rng;}
static void log_event(uint32_t kind,uint32_t a,uint32_t b,uint32_t c,uint32_t d,uint32_t e)
{if(event_count==2048)exit(3);events[event_count++]=(Event){kind,a,b,c,d,e};}
static unsigned cell_id(uintptr_t p){return (unsigned)((p-(uintptr_t)cells)/sizeof(cells[0]));}
static uint32_t grid_index(uintptr_t cell){Ra2PathPoint p;memcpy(&p,(void *)(cell+0x24),4);return (uint32_t)p.y*512+(uint32_t)p.x;}
static unsigned lower(uintptr_t cell){int32_t d=(int32_t)U(context+0x30)-(int8_t)*(uint8_t *)(cell+0x11B);return !(U(cell+0x140)&0x100)||(d>=-1&&d<=1);}
static uint32_t region_service(uintptr_t point){unsigned id=cell_id(point-0x24);log_event(1,id,0,0,0,0);if(test_case%11==0)cells[id][0x122]=1;return (id+test_case)%7+1;}
static int32_t passage_service(uintptr_t cell,unsigned direction,int32_t level,uintptr_t current,uint8_t mode){
 unsigned id=cell_id(cell);log_event(2,id,direction,(uint32_t)level,cell_id(current),mode);
 if(test_case%13==0){float w=1.0f+(float)(id%3)*0.25f;memcpy(context+4,&w,4);}
 if(test_case%17==0&&id%3==0)stamps[lower(cell)?0:1][grid_index(cell)]=U(context+0x28);
 if(test_case%16==1||test_case%16==2)return 7;
 return (int32_t)((id+test_case+direction)%10);
}
static double traversal_service(uintptr_t current,uintptr_t candidate,unsigned upper,int32_t pass,uintptr_t unit){log_event(3,(uint32_t)current,(uint32_t)candidate,upper,(uint32_t)pass,(uint32_t)unit);return 0.125*(double)(1+cell_id(U(candidate))%13)+(double)pass*0.25;}
static Ra2SearchNode *node_service(Ra2SearchNode *parent,uintptr_t reference,uintptr_t target,float step){
 uint32_t bits;memcpy(&bits,&step,4);log_event(4,(uint32_t)(uintptr_t)parent,(uint32_t)reference,(uint32_t)target,bits,0);
 if(node_count==N)exit(3);unsigned id=node_count++;uintptr_t cell=U(reference);
 links[id]=(Ra2PathLink){(void *)reference,(int8_t)*(uint8_t *)(cell+0x11B)+(lower(cell)?0:4),parent->path_link};
 nodes[id]=(Ra2SearchNode){&links[id],ra2_ground_accumulate_path_cost(parent->accumulated_cost,step,control),0,parent->path_length+1};
 nodes[id].priority=nodes[id].accumulated_cost+(float)(cell_id(cell)%3)*0.25f;return &nodes[id];
}
static uint32_t __fastcall native_region(void *self,void *unused,uint32_t point){(void)self;(void)unused;return region_service(point);}
static int32_t __fastcall native_passage(void *self,void *unused,uint32_t cell,uint32_t direction,int32_t level,uint32_t current,uint32_t mode){(void)self;(void)unused;return passage_service(cell,direction,level,current,(uint8_t)mode);}
static double __fastcall native_traversal(void *self,void *unused,uint32_t current,uint32_t candidate,uint32_t upper,int32_t pass,uint32_t unit){(void)self;(void)unused;return traversal_service(current,candidate,upper&255,pass,unit);}
static Ra2SearchNode *__fastcall native_node(void *self,void *unused,Ra2SearchNode *parent,uint32_t reference,uint32_t target,float step){(void)self;(void)unused;return node_service(parent,reference,target,step);}
static void patch_jump(uintptr_t address,uintptr_t target){*(uint8_t *)address=0xE9;U(address+1)=(uint32_t)(target-address-5);}
static uintptr_t c_neighbor(void *opaque,uintptr_t reference,unsigned direction){
 (void)opaque;if(direction<8)return reference+U(0x79C484+direction*4)*4;
 int16_t c;memcpy(&c,(void *)(U(reference)+0x116),2);if(c==-1)return 0x84E808;
 Ra2PathPoint p;memcpy(&p,connection+0x28,4);return (uintptr_t)&refs[p.y*512+p.x];
}
static int c_cell(void *opaque,uintptr_t reference,Ra2PathCell *out){
 (void)opaque;uintptr_t p=U(reference);if(!p)return 0;memcpy(&out->point,(void *)(p+0x24),4);
 out->ground_level=(int8_t)*(uint8_t *)(p+0x11B);out->has_bridge=(U(p+0x140)&0x100)!=0;out->has_region_connection=*(uint8_t *)(p+0x122);return 1;
}
static int32_t c_offset(void *opaque,unsigned d){(void)opaque;return (int32_t)U(0x84C838+d*4);}
static int32_t c_region(void *opaque,const Ra2PathSearch *s){(void)opaque;return (int16_t)*(uint16_t *)((uintptr_t)region_table+region_service(U(s->candidate_cell)+0x24)*10);}
static int32_t c_passage(void *opaque,const Ra2PathSearch *s){(void)opaque;return passage_service(U(s->candidate_cell),s->direction,*s->current_level,U(s->current_cell),*s->movement_mode);}
static double c_traversal(void *opaque,const Ra2PathSearch *s,int32_t pass){(void)opaque;return traversal_service(s->current_cell,s->candidate_cell,!s->lower_surface,pass,(uintptr_t)owner);}
static Ra2SearchNode *c_node(void *opaque,const Ra2PathSearch *s){(void)opaque;return node_service(s->current,s->candidate_cell,frame[0x64/4],s->step_cost);}
static void setup(unsigned n){
 test_case=n;rng=12345u+n*31;node_count=1;event_count=0;
 memset(context,0,sizeof(context));memset(frame_space,0,sizeof(frame_space));frame=frame_space+8192;
 for(unsigned i=0;i<16;++i)frame_space[i]=0xA17ECAFE;
 memset(refs,0,sizeof(refs));memset(stamps,0,sizeof(stamps));memset(costs,0,sizeof(costs));memset(cells,0,sizeof(cells));
 memset(nodes,0,sizeof(nodes));memset(links,0,sizeof(links));memset(items,0,sizeof(items));memset(events,0,sizeof(events));memset(regions,0,sizeof(regions));
 for(unsigned i=0;i<81;++i){
  Ra2PathPoint p={(int16_t)(4+i%9),(int16_t)(4+i/9)};memcpy(cells[i]+0x24,&p,4);*(int16_t *)(cells[i]+0x116)=-1;
  cells[i][0x11B]=(uint8_t)(random_u32()%5);cells[i][0x122]=(uint8_t)(random_u32()%4==0);U(cells[i]+0x140)=random_u32()%2?0x100:0;
  refs[p.y*512+p.x]=(uint32_t)(uintptr_t)cells[i];
  for(unsigned layer=0;layer<2;++layer)if(random_u32()%3==0){stamps[layer][p.y*512+p.x]=9;costs[layer][p.y*512+p.x]=(float)(random_u32()%16);}
 }
 if(n%5==0)for(unsigned i=0;i<8;++i)refs[8*512+8+(int32_t)U(0x79C484+i*4)]=0;
 if(n%3==0)*(int16_t *)(cells[40]+0x116)=0;
 Ra2PathPoint destination={12,8};memcpy(connection+0x28,&destination,4);
 for(unsigned i=1;i<=7;++i){
  int16_t region=(int16_t)(n%19==0?-(int)i:(int)i);
  *(int16_t *)((uintptr_t)region_table+i*10)=region;regions[8+region]=random_u32()%2?9:0;
 }
 U(context+4)=0x3F800000;context[8]=(uint8_t)(n%4);U(context+0x28)=9;U(context+0x30)=n%5;U(context+0x34)=(n/3)%5;
 for(unsigned i=0;i<100;++i)*(uint16_t *)(context+0xBE+i*2)=(uint16_t)(n%19==0?0xFFFF:i%7+1);
 heap=(Ra2PathHeap){0,n%7?N:2,items,0,UINT32_MAX};U(context+0x14)=(uint32_t)(uintptr_t)&heap;
 U(context+0x18)=(uint32_t)(uintptr_t)stamps[0];U(context+0x1C)=(uint32_t)(uintptr_t)stamps[1];U(context+0x24)=(uint32_t)(uintptr_t)costs[0];U(context+0x20)=(uint32_t)(uintptr_t)costs[1];
 links[0]=(Ra2PathLink){&refs[8*512+8],(int32_t)U(context+0x30),NULL};nodes[0]=(Ra2SearchNode){&links[0],(float)(n%4),0,0};
 frame[0x14/4]=(uint32_t)(uintptr_t)&nodes[0];frame[0x38/4]=(uint32_t)(uintptr_t)&refs[8*512+9];frame[0x40/4]=(uint32_t)(uintptr_t)(regions+8);
 frame[0x64/4]=0x12345678;frame[0x68/4]=(uint32_t)(uintptr_t)owner;frame[0x70/4]=n%16==3?0:n%8+1;
 ((uint8_t *)frame)[0x12]=(uint8_t)(n%2);((uint8_t *)frame)[0x13]=(uint8_t)((n/2)%2);((uint8_t *)frame)[0x74]=(uint8_t)((n/4)%2);
 if(n%16==0){frame[0x38/4]=(uint32_t)(uintptr_t)&refs[8*512+8];U(context+0x34)=U(context+0x30);}
 guest_stack=(uint32_t)(uintptr_t)frame;context_address=(uint32_t)(uintptr_t)context;
}
static void capture(Result *r){
 memset(r,0,sizeof(*r));r->current=frame[0x14/4];r->expanded=frame[0x28/4];r->pending=frame[0x1C/4];r->direction=frame[0x18/4];r->node_count=node_count;r->event_count=event_count;
 memcpy(r->context,context,sizeof(context));r->heap=heap;memcpy(r->items,items,sizeof(items));memcpy(r->nodes,nodes,sizeof(nodes));memcpy(r->links,links,sizeof(links));
 memcpy(r->stamps,stamps,sizeof(stamps));memcpy(r->costs,costs,sizeof(costs));memcpy(r->events,events,sizeof(events));
}
int main(int argc,char **argv){
 if(argc!=2)return 2;hold_image();map_original_image(argv[1]);
 const uint8_t start[]={0x8B,0x4C,0x24,0x70,0x8B,0x44,0x24,0x28};if(memcmp((void *)0x42764A,start,sizeof(start)))return 2;
 patch_jump(0x54FAB0,(uintptr_t)native_region);patch_jump(0x427110,(uintptr_t)native_traversal);patch_jump(0x427D40,(uintptr_t)native_node);*(uint8_t *)0x427CBB=0xC3;
 vtable[0x194/4]=(uint32_t)(uintptr_t)native_passage;owner[0]=(uint32_t)(uintptr_t)vtable;
 U(0x832618)=(uint32_t)(uintptr_t)refs;U(0x83254C)=(uint32_t)(uintptr_t)region_table;connection_items[0]=(uint32_t)(uintptr_t)connection;U(0x8661CC)=(uint32_t)(uintptr_t)connection_items;
 U(0x84E804)=512;U(0x84E808)=0;unsigned stops[4]={0},total_events=0,total_nodes=0;
 for(unsigned n=0;n<8192;++n){
  control=(uint16_t)(0x7F|((n%3==0?0:n%3==1?2:3)<<8)|(((n/3)%4)<<10));
  setup(n);__asm {fldcw control} original_loop();
  for(unsigned i=0;i<16;++i)if(frame_space[i]!=0xA17ECAFE){puts("probe guest stack guard overwritten");return 3;}
  capture(&expected);setup(n);__asm {fldcw control}
  Ra2PathSearch s={0};s.current=&nodes[0];s.destination=frame[0x38/4];s.expansion_limit=(int32_t)frame[0x70/4];
  s.ignore_soft_obstacles=((uint8_t *)frame)[0x12];s.continue_at_blocked_goal=((uint8_t *)frame)[0x13];s.restrict_to_connected_regions=((uint8_t *)frame)[0x74];
  s.current_level=(int32_t *)(context+0x30);s.destination_level=(int32_t *)(context+0x34);s.search_weight=(float *)(context+4);s.movement_mode=context+8;
  s.region_cursor=(uint32_t *)(context+0x6C);s.last_region_point=(uint32_t *)(context+0x70);s.region_route=(uint16_t *)(context+0xBE);s.connected_regions=regions+8;
  s.cache=(Ra2PathNodeCache){{stamps[0],costs[0]},{stamps[1],costs[1]},(uint32_t *)(context+0x28)};s.open=&heap;s.grid_width=512;
  memcpy(&s.cache_epsilon,(void *)0x79C4D0,8);s.direction_bias=(float *)0x7CF0DC;s.numeric_control=control;
  Ra2PathSearchServices v={NULL,c_neighbor,c_cell,c_offset,c_region,c_passage,c_traversal,c_node};++stops[ra2_path_search_neighbors(&s,&v)];
  frame[0x14/4]=(uint32_t)(uintptr_t)s.current;frame[0x28/4]=s.expanded;frame[0x1C/4]=(uint32_t)(uintptr_t)s.pending;frame[0x18/4]=s.direction;capture(&actual);
  if(memcmp(&expected,&actual,sizeof(actual))){
   size_t offset=0;while(((uint8_t *)&expected)[offset]==((uint8_t *)&actual)[offset])++offset;
   printf("search mismatch case=%u offset=%u expanded=%u/%u nodes=%u/%u events=%u/%u\n",n,(unsigned)offset,expected.expanded,actual.expanded,expected.node_count,actual.node_count,expected.event_count,actual.event_count);
   for(unsigned i=0;i<expected.event_count&&i<actual.event_count&&i<40;++i){Event a=expected.events[i],b=actual.events[i];printf("event=%u kind=%u/%u args=%x,%x,%x,%x,%x / %x,%x,%x,%x,%x\n",i,a.kind,b.kind,a.a,a.b,a.c,a.d,a.e,b.a,b.b,b.c,b.d,b.e);}return 1;
  }
  total_events+=event_count;total_nodes+=node_count-1;
 }
 for(unsigned i=0;i<4;++i)if(!stops[i])return 1;
 printf("{\"passed\":true,\"cases\":8192,\"ordered_service_events\":%u,\"created_nodes\":%u,\"stop_cases\":[%u,%u,%u,%u],\"mapped_complete_original_loop\":true,\"numeric_controls\":12,\"services_stubbed\":true}\n",total_events,total_nodes,stops[0],stops[1],stops[2],stops[3]);return 0;
}
