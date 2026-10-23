#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "native_probe_host.h"
static unsigned char cell[0x148];
int main(int argc,char **argv)
{
    if(argc!=2)return 2;hold_image();map_original_image(argv[1]);
    *(int32_t *)0x850C40=104;
    uint32_t position[2]={0,0};void *p=position,*object=cell;
    __asm { push p
      mov ecx,object
      mov eax,004706C0h
      call eax
    }
    printf("height=%d flags=%u cache=%.17g scale=%.17g\n",*(int32_t *)0x850C40,*(uint8_t *)0x850BB8,*(double *)0x850BA8,*(double *)0x850BD0);
    for(unsigned i=0;i<20;++i){double *v=(double *)(uintptr_t)(0x7D27E8+i*40);printf("%u: %.17g %.17g %.17g %.17g %.17g\n",i+1,v[0],v[1],v[2],v[3],v[4]);}
    return 0;
}
