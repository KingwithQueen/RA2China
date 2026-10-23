#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ground_sampling.h"
#include "ground_prepare_exit.h"
#include "ground_object_services.h"
#include "native_probe_host.h"
#define U(a) (*(uint32_t *)(uintptr_t)(a))
static uint32_t host_stack,guest_stack,return_slot,entry,r_bp,r_si,r_bx,r_cx,r_dx,r_ax,result,exit_stack;
static uint32_t stack_space[16384],events[512],event_count,test_case,table_pointer,connection_table[32],vtable[300];
static unsigned char drive[0x80],actor[0x600],cell[0x148],objects[8][0x60],rules[0x1400],aborted_flag;
static Ra2PathSample samples[10][16];static uint16_t control,conversion;static uint8_t original_remainder[5];
static __declspec(naked) void original(void){__asm{
 pushad
 mov host_stack,esp
 mov edx,return_slot
 lea eax,returned
 mov [edx],eax
 mov esp,guest_stack
 mov ebp,r_bp
 mov esi,r_si
 mov ebx,r_bx
 mov ecx,r_cx
 mov edx,r_dx
 mov eax,r_ax
 jmp entry
returned:
 mov result,eax
 mov exit_stack,esp
 mov esp,host_stack
 popad
 ret
}}
static __declspec(naked) void full_stop(void){__asm{mov eax,1
 ret}}
static __declspec(naked) void remainder_stop(void){__asm{mov eax,2
 ret}}
static __declspec(naked) void invalid_stop(void){__asm{mov eax,3
 ret}}
static __declspec(naked) void interpolation_stop(void){__asm{mov eax,4
 ret}}
static __declspec(naked) void done_stop(void){__asm{xor eax,eax
 ret}}
static void patch(uintptr_t a,uintptr_t b){*(uint8_t *)a=0xE9;U(a+1)=(uint32_t)(b-a-5);}
static void set_control(uint16_t c){__asm fldcw c}
static uint16_t get_control(void){uint16_t c;__asm {fnstcw c}
 return c;}
