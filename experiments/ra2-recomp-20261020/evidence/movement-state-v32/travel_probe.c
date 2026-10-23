#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_travel_bridge.h"
#include "native_probe_host.h"
#define U(a) (*(uint32_t *)(uintptr_t)(a))
#define P(a) ((uint32_t)(uintptr_t)(a))
uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
uint16_t g_fpu_cw;
static uint32_t space[8192],frame,return_slot,host_stack,entry,ia,ic,id,ib,is,ii,ip;
static uint32_t native_ax,native_sp,native_bx,native_bp,native_si,native_di,resume,native_return;
static uint16_t control,native_cw,native_sw;
static unsigned phase,number,event_count,position_calls,height_calls;
static uint32_t events[256],vt[320],route_table[2],routes[2][128],alias[3];
static unsigned char units[2][0x800],cells[2][0x180],unit_type[0x1500],drive[128];
static int32_t samples[32][3];
static __declspec(naked) void original(void){__asm{
 pushad
 mov host_stack,esp
 mov edx,return_slot
 lea eax,returned
 mov native_return,eax
 mov [edx],eax
 mov edx,frame
 mov [edx],eax
 mov esp,frame
 fninit
 fldcw control
 mov eax,ia
 mov ecx,ic
 mov edx,id
 mov ebx,ib
 mov esi,is
 mov edi,ii
 mov ebp,ip
 jmp entry
returned:
 mov native_ax,eax
 mov native_sp,esp
 mov native_bx,ebx
 mov native_bp,ebp
 mov native_si,esi
 mov native_di,edi
 fnstcw native_cw
 fnstsw native_sw
 mov esp,host_stack
 popad
 ret
}}
#define STOP(name,address) static __declspec(naked) void name(void){__asm mov resume,address __asm ret}
STOP(entry_stop,06FAB6Ah) STOP(remaining_stop,06FAD1Ch) STOP(regular_stop,06FAE1Dh)
STOP(prepare_stop,04A3433h) STOP(sample_stop,04A17D5h) STOP(neighbor_stop,070323Eh)
static void patch(uint32_t a,uint32_t b){*(uint8_t *)(uintptr_t)a=0xE9;U(a+1)=b-a-5;}
static void ev(uint32_t v){if(event_count==256)exit(3);events[event_count++]=v;}
static void ep(uint32_t p){ev(U(p));ev(U(p+4));ev(U(p+8));}
static uint32_t dispatch(unsigned k,uint32_t object,const uint32_t *a)
{
 ev(k);ev(object);
 switch(k){
 case 1:for(unsigned i=0;i<3;++i){ev(a[i]);U(object+i*4)=a[i];alias[i]=a[i];}return number%7?object:P(alias);
 case 2:ev(a[0]);++position_calls;memcpy((void *)(uintptr_t)a[0],(void *)(uintptr_t)(object+0x88),12);if(number%7==0)units[0][0x574]=1;return number%3?a[0]:object+0x88;
 case 3:ev(a[0]);ev(a[1]);ep(object);ep(a[1]);for(unsigned i=0;i<3;++i)U(a[0]+i*4)=U(object+i*4)-U(a[1]+i*4);return a[0];
 case 4:ep(object);return number*7%2000;
 case 5:ev(a[0]);ev(a[1]);ep(a[0]);ep(a[1]);U(object)=alias[0]=0xA5000000u|(number*17&65535);if(number%11==0)U(unit_type+0x5A0)+=19;return number%13?object:P(alias);
 case 6:ev(a[0]);ep(a[0]);++height_calls;U(units[0]+0x88)+=3;return number*3+(height_calls==1?211:725);
 case 7:if(number%3==0){U(drive+0xC)=P(units[1]);U(frame+0x38)^=0x80000100;}return 0xCAFE0000u|((number>>1)&1);
 case 8:ev(a[0]);ev(a[1]);ev(U(a[1]));return 0xBEEF0000u|((number>>2)&1);
 case 9:for(unsigned i=0;i<3;++i)ev(a[i]);ep(a[1]);ev(U(a[2]));U(a[0])=U(a[1])+17;U(a[0]+4)=U(a[1]+4)-13;U(a[0]+8)=U(a[2]);return number%7?a[0]:P(alias);
 case 10:ev(a[0]);return P(cells[0]);
 case 11:return number%5?P(cells[1]):0;
 default:exit(3);
 }
}
#define N0(name,k) static uint32_t __fastcall name(void*c,void*d){(void)d;return dispatch(k,P(c),NULL);}
#define N1(name,k) static uint32_t __fastcall name(void*c,void*d,uint32_t a){(void)d;return dispatch(k,P(c),&a);}
#define N2(name,k) static uint32_t __fastcall name(void*c,void*d,uint32_t a,uint32_t b){(void)d;uint32_t v[]={a,b};return dispatch(k,P(c),v);}
#define N3(name,k) static uint32_t __fastcall name(void*c,void*d,uint32_t a,uint32_t b,uint32_t e){(void)d;uint32_t v[]={a,b,e};return dispatch(k,P(c),v);}
N3(n_construct,1) N1(n_position,2) N2(n_difference,3) N0(n_distance,4) N2(n_heading,5) N1(n_height,6)
N0(n_can,7) N2(n_accept,8) N3(n_sample,9) N1(n_neighbor,10) N0(n_obstacle,11)
static void lifted(unsigned k,unsigned count){uint32_t a[3];for(unsigned i=0;i<count;++i)a[i]=U(g_esp+4+i*4);g_eax=dispatch(k,g_ecx,a);g_esp+=4+count*4;}
#define L(name,k,n) static void name(void){lifted(k,n);}
L(l_construct,1,3) L(l_position,2,1) L(l_difference,3,2) L(l_distance,4,0) L(l_heading,5,2) L(l_height,6,1)
L(l_can,7,0) L(l_accept,8,2) L(l_sample,9,3) L(l_neighbor,10,1) L(l_obstacle,11,0)
recomp_func_t recomp_lookup_manual(uint32_t a)
{
 if(a==0x41B630)return l_construct;if(a==P(n_position))return l_position;if(a==0x4348F0)return l_difference;if(a==0x41B780)return l_distance;
 if(a==0x423EF0)return l_heading;if(a==0x55A280)return l_height;if(a==P(n_can))return l_can;if(a==0x55ACD0)return l_accept;
 if(a==0x4A4740)return l_sample;if(a==0x476AC0)return l_neighbor;if(a==0x47A130)return l_obstacle;return NULL;
}
recomp_func_t recomp_lookup(uint32_t a){(void)a;return NULL;}
recomp_func_t recomp_lookup_import(uint32_t a){(void)a;return NULL;}
static void setup(unsigned n)
{
 number=n;resume=event_count=position_calls=height_calls=0;memset(events,0,sizeof(events));memset(space,0xA5,sizeof(space));memset(units,0,sizeof(units));memset(cells,0,sizeof(cells));memset(unit_type,0,sizeof(unit_type));memset(drive,0,sizeof(drive));memset(alias,0,sizeof(alias));memset(routes,0,sizeof(routes));
 frame=P(space+4096);U(frame)=0x12345678;U(frame+4)=0x23456789;U(frame+8)=0x3456789A;U(frame+12)=0x456789AB;
 for(unsigned i=0;i<2;++i){U(units[i])=P(vt);U(units[i]+0x5AC)=P(unit_type);U(units[i]+0x88)=n*17+i*39;U(units[i]+0x8C)=n*31-i*41;U(units[i]+0x90)=n%1024;U(units[i]+0x45C)=n*29;U(units[i]+0x460)=n*43;U(units[i]+0x464)=n*3;units[i][0x574]=0;units[i][0x575]=(uint8_t)(n%8);route_table[i]=P(routes[i]);routes[i][0x24/4]=0x7FFF8000u+n;routes[i][0x28/4]=0x80007FFFu-n;routes[i][0x1C0/4]=1+n%19;for(unsigned j=0;j<8;++j)routes[i][0x30/4+j]=j;}
 U(0x8661CC)=P(route_table);U(unit_type+0x5A0)=n%100;U(drive+0xC)=P(units[0]);U(drive+0x5C)=n%32;
 for(unsigned i=0;i<32;++i){samples[i][0]=n*7;samples[i][1]=n*11;samples[i][2]=n*13+i;}
 U(frame+0x38)=P(samples);U(frame+0x18)=n%40;U(frame+0x24)=n%103;U(frame+0x28)=n%13;U(frame+0x30)=n*197;
 ia=n*997;ic=P(units[0]);id=0x71727374;ib=n%8;is=P(units[0]);ii=P(units[0]+0x45C);ip=P(routes[0]);return_slot=frame;
 static const unsigned precisions[]={0,0x200,0x300};control=(uint16_t)(0x7F|precisions[n%3]|(((n/3)%4)<<10));
 if(phase==0)entry=0x6FAA66;
 if(phase==1)entry=0x6FAC70;
 if(phase==2)entry=0x6FAD75;
 if(phase==3){ip=P(drive);entry=n%2?0x4A33C3:0x4A17A2;if(n%2){U(frame+0x38)=n%4?(uint32_t)((int)n*177-999999):0x80000000u;U(frame+0x3C)=n%3?(uint32_t)((int)n*291-399999):0x7FFFFFFF;return_slot=frame+0x5C;}}
 if(phase==4){entry=0x7031F2;ib=P(cells[0]);U(frame+0x80)=n%10?(n%16):UINT32_MAX;U(cells[1]+0x2C)=n/16%16;return_slot=frame+0x78;}
 if(native_return){U(return_slot)=native_return;U(frame)=native_return;}
 *(uint16_t *)0x7D8964=(uint16_t)(0x37F|(((n/12)%4)<<10));g_fpu_cw=control;g_esp=frame;g_eax=ia;g_ecx=ic;g_edx=id;g_ebx=ib;g_esi=is;g_edi=ii;g_ebp=ip;
}
typedef struct Capture{unsigned char units[2][0x800];uint32_t events[256],count,result,locals[20];}Capture;
static Capture expected,actual;
static void capture(Capture*c,uint32_t result)
{
 memset(c,0,sizeof(*c));memcpy(c->units,units,sizeof(units));memcpy(c->events,events,sizeof(events));c->count=event_count;c->result=result;
 if(phase==0){unsigned offsets[]={0x18,0x24,0x28,0x30,0x50,0x54,0x58,0x5C,0x60,0x64};for(unsigned i=0;i<10;++i)c->locals[i]=U(frame+offsets[i]);}
 if(phase==1||phase==2){unsigned dest=phase==1?0x50:0x5C;for(unsigned i=0;i<3;++i){c->locals[i]=U(frame+dest+i*4);c->locals[i+3]=U(frame+0x74+i*4);}c->locals[6]=U(frame+0x30);}
 if(phase==3){if(number%2){c->locals[0]=U(frame+0x18);c->locals[1]=U(frame+0x28);}else{c->locals[0]=U(frame+0x30);c->locals[1]=U(frame+0xA8);c->locals[2]=U(frame+0xAC);c->locals[3]=U(frame+0xB0);}}
}
static LONG WINAPI problem(EXCEPTION_POINTERS *e){printf("exception %X ip=%X sp=%X phase=%u case=%u ret=%X slot=%X value=%X\n",e->ExceptionRecord->ExceptionCode,e->ContextRecord->Eip,e->ContextRecord->Esp,phase,number,native_return,return_slot,U(return_slot));fflush(stdout);ExitProcess(1);}
int main(int argc,char**argv)
{
 if(argc!=3)return 2;hold_image();map_original_image(argv[1]);phase=(unsigned)atoi(argv[2]);AddVectoredExceptionHandler(1,problem);
 patch(0x41B630,P(n_construct));patch(0x4348F0,P(n_difference));patch(0x41B780,P(n_distance));patch(0x423EF0,P(n_heading));patch(0x55A280,P(n_height));patch(0x55ACD0,P(n_accept));patch(0x4A4740,P(n_sample));patch(0x476AC0,P(n_neighbor));patch(0x47A130,P(n_obstacle));
 vt[0x48/4]=P(n_position);vt[0x27C/4]=P(n_can);
 if(phase==0)patch(0x6FAB6A,P(entry_stop));if(phase==1)patch(0x6FAD1C,P(remaining_stop));if(phase==2)patch(0x6FAE1D,P(regular_stop));
 if(phase==3){patch(0x4A3433,P(prepare_stop));patch(0x4A17D5,P(sample_stop));}if(phase==4)patch(0x70323E,P(neighbor_stop));
 unsigned cases=phase==1||phase==2?131072:32768;uint64_t callbacks=0;
 for(unsigned n=0;n<cases;++n){
  setup(n);__try{original();}__except(EXCEPTION_EXECUTE_HANDLER){printf("native exception phase=%u case=%u code=%X\n",phase,n,(unsigned)GetExceptionCode());return 1;}capture(&expected,resume?resume:native_ax);
  setup(n);uint32_t result=phase<3?ra2_ground_tube_travel_bridge(phase):phase==3?ra2_ground_template_next_bridge(n%2):ra2_ground_passage_neighbor_bridge();
  capture(&actual,result?result:g_eax);int returned=(phase==3&&n%2&&expected.result!=0x4A3433)||(phase==4&&expected.result==7);
  int abi=g_esp!=(returned?native_sp:frame)||(!returned&&native_sp!=frame+4)||g_ebx!=native_bx||g_ebp!=native_bp||g_esi!=native_si||g_edi!=native_di;
  if(phase<3)abi|=g_fpu_cw!=native_cw||((native_sw>>11)&7)!=0;
  if(phase==1||phase==2)abi|=g_eax!=native_ax;
  if(memcmp(&expected,&actual,sizeof(actual))||abi){unsigned j=0;while(j<sizeof(actual)&&((uint8_t*)&expected)[j]==((uint8_t*)&actual)[j])++j;printf("mismatch phase=%u case=%u byte=%u native=%02X C=%02X result=%X/%X events=%u/%u abi=%d bx=%X/%X bp=%X/%X si=%X/%X di=%X/%X ax=%X/%X sp=%X/%X cw=%X/%X\n",phase,n,j,j<sizeof(actual)?((uint8_t*)&expected)[j]:0,j<sizeof(actual)?((uint8_t*)&actual)[j]:0,expected.result,actual.result,expected.count,actual.count,abi,native_bx,g_ebx,native_bp,g_ebp,native_si,g_esi,native_di,g_edi,native_ax,g_eax,native_sp,g_esp,native_cw,g_fpu_cw);return 1;}
  callbacks+=event_count;
 }
 printf("{\"passed\":true,\"phase\":%u,\"cases\":%u,\"ordered_callback_values\":%llu,\"original_stack_cleanup_verified\":true}\n",phase,cases,(unsigned long long)callbacks);return 0;
}
