#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ground_path_prepare.h"
#include "ground_region_route.h"
#include "ground_path_rebuild.h"
#include "native_probe_host.h"
#define U(a) (*(uint32_t *)(uintptr_t)(a))
#define G (512*20)
static uint32_t host_stack,guest_stack,entry,reg_ecx,reg_eax,reg_edi,reg_esi,result,ready;
static uint32_t stack_space[16384];
static __declspec(naked) void original(void){__asm{
 pushad
 mov host_stack,esp
 mov esp,guest_stack
 lea eax,returned
 mov [esp],eax
 mov ecx,reg_ecx
 mov edi,reg_edi
 mov esi,reg_esi
 mov eax,reg_eax
 jmp entry
returned:
 mov result,eax
 mov esp,host_stack
 popad
 ret
}}
static __declspec(naked) void entry_ready(void){__asm{
 mov ready,1
 mov eax,427D2Eh
 jmp eax
}}
static void patch(uintptr_t p,uintptr_t target){*(uint8_t *)p=0xE9;U(p+1)=(uint32_t)(target-p-5);}
static uint32_t random_state;
static uint32_t random_u32(void){random_state=random_state*1664525u+1013904223u;return random_state;}
static unsigned char cells[9][0x148],owner[0xC00],type[0xC00],context[128];
static uint32_t refs[G],stamps[2][G],connected[16],vtable[128];
static float costs[2][G];
static Ra2PathPoint from,to;
static Ra2SearchNode root;
static unsigned test_case,queries,event_count;
static uint32_t events[64];
static void event(unsigned code){if(event_count==64)exit(3);events[event_count++]=code;}
static int32_t kind(void){event(10);return (int32_t)(test_case%3);}
static Ra2PathOwnerType describe_type(void){
 event(20);++queries;type[0xAA0]=(uint8_t)((test_case+queries)%2);
 return (Ra2PathOwnerType){type[0xAA0],(int32_t)U(type+0x5A4)};
}
static void toggle(void){event(30);}
static unsigned facing(void){event(40);return (test_case+event_count)%8;}
static Ra2SearchNode *create(uintptr_t ref,const Ra2PathPoint *target){
 event(50);if(ref!=(uintptr_t)&refs[8*512+8]||target!=&to)exit(3);return test_case%17?&root:NULL;
}
static int32_t __fastcall native_kind(void *s,void *d){(void)s;(void)d;return kind();}
static void *__fastcall native_type(void *s,void *d){(void)s;(void)d;describe_type();return type;}
static void __fastcall native_toggle(void *s,void *d,uint32_t actor){(void)s;(void)d;(void)actor;toggle();}
static uint32_t __fastcall native_facing(void *s,void *d,uint32_t out){(void)s;(void)d;U(out)=facing()*8192;return out;}
static Ra2SearchNode *__fastcall native_create(void *s,void *d,uint32_t parent,uint32_t ref,uint32_t target,uint32_t step){
 (void)s;(void)d;if(parent||step)exit(3);return create(ref,(Ra2PathPoint *)(uintptr_t)target);
}
static uintptr_t c_reference(void *s,const Ra2PathPoint *p){(void)s;return (uintptr_t)&refs[p->y*512+p->x];}
static int c_cell(void *s,uintptr_t r,Ra2PathCell *out){
 (void)s;uintptr_t p=U(r);if(!p)return 0;memcpy(&out->point,(void *)(p+0x24),4);out->ground_level=(int8_t)*(uint8_t *)(p+0x11B);
 out->has_bridge=(U(p+0x140)&0x100)!=0;out->has_region_connection=0;return 1;
}
static int32_t c_kind(void *s){(void)s;return kind();}
static Ra2PathOwnerType c_type(void *s){(void)s;return describe_type();}
static unsigned c_bridge(void *s){(void)s;return owner[0x79];}
static int32_t c_height(void *s){(void)s;return (int32_t)U(owner+0x90)/256;}
static unsigned c_flag(void *s){(void)s;return type[0xBA4];}
static void c_toggle(void *s){(void)s;toggle();}
static unsigned c_facing(void *s){(void)s;return facing();}
static Ra2SearchNode *c_create(void *s,uintptr_t r,const Ra2PathPoint *p){(void)s;return create(r,p);}
static uintptr_t c_adjacent(void *s,uintptr_t r,unsigned d){(void)s;return r+U(0x79C484+d*4)*4;}
typedef struct PreparationResult {
 unsigned char context[128];uint32_t stamps[2][G];float costs[2][G];uint32_t events[64];unsigned event_count,ready;
 uint32_t root,limit,ignore,blocked,regions;
} PreparationResult;
static PreparationResult expected,actual;
static void prep_setup(unsigned n){
 test_case=n;queries=event_count=ready=0;memset(events,0,sizeof(events));memset(context,0xA5,sizeof(context));
 memset(refs,0,sizeof(refs));memset(stamps,0xA5,sizeof(stamps));memset(costs,0xA5,sizeof(costs));
 memset(owner,0,sizeof(owner));memset(type,0,sizeof(type));memset(stack_space,0,sizeof(stack_space));
 for(unsigned i=0;i<9;++i){
  memset(cells[i],0,sizeof(cells[i]));Ra2PathPoint p={(int16_t)(7+i%3),(int16_t)(7+i/3)};memcpy(cells[i]+0x24,&p,4);
  cells[i][0x11B]=(uint8_t)((int)(n+i)%7-3);U(cells[i]+0x140)=((n+i)%2)*0x100;refs[p.y*512+p.x]=(uint32_t)(uintptr_t)cells[i];
 }
 from=(Ra2PathPoint){8,8};to=n%7?(Ra2PathPoint){9,8}:from;
 if(n%29==0)refs[8*512+8]=0;if(n%31==0)refs[to.y*512+to.x]=0;
 U(context+0x18)=(uint32_t)(uintptr_t)stamps[0];U(context+0x1C)=(uint32_t)(uintptr_t)stamps[1];
 U(context+0x24)=(uint32_t)(uintptr_t)costs[0];U(context+0x20)=(uint32_t)(uintptr_t)costs[1];
 U(context+0x28)=n+7;U(context+0x3C)=n%3;U(context+0x40)=(uint32_t)(uintptr_t)connected;
 U(owner)=(uint32_t)(uintptr_t)vtable;owner[0x79]=(uint8_t)(n%2);U(owner+0x90)=((uint32_t)n%9)*256;
 U(owner+0x5AC)=(uint32_t)(uintptr_t)type;U(type+0x5A4)=n%8;type[0xBA4]=(uint8_t)(n%2);
 guest_stack=(uint32_t)(uintptr_t)(stack_space+8192);uint32_t *s=(uint32_t *)(uintptr_t)guest_stack;
 s[1]=(uint32_t)(uintptr_t)&from;s[2]=(uint32_t)(uintptr_t)&to;s[3]=(uint32_t)(uintptr_t)owner;s[4]=0x11111111;s[5]=n%5?n%15:UINT32_MAX;s[6]=0;
 reg_ecx=(uint32_t)(uintptr_t)context;entry=0x427370;
}
static void capture(PreparationResult *r){
 memset(r,0,sizeof(*r));memcpy(r->context,context,sizeof(context));memcpy(r->stamps,stamps,sizeof(stamps));memcpy(r->costs,costs,sizeof(costs));memcpy(r->events,events,sizeof(events));r->event_count=event_count;r->ready=ready;
 if(ready){uint32_t *f=(uint32_t *)(uintptr_t)(guest_stack-0x5C);r->root=f[0x14/4];r->limit=f[0x70/4];r->ignore=((uint8_t *)f)[0x12];r->blocked=((uint8_t *)f)[0x13];r->regions=f[0x40/4];}
}
static int prepare_cases(void){
 patch(0x42764A,(uintptr_t)entry_ready);patch(0x427D40,(uintptr_t)native_create);patch(0x4285D0,(uintptr_t)native_toggle);patch(0x4B8BE0,(uintptr_t)native_facing);
 vtable[0x2C/4]=(uint32_t)(uintptr_t)native_kind;vtable[0x80/4]=(uint32_t)(uintptr_t)native_type;
 U(0x832618)=(uint32_t)(uintptr_t)refs;U(0x84E804)=512;U(0x84E800)=256;
 unsigned stops[4]={0};
 for(unsigned n=0;n<8192;++n){
  prep_setup(n);original();capture(&expected);prep_setup(n);
  Ra2PathPreparation p={0};p.start=&from;p.target=&to;p.expansion_limit=(int32_t)((uint32_t *)(uintptr_t)guest_stack)[5];
  p.start_level=(int32_t *)(context+0x30);p.target_level=(int32_t *)(context+0x34);p.movement_zone=(int32_t *)(context+0x2C);p.obstacle_mode=(int32_t *)(context+0x3C);
  p.region_cursor=(uint32_t *)(context+0x6C);p.last_region_point=(uint32_t *)(context+0x70);p.connected_regions=(const uint32_t **)(context+0x40);
  p.cache=(Ra2PathNodeCache){{stamps[0],costs[0]},{stamps[1],costs[1]},(uint32_t *)(context+0x28)};p.grid_width=512;
  Ra2PathPreparationServices v={NULL,c_reference,c_cell,c_kind,c_type,c_bridge,c_height,c_flag,c_create,c_toggle,c_facing,c_adjacent};
  Ra2PathPreparationResult stop=ra2_path_prepare(&p,&v);++stops[stop];ready=stop==RA2_PREPARE_READY;
  if(stop==RA2_PREPARE_EMPTY_ROOT&&*p.obstacle_mode)toggle();capture(&actual);
  if(ready){actual.root=(uint32_t)(uintptr_t)p.root;actual.limit=(uint32_t)p.expansion_limit;actual.ignore=p.ignore_soft_obstacles;actual.blocked=p.continue_at_blocked_goal;actual.regions=(uint32_t)(uintptr_t)p.saved_connected_regions;}
  if(memcmp(&expected,&actual,sizeof(actual))){size_t i=0;while(((uint8_t *)&expected)[i]==((uint8_t *)&actual)[i])++i;printf("prepare mismatch case=%u offset=%u events=%u/%u ready=%u/%u\n",n,(unsigned)i,expected.event_count,actual.event_count,expected.ready,actual.ready);return 1;}
 }
 for(unsigned i=0;i<4;++i)if(!stops[i])return 1;
 printf("{\"passed\":true,\"cases\":8192,\"stop_cases\":[%u,%u,%u,%u],\"engine_services_stubbed\":true,\"ordered_callbacks_compared\":true}\n",stops[0],stops[1],stops[2],stops[3]);return 0;
}
static Ra2RegionRouteNode region_nodes[256];
static uint32_t marks[70000],saved_marks[70000],counts[3],saved_counts[3];
static uint16_t routes[1500],saved_routes[1500];
static int route_cases(void){
 *(uint8_t *)0x42A1A6=0xC3;
 for(unsigned n=0;n<4096;++n){
  memset(context,0,sizeof(context));memset(region_nodes,0xA5,sizeof(region_nodes));memset(stack_space,0,sizeof(stack_space));random_state=n+12345;
  unsigned length=n%128+1,pass=n%3;int32_t previous=-1;Ra2RegionRouteNode *end=NULL;
  for(unsigned i=0;i<length;++i){unsigned index=i*73%256;end=&region_nodes[index];*end=(Ra2RegionRouteNode){previous,random_u32()%((n%19)?1024:70000),0,(int32_t)i};previous=(int32_t)index;}
  memset(marks,0xA5,sizeof(marks));memset(routes,0xA5,sizeof(routes));memset(counts,0xA5,sizeof(counts));
  U(context+0x28)=n;U(context+0x64)=(uint32_t)(uintptr_t)region_nodes;
  guest_stack=(uint32_t)(uintptr_t)(stack_space+8192);uint32_t *f=(uint32_t *)(uintptr_t)guest_stack;f[0x38/4]=pass;f[0x5C/4]=(uint32_t)(uintptr_t)marks;
  /* Original routes/counts live at context+BC/C74; use a larger context. */
  static unsigned char region_context[0xD00];memset(region_context,0xA5,sizeof(region_context));U(region_context+0x28)=n;U(region_context+0x64)=(uint32_t)(uintptr_t)region_nodes;
  reg_edi=(uint32_t)(uintptr_t)region_context;reg_esi=pass;reg_eax=(uint32_t)(uintptr_t)end;entry=0x42A12A;original();
  memcpy(saved_marks,marks,sizeof(marks));memcpy(saved_routes,region_context+0xBC,sizeof(routes));memcpy(saved_counts,region_context+0xC74,sizeof(counts));
  memset(marks,0xA5,sizeof(marks));ra2_region_route_publish(region_nodes,end,n,marks,routes+pass*500,counts+pass);
  if(memcmp(saved_marks,marks,sizeof(marks))||memcmp(saved_routes,routes,sizeof(routes))||memcmp(saved_counts,counts,sizeof(counts))){printf("region route mismatch case=%u\n",n);return 1;}
 }
 puts("{\"passed\":true,\"cases\":4096,\"three_route_layers\":true,\"high_region_ids\":true,\"root_not_marked\":true}");return 0;
}
static Ra2PathLink links[128];static Ra2SearchNode end_node;static uint32_t cell_refs[128];static unsigned char path_cells[128][0x28];
static int32_t directions[128],saved_directions[128],saved_levels[128];
static Ra2PathPoint read_point(void *s,void *ref){(void)s;Ra2PathPoint p;memcpy(&p,(void *)(uintptr_t)(U(ref)+0x24),4);return p;}
static int rebuild_cases(void){
 *(uint8_t *)0x84E7D4|=1;
 for(unsigned n=0;n<16384;++n){
  random_state=n+12345;unsigned length=n%127+1;
  for(unsigned i=0;i<length;++i){Ra2PathPoint p={(int16_t)(random_u32()%32),(int16_t)(random_u32()%32)};
   if(i&&i%3){Ra2PathPoint q=read_point(NULL,&cell_refs[i-1]);p.x=(int16_t)(q.x+(int)(random_u32()%3)-1);p.y=(int16_t)(q.y+(int)(random_u32()%3)-1);}
   memcpy(path_cells[i]+0x24,&p,4);cell_refs[i]=(uint32_t)(uintptr_t)path_cells[i];links[i]=(Ra2PathLink){&cell_refs[i],(int32_t)(random_u32()%12),i?&links[i-1]:NULL};
  }
  end_node=(Ra2SearchNode){&links[length-1],0,((float)(int32_t)(n%16384)-8192.0f)*0.125f,(int32_t)length};
  memset(directions,0xA5,sizeof(directions));memset((void *)0x84C858,0xA5,sizeof(saved_levels));memset(stack_space,0,sizeof(stack_space));
  guest_stack=(uint32_t)(uintptr_t)(stack_space+8192);uint32_t *s=(uint32_t *)(uintptr_t)guest_stack;s[1]=(uint32_t)(uintptr_t)&end_node;s[2]=(uint32_t)(uintptr_t)directions;
  entry=0x428370;original();Ra2RebuiltPath native_path=*(Ra2RebuiltPath *)0x84C810;memcpy(saved_directions,directions,sizeof(directions));memcpy(saved_levels,(void *)0x84C858,sizeof(saved_levels));
  memset(directions,0xA5,sizeof(directions));int32_t levels[128];memset(levels,0xA5,sizeof(levels));Ra2RebuiltPath path;
  ra2_path_rebuild(&end_node,directions,levels,(int32_t *)0x7CF100,read_point,NULL,&path);path.surface_levels=(int32_t *)0x84C858;
  if(memcmp(&native_path,&path,sizeof(path))||memcmp(directions,saved_directions,sizeof(directions))||memcmp(levels,saved_levels,sizeof(levels))){printf("path rebuild mismatch case=%u\n",n);return 1;}
 }
 puts("{\"passed\":true,\"cases\":16384,\"mapped_original_function\":true,\"adjacent_and_special_links\":true,\"score_truncation\":true}");return 0;
}
int main(int argc,char **argv){if(argc!=3)return 2;hold_image();map_original_image(argv[1]);int phase=atoi(argv[2]);return phase==0?prepare_cases():phase==1?route_cases():rebuild_cases();}
