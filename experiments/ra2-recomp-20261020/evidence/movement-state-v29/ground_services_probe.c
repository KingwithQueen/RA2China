#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ground_interpolation.h"
#include "ground_prepare_shared.h"
#include "ground_cell_services.h"
#include "native_probe_host.h"
#define U(a) (*(uint32_t *)(uintptr_t)(a))
static uint32_t host_stack,guest_stack,entry,reg_bp,reg_si,reg_bx,reg_cx,result,exit_stack,return_slot;
static uint32_t stack_space[16384],events[256],count,test_case,lookups,shared_result,stopped_head;
static unsigned char actor[0x600],drive[0x80],cells[8][0x148];
static uint32_t vtable[128],grid_slots[262144],house_storage[100000];
#define house (house_storage+20000)
static uint16_t control,conversion;
static Ra2WorldPoint start,sample_point;
static __declspec(naked) void original(void){__asm{
 pushad
 mov host_stack,esp
 mov edx,return_slot
 lea eax,returned
 mov [edx],eax
 mov esp,guest_stack
 mov ebp,reg_bp
 mov esi,reg_si
 mov ebx,reg_bx
 mov ecx,reg_cx
 xor edi,edi
 jmp entry
returned:
 mov result,eax
 mov exit_stack,esp
 mov esp,host_stack
 popad
 ret
}}
static void patch(uintptr_t a,uintptr_t b){*(uint8_t *)a=0xE9;U(a+1)=(uint32_t)(b-a-5);}
static void set_control(uint16_t c){__asm fldcw c}
static void event(uint32_t e){if(count==256)exit(3);events[count++]=e;}
static Ra2WorldPoint position(void *c){(void)c;Ra2WorldPoint p;memcpy(&p,actor+0x88,12);return p;}
static Ra2WorldPoint transform(void *c){
 (void)c;event(10);if(test_case%7==0)U(actor+0x88)+=17;
 U(drive+0x70)^=test_case;return sample_point;
}
static uintptr_t lookup(void *c,Ra2WorldPoint p){
 (void)c;event(20);event((uint32_t)p.x);event((uint32_t)p.y);event((uint32_t)p.z);++lookups;
 unsigned index=lookups==1?0:lookups==2?1:lookups==3?(test_case%3):3;
 if(test_case%11==0 && lookups<4)U(actor+0x8C)+=13;
 return (uintptr_t)cells[index];
}
static Ra2WorldPoint blend(void *c,Ra2WorldPoint p){
 (void)c;float f=ra2_ground_progress_fraction((int32_t)U(drive+0x4C),&ra2_original_ground_path_sampling,control);
 Ra2WorldPoint r=ra2_ground_interpolate_position((Ra2WorldPoint){0,0,0},p,f,control,conversion);control=conversion;return r;
}
static void leave(void *c){(void)c;event(30);if(test_case%17==0)cells[3][0x11B]=0;}
static void place(void *c,Ra2WorldPoint p){
 (void)c;event(40);event(actor[0x74]);memcpy(actor+0x88,&p,12);
 if(test_case%19==0){cells[1][0x11B]=4;cells[3][0x11B]=0;U(cells[3]+0x140)|=0x100;}
}
static Ra2InterpolationSurface surface(void *c,uintptr_t cell){(void)c;return (Ra2InterpolationSurface){(int8_t)*(uint8_t *)(cell+0x11B),(U(cell+0x140)&0x100)!=0};}
static void set_bridge(void *c,unsigned x){(void)c;actor[0x79]=(uint8_t)x;}
static void enter(void *c){(void)c;event(50);}
static uint8_t flag(void *c){(void)c;return actor[0x74];}
static void set_flag(void *c,uint8_t f){(void)c;actor[0x74]=f;}
static void *__fastcall native_transform(void *c,void *d,Ra2WorldPoint *out,void *sample,void *dir){
 (void)c;(void)d;(void)sample;U(dir)^=test_case;Ra2WorldPoint p=transform(NULL);out->x=p.x;out->y=p.y;return out;
}
static void *__fastcall native_lookup(void *c,void *d,Ra2WorldPoint *p){(void)c;(void)d;return (void *)lookup(NULL,*p);}
static void __fastcall native_mark(void *c,void *d,int value){(void)c;(void)d;if(value)enter(NULL);else leave(NULL);}
static void __fastcall native_place(void *c,void *d,Ra2WorldPoint *p){(void)c;(void)d;place(NULL,*p);}
static void reset_budget(void *c,int32_t b){(void)c;U(actor+0x53C)=(uint32_t)b;}
static int32_t path_head(void *c){(void)c;return (int32_t)U(actor+0x4D0);}
static uint32_t segment(void *c,int32_t h){(void)c;stopped_head=(uint32_t)h;return shared_result;}
static __declspec(naked) void stop_shared(void){__asm{
 mov stopped_head,ebx
 mov eax,shared_result
 ret
}}
static void setup(unsigned n){
 test_case=n;count=lookups=stopped_head=0;memset(events,0,sizeof(events));memset(actor,0,sizeof(actor));memset(drive,0,sizeof(drive));memset(cells,0,sizeof(cells));memset(stack_space,0,sizeof(stack_space));
 start=(Ra2WorldPoint){(int32_t)(n%37)*256+(int32_t)(n%511)-255,(int32_t)(n%41)*256-511,(int32_t)(n%7)*104};
 if(n%5==0){start.x=-start.x;start.y=-start.y;}
 sample_point=(Ra2WorldPoint){start.x+(int32_t)(n%1023)-511,start.y+(int32_t)((n*11)%1023)-511,0};
 memcpy(actor+0x88,&start,12);U(actor)=(uint32_t)(uintptr_t)vtable;U(drive+0xC)=(uint32_t)(uintptr_t)actor;
 U(drive+0x4C)=n%7+1;actor[0x74]=(uint8_t)n;actor[0x79]=(uint8_t)(n%2);
 U(actor+0x53C)=n%17;U(actor+0x4D0)=n%13? n%9:UINT32_MAX;shared_result=n%4;
 for(unsigned i=0;i<8;++i){cells[i][0x11B]=(uint8_t)((n+i)%9);U(cells[i]+0x140)=(n+i)%2?0x100:0;}
 guest_stack=(uint32_t)(uintptr_t)(stack_space+8192);return_slot=guest_stack+0xF4;
 reg_bp=(uint32_t)(uintptr_t)drive;reg_si=(uint32_t)start.x;reg_bx=(uint32_t)start.y;reg_cx=0;
 memcpy((void *)(uintptr_t)(guest_stack+0x80),&start,12);U(guest_stack+0x34)=n;
}
typedef struct Capture{unsigned char actor[0x600],cells[8][0x148];uint32_t events[256],count,result,head;}Capture;
static Capture expected,actual;
static void capture(Capture *r,uint32_t value){memcpy(r->actor,actor,sizeof(actor));memcpy(r->cells,cells,sizeof(cells));memcpy(r->events,events,sizeof(events));r->count=count;r->result=value;r->head=stopped_head;}
static void compare(unsigned n){if(memcmp(&expected,&actual,sizeof(actual))){unsigned i=0;while(((uint8_t *)&expected)[i]==((uint8_t *)&actual)[i])++i;printf("mismatch case=%u byte=%u value=%02x/%02x events=%u/%u\n",n,i,((uint8_t *)&expected)[i],((uint8_t *)&actual)[i],expected.count,actual.count);for(unsigned j=0;j<expected.count;++j)printf("event %u %08x/%08x\n",j,expected.events[j],actual.events[j]);exit(1);}}
int main(int argc,char **argv){
 if(argc!=3)return 2;hold_image();map_original_image(argv[1]);unsigned phase=(unsigned)atoi(argv[2]);
 conversion=*(uint16_t *)(uintptr_t)0x7D8964;
 for(unsigned i=0;i<100000;++i)house_storage[i]=i*7919;
 if(phase==0){patch(0x4A4740,(uintptr_t)native_transform);patch(0x548000,(uintptr_t)native_lookup);vtable[0x11C/4]=(uint32_t)(uintptr_t)native_mark;vtable[0x19C/4]=(uint32_t)(uintptr_t)native_place;}
 if(phase==1)patch(0x4A32CA,(uintptr_t)stop_shared);
 unsigned cases=phase==0?12288:phase==1?8192:32768;uint64_t total_events=0;
 for(unsigned n=0;n<cases;++n){
  const unsigned precision[]={0,0x200,0x300};uint16_t initial=(uint16_t)(0x7F|precision[(n/1024)/4%3]|(((n/1024)%4)<<10));control=initial;set_control(control);setup(n);
  if(phase==0)entry=0x4A237D;
  if(phase==1){entry=n%2?0x4A32B4:0x4A32CA;return_slot=guest_stack;reg_bx=n%17;}
  Ra2CellGrid grid={grid_slots,n%5?262144:(int32_t)(n%262144),(uintptr_t)0xA6F9F8,(Ra2ServiceCell *)0xA6FA1C};
  Ra2ServiceCell p={(int16_t)((int32_t)(n%1031)-256),(int16_t)((int32_t)((n*11)%1031)-256)};
  if(n%29==0 && n%4!=3)p=(Ra2ServiceCell){32767,-32768};
  unsigned service=n%4;Ra2WorldPoint world={(int32_t)p.x*256+(int32_t)(n%511)-255,(int32_t)p.y*256+(int32_t)(n%511)-255,0};
  if(n%97==0 && service==0)world=(Ra2WorldPoint){INT32_MAX,INT32_MIN,0};
  if(phase==2){
   memset(grid_slots,0,sizeof(grid_slots));U(0x832618)=(uint32_t)(uintptr_t)grid_slots;U(0x83261C)=(uint32_t)grid.count;
   if(service==2)p=(Ra2ServiceCell){(int16_t)(n%512),(int16_t)((n/512)%512)};
   int32_t index=(int32_t)p.y*512+p.x;if(index>=0&&index<262144 && n%3)grid_slots[index]=(uint32_t)(uintptr_t)cells[0];
   Ra2ServiceCell cellpoint={(int16_t)(n%512),(int16_t)((n*7)%512)};memcpy(cells[0]+0x24,&cellpoint,4);memcpy((void *)0xA6FA1C,&cellpoint,4);
   
   uint32_t *args=(uint32_t *)(uintptr_t)guest_stack;args[1]=(uint32_t)(uintptr_t)(service==0?(void *)&world:(void *)&p);args[2]=(uint32_t)(uintptr_t)house;
   return_slot=guest_stack;reg_cx=0x8324E0;entry=service==0?0x548000:service==1?0x548070:service==2?0x5480B0:0x54E3A0;
  }
  original();uint32_t value=phase==0?result&255:phase==2&&service==2?result&255:result;capture(&expected,value);
  uint32_t expected_stack=guest_stack+(phase==0?0xFC:phase==1?4:service==3?12:8);if(exit_stack!=expected_stack){printf("stack mismatch %u\n",n);return 1;}
  Ra2ServiceCell fallback_expected;memcpy(&fallback_expected,(void *)0xA6FA1C,4);
  control=initial;set_control(control);setup(n);value=0;
  if(phase==0){Ra2InterpolationServices s={NULL,transform,position,lookup,blend,leave,place,surface,set_bridge,enter,flag,set_flag};ra2_ground_interpolate_advance(start,start.x,start.y,(int32_t)U(drive+0x4C),&s);}
  if(phase==1){Ra2PrepareSharedServices s={NULL,reset_budget,path_head,segment};value=ra2_ground_prepare_shared(n%2,(int32_t)(n%17),&s);if(stopped_head!=(n%2?U(actor+0x4D0):n%17))return 1;}
  if(phase==2){
   Ra2ServiceCell cellpoint={(int16_t)(n%512),(int16_t)((n*7)%512)};memcpy(cells[0]+0x24,&cellpoint,4);memcpy((void *)0xA6FA1C,&cellpoint,4);
   if(service==0)value=(uint32_t)ra2_cell_at_world(&grid,world);
   if(service==1||service==3){value=(uint32_t)ra2_cell_at_point(&grid,p);if(service==3){memcpy(&cellpoint,(void *)(uintptr_t)(value+0x24),4);value=house[0x58DC/4+ra2_cell_threat_index(cellpoint)];}}
   if(service==2)value=(uint32_t)ra2_cell_slot_present(grid_slots,p);
   if(memcmp(&fallback_expected,(void *)0xA6FA1C,4)){printf("fallback mismatch %u\n",n);return 1;}
  }
  capture(&actual,value);compare(n);total_events+=count;
 }
 printf("{\"passed\":true,\"cases\":%u,\"phase\":%u,\"ordered_callback_values\":%llu,\"original_stack_cleanup_verified\":true}\n",cases,phase,(unsigned long long)total_events);return 0;
}
