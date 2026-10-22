#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_tube_state_bridge.h"
#include "native_probe_host.h"
#define U(a) (*(uint32_t *)(uintptr_t)(a))
#define P(a) ((uint32_t)(uintptr_t)(a))
uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
static uint32_t space[8192],frame,return_slot,host_stack,entry,ia,ic,id,ib,is,ii,ip,native_ax,native_sp,native_bx,native_bp,native_si,native_di,resume;
static uint32_t phase,number,events[1024],event_count,vt[320],other_vt[320],body_vt[64],loco_vt[16],vector_vt[8],vector_buffer[64],tubes[2][128],tube_table[2],kind_calls;
static unsigned char unit[0x800],cell[0x160],objects[12][0x600],loco[32],support_body[64],drive[128];
static int32_t samples[8][48];
static __declspec(naked) void original(void){__asm{
 pushad
 mov host_stack,esp
 mov edx,return_slot
 lea eax,returned
 mov [edx],eax
 mov esp,frame
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
 mov esp,host_stack
 popad
 ret
}}
#define STOP(name,address) static __declspec(naked) void name(void){__asm mov resume,address __asm ret}
STOP(end_stop,06FAE76h)
STOP(step_stop,06FAD75h)
STOP(next_stop,06FABAAh)
STOP(start_stop,06FAA66h)
STOP(shared_stop,04A32B4h)
STOP(interpolation_stop,04A237Dh)
STOP(done_stop,04A263Ah)
STOP(full_stop,04A166Ah)
STOP(remainder_stop,04A1FA1h)
static void patch(uint32_t a,uint32_t b){*(uint8_t *)(uintptr_t)a=0xE9;U(a+1)=b-a-5;}
static void ev(uint32_t a){if(event_count==1024)exit(3);events[event_count++]=a;}
static unsigned object_index(uint32_t p){return (unsigned)((p-P(objects))/sizeof(objects[0]));}
static uint32_t dispatch(unsigned which,uint32_t object,const uint32_t *a)
{
 ev(which);ev(object);
 switch(which)
 {
 case 1:ev(U(a[0]));ev(U(a[0]+4));ev(U(a[0]+8));return P(cell);
 case 2: /* Vector constructor */
  if(a[0]||a[1])exit(3);memset((void *)(uintptr_t)object,0,24);U(object)=P(vector_vt);*(uint8_t *)(uintptr_t)(object+0xD)=1;return object;
 case 3: /* Resize is invoked through original DynamicVector vtable. */
  ev(a[0]);ev(a[1]);if(a[1])exit(3);if(number%19==0)return 0;
  U(object+4)=P(vector_buffer);U(object+8)=a[0];return 1;
 case 4: /* kind can mutate its own kind and linked-list next pointer. */
 {unsigned i=object_index(object);ev(i);++kind_calls;uint32_t value=U(object+0x34);if(number%7==0)U(object+0x34)=15;if(number%11==0)U(object+0x30)=0;return value;}
 case 5:ev(a[0]);if(a[0]!=P(loco))exit(3);return number%3;
 case 6:ev(U(a[0]));ev(U(a[0]+4));ev(U(a[0]+8));ev(a[1]);ev(a[2]);U(object+0x490)^=number;return 0xA1234567;
 case 7:ev(a[0]);ev(a[1]);U(unit+0x88)+=number%5;return 0xAABBCCDD;
 case 8:ev(a[0]);if(a[0]!=P(vector_buffer))exit(3);return 0x12345678;
 case 9:ev(U(a[0]));ev(U(a[0]+4));ev(U(a[0]+8));memcpy((void *)(uintptr_t)(object+0x88),(void *)(uintptr_t)a[0],12);if(number%13==0)U(unit+0x494)=P(cell);if(phase==3&&number%11==0)*(uint8_t *)(uintptr_t)(frame+0x17)^=1;return 0xABCDEF42;
 case 10:ev(a[0]);ev(*(uint8_t *)(uintptr_t)(object+0x574));return 0x22446688;
 case 11:ev(a[0]);ev(*(uint8_t *)(uintptr_t)(object+0x57B));return 0x11335577;
 case 12:return number%3?P(tubes[1]):0;
 case 13:ev(*(uint16_t *)(uintptr_t)a[0]);ev(object-P(unit));return 0x778899AA;
 case 14:ev(a[0]);ev(a[1]);ev(a[2]);ev(a[3]);U(unit+0x90)^=number;return 0xABCDEF00|(number&255);
 case 15:{static const int32_t edges[]={INT32_MIN,INT32_MIN+85,-85,-1,0,1,INT32_MAX-85,INT32_MAX-84,INT32_MAX};ev(U(a[0]));ev(U(a[0]+4));cell[0x11B]++;if(number%7==0)U(cell+0xE4)=P(objects[2]);return phase==2?(uint32_t)edges[(number/3)%9]:number*103-20000;}
 case 16:ev(U(a[0]));ev(U(a[0]+4));ev(a[1]);ev(a[2]);return number%3?P(objects[11]):0;
 case 17:ev(a[0]);U(a[0])=1;U(a[0]+4)=2;U(a[0]+8)=number%2?0x7FFFFFFFu:0x80000000u;return a[0];
 default:exit(3);
 }
}
#define N0(name,k) static uint32_t __fastcall name(void*c,void*d){(void)d;return dispatch(k,P(c),NULL);}
#define N1(name,k) static uint32_t __fastcall name(void*c,void*d,uint32_t a){(void)d;return dispatch(k,P(c),&a);}
#define N2(name,k) static uint32_t __fastcall name(void*c,void*d,uint32_t a,uint32_t b){(void)d;uint32_t v[]={a,b};return dispatch(k,P(c),v);}
#define N3(name,k) static uint32_t __fastcall name(void*c,void*d,uint32_t a,uint32_t b,uint32_t e){(void)d;uint32_t v[]={a,b,e};return dispatch(k,P(c),v);}
N1(n_lookup,1) N2(n_ctor,2) N2(n_resize,3) N0(n_kind,4) N1(n_moving,5) N3(n_stop,6) N2(n_speed,7)
static uint32_t __cdecl n_delete(uint32_t a){return dispatch(8,0,&a);}
N1(n_place,9) N1(n_enter,10) N1(n_mission,11) N0(n_connection,12) N1(n_face,13)
static uint32_t __fastcall n_classify(void*c,void*d,uint32_t a,uint32_t b,uint32_t e,uint32_t f){(void)d;uint32_t v[]={a,b,e,f};return dispatch(14,P(c),v);}
N1(n_height,15) N3(n_fallback,16) N1(n_support,17)
static void lifted(unsigned k,unsigned n,int caller_cleanup){uint32_t a[4];for(unsigned i=0;i<n;++i)a[i]=U(g_esp+4+i*4);g_eax=dispatch(k,g_ecx,a);g_esp+=4+(caller_cleanup?0:n*4);}
#define L(name,k,n,c) static void name(void){lifted(k,n,c);}
L(l_lookup,1,1,0) L(l_ctor,2,2,0) L(l_resize,3,2,0) L(l_kind,4,0,0) L(l_moving,5,1,0) L(l_stop,6,3,0)
L(l_speed,7,2,0) L(l_delete,8,1,1) L(l_place,9,1,0) L(l_enter,10,1,0) L(l_mission,11,1,0)
L(l_connection,12,0,0) L(l_face,13,1,0) L(l_classify,14,4,0) L(l_height,15,1,0) L(l_fallback,16,3,0) L(l_support,17,1,0)
recomp_func_t recomp_lookup_manual(uint32_t a)
{
 if(a==0x548000)return l_lookup;if(a==0x4BFBD0)return l_ctor;if(a==P(n_resize)||a==0x416230)return l_resize;
 if(a==P(n_kind))return l_kind;if(a==P(n_moving))return l_moving;if(a==P(n_stop))return l_stop;
 if(a==P(n_speed))return l_speed;if(a==0x781D3B)return l_delete;if(a==P(n_place))return l_place;
 if(a==P(n_enter))return l_enter;if(a==P(n_mission))return l_mission;if(a==0x47A130)return l_connection;
 if(a==0x4B8B10)return l_face;if(a==0x476920)return l_classify;if(a==0x4706C0)return l_height;
 if(a==0x471660)return l_fallback;if(a==P(n_support))return l_support;return NULL;
}
recomp_func_t recomp_lookup(uint32_t a){(void)a;return NULL;}
recomp_func_t recomp_lookup_import(uint32_t a){(void)a;return NULL;}
static void setup(unsigned n)
{
 number=n;event_count=kind_calls=resume=0;memset(events,0,sizeof(events));memset(space,0xA5,sizeof(space));memset(unit,0,sizeof(unit));memset(cell,0,sizeof(cell));memset(objects,0,sizeof(objects));memset(drive,0,sizeof(drive));memset(vector_buffer,0,sizeof(vector_buffer));
 frame=P(space+4096);uint32_t oldbp=frame+0x88;U(frame)=0x12345678;U(frame+4)=0x23456789;U(frame+8)=oldbp;U(frame+12)=0x3456789A;U(oldbp)=0x456789AB;
 U(unit)=P(vt);U(unit+0x88)=n*17+1000;U(unit+0x8C)=n*31+2000;U(unit+0x90)=n;U(unit+0x464)=n*104;unit[0x574]=(uint8_t)(n%2);unit[0x575]=0;U(unit+0x494)=n%2?P(cell):0;U(unit+0x45C)=n+10;U(unit+0x460)=n+20;U(unit+0x464)=n+30;
 U(loco)=P(loco_vt);U(support_body)=P(body_vt);
 for(unsigned i=0;i<12;++i){U(objects[i])=P(other_vt);U(objects[i]+0x30)=i+1<12?P(objects[i+1]):0;static const uint32_t kinds[]={1,15,6,7};U(objects[i]+0x34)=kinds[(n+i)%4];U(objects[i]+0x564)=P(loco);U(objects[i]+0x418)=P(support_body);}
 U(cell+0xE4)=n%3?P(objects[0]):0;U(cell+0x140)=n%2?0x100:0;cell[0x11B]=(uint8_t)n;U(0x8661CC)=P(tube_table);U(0x8661D8)=2;
 for(unsigned i=0;i<2;++i){tubes[i][0x28/4]=n*17;tubes[i][0x2C/4]=n%8;tubes[i][0x30/4]=n%3?2:UINT32_MAX;tubes[i][0x34/4]=n%5?6:UINT32_MAX;}
 ia=0xABCDEF00|(n&255);ic=P(unit);id=P(tube_table);ib=n;is=P(unit);ii=n;ip=P(tubes[n%2]);return_slot=frame;
 if(phase==0){entry=0x6FAE76;return_slot=oldbp+4;}
 if(phase==1)
 {
  entry=n%3==0?0x4A3257:n%3==1?0x4A2311:0x4A1F90;ip=P(drive);is=P(cell);U(drive+0xC)=P(unit);U(drive+0x5C)=n%16;
  static const int32_t heights[]={104,1,256,3,-104,INT32_MAX};U(0x8529D0)=(uint32_t)heights[(n/6)%6];U(unit+0x90)=n%11? n*17-100000:INT32_MIN;
  ia=(n/3)%8;ii=(n/16)%3?0:n%7;ic=n%17? n:INT32_MAX;U(frame+0x3C)=n%16;
  for(unsigned i=0;i<8;++i){U(0x7A00A0+i*16)=P(samples[i]);for(unsigned j=0;j<16;++j){samples[i][j*3]=j%3?(int32_t)n:0;samples[i][j*3+1]=j%3?(int32_t)(n+1):0;samples[i][j*3+2]=(int32_t)(n+j);}}
 }
 if(phase==2){
  static const int32_t starts[]={INT32_MIN,INT32_MIN+1,-15,-14,-1,0,1,INT32_MAX-14,INT32_MAX-13,INT32_MAX-1,INT32_MAX};
  static const int32_t offsets[]={-1,0,1,13,14,15,INT32_MIN};
  static const int32_t counts[]={INT32_MIN,-1,0,1,2,INT32_MAX};
  static const int16_t indexes[]={INT16_MIN,-2,-1,0,1,2,INT16_MAX};
  entry=n%3==0?0x479CC0:n%3==1?0x47A270:0x47A290;ic=P(cell);
  U(0xA52580)=(uint32_t)starts[(n/3)%11];U(cell+0x38)=U(0xA52580)+(uint32_t)offsets[(n/33)%7];
  *(int16_t *)(cell+0x116)=indexes[(n/3)%7];U(0x8661D8)=(uint32_t)counts[(n/21)%6];
  U(cell+0xEC)=n%4?10:7;*(uint8_t *)0xA40958=(uint8_t)(n%5!=0);
 }
 if(phase==3){static const int32_t edges[]={INT32_MIN,-1,0,1,18,19,20,INT32_MAX};entry=n%2?0x6FAA45:0x6FAB6A;ia=(uint32_t)edges[(n/2)%8];ic=(uint32_t)edges[(n/16)%8];ii=P(unit+0x45C);U(frame+0x28)=ia;ia^=0x12345600;}
 g_esp=frame;g_eax=ia;g_ecx=ic;g_edx=id;g_ebx=ib;g_esi=is;g_edi=ii;g_ebp=ip;
}
typedef struct Capture{unsigned char unit[0x800],cell[0x160],objects[12][0x600],drive[128];uint32_t events[1024],event_count,buffer[64],result,locals[9];}Capture;
static Capture expected,actual;
static void capture(Capture*c,uint32_t result)
{
 memset(c,0,sizeof(*c));memcpy(c->unit,unit,sizeof(unit));memcpy(c->cell,cell,sizeof(cell));memcpy(c->objects,objects,sizeof(objects));memcpy(c->drive,drive,sizeof(drive));memcpy(c->events,events,sizeof(events));memcpy(c->buffer,vector_buffer,sizeof(vector_buffer));c->event_count=event_count;c->result=result;
 if(phase==1){unsigned offsets[]={0x18,0x44,0x48,0x80,0x84,0x88,0x8C,0x90,0x34};for(unsigned i=0;i<9;++i)c->locals[i]=U(frame+offsets[i]);}
}
int main(int argc,char**argv)
{
 if(argc!=3)return 2;hold_image();map_original_image(argv[1]);phase=(unsigned)atoi(argv[2]);
 patch(0x548000,P(n_lookup));patch(0x4BFBD0,P(n_ctor));patch(0x781D3B,P(n_delete));patch(0x47A130,P(n_connection));patch(0x4B8B10,P(n_face));patch(0x476920,P(n_classify));patch(0x4706C0,P(n_height));patch(0x471660,P(n_fallback));
 vt[0x19C/4]=P(n_place);vt[0x11C/4]=P(n_enter);vt[0x15C/4]=P(n_stop);vt[0x174/4]=P(n_mission);vt[0x4C8/4]=P(n_speed);
 memcpy(other_vt,vt,sizeof(vt));other_vt[0x2C/4]=P(n_kind);body_vt[0x7C/4]=P(n_support);loco_vt[0x10/4]=P(n_moving);vector_vt[2]=P(n_resize);
 /* Production uses the original DynamicVector vtable; replace only its resize entry. */
 U(0x79DB7C+8)=P(n_resize);
 tube_table[0]=P(tubes[0]);tube_table[1]=P(tubes[1]);
 if(phase==1){patch(0x4A32B4,P(shared_stop));patch(0x4A237D,P(interpolation_stop));patch(0x4A263A,P(done_stop));patch(0x4A166A,P(full_stop));patch(0x4A1FA1,P(remainder_stop));}
 if(phase==3){patch(0x6FAE76,P(end_stop));patch(0x6FAD75,P(step_stop));patch(0x6FABAA,P(next_stop));patch(0x6FAA66,P(start_stop));}
 uint64_t callbacks=0;unsigned cases=32768;
 for(unsigned n=0;n<cases;++n)
 {
  setup(n);original();capture(&expected,phase==0||phase==2?native_ax:resume);
  setup(n);uint32_t result=0;if(phase==0)ra2_ground_tube_state_bridge(0);
  else if(phase==1)result=ra2_ground_internal_handoff_bridge(n%3==0?0:n%3==1?1:2);
  else if(phase==2)ra2_ground_surface_class_bridge(n%3);
  else result=ra2_ground_tube_state_bridge(n%2?2:1);
  capture(&actual,phase==0||phase==2?g_eax:result);
  int abi=(phase==0||phase==2)&&(g_esp!=native_sp||g_ebx!=native_bx||g_ebp!=native_bp||g_esi!=native_si||g_edi!=native_di);
  if(memcmp(&expected,&actual,sizeof(actual))||abi)
  {unsigned i=0;while(i<sizeof(actual)&&((uint8_t*)&expected)[i]==((uint8_t*)&actual)[i])++i;printf("mismatch phase=%u case=%u byte=%u native=%02X C=%02X result=%X/%X events=%u/%u abi=%d\n",phase,n,i,i<sizeof(actual)?((uint8_t*)&expected)[i]:0,i<sizeof(actual)?((uint8_t*)&actual)[i]:0,expected.result,actual.result,expected.event_count,actual.event_count,abi);return 1;}
  callbacks+=event_count;
 }
 printf("{\"passed\":true,\"phase\":%u,\"cases\":%u,\"ordered_callback_values\":%llu,\"original_stack_cleanup_verified\":true}\n",phase,cases,(unsigned long long)callbacks);return 0;
}
