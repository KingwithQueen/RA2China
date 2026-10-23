#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_completion_bridge.h"
#include "native_probe_host.h"
#define U(a) (*(uint32_t *)(uintptr_t)(a))
#define P(a) ((uint32_t)(uintptr_t)(a))
uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
uint16_t g_fpu_cw;
static unsigned char drive[128],actor[0x700],alternate[0x700],to[0x148],from[0x148],locomotor[16];
static uint32_t vtable[300],com_table[16],cells[4096],events[128],event_count,case_number,phase;
static uint32_t stack_space[8192],frame,host_stack,return_slot,entry,input_ax,input_cx,input_dx,input_si;
static uint32_t native_ax,native_sp,native_bx,native_bp,native_si,native_di,continued;
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
static __declspec(naked) void loop_stop(void) { __asm {
 mov continued,1
 mov edi,[esp]
 mov esi,[esp+4]
 mov ebp,[esp+8]
 mov ebx,[esp+12]
 add esp,5Ch
 ret 0Ch
} }
static void patch(uint32_t a,uint32_t b) { *(uint8_t *)(uintptr_t)a=0xE9;U(a+1)=b-a-5; }
static void event(uint32_t value) { if(event_count==128)exit(3);events[event_count++]=value; }
static uint32_t current_owner(void) { return U(drive+0xC); }
static uint32_t cancel(uint32_t object)
{
 event(10);event(object);U(object+0x488)=0;
 if(case_number%3==0)U(drive+0xC)=current_owner()==P(actor)?P(alternate):P(actor);
 return 0xA1234567;
}
static uint32_t stop(uint32_t object,int target,uint32_t a,uint32_t b)
{
 if(a||b!=1)exit(3);event(target?21:20);event(object);event(U(drive+0x58));event(drive[0x63]);
 U(object+0x4D0)+=3;return 0x12340000u|(case_number&255);
}
static uint32_t recurse(uint32_t object,uint32_t aborted,uint32_t a,uint32_t b)
{
 if(object!=P(drive)||aborted!=0x23456789||a||b)exit(3);
 event(30);event(U(current_owner()+0x4D0));event(U(actor+0x530));event(U(actor+0x534));event(U(actor+0x538));
 U(drive+0x58)^=case_number;U(current_owner()+0x4D0)+=5;
 if(case_number%7==0)U(drive+0xC)=P(alternate);
 return 0xAABBCC00u|(case_number&255);
}
static uint32_t lookup(uint32_t p)
{
 event(40);event(U(p));to[0x11B]^=(uint8_t)(case_number%5==0);
 return case_number%11==0?0:P(from);
}
static uint32_t can_enter(uint32_t self,uint32_t packed)
{
 if(self!=P(locomotor))exit(3);event(50);event(packed);U(actor+0x564)=0;
 return 0x10203000u|(case_number&255);
}
static uint32_t height(uint32_t cell,uint32_t p)
{
 event(60);event(cell);event(U(p));event(U(p+4));
 U(to+0x50)^=case_number;U(0xA6FA1C)^=case_number%7;
 return U(p)*13u+U(p+4)*31u+cell;
}
static uint32_t __fastcall native_cancel(void *c,void *d) { (void)d;return cancel(P(c)); }
static uint32_t __fastcall native_stop(void *c,void *d,uint32_t a,uint32_t b) { (void)d;return stop(P(c),0,a,b); }
static uint32_t __fastcall native_target_stop(void *c,void *d,uint32_t a,uint32_t b) { (void)d;return stop(P(c),1,a,b); }
static uint32_t __fastcall native_recurse(void *c,void *d,uint32_t a,uint32_t b,uint32_t e) { (void)d;return recurse(P(c),a,b,e); }
static uint32_t __fastcall native_lookup(void *c,void *d,uint32_t a) { (void)c;(void)d;return lookup(a); }
static uint32_t __stdcall native_can_enter(uint32_t self,uint32_t packed) { return can_enter(self,packed); }
static uint32_t __fastcall native_height(void *c,void *d,uint32_t a) { (void)d;return height(P(c),a); }
static void lifted_cancel(void) { g_eax=cancel(g_ecx);g_esp+=4; }
static void lifted_stop(void) { g_eax=stop(g_ecx,0,U(g_esp+4),U(g_esp+8));g_esp+=12; }
static void lifted_target_stop(void) { g_eax=stop(g_ecx,1,U(g_esp+4),U(g_esp+8));g_esp+=12; }
static void lifted_recurse(void) { g_eax=recurse(g_ecx,U(g_esp+4),U(g_esp+8),U(g_esp+12));g_esp+=16; }
static void lifted_lookup(void) { g_eax=lookup(U(g_esp+4));g_esp+=8; }
static void lifted_can_enter(void) { g_eax=can_enter(U(g_esp+4),U(g_esp+8));g_esp+=12; }
static void lifted_height(void) { g_eax=height(g_ecx,U(g_esp+4));g_esp+=8; }
recomp_func_t recomp_lookup_manual(uint32_t a)
{
 if(a==0x4CD9B0)return lifted_cancel;if(a==0x4A2670)return lifted_recurse;
 if(a==0x548070)return lifted_lookup;if(a==0x4706C0)return lifted_height;
 if(a==P(native_stop))return lifted_stop;if(a==P(native_target_stop))return lifted_target_stop;
 if(a==P(native_can_enter))return lifted_can_enter;return NULL;
}
recomp_func_t recomp_lookup(uint32_t a) { (void)a;return NULL; }
recomp_func_t recomp_lookup_import(uint32_t a) { (void)a;return NULL; }
static void setup(unsigned n)
{
 case_number=n;event_count=continued=0;memset(events,0,sizeof(events));
 memset(drive,0,sizeof(drive));memset(actor,0,sizeof(actor));memset(alternate,0,sizeof(alternate));
 memset(to,0,sizeof(to));memset(from,0,sizeof(from));memset(stack_space,0xA5,sizeof(stack_space));
 frame=P(stack_space+4096);return_slot=phase==0?frame+0x5C:frame;
 U(drive+0xC)=P(actor);U(actor)=U(alternate)=P(vtable);U(locomotor)=P(com_table);
 U(actor+0x488)=n%2;U(alternate+0x488)=(n/2)%2;U(actor+0x4D0)=17;U(alternate+0x4D0)=19;
 U(drive+0x58)=n;U(drive+0x5C)=n+7;drive[0x63]=(uint8_t)n;
 memcpy(drive+0x40,(void *)0x852998,12);if(n%3)U(drive+0x44)+=1;
 U(actor+0x530)=U(alternate+0x530)=123;U(actor+0x534)=U(alternate+0x534)=456;U(actor+0x538)=U(alternate+0x538)=789;
 U(frame)=0x12345678;U(frame+4)=0x23456789;U(frame+8)=0x3456789A;U(frame+12)=0x456789AB;
 U(frame+0x54)=n^0x12345678;U(frame+0x60)=0x23456789;*(uint8_t *)(uintptr_t)(frame+0x64)=(uint8_t)((n/8)%2);
 U(0xA40D2C)=n+100;
 input_cx=n%5==0?P(alternate):P(actor);input_dx=P(actor+0x530);input_ax=0x11223344;input_si=n%9;
 if(phase==0)
 {
  static const uint32_t entries[]={0x4A322E,0x4A44B3,0x4A4450,0x4A4522,0x4A4502,0x4A4429,0x4A44D1,0x4A322A};
  entry=entries[n%8];if(n%8==4)input_cx=0;
 }
 if(phase==1)
 {
  entry=n%2?0x4C8730:0x4C86E0;input_cx=P(actor);
  U(actor+0x564)=n%3?P(locomotor):0;U(to+0x24)=n*17;
  to[0x11B]=(uint8_t)((int)((n/2)%13)-6);from[0x11B]=(uint8_t)((int)((n/26)%13)-6);
  to[0x11C]=(uint8_t)((n/338)%2);from[0x11C]=(uint8_t)((n/676)%2);
  U(to+0x140)=((n/1352)%4)*0x100;U(from+0x140)=((n/5408)%4)*0x100;
  U(actor+0x50)=(uint32_t)((int)((n/4)%15)-7);actor[0x60]=(uint8_t)(n%7);
  U(frame+4)=P(to);U(frame+8)=n%7==0?UINT32_MAX:(n/2)%8;
  U(frame+0xC)=P(actor+0x50);U(frame+0x10)=P(actor+0x60);
  U(frame+0x14)=n%2?(n%5?P(from):0):(n%4?256:1);
 }
 if(phase==2)
 {
  entry=0x55A280;input_cx=0x8324E0;
  static const int32_t coordinates[]={0,1,255,256,-1,-255,-256,-257,512,1024,INT32_MIN,INT32_MAX,16777216,-16777216};
  U(actor+0x88)=(uint32_t)coordinates[n%14];U(actor+0x8C)=(uint32_t)coordinates[(n/14)%14];U(actor+0x90)=n;
  U(frame+4)=P(actor+0x88);U(0x832618)=P(cells);U(0x83261C)=n%3?4096:0;U(0xA6FA1C)=0x12345678;
 }
 g_esp=frame;g_ebp=P(drive);g_eax=input_ax;g_ecx=input_cx;g_edx=input_dx;g_esi=input_si;
 g_ebx=0x87654321;g_edi=0x76543210;
}
typedef struct Capture
{
 unsigned char drive[128],actor[0x700],alternate[0x700],to[0x148],from[0x148];
 uint32_t events[128],count,result,fallback;
} Capture;
static Capture expected,actual;
static void capture(Capture *c,uint32_t result)
{
 memset(c,0,sizeof(*c));memcpy(c->drive,drive,sizeof(drive));memcpy(c->actor,actor,sizeof(actor));
 memcpy(c->alternate,alternate,sizeof(alternate));memcpy(c->to,to,sizeof(to));memcpy(c->from,from,sizeof(from));
 memcpy(c->events,events,sizeof(events));c->count=event_count;c->result=result;c->fallback=U(0xA6FA1C);
}
int main(int argc,char **argv)
{
 if(argc!=3)return 2;hold_image();map_original_image(argv[1]);phase=(unsigned)atoi(argv[2]);
 patch(0x4CD9B0,P(native_cancel));patch(0x4A2670,P(native_recurse));patch(0x4A4174,P(loop_stop));
 patch(0x548070,P(native_lookup));patch(0x4706C0,P(native_height));
 vtable[0x410/4]=P(native_stop);vtable[0x414/4]=P(native_target_stop);com_table[0x1C/4]=P(native_can_enter);
 for(unsigned i=0;i<4096;++i)cells[i]=i%5?P(to):0;
 /* Direction table is normally initialized by 491620, rather than stored in the PE. */
 static const int16_t directions[8][2]={{0,-1},{1,-1},{1,0},{1,1},{0,1},{-1,1},{-1,0},{-1,-1}};
 memcpy((void *)0x851A70,directions,sizeof(directions));
 uint64_t callbacks=0;
 for(unsigned n=0;n<32768;++n)
 {
  setup(n);original();unsigned expected_continue=continued;
  capture(&expected,expected_continue?0:native_ax);
  uint32_t expected_sp=frame+(phase==0?0x6C:phase==1?0x18:8);
  if(native_sp!=expected_sp){printf("stack phase=%u case=%u\n",phase,n);return 1;}
  setup(n);uint32_t resume=0;
  if(phase==0)resume=ra2_ground_prepare_finish_bridge(n%8);
  else ra2_ground_passage_bridge(phase==1?n%2:2);
  capture(&actual,resume?0:g_eax);
  int abi=phase==0&&!resume&&(g_esp!=native_sp||g_ebx!=native_bx||g_ebp!=native_bp||g_esi!=native_si||g_edi!=native_di);
  if(memcmp(&expected,&actual,sizeof(actual))||abi||(resume!=0)!=(expected_continue!=0)||(!resume&&g_esp!=expected_sp))
  {
   unsigned i=0;while(i<sizeof(actual)&&((uint8_t *)&expected)[i]==((uint8_t *)&actual)[i])++i;
   printf("mismatch phase=%u case=%u byte=%u results=%08X/%08X events=%u/%u abi=%d\n",phase,n,i,expected.result,actual.result,expected.count,actual.count,abi);return 1;
  }
  callbacks+=event_count;
 }
 printf("{\"passed\":true,\"cases\":32768,\"phase\":%u,\"ordered_callback_values\":%llu,\"original_stack_cleanup_verified\":true}\n",phase,(unsigned long long)callbacks);
 return 0;
}
