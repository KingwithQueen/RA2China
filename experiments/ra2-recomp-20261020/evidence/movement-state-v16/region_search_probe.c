#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <float.h>
#include "ground_region_search.h"
#include "native_probe_host.h"
#define U(a) (*(uint32_t *)(uintptr_t)(a))
#define N 16
#define POOL 512
static uint32_t host_stack,guest_stack,entry=0x429B60,reg_ecx,result,stack_space[16384];
static __declspec(naked) void original(void){__asm{
 pushad
 mov host_stack,esp
 mov esp,guest_stack
 lea eax,returned
 mov [esp],eax
 mov ecx,reg_ecx
 jmp entry
returned:
 mov result,eax
 mov esp,host_stack
 popad
 ret
}}
static void set_control(uint16_t control){__asm fldcw control}
static void patch(uintptr_t address,uintptr_t target){*(uint8_t *)address=0xE9;U(address+1)=(uint32_t)(target-address-5);}
static unsigned test_case,event_count;static uint32_t random_state,events[8192];
static unsigned char context[0xD00],actor[0x200],records[3][N][36];
static uint32_t connected[3][N],visited[3][N],pairs[3][4];
static float costs[3][N];static Ra2RegionEdge edges[3][N][3];
static Ra2RegionRouteNode nodes[POOL];static Ra2RegionRouteNode *items[128];static Ra2RegionHeap heap;
static Ra2PathPoint start={0,0},goal={1,0};static int16_t region_table[2][5];
static uint32_t random_u32(void){random_state=random_state*1664525u+1013904223u;return random_state;}
static void event(uint32_t code){if(event_count>=8192)exit(3);events[event_count++]=code;}
static double c_factor(void *s){(void)s;event(10);return test_case%7==0?0.00001:test_case%5==0?0.0:1.30000000000001;}
static uint32_t c_house(void *s){(void)s;return U(actor+0x1B4);}
static int32_t c_region_at(void *s,const Ra2PathPoint *p,unsigned layer){(void)s;event(20u+(unsigned)p->x);return region_table[p->x][layer];}
static Ra2RegionView c_region(void *s,unsigned layer,uint32_t id){(void)s;unsigned char *p=records[layer][id];return (Ra2RegionView){(Ra2RegionEdge *)(uintptr_t)U(p+4),(int32_t)U(p+0x10),*(uint16_t *)(p+0x18),U(p+0x1C)};}
static int32_t c_penalty(void *s,uint32_t house,unsigned layer,uint32_t from,uint32_t to){
 (void)s;if(house!=0x1234)exit(3);event(0x10000u|layer<<12|from<<6|to);return (int32_t)((test_case+from*7+to*13)%5);
}
static Ra2BlockedRegionEdges c_blocked(void *s,unsigned layer){(void)s;return (Ra2BlockedRegionEdges){pairs[layer],(int32_t)U(context+0x84+layer*24)};}
static double __fastcall native_factor(void *s,void *d){(void)s;(void)d;return c_factor(NULL);}
static uint32_t __fastcall native_lookup(void *s,void *d,Ra2PathPoint *p){(void)s;(void)d;event(20u+(unsigned)p->x);return (uint32_t)p->x;}
static int32_t __fastcall native_penalty(void *s,void *d,uint32_t h,unsigned l,uint32_t f,uint32_t t){(void)s;(void)d;return c_penalty(NULL,h,l,f,t);}
typedef struct Capture {
 unsigned char context[0xD00];uint32_t connected[3][N],visited[3][N];float costs[3][N];
 Ra2RegionRouteNode nodes[POOL];Ra2RegionHeap heap;Ra2RegionRouteNode *items[128];
 uint32_t events[8192],event_count,success;
} Capture;
static Capture expected,actual;
static void setup(unsigned n){
 test_case=n;random_state=n+12345;event_count=0;memset(events,0,sizeof(events));memset(context,0xA5,sizeof(context));
 memset(nodes,0xA5,sizeof(nodes));memset(connected,0,sizeof(connected));memset(visited,0,sizeof(visited));memset(costs,0xA5,sizeof(costs));
 memset(items,0,sizeof(items));heap=(Ra2RegionHeap){n%3,n%11==0?2:n%13==0?4:128,items,0,UINT32_MAX};
 for(unsigned j=0;j<heap.count;++j)items[j+1]=&nodes[j];
 U(context+0x28)=n+123;U(context+0x64)=(uint32_t)(uintptr_t)nodes;U(context+0x68)=(uint32_t)(uintptr_t)&heap;
 U(actor+0x1B4)=0x1234;
 for(unsigned k=0;k<8;++k){U(0x7E00C4+k*4)=n%23==0&&k==3?2:1;*(float *)(0x79C4A4+k*4)=0.125f+(float)k*0.25f;}
 for(unsigned l=0;l<3;++l){
  U(0x83256C+l*24)=(uint32_t)(uintptr_t)records[l];
  region_table[0][l]=0;region_table[1][l]=(int16_t)(n%17==0||n%19==l?0:15);
  U(context+0x40+l*4)=(uint32_t)(uintptr_t)connected[l];U(context+0x4C+l*4)=(uint32_t)(uintptr_t)visited[l];U(context+0x58+l*4)=(uint32_t)(uintptr_t)costs[l];
  U(context+0x78+l*24)=(uint32_t)(uintptr_t)pairs[l];U(context+0x84+l*24)=n%4?0:2;
  pairs[l][0]=((n%14)<<16)|(n%14+1);pairs[l][1]=0x00010004;
  for(unsigned r=0;r<N;++r){
   unsigned char *p=records[l][r];memset(p,0,sizeof(records[l][r]));U(p+4)=(uint32_t)(uintptr_t)edges[l][r];
   U(p+0x10)=r==15||n%29==0?0:3;*(uint16_t *)(p+0x18)=(uint16_t)(n%2?r:r%4);U(p+0x1C)=n%3==0?1:r%4;
   edges[l][r][0]=(Ra2RegionEdge){(r+1)%N,(uint8_t)(random_u32()%2),{0}};
   edges[l][r][1]=(Ra2RegionEdge){(r+3)%N,(uint8_t)(random_u32()%2),{0}};
   edges[l][r][2]=(Ra2RegionEdge){random_u32()%N,(uint8_t)(random_u32()%2),{0}};
   if(n%31==0 && r%3==0){visited[l][r]=n+123;costs[l][r]=0.25f;}
  }
 }
 U(0x83254C)=(uint32_t)(uintptr_t)region_table;memset(stack_space,0,sizeof(stack_space));
 guest_stack=(uint32_t)(uintptr_t)(stack_space+8192);uint32_t *a=(uint32_t *)(uintptr_t)guest_stack;
 a[1]=(uint32_t)(uintptr_t)&start;a[2]=(uint32_t)(uintptr_t)&goal;a[3]=0;a[4]=n%9?(uint32_t)(uintptr_t)actor:0;
 reg_ecx=(uint32_t)(uintptr_t)context;
}
static void capture(Capture *out,int success){
 memset(out,0,sizeof(*out));memcpy(out->context,context,sizeof(context));memcpy(out->connected,connected,sizeof(connected));
 memcpy(out->visited,visited,sizeof(visited));memcpy(out->costs,costs,sizeof(costs));memcpy(out->nodes,nodes,sizeof(nodes));
 out->heap=heap;memcpy(out->items,items,sizeof(items));memcpy(out->events,events,sizeof(events));out->event_count=event_count;out->success=(unsigned)success;
}
int main(int argc,char **argv){
 if(argc!=2)return 2;hold_image();map_original_image(argv[1]);patch(0x4CAFB0,(uintptr_t)native_factor);patch(0x54FAB0,(uintptr_t)native_lookup);patch(0x567D20,(uintptr_t)native_penalty);
 unsigned successes=0,failures=0;const unsigned modes[]={0x000,0x200,0x300};
 for(unsigned mode=0;mode<12;++mode)for(unsigned n=0;n<512;++n){
  unsigned cw=0x7F|modes[mode/4]|((mode%4)<<10);set_control((uint16_t)cw);setup(n);original();capture(&expected,(result&255)!=0);
  set_control((uint16_t)cw);setup(n);Ra2RegionSearch s={0};s.generation=(uint32_t *)(context+0x28);s.nodes=nodes;s.heap=&heap;
  s.terrain_allowed=(int32_t *)0x7E00C4;s.terrain_cost=(float *)0x79C4A4;uint16_t control=(uint16_t)cw;s.numeric_control=&control;s.integer_conversion_control=(uint16_t)U(0x7D8964);
  for(unsigned l=0;l<3;++l)s.layers[l]=(Ra2RegionLayer){connected[l],visited[l],costs[l],(uint16_t *)(context+0xBC+l*1000),(uint32_t *)(context+0xC74+l*4)};
  Ra2RegionSearchServices v={NULL,c_factor,c_house,c_region_at,c_region,c_penalty,c_blocked};
  int ok=ra2_region_search(&s,&v,&start,&goal,n%9!=0);capture(&actual,ok);
  if(memcmp(&actual,&expected,sizeof(actual))){size_t i=0;while(((uint8_t *)&actual)[i]==((uint8_t *)&expected)[i])++i;printf("region mismatch mode=%u case=%u byte=%u events=%u/%u result=%u/%u native=%02x C=%02x\n",mode,n,(unsigned)i,expected.event_count,actual.event_count,expected.success,actual.success,((uint8_t *)&expected)[i],((uint8_t *)&actual)[i]);return 1;}
  if(ok)++successes;else ++failures;
 }
 if(!successes||!failures)return 1;
 printf("{\"passed\":true,\"cases\":6144,\"successes\":%u,\"failures\":%u,\"numeric_modes\":12,\"three_layers\":true,\"same_region_shortcut\":true,\"heap_capacity_and_ties\":true,\"ordered_engine_callbacks_compared\":true,\"engine_services_stubbed\":true}\n",successes,failures);return 0;
}