static void event(uint32_t n){if(event_count>=512)exit(3);events[event_count++]=n;}
static Ra2SamplingTemplate template_at(void *c,int32_t selector){(void)c;uint8_t *p=(uint8_t *)(uintptr_t)(0x7A0180+(uint32_t)selector*12);return (Ra2SamplingTemplate){(int8_t)p[0],(int8_t)p[1],p[4]};}
static void select_table(void *c,int32_t table){(void)c;table_pointer=U(0x7A00A0+(uint32_t)table*16);}
static Ra2PathSample sample_at(void *c,int32_t index){(void)c;return ((Ra2PathSample *)(uintptr_t)table_pointer)[index];}
static int owner_exists(void *c){(void)c;return U(drive+0xC)!=0;}
static void write_aborted(void *c){(void)c;aborted_flag=1;}
static int accepted(void *c){(void)c;event(10);U(actor+0x490)^=test_case;return test_case%3==0;}
static void stop(void *c){(void)c;event(20);U(drive+0x58)=test_case;}
static int32_t current_frame(void *c){(void)c;return (int32_t)U(0xA40D2C);}
static int32_t delay(void *c){(void)c;double factor;memcpy(&factor,rules+0x13C8,8);int32_t d=ra2_ground_scale_speed(900,factor,control);control=conversion;return d;}
static void restart(void *c,int32_t frame,int32_t d){(void)c;U(actor+0x530)=(uint32_t)frame;U(actor+0x534)=U(guest_stack+0x54);U(actor+0x538)=(uint32_t)d;}
static int __fastcall native_accepted(void *c,void *d,void *p){(void)c;(void)d;if(p!=drive+0x34)exit(3);return accepted(NULL);}
static int __fastcall native_stop(void *c,void *d,int a,int b){(void)c;(void)d;if(a||b!=1)exit(3);stop(NULL);return 1;}
static int enabled(void *c){(void)c;return *(uint8_t *)0xA40958!=0;}
static uintptr_t head(void *c,int upper){(void)c;return U(cell+(upper?0xE8:0xE4));}
static int32_t kind(void *c,uintptr_t object){
 (void)c;unsigned i=(unsigned)((object-(uintptr_t)objects)/sizeof(objects[0]));event(30);event(i);
 if(test_case%17==0 && i+2<8)U(object+0x30)=(uint32_t)(uintptr_t)objects[i+2];
 if(test_case%13==0)*(uint8_t *)0xA40958^=1;
 return (int32_t)U(object+0x34);
}
static uintptr_t next(void *c,uintptr_t object){(void)c;return U(object+0x30);}
static uintptr_t fallback(void *c){(void)c;event(40);U(cell+0x50)=test_case;*(uint8_t *)0xA40958=(uint8_t)(test_case%3!=0);return test_case%5==0?(uintptr_t)objects[7]:0;}
static uint32_t __fastcall native_kind(void *c,void *d){(void)d;return (uint32_t)kind(NULL,(uintptr_t)c);}
static uint32_t __fastcall native_fallback(void *c,void *d,uint32_t a,uint32_t b,uint32_t last){(void)c;(void)d;if(a!=0x12345678||b!=0x23456789||last)exit(3);return (uint32_t)fallback(NULL);}
static uintptr_t current_cell(void){event(50);actor[0x79]^=1;cell[0x11B]++;return (uintptr_t)cell;}
static uint32_t __fastcall native_current_cell(void *c,void *d){(void)c;(void)d;return (uint32_t)current_cell();}
static int32_t cell_level(void *c){(void)c;return (int8_t)*(uint8_t *)(current_cell()+0x11B);}
static unsigned bridge_layer(void *c){(void)c;return actor[0x79]!=0;}
static Ra2WorldPoint position(void *c){(void)c;Ra2WorldPoint p;memcpy(&p,actor+0x88,12);return p;}
static int32_t ground_height(void *c,Ra2WorldPoint p){
 (void)c;event(60);event((uint32_t)p.x);event((uint32_t)p.y);event((uint32_t)p.z);
 U(actor+0x90)+=test_case%5?0:104;actor[0x79]^=(uint8_t)(test_case%7==0);U(0xA72F30)+=8;
 return (int32_t)(test_case%2048)-1024;
}
static int32_t __fastcall native_height(void *c,void *d,Ra2WorldPoint *p){(void)c;(void)d;return ground_height(NULL,*p);}
static int32_t bridge_height(void *c){(void)c;return (int32_t)U(0xA72F30);}
static void setup(unsigned n,unsigned phase){
 test_case=n;event_count=0;memset(events,0,sizeof(events));memset(drive,0,sizeof(drive));memset(actor,0,sizeof(actor));memset(cell,0,sizeof(cell));memset(objects,0,sizeof(objects));memset(stack_space,0xA5,sizeof(stack_space));aborted_flag=0;
 guest_stack=(uint32_t)(uintptr_t)(stack_space+8192);return_slot=guest_stack;
 U(drive+0xC)=(uint32_t)(uintptr_t)actor;U(actor)=(uint32_t)(uintptr_t)vtable;
 U(drive+0x58)=n%31;U(drive+0x5C)=(n/3)%16;drive[0x60]=(uint8_t)(n%2);
 U(actor+0x88)=n*17-1024;U(actor+0x8C)=n*31-2048;U(actor+0x90)=n*104;
 actor[0x79]=(uint8_t)(n%2);actor[0x57A]=(uint8_t)n;U(actor+0x490)=n;U(actor+0x530)=n+123;U(actor+0x534)=17;U(actor+0x538)=19;
 static const int32_t progress[]={-1,0,1,3,7,8,9,15};U(guest_stack+0x3C)=(uint32_t)progress[(n/3)%8];
 r_bp=(uint32_t)(uintptr_t)drive;r_cx=(uint32_t)(uintptr_t)actor;r_si=(uint32_t)(uintptr_t)(drive+0x34);r_bx=n;r_ax=(n/24)%12-2;r_dx=U(guest_stack+0x3C);
 for(unsigned i=0;i<32;++i){uint8_t *p=(uint8_t *)(uintptr_t)(0x7A0180+i*12);p[0]=(uint8_t)((int)((n+i)%10)-2);p[1]=(uint8_t)((int)((n+i+3)%10)-2);p[4]=(uint8_t)(n+i*17);}
 for(int i=-2;i<8;++i){U(0x7A00A0+(uint32_t)i*16)=(uint32_t)(uintptr_t)samples[i+2];for(unsigned j=0;j<16;++j)samples[i+2][j]=(Ra2PathSample){j%3? (int32_t)(n+j):0,j%3?(int32_t)(n-j):0,(int32_t)(n+j*19)};}
 if(phase==0){
  unsigned mode=n%3;if(mode==2 && n%17==0)U(drive+0x58)=UINT32_MAX;
  if(mode==1)U(drive+0x5C)=n%5==0?INT32_MAX:n;
  entry=mode==0?0x4A15ED:mode==1?0x4A1F8D:0x4A1FA1;
  if(mode==2)memcpy((void *)0x4A1FA1,original_remainder,5);else patch(0x4A1FA1,(uintptr_t)remainder_stop);
 }
 if(phase==1){
  unsigned mode=n%5;entry=mode==0?0x4A3A0A:mode==1?0x4A3A24:mode==2?0x4A3A50:mode==3?0x4A3C75:0x4A3A44;
  if(mode==0 && n%17==0)U(drive+0xC)=0;
  U(guest_stack+0x60)=(uint32_t)(uintptr_t)&aborted_flag;U(guest_stack+0x54)=n^0x1234;U(0xA40D2C)=n+100;
  U(0x839848)=(uint32_t)(uintptr_t)rules;static const double factors[]={0,0.00001,0.2,1,2,1.0000000000000002,-1};double factor=factors[n%7];memcpy(rules+0x13C8,&factor,8);
  r_ax=n%2;return_slot=guest_stack+0x5C;
 }
 if(phase==2){
  unsigned mode=n%6;entry=mode==0?0x4717B0:mode==1?0x4717E0:mode==2?0x471830:mode==3?0x47A130:mode==4?0x5D47D0:0x5D4810;
  r_cx=(uint32_t)(uintptr_t)(mode<4?cell:actor);*(uint8_t *)0xA40958=(uint8_t)(n%4!=0);
  for(unsigned i=0;i<8;++i){U(objects[i])=(uint32_t)(uintptr_t)vtable;U(objects[i]+0x30)=i+1<8?(uint32_t)(uintptr_t)objects[i+1]:0;static const unsigned kinds[]={0,1,2,6,36,17};U(objects[i]+0x34)=kinds[(n/6+i)%6];}
  U(cell+0xE4)=n%7?(uint32_t)(uintptr_t)objects[0]:0;U(cell+0xE8)=n%5?(uint32_t)(uintptr_t)objects[4]:0;
  U(guest_stack+4)=mode==1?(n%2?256:1):0x12345678;U(guest_stack+8)=0x23456789;
  *(int16_t *)(cell+0x116)=(int16_t)((int)(n%35)-2);U(0x8661D8)=n%5?32:0;U(0x8661CC)=(uint32_t)(uintptr_t)connection_table;
  cell[0x11B]=(uint8_t)n;U(0xA72F30)=416;
 }
}
static const unsigned locals[]={0x13,0x14,0x34,0x38,0x58,0x64,0x80,0x84,0x88,0x8C,0x90,0xA8};
typedef struct Capture{unsigned char drive[0x80],actor[0x600],cell[0x148],objects[8][0x60];uint32_t events[512],count,result,locals[12],enabled;uint16_t control;uint8_t aborted;}Capture;
static Capture expected,actual;
static void capture(Capture *r,uint32_t value,uint16_t cw,unsigned phase){
 memset(r,0,sizeof(*r));memcpy(r->drive,drive,sizeof(drive));memcpy(r->actor,actor,sizeof(actor));memcpy(r->cell,cell,sizeof(cell));memcpy(r->objects,objects,sizeof(objects));memcpy(r->events,events,sizeof(events));r->count=event_count;r->result=value;r->aborted=aborted_flag;r->control=cw;
 if(phase==0)for(unsigned i=0;i<12;++i)r->locals[i]=locals[i]==0x13?*(uint8_t *)(uintptr_t)(guest_stack+locals[i]):U(guest_stack+locals[i]);
 if(phase==2)r->enabled=*(uint8_t *)0xA40958;
}
static uint32_t readable_sampling(unsigned n){
 unsigned mode=n%3;Ra2SamplingChoice choice={0};Ra2SamplingServices s={NULL,template_at,select_table,sample_at};Ra2SamplingPhase phase;
 if(mode==1){int32_t index=(int32_t)U(drive+0x5C);phase=ra2_ground_finish_sample(&index,(int32_t)U(guest_stack+0x3C));U(drive+0x5C)=(uint32_t)index;return phase;}
 if(mode==0){
  phase=ra2_ground_choose_full_sample((int32_t)r_dx,(int32_t)r_ax,(int32_t)U(drive+0x58),drive[0x60],&choice,&s);
  if(phase==RA2_SAMPLING_REMAINDER)return phase;
  U(guest_stack+0xA8)=0x7A0180+U(drive+0x58)*12;U(guest_stack+0x58)=(uint32_t)choice.table*16;U(guest_stack+0x38)=table_pointer;
  if(phase==RA2_SAMPLING_INVALID_DIRECTION)return phase;
  *(uint8_t *)(uintptr_t)(guest_stack+0x13)=(uint8_t)choice.turning;
  if((int32_t)r_ax!=-1 && r_ax!=8)*(uint16_t *)(uintptr_t)(guest_stack+0x14)=(uint16_t)((uint32_t)template_at(NULL,(int32_t)U(drive+0x58)).facing<<8);
  return phase;
 }
 U(drive+0x4C)=U(guest_stack+0x3C);phase=ra2_ground_choose_remainder((int32_t)U(drive+0x4C),(int32_t)U(drive+0x58),drive[0x60],(int32_t)U(drive+0x5C),&choice,&s);
 if((int32_t)U(drive+0x4C)>0 && (int32_t)U(drive+0x58)>=0){U(guest_stack+0x8C)=(uint32_t)choice.sample.x;U(guest_stack+0x90)=(uint32_t)choice.sample.y;}
 if(phase==RA2_SAMPLING_INTERPOLATE){memcpy((void *)(uintptr_t)(guest_stack+0x80),actor+0x88,12);U(guest_stack+0x34)=(uint32_t)choice.sample.direction;}
 return phase;
}
int main(int argc,char **argv){
 if(argc!=3)return 2;hold_image();map_original_image(argv[1]);unsigned phase=(unsigned)atoi(argv[2]);conversion=*(uint16_t *)0x7D8964;
 for(unsigned i=0;i<32;++i)connection_table[i]=0x12340000+i*16;
 if(phase==0){memcpy(original_remainder,(void *)0x4A1FA1,5);patch(0x4A166A,(uintptr_t)full_stop);patch(0x4A22F9,(uintptr_t)invalid_stop);patch(0x4A237D,(uintptr_t)interpolation_stop);patch(0x4A263A,(uintptr_t)done_stop);}
 vtable[0x2AC/4]=(uint32_t)(uintptr_t)native_accepted;vtable[0x410/4]=(uint32_t)(uintptr_t)native_stop;vtable[0x2C/4]=(uint32_t)(uintptr_t)native_kind;vtable[0x1A4/4]=(uint32_t)(uintptr_t)native_current_cell;
 if(phase==2){patch(0x471660,(uintptr_t)native_fallback);patch(0x55A280,(uintptr_t)native_height);}
 unsigned cases=phase==1?12288:32768;uint64_t total_events=0;
 for(unsigned n=0;n<cases;++n){
  const unsigned precisions[]={0,0x200,0x300};uint16_t initial=(uint16_t)(0x7F|precisions[(n/1024)/4%3]|(((n/1024)%4)<<10));control=initial;set_control(control);setup(n,phase);
  original();uint32_t value=phase==1?result&255:result;capture(&expected,value,get_control(),phase);
  uint32_t expected_sp=guest_stack+(phase==1?0x6C:phase==2&&n%6==1?8:phase==2&&n%6==2?12:4);if(exit_stack!=expected_sp){printf("stack mismatch phase=%u case=%u\n",phase,n);return 1;}
  control=initial;set_control(control);setup(n,phase);value=0;
  if(phase==0)value=readable_sampling(n);
  if(phase==1){
   unsigned mode=n%5;Ra2PrepareExitServices s={NULL,owner_exists,write_aborted,accepted,stop,current_frame,delay,restart};
   if(mode<3)value=(uint32_t)ra2_ground_prepare_after_rebuild(n%2,mode==2,&s);
   if(mode==3){Ra2PreparePendingState state={actor[0x57A],(int32_t)U(drive+0x58)};ra2_ground_prepare_clear_pending(&state);actor[0x57A]=state.sound_pending;U(drive+0x58)=(uint32_t)state.selector;value=1;}
  }
  if(phase==2){
   Ra2ObjectScanServices s={NULL,enabled,head,kind,next,fallback};Ra2HeightServices h={NULL,cell_level,bridge_layer,position,ground_height,bridge_height};unsigned mode=n%6;
   if(mode==0)value=(uint32_t)ra2_ground_find_kind(0,6,&s);
   if(mode==1)value=(uint32_t)ra2_ground_find_kind((U(guest_stack+4)&255)!=0,36,&s);
   if(mode==2)value=(uint32_t)ra2_ground_find_blocking_object(&s);
   if(mode==3)value=(uint32_t)ra2_ground_cell_connection(*(int16_t *)(cell+0x116),(int32_t)U(0x8661D8),connection_table);
   if(mode==4)value=(uint32_t)ra2_ground_surface_level(&h);
   if(mode==5)value=(uint32_t)ra2_ground_height_above_surface(&h);
  }
  capture(&actual,value,control,phase);
  if(memcmp(&expected,&actual,sizeof(actual))){unsigned i=0;while(((uint8_t *)&expected)[i]==((uint8_t *)&actual)[i])++i;printf("mismatch phase=%u case=%u byte=%u values=%02x/%02x result=%u/%u events=%u/%u\n",phase,n,i,((uint8_t *)&expected)[i],((uint8_t *)&actual)[i],expected.result,actual.result,expected.count,actual.count);return 1;}
  total_events+=event_count;
 }
 printf("{\"passed\":true,\"cases\":%u,\"phase\":%u,\"ordered_callback_values\":%llu,\"original_stack_cleanup_verified\":true}\n",cases,phase,(unsigned long long)total_events);return 0;
}
