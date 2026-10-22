#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_progress_bridge.h"
#include "native_probe_host.h"
#define U(a) (*(uint32_t *)(uintptr_t)(a))
#define P(a) ((uint32_t)(uintptr_t)(a))
uint32_t g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func;
uint16_t g_fpu_cw;
static uint32_t space[8192],frame,return_slot,host_stack,entry,ia,ic,id,ib,is,ii,ip;
static uint32_t native_ax,native_sp,native_bx,native_bp,native_si,native_di,resume,native_return;
static uint16_t control,native_cw,native_sw;
static uint32_t phase,number,events[128],event_count,map_calls,ctor_calls,weapon_calls,target_calls;
static uint32_t vt[320],centers[2][3],ctor_other[3],angle_other,weapon_boxes[2],weapon[0x100/4],warhead[0x300/4];
static unsigned char units[2][0x800],cells[2][0x180],unit_type[0x1500],drive[128];
static int32_t samples[32][3],input_direction;
static __declspec(naked) void original(void){__asm{
 pushad
 mov host_stack,esp
 mov edx,return_slot
 lea eax,returned
 mov native_return,eax
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
STOP(approach_stop,06FAC70h)
STOP(sample_stop,04A16A6h)
STOP(exhausted_stop,04A1FDCh)
STOP(prepare_stop,04A33C3h)
STOP(connection_stop,04A3A44h)
static void patch(uint32_t a,uint32_t b){*(uint8_t *)(uintptr_t)a=0xE9;U(a+1)=b-a-5;}
static void ev(uint32_t value){if(event_count==128)exit(3);events[event_count++]=value;}
static void evpoint(uint32_t p){ev(U(p));ev(U(p+4));ev(U(p+8));}
static uint32_t dispatch(unsigned k,uint32_t object,const uint32_t *a)
{
 ev(k);ev(object);
 switch(k){
 case 1:{
  for(unsigned i=0;i<3;++i){ev(a[i]);U(object+i*4)=a[i];ctor_other[i]=a[i];}
  ++ctor_calls;
  if(phase==2&&number%7==0)U(drive+0xC)=P(units[ctor_calls%2]);
  return number%17?object:P(ctor_other);
 }
 case 2:{
  ev(a[0]);evpoint(a[0]);unsigned index=map_calls++%2;
  if(phase==0&&index&&number%5==0){U(frame+0x40)+=37;U(units[0]+0x45C)+=15;}
  if(phase==2&&index==0&&number%11==0){U(drive+0xC)=P(units[1]);U(0x851AC0+((uint32_t)input_direction&7u)*8)+=17;}
  return P(cells[index]);
 }
 case 3:{
  unsigned index=object==P(cells[1]);ev(a[0]);memcpy((void *)(uintptr_t)a[0],centers[index],12);
  if(index&&number%3==0){U(frame+0x40)^=0x1234;U(frame+0x44)+=13;centers[0][0]^=0x2244;}
  return number%13?a[0]:P(centers[index]);
 }
 case 4:ev(a[0]);memcpy((void *)(uintptr_t)a[0],(void *)(uintptr_t)(object+0x88),12);return number%7?a[0]:object+0x88;
 case 5:ev(a[0]);ev(a[1]);evpoint(a[0]);evpoint(a[1]);U(object)=angle_other=0xA5000000u|((number*17)&65535);return number%13?object:P(&angle_other);
 case 6:ev(a[0]);evpoint(a[0]);memcpy((void *)(uintptr_t)(object+0x88),(void *)(uintptr_t)a[0],12);return 0xA1234567;
 case 7:ev(a[0]);if(number%13==0)unit_type[0xAF3]=1;return (number>>5)&1;
 case 8:ev(a[0]);if(number%7==0)unit_type[0xAA0]=1;return (number>>6)&1;
 case 9:ev(a[0]);return P(&weapon_boxes[(weapon_calls++)%2]);
 case 10:ev(a[0]);++target_calls;return number%5?P(units[1]):0;
 default:exit(3);
 }
}
#define N1(name,k) static uint32_t __fastcall name(void*c,void*d,uint32_t a){(void)d;return dispatch(k,P(c),&a);}
#define N2(name,k) static uint32_t __fastcall name(void*c,void*d,uint32_t a,uint32_t b){(void)d;uint32_t v[]={a,b};return dispatch(k,P(c),v);}
static uint32_t __fastcall n_construct(void*c,void*d,uint32_t a,uint32_t b,uint32_t e){(void)d;uint32_t v[]={a,b,e};return dispatch(1,P(c),v);}
N1(n_lookup,2) N1(n_center,3) N1(n_position,4) N2(n_heading,5) N1(n_place,6)
N1(n_allied,7) N1(n_ability,8) N1(n_weapon,9) N1(n_target,10)
static void lifted(unsigned k,unsigned count){uint32_t a[3];for(unsigned i=0;i<count;++i)a[i]=U(g_esp+4+i*4);g_eax=dispatch(k,g_ecx,a);g_esp+=4+count*4;}
#define L(name,k,n) static void name(void){lifted(k,n);}
L(l_construct,1,3) L(l_lookup,2,1) L(l_center,3,1) L(l_position,4,1) L(l_heading,5,2)
L(l_place,6,1) L(l_allied,7,1) L(l_ability,8,1) L(l_weapon,9,1) L(l_target,10,1)
recomp_func_t recomp_lookup_manual(uint32_t a)
{
 if(a==0x41B630)return l_construct;if(a==0x548000)return l_lookup;if(a==0x475D60)return l_center;
 if(a==P(n_position))return l_position;if(a==0x423EF0)return l_heading;if(a==P(n_place))return l_place;
 if(a==0x4E5500)return l_allied;if(a==0x6D7910)return l_ability;if(a==P(n_weapon))return l_weapon;if(a==0x473E30)return l_target;return NULL;
}
recomp_func_t recomp_lookup(uint32_t a){(void)a;return NULL;}
recomp_func_t recomp_lookup_import(uint32_t a){(void)a;return NULL;}
static void setup(unsigned n)
{
 number=n;resume=map_calls=ctor_calls=weapon_calls=target_calls=event_count=0;memset(events,0,sizeof(events));
 memset(space,0xA5,sizeof(space));memset(units,0,sizeof(units));memset(cells,0,sizeof(cells));memset(drive,0,sizeof(drive));memset(unit_type,0,sizeof(unit_type));
 frame=P(space+4096);uint32_t oldbp=frame+0xA0;U(frame)=0x12345678;U(frame+4)=0x23456789;U(frame+8)=oldbp;U(frame+12)=0x3456789A;U(oldbp)=0x456789AB;
 for(unsigned i=0;i<2;++i){U(units[i])=P(vt);U(units[i]+0x5AC)=P(unit_type);U(units[i]+0x1B4)=P(cells[1]);U(units[i]+0x88)=n*17+i*333;U(units[i]+0x8C)=n*31-i*121;U(units[i]+0x90)=n*3;U(units[i]+0x45C)=n*37;U(units[i]+0x460)=n*33;U(units[i]+0x464)=n*7;units[i][0x79]=(uint8_t)((n+i)%3);cells[i][0x11B]=(uint8_t)(n+i*17);U(cells[i]+0x140)=n%3?0x100:0;centers[i][0]=n*13+i*256;centers[i][1]=n*27-i*256;centers[i][2]=0;}
 for(unsigned i=0;i<8;++i){U(0x851AC0+i*8)=(uint32_t)((int)i*70-256);U(0x851AC4+i*8)=(uint32_t)((int)i*30-128);}
 U(drive+0xC)=P(units[0]);U(drive+0x5C)=n%32;U(frame+0x38)=P(samples);U(frame+0x3C)=n%13;
 for(unsigned i=0;i<32;++i){samples[i][0]=n%3?(int32_t)n:0;samples[i][1]=n%5?(int32_t)n:0;samples[i][2]=(int32_t)i;}
 ia=n;ic=P(units[0]);id=0x71727374;ib=n%8;is=P(units[0]);ii=P(units[0]+0x45C);ip=P(drive);return_slot=frame;control=0xF7F;
 if(phase==0){entry=0x6FABAA;U(frame+0x24)=n*13-100000;}
 if(phase==1){
  static const unsigned precisions[]={0,0x200,0x300};unsigned mode=n%12;control=(uint16_t)(0x7F|precisions[mode%3]|((mode/3)<<10));
  entry=(n/12)%2?0x6FAD1C:0x6FAE1D;ib=ip=(n/96)%8;
  static const int32_t rises[]={0,1,-1,10,-13,104,-104,1000,-1000};U(frame+0x24)=(uint32_t)rises[(n/768)%9];
  static const double distances[]={0,1,-1,0.1,0.5,255,256,257,362,363,16777217,2147483647,-2147483647};
  double distance=distances[(n/6912)%13];if(entry==0x6FAD1C)U(frame+0x30)=(uint32_t)(int32_t)distance;else memcpy((void *)(uintptr_t)(frame+0x28),&distance,8);
  uint32_t a=frame+(entry==0x6FAD1C?0x50:0x5C);U(a)=n;U(a+4)=n+1;U(a+8)=n*17-100000;return_slot=oldbp+4;
 }
 if(phase==2){entry=n%2?0x4A32B4:0x4A166A;input_direction=(int32_t)((n/2)%11)-1;U(units[0]+0x4D0)=(uint32_t)input_direction;ip=P(drive);}
 if(phase==3){entry=0x703AA9;ip=P(units[0]);ib=P(cells[0]);ii=n%7?0:n%13;U(frame+0x18)=n%3?2:UINT32_MAX;*(uint8_t *)(uintptr_t)(frame+0x88)=(uint8_t)((n>>1)&1);*(uint8_t *)(uintptr_t)(frame+0x12)=(uint8_t)(n>>2);*(uint8_t *)(uintptr_t)(frame+0x13)=(uint8_t)((n>>4)&1);unit_type[0xAF3]=(uint8_t)((n>>7)&1);unit_type[0xAA0]=(uint8_t)((n>>8)&1);unit_type[0x1FD]=(uint8_t)((n>>9)&1);weapon_boxes[0]=n%5?P(weapon):0;weapon_boxes[1]=P(weapon);U(weapon+0xA0/4)=P(warhead);*(uint8_t *)((uintptr_t)warhead+0x275)=(uint8_t)((n>>10)&1);return_slot=frame+0x78;}
 if(native_return)U(return_slot)=native_return;
 *(uint16_t *)0x7D8964=phase==1?(uint16_t)(0x37F|(((n/24)%4)<<10)):control;g_fpu_cw=control;g_esp=frame;g_eax=ia;g_ecx=ic;g_edx=id;g_ebx=ib;g_esi=is;g_edi=ii;g_ebp=ip;
}
typedef struct Capture{unsigned char units[2][0x800],drive[128];uint32_t events[128],count,result,locals[33],centers[2][3],offsets[16];}Capture;
static Capture expected,actual;
static void capture(Capture*c,uint32_t result)
{
 memset(c,0,sizeof(*c));memcpy(c->units,units,sizeof(units));memcpy(c->drive,drive,sizeof(drive));memcpy(c->events,events,sizeof(events));c->count=event_count;c->result=result;memcpy(c->centers,centers,sizeof(centers));memcpy(c->offsets,(void *)0x851AC0,64);
 for(unsigned i=0;i<33;++i)c->locals[i]=U(frame+0x18+i*4);
}
int main(int argc,char**argv)
{
 if(argc!=3)return 2;hold_image();map_original_image(argv[1]);phase=(unsigned)atoi(argv[2]);
 patch(0x41B630,P(n_construct));patch(0x548000,P(n_lookup));patch(0x475D60,P(n_center));patch(0x423EF0,P(n_heading));patch(0x4E5500,P(n_allied));patch(0x6D7910,P(n_ability));patch(0x473E30,P(n_target));
 vt[0x48/4]=P(n_position);vt[0x19C/4]=P(n_place);vt[0x39C/4]=P(n_weapon);
 if(phase==0)patch(0x6FAC70,P(approach_stop));
 if(phase==2){patch(0x4A16A6,P(sample_stop));patch(0x4A1FDC,P(exhausted_stop));patch(0x4A33C3,P(prepare_stop));patch(0x4A3A44,P(connection_stop));}
 unsigned cases=phase==1?393216:32768;uint64_t callbacks=0;
 for(unsigned n=0;n<cases;++n){
  setup(n);original();capture(&expected,phase==0||phase==2?resume:native_ax);
  setup(n);uint32_t result=0;
  if(phase==0)result=ra2_ground_tube_progress_bridge(0);
  else if(phase==1)ra2_ground_tube_progress_bridge(entry==0x6FAD1C?1:2);
  else if(phase==2)result=ra2_ground_internal_next_bridge(n%2?1:0);
  else ra2_ground_passage_finish_bridge();
  capture(&actual,phase==0||phase==2?result:g_eax);
  int abi=(phase==1||phase==3)&&(g_esp!=native_sp||g_ebx!=native_bx||g_ebp!=native_bp||g_esi!=native_si||g_edi!=native_di);
  if(phase==0||phase==2)abi=g_esp!=frame||native_sp!=frame+4||g_ebx!=native_bx||g_ebp!=native_bp||g_esi!=native_si||g_edi!=native_di;
  if(phase==1)abi|=g_fpu_cw!=native_cw||((native_sw>>11)&7)!=0;
  if(memcmp(&expected,&actual,sizeof(actual))||abi){unsigned j=0;while(j<sizeof(actual)&&((uint8_t*)&expected)[j]==((uint8_t*)&actual)[j])++j;printf("mismatch phase=%u case=%u byte=%u native=%02X C=%02X result=%X/%X events=%u/%u abi=%d\n",phase,n,j,j<sizeof(actual)?((uint8_t*)&expected)[j]:0,j<sizeof(actual)?((uint8_t*)&actual)[j]:0,expected.result,actual.result,expected.count,actual.count,abi);return 1;}
  callbacks+=event_count;
 }
 printf("{\"passed\":true,\"phase\":%u,\"cases\":%u,\"ordered_callback_values\":%llu,\"original_stack_cleanup_verified\":true}\n",phase,cases,(unsigned long long)callbacks);return 0;
}
