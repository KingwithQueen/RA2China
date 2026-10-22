#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_slope.h"
#include "ground_remainder_bridge.h"
#include "native_probe_host.h"
#define U(a) (*(uint32_t *)(uintptr_t)(a))
#define P(a) ((uint32_t)(uintptr_t)(a))
uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
uint16_t g_fpu_cw;
static unsigned char drive[128],actor[0x700],alternate[0x700],cell[0x148],connections[2][0x1C4];
static uint32_t vtable[300],connection_table[2],events[128],event_count,case_number,phase,height_calls;
static uint32_t stack_space[8192],frame,host_stack,return_slot,entry,input_ax,input_cx,input_dx,input_si,input_bx,input_di;
static uint32_t native_ax,native_sp,native_bx,native_bp,native_si,native_di,continued;
static uint16_t initial_control;
static __declspec(naked) void original(void) { __asm {
 pushad
 mov host_stack,esp
 mov edx,return_slot
 lea eax,returned
 mov [edx],eax
 mov esp,frame
 lea ebp,drive
 mov eax,input_ax
 mov ecx,input_cx
 mov edx,input_dx
 mov esi,input_si
 mov ebx,input_bx
 mov edi,input_di
 jmp entry
returned:
 mov native_ax,eax
 mov native_sp,esp
 mov native_bx,ebx
 mov native_bp,ebp
 mov native_si,esi
 mov native_di,edi
 mov esp,host_stack
 popad
 ret
} }
static __declspec(naked) void sample_stop(void) { __asm {
 mov continued,1
 mov edi,[esp]
 mov esi,[esp+4]
 mov ebp,[esp+8]
 mov ebx,[esp+12]
 add esp,0F4h
 ret 4
} }
static void set_control(uint16_t c) { __asm fldcw c }
static uint16_t get_control(void) { uint16_t c;__asm {fnstcw c} return c; }
static void patch(uint32_t a,uint32_t b) { *(uint8_t *)(uintptr_t)a=0xE9;U(a+1)=b-a-5; }
static void event(uint32_t value) { if(event_count==128)exit(3);events[event_count++]=value; }
static uint32_t current_owner(void) { return U(drive+0xC); }
static void swap_owner(void) { if(case_number%7==0)U(drive+0xC)=current_owner()==P(actor)?P(alternate):P(actor); }
static uint32_t cancel(uint32_t object)
{ event(10);event(object);U(object+0x488)=0;swap_owner();return 0xA1234567; }
static uint32_t stop(uint32_t object,int target,uint32_t a,uint32_t b)
{
 if(a||b!=1)exit(3);event(target?21:20);event(object);event(U(drive+0x58));event(drive[0x63]);
 U(object+0x4D0)+=3;return 0x12340000u|(case_number&255);
}
static uint32_t recurse(uint32_t object,uint32_t aborted,uint32_t a,uint32_t b)
{
 if(object!=P(drive)||aborted!=0x23456789||a||b)exit(3);
 event(30);event(U(current_owner()+0x4D0));event(U(actor+0x530));event(U(actor+0x534));event(U(actor+0x538));
 U(drive+0x58)^=case_number;U(current_owner()+0x4D0)+=5;swap_owner();return 0xAABBCC00u|(case_number&255);
}
static uint32_t leave(uint32_t object,uint32_t a)
{ if(a)exit(3);event(40);event(object);swap_owner();if(case_number%11==0)U(drive+0x40)=17;return 1; }
static uint32_t current_cell(uint32_t object)
{ event(50);event(object);swap_owner();if(case_number%17==0){U(drive+0x40)=31;drive[0x63]=1;}return P(cell); }
static uint32_t lookup(uint32_t p)
{ event(60);event(U(p));swap_owner();return P(cell); }
static uint32_t cell_point(uint32_t object,uint32_t output)
{
 if(object!=P(cell))exit(3);event(70);U(output)=case_number*13;U(output+4)=case_number*17;U(output+8)=case_number*104;
 swap_owner();return output;
}
static uint32_t height(uint32_t p)
{
 event(80);event(U(p));event(U(p+4));event(U(p+8));++height_calls;swap_owner();
 if(height_calls==1)for(unsigned i=0;i<2;++i){U(connections[i]+0x28)^=0x00010001;U(connections[i]+0x1C0)=case_number%7+1;}
 return height_calls==1?case_number*123u-100000u:case_number*321u+100000u;
}
static uint32_t __fastcall n_cancel(void *c,void *d) { (void)d;return cancel(P(c)); }
static uint32_t __fastcall n_stop(void *c,void *d,uint32_t a,uint32_t b) { (void)d;return stop(P(c),0,a,b); }
static uint32_t __fastcall n_target_stop(void *c,void *d,uint32_t a,uint32_t b) { (void)d;return stop(P(c),1,a,b); }
static uint32_t __fastcall n_recurse(void *c,void *d,uint32_t a,uint32_t b,uint32_t e) { (void)d;return recurse(P(c),a,b,e); }
static uint32_t __fastcall n_leave(void *c,void *d,uint32_t a) { (void)d;return leave(P(c),a); }
static uint32_t __fastcall n_cell(void *c,void *d) { (void)d;return current_cell(P(c)); }
static uint32_t __fastcall n_lookup(void *c,void *d,uint32_t a) { (void)c;(void)d;return lookup(a); }
static uint32_t __fastcall n_point(void *c,void *d,uint32_t a) { (void)d;return cell_point(P(c),a); }
static uint32_t __fastcall n_height(void *c,void *d,uint32_t a) { (void)c;(void)d;return height(a); }
static void l_cancel(void) { g_eax=cancel(g_ecx);g_esp+=4; }
static void l_stop(void) { g_eax=stop(g_ecx,0,U(g_esp+4),U(g_esp+8));g_esp+=12; }
static void l_target_stop(void) { g_eax=stop(g_ecx,1,U(g_esp+4),U(g_esp+8));g_esp+=12; }
static void l_recurse(void) { g_eax=recurse(g_ecx,U(g_esp+4),U(g_esp+8),U(g_esp+12));g_esp+=16; }
static void l_leave(void) { g_eax=leave(g_ecx,U(g_esp+4));g_esp+=8; }
static void l_cell(void) { g_eax=current_cell(g_ecx);g_esp+=4; }
static void l_lookup(void) { g_eax=lookup(U(g_esp+4));g_esp+=8; }
static void l_point(void) { g_eax=cell_point(g_ecx,U(g_esp+4));g_esp+=8; }
static void l_height(void) { g_eax=height(U(g_esp+4));g_esp+=8; }
recomp_func_t recomp_lookup_manual(uint32_t a)
{
 if(a==0x4CD9B0)return l_cancel;if(a==0x4A2670)return l_recurse;
 if(a==0x548070)return l_lookup;if(a==0x475D60)return l_point;if(a==0x55A280)return l_height;
 if(a==P(n_stop))return l_stop;if(a==P(n_target_stop))return l_target_stop;
 if(a==P(n_leave))return l_leave;if(a==P(n_cell))return l_cell;return NULL;
}
recomp_func_t recomp_lookup(uint32_t a) { (void)a;return NULL; }
recomp_func_t recomp_lookup_import(uint32_t a) { (void)a;return NULL; }
static void setup(unsigned n)
{
 case_number=n;event_count=continued=height_calls=0;memset(events,0,sizeof(events));
 memset(drive,0,sizeof(drive));memset(actor,0,sizeof(actor));memset(alternate,0,sizeof(alternate));
 memset(cell,0,sizeof(cell));memset(connections,0,sizeof(connections));memset(stack_space,0xA5,sizeof(stack_space));
 frame=P(stack_space+4096);return_slot=phase==0?frame+0xF4:phase==1?frame+0x5C:frame;
 U(drive+0xC)=P(actor);U(actor)=U(alternate)=P(vtable);
 U(actor+0x488)=n%2;U(alternate+0x488)=(n/2)%2;U(actor+0x4D0)=17;U(alternate+0x4D0)=19;
 for(unsigned i=1;i<24;++i){U(actor+0x4D0+i*4)=n+i;U(alternate+0x4D0+i*4)=n+i+100;}
 U(drive+0x58)=n%4?UINT32_MAX:3;drive[0x63]=(uint8_t)n;actor[0x57A]=(uint8_t)n;
 memcpy(drive+0x40,(void *)0x852998,12);if(n%3)U(drive+0x44)+=1;
 U(actor+0x88)=n*31-10000;U(actor+0x8C)=n*17-50000;U(actor+0x90)=n;
 memcpy(alternate+0x88,actor+0x88,12);U(alternate+0x88)^=0x100;
 U(actor+0x530)=U(alternate+0x530)=123;U(actor+0x534)=U(alternate+0x534)=456;U(actor+0x538)=U(alternate+0x538)=789;
 U(frame)=0x12345678;U(frame+4)=0x23456789;U(frame+8)=0x3456789A;U(frame+12)=0x456789AB;
 U(frame+0x54)=n^0x12345678;U(frame+0x60)=0x23456789;*(uint8_t *)(uintptr_t)(frame+0x64)=(uint8_t)((n/7)%2);
 U(frame+0x18)=(n/14)%9;U(0xA40D2C)=n+100;
 input_cx=n%5==0?P(alternate):P(actor);input_dx=n;input_ax=0xABCDEF00|(n&255);input_si=n%13;
 input_bx=P(drive+0x40);input_di=n%3?UINT32_MAX:n;U(0x8661CC)=P(connection_table);U(0x8661D8)=2;
 *(int16_t *)(cell+0x116)=(int16_t)((int)((n/3)%5)-1);
 for(unsigned i=0;i<2;++i){U(connections[i]+0x24)=n*17;U(connections[i]+0x28)=n*31;U(connections[i]+0x30)=n%8;U(connections[i]+0x1C0)=n%3+1;}
 if(phase==0){static const uint32_t e[]={0x4A1388,0x4A22F9,0x4A263A};entry=e[n%3];if(n%3==0){input_ax=8;input_cx=P(actor);}}
 if(phase==1)
 {
  static const uint32_t e[]={0x4A395A,0x4A3BFD,0x4A3985,0x4A3C34,0x4A3A38,0x4A39AF,0x4A3C5D};entry=e[n%7];
  if(n%7==3||n%7==6){input_bx=P(cell+0x60);memcpy(cell+0x60,drive+0x40,12);}
  if(n%7>=5)input_ax=U(0x852998);
 }
 if(phase==2)
 {
  entry=0x4706C0;input_cx=P(cell);U(frame+4)=P(actor+0x88);
  static const int32_t hs[]={104,1,256,3,0,-104,16777217,INT32_MAX,INT32_MIN};U(0x850C40)=(uint32_t)hs[n%9];
  static const double cached[]={104,117.1,-52.75,16777217.5,0.000000000001,-0.0};double h=cached[(n/9)%6];memcpy((void *)0x850BA8,&h,8);
  double scale=(n%5?1:-1)*0.003;memcpy((void *)0x850BD0,&scale,8);
  *(uint8_t *)0x850BB8=(uint8_t)(0x80|((n/54)%8));
  Ra2SlopePlane *planes=(Ra2SlopePlane *)0x7D27E8;
  for(unsigned i=0;i<20;++i)planes[i]=(Ra2SlopePlane){i%2?-1.0:0.5,i%3?0.3333333333333333:-0.125,(double)(n%11)-5,(double)(n%2048)-17,(double)(i%7)-3};
  cell[0x11B]=(uint8_t)(n/21);cell[0x11C]=(uint8_t)(n%21);
 }
 const unsigned precisions[]={0,0x200,0x300};initial_control=(uint16_t)(0x7F|precisions[(n/1024)%3]|(((n/3072)%4)<<10));
 set_control(initial_control);g_fpu_cw=initial_control;
 g_esp=frame;g_ebp=P(drive);g_eax=input_ax;g_ecx=input_cx;g_edx=input_dx;g_esi=input_si;g_ebx=input_bx;g_edi=input_di;
}
typedef struct Capture
{
 unsigned char drive[128],actor[0x700],alternate[0x700],cell[0x148],connections[2][0x1C4];
 uint32_t events[128],count,result;uint16_t control;Ra2SlopeCache cache;
} Capture;
static Capture expected,actual;
static void capture(Capture *c,uint32_t result,uint16_t control)
{
 memset(c,0,sizeof(*c));memcpy(c->drive,drive,sizeof(drive));memcpy(c->actor,actor,sizeof(actor));
 memcpy(c->alternate,alternate,sizeof(alternate));memcpy(c->cell,cell,sizeof(cell));memcpy(c->connections,connections,sizeof(connections));
 memcpy(c->events,events,sizeof(events));c->count=event_count;c->result=result;c->control=control;
 if(phase==2){c->cache.initialized=*(uint8_t *)0x850BB8;memcpy(&c->cache.level_height,(void *)0x850BA8,8);memcpy(&c->cache.world_scale,(void *)0x850BD0,8);memcpy(c->cache.planes,(void *)0x7D27E8,sizeof(c->cache.planes));}
}
int main(int argc,char **argv)
{
 if(argc!=3)return 2;hold_image();map_original_image(argv[1]);phase=(unsigned)atoi(argv[2]);
 patch(0x4CD9B0,P(n_cancel));patch(0x4A2670,P(n_recurse));patch(0x4A15F0,P(sample_stop));
 patch(0x548070,P(n_lookup));patch(0x475D60,P(n_point));patch(0x55A280,P(n_height));
 vtable[0x410/4]=P(n_stop);vtable[0x414/4]=P(n_target_stop);vtable[0x11C/4]=P(n_leave);vtable[0x1A4/4]=P(n_cell);
 for(unsigned i=0;i<2;++i)connection_table[i]=P(connections[i]);
 static const int16_t directions[8][2]={{0,-1},{1,-1},{1,0},{1,1},{0,1},{-1,1},{-1,0},{-1,-1}};memcpy((void *)0x851A70,directions,sizeof(directions));
 uint64_t callbacks=0;unsigned cases=phase==2?131072:32768;
 for(unsigned n=0;n<cases;++n)
 {
  setup(n);original();unsigned expected_continue=continued;capture(&expected,expected_continue?0:native_ax,phase==2?get_control():0);
  uint32_t expected_sp=frame+(phase==0?0xFC:phase==1?0x6C:8);
  if(native_sp!=expected_sp){printf("stack phase=%u case=%u\n",phase,n);return 1;}
  setup(n);uint32_t resume=0;
  if(phase==0)resume=ra2_ground_landing_bridge(n%3);else if(phase==1)ra2_ground_failure_bridge(n%7);else ra2_ground_slope_bridge();
  capture(&actual,resume?0:g_eax,phase==2?g_fpu_cw:0);
  int abi=phase<2&&!resume&&(g_esp!=native_sp||g_ebx!=native_bx||g_ebp!=native_bp||g_esi!=native_si||g_edi!=native_di);
  if(memcmp(&expected,&actual,sizeof(actual))||abi||(resume!=0)!=(expected_continue!=0)||(!resume&&g_esp!=expected_sp))
  {
   unsigned i=0;while(i<sizeof(actual)&&((uint8_t *)&expected)[i]==((uint8_t *)&actual)[i])++i;
   printf("mismatch phase=%u case=%u byte=%u values=%02X/%02X results=%08X/%08X events=%u/%u abi=%d\n",phase,n,i,i<sizeof(actual)?((uint8_t *)&expected)[i]:0,i<sizeof(actual)?((uint8_t *)&actual)[i]:0,expected.result,actual.result,expected.count,actual.count,abi);return 1;
  }
  callbacks+=event_count;
 }
 printf("{\"passed\":true,\"cases\":%u,\"phase\":%u,\"ordered_callback_values\":%llu,\"original_stack_cleanup_verified\":true}\n",cases,phase,(unsigned long long)callbacks);return 0;
}
