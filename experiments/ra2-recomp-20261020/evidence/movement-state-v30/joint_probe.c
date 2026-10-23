#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_joint_bridge.h"
#include "native_probe_host.h"
#define U(a) (*(uint32_t *)(uintptr_t)(a))
#define P(a) ((uint32_t)(uintptr_t)(a))
uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
uint16_t g_fpu_cw;
static uint32_t space[8192],frame,return_slot,host_stack,entry,ia,ic,id,ib,is,ii,ip;
static uint32_t native_ax,native_sp,native_bx,native_bp,native_si,native_di,resume,native_return;
static uint16_t control,native_cw,native_sw;
static unsigned phase,number,event_count;
static uint32_t events[128],vt[320];
static unsigned char units[2][0x800],cells[0x180],drive[128];
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
STOP(sample_stop,04A17FEh) STOP(prepare_stop,04A3502h) STOP(passage_stop,0703331h)
static void patch(uint32_t a,uint32_t b){*(uint8_t *)(uintptr_t)a=0xE9;U(a+1)=b-a-5;}
static void ev(uint32_t v){if(event_count==128)exit(3);events[event_count++]=v;}
static uint32_t dispatch(unsigned k,uint32_t object,const uint32_t *a)
{
 ev(k);ev(object);
 switch(k){
 case 1:ev(a[0]);ev(U(a[0]));return P(cells);
 case 2:ev(a[0]);if(!a[0]&&number%3==0)U(drive+0xC)=P(units[1]);if(a[0]&&number%7==0)U(frame+0x18)^=7;return 0xCAFE0000;
 case 3:for(unsigned i=0;i<5;++i)ev(a[i]);return number%9;
 case 4:for(unsigned i=0;i<5;++i)ev(a[i]);U(a[2])=number%3?U(a[2]):UINT32_MAX;*(uint8_t *)(uintptr_t)a[3]=(uint8_t)(number%2);return number%7;
 case 5:ev(a[0]);ev(a[1]);if(number%11==0)U(frame+0x84)+=3;return 0xABCD0000u|((number>>1)&1);
 case 6:if(number%5==0)U(frame+0x84)^=1;return 0xACED0000u|((number>>2)&1);
 case 7:for(unsigned i=0;i<5;++i)ev(a[i]);return number/7%9;
 default:exit(3);
 }
}
static uint32_t __fastcall n_lookup(void*c,void*d,uint32_t a){(void)d;return dispatch(1,P(c),&a);}
static uint32_t __fastcall n_mark(void*c,void*d,uint32_t a){(void)d;return dispatch(2,P(c),&a);}
static uint32_t __fastcall n_classify(void*c,void*d,uint32_t a,uint32_t b,uint32_t e,uint32_t f,uint32_t g){(void)d;uint32_t v[]={a,b,e,f,g};return dispatch(3,P(c),v);}
static uint32_t __fastcall n_delegate(void*c,void*d,uint32_t a,uint32_t b,uint32_t e,uint32_t f,uint32_t g){(void)d;uint32_t v[]={a,b,e,f,g};return dispatch(4,P(c),v);}
static uint32_t __fastcall n_visible(void*c,void*d,uint32_t a,uint32_t b){(void)d;uint32_t v[]={a,b};return dispatch(5,P(c),v);}
static uint32_t __fastcall n_ignore(void*c,void*d){(void)d;return dispatch(6,P(c),NULL);}
static uint32_t __fastcall n_foot(void*c,void*d,uint32_t a,uint32_t b,uint32_t e,uint32_t f,uint32_t g){(void)d;uint32_t v[]={a,b,e,f,g};return dispatch(7,P(c),v);}
static void lifted(unsigned k,unsigned count){uint32_t a[5];for(unsigned i=0;i<count;++i)a[i]=U(g_esp+4+i*4);g_eax=dispatch(k,g_ecx,a);g_esp+=4+count*4;}
#define L(name,k,n) static void name(void){lifted(k,n);}
L(l_lookup,1,1) L(l_mark,2,1) L(l_classify,3,5) L(l_delegate,4,5) L(l_visible,5,2) L(l_ignore,6,0) L(l_foot,7,5)
recomp_func_t recomp_lookup_manual(uint32_t a){if(a==0x548070)return l_lookup;if(a==P(n_mark))return l_mark;if(a==P(n_classify))return l_classify;if(a==P(n_delegate))return l_delegate;if(a==0x55A740)return l_visible;if(a==P(n_ignore))return l_ignore;if(a==0x4C86E0)return l_foot;return NULL;}
recomp_func_t recomp_lookup(uint32_t a){(void)a;return NULL;}
recomp_func_t recomp_lookup_import(uint32_t a){(void)a;return NULL;}
static void setup(unsigned n)
{
 number=n;resume=event_count=0;memset(events,0,sizeof(events));memset(space,0xA5,sizeof(space));memset(units,0,sizeof(units));memset(cells,0,sizeof(cells));memset(drive,0,sizeof(drive));
 frame=P(space+4096);U(frame)=0x12345678;U(frame+4)=0x23456789;U(frame+8)=0x3456789A;U(frame+12)=0x456789AB;
 for(unsigned i=0;i<2;++i){U(units[i])=P(vt);units[i][0x32D]=(uint8_t)((n>>3)&1);}
 U(drive+0xC)=P(units[0]);
 static const int32_t edge[]={0,1,-1,255,-255,256,-256,257,-257,INT32_MAX,INT32_MIN};
 U(frame+0x38)=(uint32_t)edge[n%11];U(frame+0x3C)=(uint32_t)edge[(n/11)%11];
 U(frame+0x84)=n%5?((uint32_t)(int32_t)(int8_t)n+4):UINT32_MAX;U(frame+0x88)=n&255;U(frame+0x8C)=n%9;
 cells[0x11B]=(uint8_t)n;U(cells+0x140)=n%3?0x100:0;U(cells+0x128)=n*3;U(cells+0x58)=n%4;U(0xA40774)=n%7==0;
 ia=n*997;ic=(uint32_t)edge[n%11];id=0x71727374;ib=n%9;is=P(units[0]);ii=(uint32_t)edge[(n/11)%11];ip=P(drive);return_slot=frame;
 if(phase==0)entry=0x4A17D5;
 if(phase==1)entry=0x4A3486;
 if(phase==2){entry=0x70323E;ip=P(units[0]);ib=P(cells);ii=n%8;return_slot=frame+0x78;}
 if(phase==3){static const uint32_t entries[]={0x4A263A,0x4A3A44,0x4A3427,0x703B5A};entry=entries[n%4];return_slot=frame+(n%4==0?0xF4:n%4==3?0x78:0x5C);}
 if(native_return){U(return_slot)=native_return;U(frame)=native_return;}
 control=0xF7F;g_fpu_cw=control;g_esp=frame;g_eax=ia;g_ecx=ic;g_edx=id;g_ebx=ib;g_esi=is;g_edi=ii;g_ebp=ip;
}
typedef struct Capture{unsigned char units[2][0x800];uint32_t events[128],count,result,locals[10];}Capture;
static Capture expected,actual;
static void capture(Capture*c,uint32_t result){memset(c,0,sizeof(*c));memcpy(c->units,units,sizeof(units));memcpy(c->events,events,sizeof(events));c->count=event_count;c->result=result;
 if(phase==0){c->locals[0]=U(frame+0x48);c->locals[1]=U(frame+0x4C);c->locals[2]=U(frame+0x50);}
 if(phase==1){c->locals[0]=U(frame+0x18);c->locals[1]=U(frame+0x14);c->locals[2]=U(frame+0x2C);c->locals[3]=*(uint8_t *)(uintptr_t)(frame+0x13);}
 if(phase==2){c->locals[0]=U(frame+0x10);c->locals[1]=U(frame+0x18);c->locals[2]=U(frame+0x84);c->locals[3]=U(frame+0x8C);}
}
int main(int argc,char**argv)
{
 if(argc!=3)return 2;hold_image();map_original_image(argv[1]);phase=(unsigned)atoi(argv[2]);
 patch(0x548070,P(n_lookup));patch(0x55A740,P(n_visible));patch(0x4C86E0,P(n_foot));vt[0x11C/4]=P(n_mark);vt[0x194/4]=P(n_classify);vt[0x198/4]=P(n_delegate);vt[0x2F4/4]=P(n_ignore);
 if(phase==0)patch(0x4A17FE,P(sample_stop));if(phase==1)patch(0x4A3502,P(prepare_stop));if(phase==2)patch(0x703331,P(passage_stop));
 unsigned cases=65536;uint64_t callbacks=0;
 for(unsigned n=0;n<cases;++n){setup(n);original();capture(&expected,resume?resume:native_ax);setup(n);uint32_t result=0;
 if(phase<2)result=ra2_ground_template_entry_bridge(phase);
 else if(phase==2)result=ra2_ground_passage_entry_bridge();
 else{unsigned kind=n%4==0?0:n%4==3?2:1;uint32_t value=n%4==3?7:n%4==2?(ia&0xFFFFFF00u)|1:ia&0xFFFFFF00u;ra2_ground_return_frame(frame,(Ra2GroundFrameKind)kind,value);}
 capture(&actual,result?result:g_eax);int returned=phase==3||(phase==2&&expected.result==7);
 int abi=g_esp!=(returned?native_sp:frame)||(!returned&&native_sp!=frame+4)||g_ebx!=native_bx||g_ebp!=native_bp||g_esi!=native_si||g_edi!=native_di;
 if(phase==0)abi|=g_eax!=native_ax;
 if(memcmp(&expected,&actual,sizeof(actual))||abi){unsigned j=0;while(j<sizeof(actual)&&((uint8_t*)&expected)[j]==((uint8_t*)&actual)[j])++j;printf("mismatch phase=%u case=%u byte=%u native=%02X C=%02X result=%X/%X events=%u/%u abi=%d ax=%X/%X bx=%X/%X bp=%X/%X si=%X/%X di=%X/%X sp=%X/%X\n",phase,n,j,j<sizeof(actual)?((uint8_t*)&expected)[j]:0,j<sizeof(actual)?((uint8_t*)&actual)[j]:0,expected.result,actual.result,expected.count,actual.count,abi,native_ax,g_eax,native_bx,g_ebx,native_bp,g_ebp,native_si,g_esi,native_di,g_edi,native_sp,g_esp);return 1;}
 callbacks+=event_count;
 }
 printf("{\"passed\":true,\"phase\":%u,\"cases\":%u,\"ordered_callback_values\":%llu,\"original_stack_cleanup_verified\":true}\n",phase,cases,(unsigned long long)callbacks);return 0;
}
