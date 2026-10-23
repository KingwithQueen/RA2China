#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ground_path_local.h"
#include "ground_path_completion.h"
#include "native_probe_host.h"
#define U(a) (*(uint32_t *)(uintptr_t)(a))
static uint32_t host_stack,guest_stack,return_slot,entry,reg_esi,reg_ebx,result,exit_stack,stack_space[16384];
static __declspec(naked) void original(void){__asm{
 pushad
 mov host_stack,esp
 lea eax,returned
 mov edx,return_slot
 mov [edx],eax
 mov esp,guest_stack
 mov esi,reg_esi
 mov ebx,reg_ebx
 mov ecx,123456h
 jmp entry
returned:
 mov result,eax
 mov exit_stack,esp
 mov esp,host_stack
 popad
 ret
}}
static void patch(uintptr_t address,uintptr_t target){*(uint8_t *)address=0xE9;U(address+1)=(uint32_t)(target-address-5);}
static void set_control(uint16_t control){__asm fldcw control}
static uint32_t random_state,events[8192],event_count,test_case,lookups,passages,threats;
static unsigned char cells[64][0x148],actor[0x200],context[128],connection[0x30];
static uint32_t vtable[128],connection_table[1];static int32_t directions[128],levels[128],anchor_index;
static Ra2PathPoint anchor,delta;static int32_t first_count,second_count,initial_level,final_segment,buffer_count;
static uint16_t control;static Ra2SearchNode end_node;static Ra2RebuiltPath rebuilt;
static uint32_t random_u32(void){random_state=random_state*1664525u+1013904223u;return random_state;}
static uint32_t bits(Ra2PathPoint p){uint32_t x;memcpy(&x,&p,4);return x;}
static void event(uint32_t value){if(event_count>=8192)exit(3);events[event_count++]=value;}
static double owner_factor(void *s){
 (void)s;static const double values[]={0.0,0.00001,0.005,0.01,0.25,1.0,1.0000000000000002,0.9999999999999999,-1.0};
 event(10);return values[test_case%9];
}
static uint32_t owner_house(void *s){(void)s;return U(actor+0x1B4);}
static uintptr_t lookup(void *s,const Ra2PathPoint *p){
 (void)s;event(20);event(bits(*p));++lookups;unsigned index=((uint32_t)(uint16_t)p->x+(uint32_t)(uint16_t)p->y*31)&63;
 unsigned char *cell=cells[index];cell[0x11B]=(uint8_t)((test_case+index+lookups)%9-4);
 U(cell+0x140)=((test_case+index)%2?0x100u:0u)|(test_case%13==0 && (index+lookups)%7==0?0x40000u:0u);
 *(int16_t *)(cell+0x116)=(int16_t)(test_case%3?0:-1);return (uintptr_t)cell;
}
static Ra2LocalPathCell properties(void *s,uintptr_t cell){(void)s;return (Ra2LocalPathCell){(int8_t)*(uint8_t *)(cell+0x11B),U(cell+0x140)};}
static Ra2PathPoint connection_exit(void *s,const Ra2PathPoint *point){
 uintptr_t cell=lookup(s,point);Ra2PathPoint p={0,0};if(*(int16_t *)(cell+0x116)!=-1)memcpy(&p,connection+0x28,4);return p;
}
static int32_t passage(void *s,uintptr_t cell,int32_t direction,int32_t level){
 (void)s;event(30);event((uint32_t)((cell-(uintptr_t)cells)/sizeof(cells[0])));event((uint32_t)direction);event((uint32_t)level);++passages;
 if(test_case%19==0){*(uint8_t *)(cell+0x11B)=(uint8_t)(level-4);U(cell+0x140)|=0x100;}
 return test_case%5==0 && (passages+test_case)%3==0?2:0;
}
static int32_t threat(void *s,const Ra2PathPoint *point,uint32_t house){
 (void)s;if(house!=0x1234)exit(3);event(40);event(bits(*point));++threats;
 return test_case%17==0?0:(int32_t)((bits(*point)^test_case)%7)-2;
}
static double __fastcall native_factor(void *s,void *d){(void)s;(void)d;return owner_factor(NULL);}
static void *__fastcall native_lookup(void *s,void *d,const Ra2PathPoint *p){(void)s;(void)d;return (void *)lookup(NULL,p);}
static int32_t __fastcall native_passage(void *s,void *d,void *cell,int32_t direction,int32_t level,uint32_t source,uint32_t final){
 (void)s;(void)d;if(source||final!=1)exit(3);return passage(NULL,(uintptr_t)cell,direction,level);
}
static int32_t __fastcall native_threat(void *s,void *d,const Ra2PathPoint *p,uint32_t house){(void)s;(void)d;return threat(NULL,p,house);}
static void setup(unsigned n,unsigned phase){
 test_case=n;random_state=n+12345;event_count=lookups=passages=threats=0;
 memset(cells,0,sizeof(cells));memset(events,0,sizeof(events));memset(directions,0xA5,sizeof(directions));memset(levels,0xA5,sizeof(levels));
 memset(context,0,sizeof(context));memset(&rebuilt,0,sizeof(rebuilt));memset(stack_space,0,sizeof(stack_space));
 for(unsigned i=0;i<128;++i){directions[i]=(int32_t)((random_u32()>>16)%9);levels[i]=(int32_t)((random_u32()>>16)%13)-4;}
 anchor=(Ra2PathPoint){(int16_t)(n%2?32767:n%37),(int16_t)(n%3?-(int)(n%31):-32768)};anchor_index=(int32_t)0xA5A5A5A5;
 first_count=(int32_t)(n%9);second_count=(int32_t)((n/9)%9);
 int32_t first=(int32_t)(n%8),second=(first+(n%2?2:6))&7;
 if(n%11==0)first=8;if(n%13==0)second=8;
 if(phase==1){
  for(int32_t i=0;i<first_count;++i)directions[i]=first;
  for(int32_t i=0;i<=second_count;++i)directions[first_count+i]=second;
  if(n%29==0 && first_count>2)directions[1]=8;
 }
 if(phase==0)for(unsigned i=0;i<128;++i)if((random_u32()>>16)%3==0)directions[i]=-2;
 delta=(Ra2PathPoint){(int16_t)((int)(n%15)-7),(int16_t)((int)((n/15)%15)-7)};
 initial_level=(int32_t)(n%13)-4;final_segment=(int32_t)(n%4==0?0:n%4==1?1:n%4==2?256:257);buffer_count=20;
 U(actor)=(uint32_t)(uintptr_t)vtable;U(actor+0x1B4)=0x1234;
 Ra2PathPoint exit={17,-23};memcpy(connection+0x28,&exit,4);connection_table[0]=(uint32_t)(uintptr_t)connection;U(0x8661CC)=(uint32_t)(uintptr_t)connection_table;
 guest_stack=(uint32_t)(uintptr_t)(stack_space+8192);return_slot=guest_stack;
 reg_esi=(uint32_t)(uintptr_t)context;reg_ebx=(uint32_t)(uintptr_t)actor;
 uint32_t *a=(uint32_t *)(uintptr_t)guest_stack;
 if(phase==0){entry=0x429570;a[1]=(uint32_t)(uintptr_t)directions;a[2]=n%64;a[3]=n%17==0?a[2]+1:n%((unsigned)a[2]+1);a[4]=(uint32_t)(uintptr_t)&anchor_index;a[5]=(uint32_t)(uintptr_t)&anchor;}
 if(phase==1){entry=0x428CF0;a[1]=(uint32_t)(uintptr_t)actor;a[2]=(uint32_t)(uintptr_t)directions;a[3]=(uint32_t)(uintptr_t)levels;a[4]=(uint32_t)first_count;a[5]=(uint32_t)second_count;a[6]=(uint32_t)(uintptr_t)&anchor;}
 if(phase==2){entry=0x4296F0;a[1]=(uint32_t)(uintptr_t)directions;a[2]=(uint32_t)buffer_count;a[3]=(uint32_t)(uintptr_t)&anchor;a[4]=(uint32_t)(uintptr_t)&delta;a[5]=(uint32_t)(uintptr_t)actor;a[6]=(uint32_t)initial_level;a[7]=(uint32_t)final_segment;}
}
typedef struct Capture {
 int32_t directions[128],levels[128],anchor_index;Ra2PathPoint anchor,delta;
 unsigned char cells[64][0x148],context[128];Ra2RebuiltPath rebuilt;
 uint32_t events[8192],count,result;
} Capture;
static Capture expected,actual;
static void capture(Capture *r,uint32_t value){
 memset(r,0,sizeof(*r));memcpy(r->directions,directions,sizeof(directions));memcpy(r->levels,levels,sizeof(levels));r->anchor=anchor;r->delta=delta;r->anchor_index=anchor_index;
 memcpy(r->cells,cells,sizeof(cells));memcpy(r->context,context,sizeof(context));r->rebuilt=rebuilt;memcpy(r->events,events,sizeof(events));r->count=event_count;r->result=value;
}
static Ra2RebuiltPath *complete_rebuild(void *s,Ra2SearchNode *node){
 (void)s;if(node!=&end_node)exit(3);event(50);rebuilt.length=17;rebuilt.directions=directions;rebuilt.surface_levels=levels;return test_case%23?&rebuilt:NULL;
}
static void complete_smooth(void *s,Ra2RebuiltPath *path){(void)s;event(60);event(path==&rebuilt);directions[0]=(int32_t)test_case;}
static void complete_post(void *s,Ra2RebuiltPath *path){(void)s;event(70);event(path==&rebuilt);levels[0]=(int32_t)test_case;U(context+0x3C)=test_case%3;}
static void complete_restore(void *s){(void)s;event(80);U(context+0x3C)=0;}
static void *__fastcall native_rebuild(void *s,void *d,Ra2SearchNode *node,int32_t *dirs){(void)s;(void)d;if(dirs!=directions)exit(3);return complete_rebuild(NULL,node);}
static void __fastcall native_smooth(void *s,void *d,Ra2RebuiltPath *path,uint32_t owner){(void)s;(void)d;if(owner!=(uint32_t)(uintptr_t)actor)exit(3);complete_smooth(NULL,path);}
static void __fastcall native_post(void *s,void *d,Ra2RebuiltPath *path,uint32_t owner){(void)s;(void)d;if(owner!=(uint32_t)(uintptr_t)actor)exit(3);complete_post(NULL,path);}
static void __fastcall native_restore(void *s,void *d,uint32_t owner){(void)s;(void)d;if(owner!=(uint32_t)(uintptr_t)actor)exit(3);complete_restore(NULL);}
static Ra2PathCompletion completion_setup(unsigned n){
 setup(n,3);unsigned preparation=n%4;static const uint32_t expanded[]={0,1,9999,10000,10001,0xFFF7,0xFFF8};
 uint32_t count=expanded[(n/4)%7];int32_t limit=n%5?(int32_t)count:17;
 end_node.path_length=(int32_t)((n/28)%6)-1;Ra2SearchNode *current=n%11?&end_node:NULL;
 U(context+0x3C)=n%2;
 uint32_t *a=(uint32_t *)(uintptr_t)guest_stack;a[0x14/4]=(uint32_t)(uintptr_t)current;a[0x28/4]=count;
 a[0x68/4]=(uint32_t)(uintptr_t)actor;a[0x6C/4]=(uint32_t)(uintptr_t)directions;a[0x70/4]=(uint32_t)limit;
 return_slot=guest_stack+0x5C;entry=preparation<2?0x427D2E:preparation==2?0x427D1F:0x427CBB;
 return (Ra2PathCompletion){(Ra2PathPreparationResult)preparation,current,count,limit,(int32_t *)(context+0x3C)};
}
int main(int argc,char **argv){
 if(argc!=3)return 2;hold_image();map_original_image(argv[1]);((void(__cdecl *)(void))(uintptr_t)0x491620)();unsigned phase=(unsigned)atoi(argv[2]);
 patch(0x4CAFB0,(uintptr_t)native_factor);patch(0x548070,(uintptr_t)native_lookup);patch(0x54E3A0,(uintptr_t)native_threat);vtable[0x194/4]=(uint32_t)(uintptr_t)native_passage;
 if(phase==3){patch(0x428370,(uintptr_t)native_rebuild);patch(0x428AE0,(uintptr_t)native_smooth);patch(0x4290C0,(uintptr_t)native_post);patch(0x4285D0,(uintptr_t)native_restore);}
 unsigned cases=phase==1||phase==2?12288:8192,successes=0,failures=0;uint64_t total_events=0;
 const unsigned precision[]={0,0x200,0x300};
 for(unsigned n=0;n<cases;++n){
  control=(uint16_t)(0x7F|precision[(n/1024)/4%3]|(((n/1024)%4)<<10));set_control(control);
  if(phase==3)completion_setup(n);else setup(n,phase);
  original();uint32_t value=phase==0?0:phase==2?(result&255):result;capture(&expected,value);
  uint32_t expected_stack=guest_stack+(phase==0?24:phase==1?28:phase==2?32:0x78);
  if(exit_stack!=expected_stack){printf("stack mismatch phase=%u case=%u\n",phase,n);return 1;}
  set_control(control);Ra2PathCompletion finish={0};
  if(phase==3)finish=completion_setup(n);else setup(n,phase);
  Ra2LocalPathServices v={NULL,(Ra2PathPoint *)0x851A70,&control,owner_factor,owner_house,lookup,properties,connection_exit,passage,threat};
  value=0;
  if(phase==0){uint32_t *a=(uint32_t *)(uintptr_t)guest_stack;ra2_path_find_anchor(directions,(int32_t)a[2],(int32_t)a[3],&anchor_index,&anchor,(Ra2PathPoint *)0x851A70);}
  if(phase==1)value=(uint32_t)ra2_path_shorten_turn(directions,levels,first_count,second_count,&anchor,&v);
  if(phase==2)value=(uint32_t)ra2_path_rewrite_segment(directions,buffer_count,&anchor,&delta,initial_level,final_segment,&v);
  if(phase==3){Ra2PathCompletionServices c={NULL,complete_rebuild,complete_smooth,complete_post,complete_restore};value=(uint32_t)(uintptr_t)ra2_path_complete(&finish,&c);}
  capture(&actual,value);
  if(memcmp(&expected,&actual,sizeof(actual))){size_t i=0;while(((uint8_t *)&expected)[i]==((uint8_t *)&actual)[i])++i;printf("local mismatch phase=%u case=%u byte=%u events=%u/%u result=%u/%u native=%02x C=%02x\n",phase,n,(unsigned)i,expected.count,actual.count,expected.result,actual.result,((uint8_t *)&expected)[i],((uint8_t *)&actual)[i]);return 1;}
  total_events+=event_count;if(value)++successes;else ++failures;
 }
 if((phase==1||phase==2||phase==3) && (!successes||!failures))return 1;
 printf("{\"passed\":true,\"phase\":%u,\"cases\":%u,\"successes\":%u,\"failures_or_zero_prefix\":%u,\"event_words_compared\":%llu,\"numeric_modes\":%u,\"full_buffers_and_ordered_callbacks_compared\":true,\"engine_services_stubbed\":true,\"original_direction_initializer_executed\":true,\"original_stack_cleanup_verified\":true}\n",phase,cases,successes,failures,(unsigned long long)total_events,phase==1||phase==2?12u:1u);return 0;
}
