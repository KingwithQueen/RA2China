#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_internal_bridge.h"
#include "native_probe_host.h"
#define U(a) (*(uint32_t *)(uintptr_t)(a))
#define P(a) ((uint32_t)(uintptr_t)(a))
uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
static uint32_t space[8192],frame,host_stack,entry,input_ax,input_cx,input_dx,input_bx,input_si,input_di;
static uint32_t native_ax,native_sp,native_si,native_bx,native_dx,resume,number,phase,events[16],event_count;
static unsigned char drive[128],actor[0x700],other[0x700];
static int32_t samples[10][48];
static __declspec(naked) void original(void) { __asm {
 pushad
 mov host_stack,esp
 mov edx,frame
 lea eax,returned
 mov [edx],eax
 mov esp,frame
 lea ebp,drive
 mov eax,input_ax
 mov ecx,input_cx
 mov edx,input_dx
 mov ebx,input_bx
 mov esi,input_si
 mov edi,input_di
 jmp entry
returned:
 mov native_ax,eax
 mov native_sp,esp
 mov native_si,esi
 mov native_bx,ebx
 mov native_dx,edx
 mov esp,host_stack
 popad
 ret
} }
#define STOP(name,address) static __declspec(naked) void name(void) { __asm mov resume,address __asm ret }
STOP(full,04A166Ah)
STOP(remainder_stop,04A1FA1h)
STOP(invalid,04A22F9h)
STOP(interpolate,04A237Dh)
STOP(done,04A263Ah)
STOP(after_rebuild,04A3A0Ah)
STOP(after_clear,04A322Ah)
static void patch(uint32_t a,uint32_t b) { *(uint8_t *)(uintptr_t)a=0xE9;U(a+1)=b-a-5; }
static uint32_t rebuild(uint32_t owner,uint32_t cell,uint32_t zero,uint32_t attempts)
{
 if(zero||attempts<1||attempts>2)exit(3);
 events[event_count++]=owner;events[event_count++]=cell;events[event_count++]=attempts;
 U(drive+0xC)=P(other);U(owner+0x4D0)^=number;return 0xABCDEF00u|(number&255);
}
static uint32_t __fastcall n_rebuild(void *c,void *unused,uint32_t cell,uint32_t zero,uint32_t attempts)
{ (void)unused;return rebuild(P(c),cell,zero,attempts); }
static void l_rebuild(void)
{ g_eax=rebuild(g_ecx,U(g_esp+4),U(g_esp+8),U(g_esp+12));g_esp+=16; }
recomp_func_t recomp_lookup_manual(uint32_t a) { return a==0x4C3000?l_rebuild:NULL; }
recomp_func_t recomp_lookup(uint32_t a) { (void)a;return NULL; }
void ra2_ground_prepare_exit_bridge(unsigned e) { if(e)exit(3);resume=0x4A3A0A;g_esp+=4; }
uint32_t ra2_ground_prepare_finish_bridge(unsigned e) { if(e!=7)exit(3);resume=0x4A322A;g_esp+=4;return 0; }
static void setup(unsigned n)
{
 number=n;event_count=resume=0;memset(events,0,sizeof(events));memset(drive,0,sizeof(drive));
 memset(actor,0,sizeof(actor));memset(other,0,sizeof(other));memset(space,0xA5,sizeof(space));frame=P(space+4096);
 U(drive+0xC)=P(actor);U(drive+0x58)=n%32;U(drive+0x5C)=(n/2)%16;drive[0x60]=(uint8_t)(n%2);
 U(actor+0x88)=n*171-50000;U(actor+0x8C)=n*31-10000;U(actor+0x90)=n*104;
 static const int32_t coords[]={INT32_MIN,INT32_MAX,-257,-256,-255,-1,0,1,255,256,257,16777217};
 U(drive+0x34)=(uint32_t)coords[(n/3)%12];U(drive+0x38)=(uint32_t)coords[(n/36)%12];U(drive+0x3C)=n;
 for(unsigned i=0;i<32;++i){uint8_t *p=(uint8_t *)(uintptr_t)(0x7A0180+i*12);p[0]=(uint8_t)((int)((n+i)%10)-2);p[1]=(uint8_t)((int)((n+i+3)%10)-2);p[4]=(uint8_t)(n+i*17);}
 for(int i=-2;i<8;++i){U(0x7A00A0+(uint32_t)i*16)=P(samples[i+2]);for(unsigned j=0;j<16;++j){samples[i+2][j*3]=j%3?(int32_t)n:0;samples[i+2][j*3+1]=j%3?(int32_t)(n+1):0;samples[i+2][j*3+2]=(int32_t)(n+j);}}
 input_ax=(n/8)%14-3;input_dx=n%16-3;input_di=(n/16)%2?UINT32_MAX:0;input_bx=n;input_si=0x13572468;input_cx=n%2?P(actor):P(other);
 if(phase==0){entry=n%2?0x4A230E:0x4A15F0;if(n%2){input_ax=0x7A0180+(n%32)*12+(n%4==1?0:1);input_di=(n/32)%3?0:n%7;}}
 else {static const uint32_t entries[]={0x4A39C8,0x4A39CA,0x4A3216};entry=entries[n%3];}
 g_esp=frame;g_ebp=P(drive);g_eax=input_ax;g_ecx=input_cx;g_edx=input_dx;g_ebx=input_bx;g_esi=input_si;g_edi=input_di;
}
typedef struct Capture { unsigned char drive[128],actor[0x700],other[0x700];uint32_t locals[13],events[16],count,resume,result; } Capture;
static Capture expected,actual;
static void capture(Capture *c,uint32_t result)
{
 static const unsigned locals[]={0x13,0x14,0x34,0x38,0x58,0x64,0x68,0x80,0x84,0x88,0x8C,0x90,0xA8};
 memset(c,0,sizeof(*c));memcpy(c->drive,drive,sizeof(drive));memcpy(c->actor,actor,sizeof(actor));memcpy(c->other,other,sizeof(other));
 memcpy(c->events,events,sizeof(events));c->count=event_count;c->resume=resume;c->result=result;
 for(unsigned i=0;i<13;++i)c->locals[i]=locals[i]==0x13?*(uint8_t *)(uintptr_t)(frame+locals[i]):U(frame+locals[i]);
}
int main(int argc,char **argv)
{
 if(argc!=3)return 2;hold_image();map_original_image(argv[1]);phase=(unsigned)atoi(argv[2]);
 patch(0x4A166A,P(full));patch(0x4A1FA1,P(remainder_stop));patch(0x4A22F9,P(invalid));patch(0x4A237D,P(interpolate));patch(0x4A263A,P(done));
 patch(0x4A3A0A,P(after_rebuild));patch(0x4A322A,P(after_clear));patch(0x4C3000,P(n_rebuild));
 uint64_t callbacks=0;unsigned cases=65536;
 for(unsigned n=0;n<cases;++n)
 {
  setup(n);original();capture(&expected,native_ax);if(native_sp!=frame+4){printf("stack case=%u\n",n);return 1;}
  setup(n);if(!phase)resume=ra2_ground_sampling_shared_bridge(n%2);else ra2_ground_prepare_internal_bridge(n%3);
  capture(&actual,g_eax);
  int regs=!phase&&resume==0x4A237D&&(g_esi!=native_si||g_ebx!=native_bx||g_edx!=native_dx);
  if(memcmp(&expected,&actual,sizeof(actual))||regs)
  {
   unsigned i=0;while(i<sizeof(actual)&&((uint8_t *)&expected)[i]==((uint8_t *)&actual)[i])++i;
   printf("mismatch phase=%u case=%u byte=%u value=%02X/%02X resume=%X/%X registers=%d\n",phase,n,i,i<sizeof(actual)?((uint8_t *)&expected)[i]:0,i<sizeof(actual)?((uint8_t *)&actual)[i]:0,expected.resume,actual.resume,regs);return 1;
  }
  callbacks+=event_count;
 }
 printf("{\"passed\":true,\"cases\":%u,\"phase\":%u,\"ordered_callback_values\":%llu,\"original_stack_cleanup_verified\":true}\n",cases,phase,(unsigned long long)callbacks);return 0;
}
