#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ground_connection_numeric.h"
#include "ground_connection_trig.h"
#include "native_probe_host.h"
#define U(a) (*(uint32_t *)(uintptr_t)(a))
#define P(a) ((uint32_t)(uintptr_t)(a))
static uint32_t space[4096],frame,host_stack,host_return,entry,result,exit_stack,whole,input_cx;
static double component;
static uint16_t control,converted;
static __declspec(naked) void original(void) { __asm {
 pushad
 mov host_stack,esp
 lea eax,returned
 mov host_return,eax
 mov esp,frame
 fninit
 fldcw control
 cmp whole,0
 jne no_component
 fld component
no_component:
 mov ecx,input_cx
 jmp entry
returned:
 mov esp,host_stack
 popad
 ret
} }
static __declspec(naked) void finish(void) { __asm {
 mov result,eax
 mov exit_stack,esp
 fnstcw converted
 jmp dword ptr [host_return]
} }
static void patch(uint32_t a,uint32_t b) { *(uint8_t *)(uintptr_t)a=0xE9;U(a+1)=b-a-5; }
int main(int argc,char **argv)
{
 if(argc!=2)return 2;hold_image();map_original_image(argv[1]);
 uint8_t saved_y[5];memcpy(saved_y,(void *)0x6FADE2,5);
 patch(0x6FADE2,P(finish));patch(0x6FAE01,P(finish));patch(0x6FAD00,P(finish));frame=P(space+2048);
 static const int32_t origins[]={29312,20096,0,-1,-29312,INT32_MAX,INT32_MIN,1,128,16777217};
 static const double distances[]={0,1,7,15,16,31,256,1024,65535,-1,-15};
 static const double components[]={0,1,-1,0.7071067811865476,-0.7071067811865476,1.2246467991473532e-16,-1.2246467991473532e-16,6.123233995736766e-17,-6.123233995736766e-17,0.1,-0.1};
 static const unsigned precisions[]={0,0x200,0x300};
 unsigned cases=0;
 for(unsigned mode=0;mode<12;++mode)for(unsigned o=0;o<10;++o)for(unsigned d=0;d<11;++d)for(unsigned c=0;c<11;++c)for(unsigned axis=0;axis<2;++axis)
 {
  control=(uint16_t)(0x7F|precisions[mode%3]|((mode/3)<<10));component=components[c];double origin=(double)origins[o],distance=distances[d];
  memset(space,0xA5,sizeof(space));entry=axis?0x6FADF1:0x6FADD5;
  memcpy((void *)(uintptr_t)(frame+(axis?0x38:0x30)),&distance,8);
  if(axis)U(frame+0x84)=(uint32_t)origins[o];else memcpy((void *)(uintptr_t)(frame+0x38),&origin,8);
  original();int32_t actual=ra2_ground_connection_axis(origin,distance,component,!axis,control);
  if(result!=(uint32_t)actual||exit_stack!=frame+(axis?16:0)||converted!=*(uint16_t *)0x7D8964)
  {printf("mismatch mode=%u origin=%u distance=%u component=%u axis=%u native=%d C=%d\n",mode,o,d,c,axis,(int32_t)result,actual);return 1;}
  ++cases;
 }
 memcpy((void *)0x6FADE2,saved_y,5);whole=1;unsigned chain_cases=0;
 double scale;memcpy(&scale,(void *)0x79B620,8);float sine_scale=*(float *)0x7D8048,cosine_scale=*(float *)0x7D804C;
 for(unsigned branch=0;branch<2;++branch)for(unsigned mode=0;mode<12;++mode)for(unsigned facing=0;facing<65536;++facing)
 {
  control=(uint16_t)(0x7F|precisions[mode%3]|((mode/3)<<10));whole=branch+1;entry=branch?0x6FACA0:0x6FADA5;
  int32_t direction=(int32_t)(int16_t)(uint16_t)facing-16383;
  int32_t x=origins[facing%10],y=origins[(facing/10)%10],step=(int32_t)distances[(facing/100)%11];
  memset(space,0xA5,sizeof(space));U(frame+(branch?0x28:0x30))=(uint32_t)direction;input_cx=(uint32_t)step;U(frame+0x18)=(uint32_t)step;U(frame+0x74)=(uint32_t)x;U(frame+0x78)=(uint32_t)y;
  original();uint16_t conversion=*(uint16_t *)0x7D8964;
  double angle=ra2_ground_connection_angle(direction,scale,control);
  double sine=ra2_ground_connection_component(angle,sine_scale,(float *)0x801DC4,0,control);
  int32_t actual_y=ra2_ground_connection_axis((double)y,(double)step,sine,1,conversion);
  double cosine=ra2_ground_connection_component(angle,cosine_scale,(float *)0x801DC4,1,conversion);
  int32_t actual_x=ra2_ground_connection_axis((double)x,(double)step,cosine,0,conversion);
  if(result!=(uint32_t)actual_x || U(frame+(branch?0x28:0x30))!=(uint32_t)actual_y || exit_stack!=frame)
  {printf("chain mismatch mode=%u facing=%u origin=%d,%d step=%d native=%d,%d C=%d,%d\n",mode,facing,x,y,step,(int32_t)result,(int32_t)U(frame+0x30),actual_x,actual_y);return 1;}
  ++chain_cases;
 }
 /* Real westbound frame-42 counterexample: default double rounds away this decrement. */
 if(ra2_ground_connection_axis(29312,15,1.2246467991473532e-16,1,0xE7F)!=29311)return 1;
 printf("{\"passed\":true,\"cases\":%u,\"precision_modes\":3,\"rounding_modes\":4,\"axes\":2,\"west_frame_42_regression\":true,\"original_stack_cleanup_verified\":true}\n",cases+chain_cases);return 0;
}
