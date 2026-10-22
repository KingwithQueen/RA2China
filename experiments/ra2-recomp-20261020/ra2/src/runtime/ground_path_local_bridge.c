#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_path_local.h"
#include "ground_path_completion.h"
#include "ground_path_local_bridge.h"
typedef struct LocalContext {uint32_t search,owner,frame;} LocalContext;
static uint32_t call(uint32_t address,uint32_t object,const uint32_t *args,unsigned count)
{
    uint32_t stack=g_esp,caller=g_cur_func;
    for(unsigned i=count;i;--i){g_esp-=4;MEM32(g_esp)=args[i-1];}
    g_esp-=4;MEM32(g_esp)=RECOMP_RETADDR;g_ecx=object;
    recomp_func_t fn=recomp_lookup_manual(address);if(!fn)fn=recomp_lookup(address);if(!fn)fn=recomp_lookup_import(address);
    if(!fn){fprintf(stderr,"[path-local] missing %08X\n",address);abort();}
    fn();if(g_esp!=stack){fprintf(stderr,"[path-local] stack mismatch %08X\n",address);abort();}
    g_cur_func=caller;return g_eax;
}
static double factor(void *opaque)
{
    LocalContext *c=opaque;call(0x4CAFB0,c->owner,NULL,0);
    int top=g_fp_top;double value=fp_pop_impl(g_st,&top);g_fp_top=top;return value;
}
static uint32_t house(void *opaque){LocalContext *c=opaque;return MEM32(c->owner+0x1B4);}
static uintptr_t cell_at(void *opaque,const Ra2PathPoint *point)
{(void)opaque;uint32_t arg=(uint32_t)(uintptr_t)point;return call(0x548070,0x8324E0,&arg,1);}
static Ra2LocalPathCell properties(void *opaque,uintptr_t cell)
{(void)opaque;return (Ra2LocalPathCell){(int8_t)MEM8((uint32_t)cell+0x11B),MEM32((uint32_t)cell+0x140)};}
static Ra2PathPoint connection_exit(void *opaque,const Ra2PathPoint *point)
{
    uint32_t cell=(uint32_t)cell_at(opaque,point);int32_t id=(int16_t)MEM16(cell+0x116);Ra2PathPoint result={0,0};
    if(id!=-1)memcpy(&result,(void *)(uintptr_t)(MEM32(MEM32(0x8661CC)+(uint32_t)id*4)+0x28),4);
    return result;
}
static int32_t passage(void *opaque,uintptr_t cell,int32_t direction,int32_t level)
{
    LocalContext *c=opaque;uint32_t args[]={(uint32_t)cell,(uint32_t)direction,(uint32_t)level,0,1};
    return (int32_t)call(MEM32(MEM32(c->owner)+0x194),c->owner,args,5);
}
static int32_t threat(void *opaque,const Ra2PathPoint *point,uint32_t owner_house)
{(void)opaque;uint32_t args[]={(uint32_t)(uintptr_t)point,owner_house};return (int32_t)call(0x54E3A0,0x8324E0,args,2);}
static Ra2LocalPathServices services(LocalContext *c)
{return (Ra2LocalPathServices){c,(Ra2PathPoint *)0x851A70,&g_fpu_cw,factor,house,cell_at,properties,connection_exit,passage,threat};}
void ra2_path_anchor_bridge(void)
{
    uint32_t s=g_esp;
    ra2_path_find_anchor((int32_t *)(uintptr_t)MEM32(s+4),(int32_t)MEM32(s+8),(int32_t)MEM32(s+12),
        (int32_t *)(uintptr_t)MEM32(s+16),(Ra2PathPoint *)(uintptr_t)MEM32(s+20),(Ra2PathPoint *)0x851A70);
    g_esp=s+24;
}
void ra2_path_turn_rewrite_bridge(void)
{
    uint32_t s=g_esp,b=g_ebx,p=g_ebp,i=g_esi,d=g_edi;LocalContext c={g_ecx,MEM32(s+4),0};
    Ra2LocalPathServices v=services(&c);g_esp=s-0x100;
    int32_t result=ra2_path_shorten_turn((int32_t *)(uintptr_t)MEM32(s+8),(int32_t *)(uintptr_t)MEM32(s+12),
        (int32_t)MEM32(s+16),(int32_t)MEM32(s+20),(Ra2PathPoint *)(uintptr_t)MEM32(s+24),&v);
    g_eax=(uint32_t)result;g_esp=s+28;g_ebx=b;g_ebp=p;g_esi=i;g_edi=d;
}
void ra2_path_segment_rewrite_bridge(void)
{
    uint32_t s=g_esp,b=g_ebx,p=g_ebp,i=g_esi,d=g_edi;LocalContext c={g_ecx,MEM32(s+20),0};
    Ra2LocalPathServices v=services(&c);g_esp=s-0x100;
    int result=ra2_path_rewrite_segment((int32_t *)(uintptr_t)MEM32(s+4),(int32_t)MEM32(s+8),
        (Ra2PathPoint *)(uintptr_t)MEM32(s+12),(Ra2PathPoint *)(uintptr_t)MEM32(s+16),(int32_t)MEM32(s+24),MEM8(s+28),&v);
    g_eax=(uint32_t)result;g_esp=s+32;g_ebx=b;g_ebp=p;g_esi=i;g_edi=d;
}
static Ra2RebuiltPath *rebuild(void *opaque,Ra2SearchNode *end)
{
    LocalContext *c=opaque;uint32_t args[]={(uint32_t)(uintptr_t)end,MEM32(c->frame+0x6C)};
    uint32_t result=call(0x428370,c->search,args,2);c->owner=MEM32(c->frame+0x68);
    return (Ra2RebuiltPath *)(uintptr_t)result;
}
static void smooth(void *opaque,Ra2RebuiltPath *path)
{LocalContext *c=opaque;uint32_t args[]={(uint32_t)(uintptr_t)path,c->owner};call(0x428AE0,c->search,args,2);}
static void postprocess(void *opaque,Ra2RebuiltPath *path)
{LocalContext *c=opaque;uint32_t args[]={(uint32_t)(uintptr_t)path,c->owner};call(0x4290C0,c->search,args,2);}
static void restore(void *opaque){LocalContext *c=opaque;call(0x4285D0,c->search,&c->owner,1);}
void ra2_path_completion_bridge(unsigned preparation)
{
    uint32_t f=g_esp;LocalContext c={g_esi,MEM32(f+0x68),f};
    Ra2PathCompletion finish={(Ra2PathPreparationResult)preparation,(Ra2SearchNode *)(uintptr_t)MEM32(f+0x14),
        MEM32(f+0x28),(int32_t)MEM32(f+0x70),(int32_t *)(uintptr_t)(c.search+0x3C)};
    Ra2PathCompletionServices v={&c,rebuild,smooth,postprocess,restore};g_esp=f-0x100;
    g_eax=(uint32_t)(uintptr_t)ra2_path_complete(&finish,&v);
    g_edi=MEM32(f);g_esi=MEM32(f+4);g_ebp=MEM32(f+8);g_ebx=MEM32(f+12);g_esp=f+0x78;
}
