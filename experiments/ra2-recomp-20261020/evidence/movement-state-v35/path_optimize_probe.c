#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ground_path_optimize.h"
#include "native_probe_host.h"
#define U(a) (*(uint32_t *)(uintptr_t)(a))
static uint32_t host_stack,guest_stack,entry,stack_space[16384];
static __declspec(naked) void original(void){__asm{
 pushad
 mov host_stack,esp
 mov esp,guest_stack
 lea eax,returned
 mov [esp],eax
 mov ecx,123456h
 jmp entry
returned:
 mov esp,host_stack
 popad
 ret
}}
static void patch(uintptr_t address,uintptr_t target){*(uint8_t *)address=0xE9;U(address+1)=(uint32_t)(target-address-5);}
static unsigned test_case,event_count,shortens,rewrites,final_rewrites,connections,retained;
static uint32_t random_state,events[4096];static int32_t directions[128],levels[128];static Ra2RebuiltPath path;
static unsigned char cell[0x148],connection[0x30];static uint32_t connection_table[1];
static uint32_t random_u32(void){random_state=random_state*1664525u+1013904223u;return random_state;}
static uint32_t bits(Ra2PathPoint p){uint32_t x;memcpy(&x,&p,4);return x;}
static void event(uint32_t x){if(event_count>=4096)exit(3);events[event_count++]=x;}
static Ra2PathPoint add(Ra2PathPoint a,Ra2PathPoint b){return (Ra2PathPoint){(int16_t)(a.x+b.x),(int16_t)(a.y+b.y)};}
static Ra2PathPoint c_connection(void *s,const Ra2PathPoint *p){
 (void)s;event(1);event(bits(*p));++connections;
 return test_case%3?(Ra2PathPoint){17,-23}:(Ra2PathPoint){0,0};
}
static int32_t c_shorten(void *s,int32_t *dirs,int32_t *heights,int32_t first,int32_t second,Ra2PathPoint *anchor){
 (void)s;if(dirs-directions!=heights-levels)exit(3);event(2);event((uint32_t)(dirs-directions));event((uint32_t)first);event((uint32_t)second);event(bits(*anchor));++shortens;
 int32_t advance=first+second-1;
 for(int32_t i=0;i<advance;++i)*anchor=add(*anchor,((Ra2PathPoint *)0x851A70)[dirs[i]&7]);
 if(test_case%2)dirs[advance]=(dirs[advance]+2)&7;
 heights[advance]=(int32_t)test_case;
 return advance;
}
static void c_anchor(void *s,int32_t *dirs,int32_t end,int32_t start,int32_t *out_index,Ra2PathPoint *point){
 (void)s;if(dirs!=directions)exit(3);event(3);event((uint32_t)end);event((uint32_t)start);event(bits(*point));
 *out_index=test_case%2?start:end;
 for(int32_t i=end;i>=*out_index;--i)if(dirs[i]>=0 && dirs[i]<8){Ra2PathPoint step=((Ra2PathPoint *)0x851A70)[dirs[i]];*point=add(*point,(Ra2PathPoint){(int16_t)-step.x,(int16_t)-step.y});}
}
static void c_rewrite(void *s,int32_t *dirs,int32_t count,Ra2PathPoint *anchor,Ra2PathPoint *delta,int32_t level,int final_segment){
 (void)s;event(4);event((uint32_t)(dirs-directions));event((uint32_t)count);event(bits(*anchor));event(bits(*delta));event((uint32_t)level);event((unsigned)final_segment);++rewrites;if(final_segment)++final_rewrites;
 if(test_case%3 && count>0)dirs[count-1]=-2;else ++retained;
 anchor->x=(int16_t)(anchor->x+1);delta->y=(int16_t)(delta->y-1);
}
static void *__fastcall native_connection(void *s,void *d,const Ra2PathPoint *p){(void)s;(void)d;c_connection(NULL,p);return cell;}
static int32_t __fastcall native_shorten(void *s,void *d,uint32_t owner,int32_t *dirs,int32_t *heights,int32_t first,int32_t second,Ra2PathPoint *p){(void)s;(void)d;if(owner!=0x789ABC)exit(3);return c_shorten(NULL,dirs,heights,first,second,p);}
static void __fastcall native_anchor(void *s,void *d,int32_t *dirs,int32_t end,int32_t start,int32_t *out,Ra2PathPoint *point){(void)s;(void)d;c_anchor(NULL,dirs,end,start,out,point);}
static void __fastcall native_rewrite(void *s,void *d,int32_t *dirs,int32_t count,Ra2PathPoint *point,Ra2PathPoint *delta,uint32_t owner,int32_t level,int final_segment){(void)s;(void)d;if(owner!=0x789ABC)exit(3);c_rewrite(NULL,dirs,count,point,delta,level,final_segment);}
typedef struct Capture {Ra2RebuiltPath path;int32_t dirs[128],levels[128];uint32_t events[4096],count;} Capture;
static Capture expected,actual;
static void setup(unsigned n,unsigned phase){
 test_case=n;random_state=n+12345;event_count=0;memset(events,0,sizeof(events));memset(directions,0xA5,sizeof(directions));memset(levels,0xA5,sizeof(levels));
 unsigned length=n%96+1;
 static const int32_t final_case[]={3,6,2,3,4,5,5,6,6,3,7,1,3,1,2,0,1,0,2,2,4,4,6,3,5};
 if(phase && n%37==0)length=26;
 for(unsigned i=0;i<length;++i){
  unsigned direction=(random_u32()>>16)%(n%2?8u:9u);
  if(n%5==0)direction=(i/(n%7+1)%2)?3:1;
  if(n%7==0)direction=(i%8<4)?0:4;
  if(phase && n%11==0 && i%3==0)directions[i]=-2;else directions[i]=(int32_t)direction;
  levels[i]=(int32_t)(random_u32()%4);
 }
 if(phase && n%37==0)memcpy(directions,final_case,sizeof(final_case));
 directions[length-1]=-1;
 if(phase && n%17==0 && length>2)directions[length/2]=-1;
 path=(Ra2RebuiltPath){{(int16_t)(n%32768),(int16_t)(n%2?-4:32767)},17,(int32_t)length,directions,0xA5A5,levels,{9,13}};
 *(int16_t *)(cell+0x116)=(int16_t)(n%3?0:-1);Ra2PathPoint p={17,-23};memcpy(connection+0x28,&p,4);
 connection_table[0]=(uint32_t)(uintptr_t)connection;U(0x8661CC)=(uint32_t)(uintptr_t)connection_table;
 memset(stack_space,0,sizeof(stack_space));guest_stack=(uint32_t)(uintptr_t)(stack_space+8192);uint32_t *a=(uint32_t *)(uintptr_t)guest_stack;a[1]=(uint32_t)(uintptr_t)&path;a[2]=0x789ABC;
}
static void capture(Capture *out){memset(out,0,sizeof(*out));out->path=path;memcpy(out->dirs,directions,sizeof(directions));memcpy(out->levels,levels,sizeof(levels));memcpy(out->events,events,sizeof(events));out->count=event_count;}
int main(int argc,char **argv){
 if(argc!=3)return 2;hold_image();map_original_image(argv[1]);
 /* Original startup initializes this BSS direction table (491620). */
 ((void(__cdecl *)(void))(uintptr_t)0x491620)();unsigned phase=(unsigned)atoi(argv[2]);
 patch(0x548070,(uintptr_t)native_connection);patch(0x428CF0,(uintptr_t)native_shorten);patch(0x429570,(uintptr_t)native_anchor);patch(0x4296F0,(uintptr_t)native_rewrite);
 entry=phase?0x4290C0:0x428AE0;
 Ra2PathOptimizationServices v={NULL,(Ra2PathPoint *)0x851A70,c_connection,c_shorten,c_anchor,c_rewrite};
 for(unsigned n=0;n<8192;++n){
  setup(n,phase);original();capture(&expected);setup(n,phase);
  if(phase)ra2_path_postprocess(&path,&v);else ra2_path_smooth(&path,&v);capture(&actual);
  if(memcmp(&expected,&actual,sizeof(actual))){size_t i=0;while(((uint8_t *)&expected)[i]==((uint8_t *)&actual)[i])++i;printf("optimization mismatch phase=%u case=%u byte=%u callbacks=%u/%u length=%d/%d native=%02x C=%02x\n",phase,n,(unsigned)i,expected.count,actual.count,expected.path.length,actual.path.length,((uint8_t *)&expected)[i],((uint8_t *)&actual)[i]);return 1;}
 }
 if(phase?!rewrites||!final_rewrites||!retained:!shortens||!connections)return 1;
 printf("{\"passed\":true,\"cases\":8192,\"phase\":%u,\"shorten_callbacks\":%u,\"connection_callbacks\":%u,\"rewrite_callbacks\":%u,\"final_rewrites\":%u,\"retained_segments\":%u,\"ordered_callbacks_and_buffers_compared\":true,\"engine_services_stubbed\":true}\n",phase,shortens,connections,rewrites,final_rewrites,retained);return 0;
}
