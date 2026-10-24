extern void __cdecl ra2_internal_observe(unsigned drive,unsigned unit,unsigned stage,int x,int y);
#include "ground_cell_placement.h"
#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "ground_template_entry.h"
#include "ground_passage_entry.h"
#include "ground_joint_bridge.h"
#include "ground_template_transition.h"
typedef struct JointContext { uint32_t frame,drive,unit,cell,direction,flags;int32_t level; } JointContext;
static uint32_t call(uint32_t address,uint32_t object,const uint32_t *args,unsigned count)
{
    uint32_t stack=g_esp,caller=g_cur_func;
    for(unsigned i=count;i;--i){g_esp-=4;MEM32(g_esp)=args[i-1];}
    g_esp-=4;MEM32(g_esp)=RECOMP_RETADDR;g_ecx=object;
    recomp_func_t fn=recomp_lookup_manual(address);if(!fn)fn=recomp_lookup(address);if(!fn)fn=recomp_lookup_import(address);
    if(!fn){fprintf(stderr,"[movement-joint] unresolved %08X\n",address);abort();}
    fn();if(g_esp!=stack){fprintf(stderr,"[movement-joint] stack %08X\n",address);abort();}
    g_cur_func=caller;return g_eax;
}
static uint32_t method(uint32_t unit,uint32_t slot,const uint32_t *args,unsigned count)
{return call(MEM32(MEM32(unit)+slot),unit,args,count);}
static uint32_t owner(JointContext *c){return MEM32(c->drive+0xC);}
static uintptr_t next_cell(void *opaque)
{
    JointContext *c=opaque;uint32_t packed=ra2_ground_sample_cell((int32_t)MEM32(c->frame+0x38),(int32_t)MEM32(c->frame+0x3C));
    MEM32(c->frame+0x18)=packed;MEM32(c->frame+0x14)=packed;
    uint32_t p=c->frame+0x14;c->cell=call(0x548070,0x8324E0,&p,1);MEM32(c->frame+0x2C)=c->cell;MEM8(c->frame+0x13)=0;return c->cell;
}
static void mark(void *opaque,unsigned enter){JointContext *c=opaque;method(owner(c),0x11C,&enter,1);}
static int32_t classify(void *opaque,uintptr_t cell)
{
    JointContext *c=opaque;uint32_t args[]={(uint32_t)cell,c->direction,(uint32_t)c->level,0,1};
    int32_t result=(int32_t)method(owner(c),0x194,args,5);MEM32(c->frame+0x18)=(uint32_t)result;return result;
}
uint32_t ra2_ground_template_entry_bridge(unsigned entry)
{
    JointContext c={0};c.frame=g_esp;c.drive=g_ebp;c.direction=g_ebx;c.level=(int32_t)g_edi;
    if(!entry){ra2_internal_observe(c.drive,0,12,(int)g_ecx,(int)g_edi);
        int32_t x=(int32_t)g_ecx,y=(int32_t)g_edi;MEM32(c.frame+0x48)=(uint32_t)x;MEM32(c.frame+0x4C)=(uint32_t)y;MEM32(c.frame+0x50)=0;
        g_esi=ra2_ground_sample_adjusted(x);g_eax=ra2_ground_sample_adjusted(y);g_edx=y<0?255:0;g_ecx=owner(&c);return 0x4A17FE;
    }
    ra2_internal_observe(c.drive,0,13,0,0);
    Ra2TemplatePassageServices s={&c,next_cell,mark,classify};g_esp=c.frame-0x100;
    (void)ra2_ground_prepare_template_passage(&s);g_esp=c.frame;g_ebp=c.drive;g_esi=c.cell;g_ebx=c.direction;g_edi=(uint32_t)c.level;return 0x4A3502;
}
static int32_t delegate(void *opaque)
{
    JointContext *c=opaque;uint32_t args[]={c->cell,c->direction,c->frame+0x84,c->frame+0x11,c->flags};
    return (int32_t)method(c->unit,0x198,args,5);
}
static int32_t requested_level(void *opaque){JointContext *c=opaque;return (int32_t)MEM32(c->frame+0x84);}
static Ra2PassageEntryCell cell(void *opaque)
{JointContext *c=opaque;return (Ra2PassageEntryCell){(int8_t)MEM8(c->cell+0x11B),MEM32(c->cell+0x140),MEM32(c->cell+0x128),MEM32(c->cell+0x58)};}
static void import_upper(void *opaque,Ra2PassageEntryCell value)
{JointContext *c=opaque;MEM8(c->frame+0x12)=(uint8_t)value.occupancy;MEM8(c->frame+0x13)=(uint8_t)((value.occupancy>>5)&1u);MEM32(c->frame+0x18)=value.owner;}
static unsigned special(void *opaque){(void)opaque;return MEM32(0xA40774);}
static unsigned visible(void *opaque){JointContext *c=opaque;uint32_t args[]={c->cell,1};return call(0x55A740,0x8324E0,args,2);}
static unsigned ignores(void *opaque){return method(((JointContext *)opaque)->unit,0x2F4,NULL,0);}
static unsigned requires(void *opaque){return MEM8(((JointContext *)opaque)->unit+0x32D);}
static int32_t foot(void *opaque)
{
    JointContext *c=opaque;uint32_t args[]={c->cell,MEM32(c->frame+0x80),MEM32(c->frame+0x84),c->flags,MEM32(c->frame+0x8C)};
    int32_t result=(int32_t)call(0x4C86E0,c->unit,args,5);MEM32(c->frame+0x8C)=(uint32_t)result;return result;
}
uint32_t ra2_ground_passage_entry_bridge(void)
{
    JointContext c={0};c.frame=g_esp;c.unit=g_ebp;c.cell=g_ebx;c.direction=g_edi;c.flags=MEM32(c.frame+0x88);
    ra2_internal_observe(0,c.unit,14,0,0);
    Ra2PassageEntryServices s={&c,delegate,requested_level,cell,import_upper,special,visible,ignores,requires,foot};g_esp=c.frame-0x100;
    int32_t result=ra2_ground_classify_entry(&s);g_esp=c.frame;g_ebp=c.unit;g_ebx=c.cell;g_esi=c.flags;g_edi=(uint32_t)result;g_eax=(uint32_t)result;
    if(result==7){ra2_ground_return_frame(c.frame,RA2_FRAME_PASSAGE,7);return 0;}
    return 0x703331;
}
void ra2_ground_return_frame(uint32_t frame,Ra2GroundFrameKind kind,uint32_t result)
{
    Ra2GroundReturnPlan plan=ra2_ground_return_plan(kind);
    g_eax=result;g_edi=MEM32(frame);g_esi=MEM32(frame+4);g_ebp=MEM32(frame+8);g_ebx=MEM32(frame+12);
    g_flag_k=FK_ADD;g_flag_a=frame+16;g_flag_b=plan.locals;g_flag_cf=frame+16+plan.locals<frame+16;g_esp=frame+plan.total;
}

void ra2_ground_prepare_written_return_bridge(unsigned entry)
{
    uint32_t frame=g_esp,result=g_eax;
    uint32_t saved_edi=MEM32(frame);
    if(entry==2)
    {
        /* Original pops EDI before the writes, then ESI/EBP/EBX afterward. */
        MEM32(g_ebp+0x58)=UINT32_MAX;
        MEM8(g_ebp+0x61)=0;
        ra2_ground_return_frame(frame,RA2_FRAME_PREPARE,result&UINT32_C(0xFFFFFF00));
        g_edi=saved_edi;
        return;
    }
    uint32_t output=MEM32(frame+0x60),saved_esi=MEM32(frame+4),saved_ebp=MEM32(frame+8);
    if(entry==1)result=output;
    else g_ecx=output;
    MEM8(output)=entry==0?(uint8_t)result:1;
    if(entry!=3)result&=UINT32_C(0xFFFFFF00);
    ra2_ground_return_frame(frame,RA2_FRAME_PREPARE,result);
    /* Output may alias saved EDI/ESI/EBP; those were already popped. EBX was not. */
    g_edi=saved_edi;g_esi=saved_esi;g_ebp=saved_ebp;
}

void ra2_ground_prepare_service_return_bridge(unsigned entry)
{
    uint32_t frame=g_esp,drive=g_ebp,result;
    if(entry==0)
    {
        uint32_t first_owner=MEM32(drive+0xC);
        MEM32(drive+0x58)=g_edi;
        MEM32(first_owner+0x4D0)=g_edi;
        uint32_t current_owner=MEM32(drive+0xC),args[]={0,0};
        g_edx=MEM32(current_owner);
        result=method(current_owner,0x4C8,args,2)&UINT32_C(0xFFFFFF00);
    }
    else
    {
        uint32_t second=entry==1?g_ebx:MEM32(frame+0x64);
        uint32_t args[]={MEM32(frame+0x60),second,1};
        result=call(0x4A2670,drive,args,3);
    }
    ra2_ground_return_frame(frame,RA2_FRAME_PREPARE,result);
}

uint32_t ra2_ground_advance_service_return_bridge(unsigned entry)
{
    uint32_t frame=g_esp,drive=g_ebp,result;
    if(!entry)
    {
        uint32_t unit=MEM32(drive+0xC),args[]={0,1};
        result=method(unit,0x414,args,2);
        if(result&255u)
        {
            ra2_ground_return_frame(frame,RA2_FRAME_ADVANCE,(result&UINT32_C(0xFFFFFF00))|1u);
            return 0;
        }
    }
    uint32_t unit=MEM32(drive+0xC);
    g_edx=MEM32(unit);
    result=method(unit,0x490,NULL,0);
    if(result&255u)
    {
        ra2_ground_return_frame(frame,RA2_FRAME_ADVANCE,(result&UINT32_C(0xFFFFFF00))|1u);
        return 0;
    }
    unit=MEM32(drive+0xC);unsigned alive=MEM8(unit+0x7D);
    g_eax=unit;g_ecx=(g_ecx&UINT32_C(0xFFFFFF00))|alive;
    if(alive)
    {
        g_flag_k=FK_NARROW(FK_TEST,24);g_flag_a=alive<<24;g_flag_b=alive<<24;g_flag_cf=0;
        return 0x4A1FA1;
    }
    ra2_ground_return_frame(frame,RA2_FRAME_ADVANCE,unit&UINT32_C(0xFFFFFF00));
    return 0;
}

uint32_t ra2_ground_template_destination_bridge(unsigned alternate)
{
    uint32_t frame=g_esp,drive=g_ebp,offset=alternate?0x24u:0x74u;
    uint32_t x,y,z;
    if(alternate>=2){x=g_ecx;y=g_edx;z=g_ebx;if(alternate==3)MEM32(frame+0x20)=z;}
    else
    {
        x=MEM32(frame+offset);y=MEM32(frame+offset+4);z=MEM32(frame+offset+8);
        MEM32(frame+0x18)=x;MEM32(frame+0x1C)=y;MEM32(frame+0x20)=z;
    }
    MEM32(frame+0xD0)=x;MEM32(frame+0xD4)=y;MEM32(frame+0xD8)=z;
    uint32_t pointer=frame+0xD0;
    uint32_t result=call(0x548000,0x8324E0,&pointer,1);
    /* The map service may replace the drive's owner. Read it after the call. */
    g_ecx=MEM32(drive+0xC);MEM32(frame+0x54)=result;
    g_eax=result;g_edx=g_ecx+0x88u;g_ebx=z;
    return 0x4A2528;
}

void ra2_ground_prepare_stop_return_bridge(unsigned entry)
{
    uint32_t frame=g_esp,args[]={0,1};
    g_ebp=MEM32(g_ebp+0xC);
    uint32_t result=method(g_ebp,entry?0x410u:0x414u,args,2);
    if(entry)
        ra2_ground_return_frame(frame,RA2_FRAME_PREPARE,result&UINT32_C(0xFFFFFF00));
    else
        /* Re-read the output pointer after the callback; saved slots can alias it. */
        ra2_ground_prepare_written_return_bridge(0);
}

void ra2_ground_prepare_following_return_bridge(unsigned entry)
{
    uint32_t frame=g_esp,drive=g_ebp,result;
    if(entry)
    {
        uint32_t args[]={frame+0x38,1};
        result=call(0x4A0BC0,drive,args,2)&UINT32_C(0xFFFFFF00);
    }
    else
    {
        /* 第一项服务完成后重读owner，不能沿用回调前的对象。 */
        call(0x4CD9B0,g_ecx,NULL,0);
        uint32_t unit=MEM32(drive+0xC),args[]={0,1};
        result=method(unit,0x414,args,2);
    }
    ra2_ground_return_frame(frame,RA2_FRAME_PREPARE,result);
}

void ra2_ground_prepare_owner_stop_return_bridge(void)
{
    uint32_t frame=g_esp,unit=g_ecx,args[]={0,1};
    uint32_t result=method(unit,0x410,args,2);
    ra2_ground_return_frame(frame,RA2_FRAME_PREPARE,result&UINT32_C(0xFFFFFF00));
}

void ra2_ground_prepare_invalidate_return_bridge(void)
{
    uint32_t drive=g_ebp,unit=MEM32(drive+0xC);
    g_eax=unit;g_ecx=(g_ecx&UINT32_C(0xFFFFFF00))|MEM8(unit+0x7D);
    if(g_ecx&255u)
    {
        uint32_t out=g_esi;
        g_ecx=MEM32(0x852998);MEM32(out)=g_ecx;
        g_edx=MEM32(0x85299C);MEM32(out+4)=g_edx;
        g_eax=MEM32(0x8529A0);MEM32(out+8)=g_eax;
        MEM8(drive+0x63)=0;
    }
    ra2_ground_prepare_service_return_bridge(0);
}

void ra2_ground_advance_place_return_bridge(void)
{
    uint32_t frame=g_esp,drive=g_ebp,unit=g_ecx;
    uint8_t old_flag=MEM8(unit+0x74);MEM8(unit+0x74)=0;
    unit=MEM32(drive+0xC);uint32_t argument=frame+0x18;
    method(unit,0x19C,&argument,1);
    uint32_t current_owner=MEM32(drive+0xC);
    uint32_t saved_edi=MEM32(frame),saved_esi=MEM32(frame+4),saved_ebp=MEM32(frame+8);
    MEM8(current_owner+0x74)=old_flag;
    ra2_ground_return_frame(frame,RA2_FRAME_ADVANCE,current_owner&UINT32_C(0xFFFFFF00));
    g_edi=saved_edi;g_esi=saved_esi;g_ebp=saved_ebp;
}

void ra2_ground_advance_mark_return_bridge(void)
{
    uint32_t frame=g_esp,unit=MEM32(g_ebp+0xC),argument=1;
    g_ebp=unit;g_edx=MEM32(unit);
    uint32_t result=method(unit,0x11C,&argument,1);
    ra2_ground_return_frame(frame,RA2_FRAME_ADVANCE,result&UINT32_C(0xFFFFFF00));
}

typedef struct LateLayerContext { uint32_t drive,previous,next; } LateLayerContext;
static int32_t late_level(void *opaque,unsigned next)
{
    LateLayerContext *c=opaque;
    int32_t value=(int8_t)MEM8((next?c->next:c->previous)+0x11B);
    if(next){g_esi=(uint32_t)value;g_edx=0x100;}else g_edx=(uint32_t)value;
    return value;
}
static uint32_t late_flags(void *opaque,unsigned next)
{
    LateLayerContext *c=opaque;uint32_t value=MEM32((next?c->next:c->previous)+0x140);
    g_flag_k=FK_TEST;g_flag_a=value;g_flag_b=0x100;g_flag_cf=0;
    return value;
}
static void late_set_layer(void *opaque,unsigned upper)
{
    LateLayerContext *c=opaque;uint32_t unit=MEM32(c->drive+0xC);
    if(upper)g_esi=unit;else g_eax=unit;
    /* 写回可能覆盖格子标志；下次查询必须重新读取。 */
    MEM8(unit+0x79)=(uint8_t)upper;
}
uint32_t ra2_ground_late_layer_bridge(void)
{
    LateLayerContext c={g_ebp,MEM32(g_esp+0x6C),MEM32(g_esp+0x54)};
    g_ecx=c.previous;g_eax=c.next;
    Ra2TemplateLayerServices services={&c,late_level,late_flags,late_set_layer};
    ra2_ground_template_layer(&services);return 0x4A25E8;
}

typedef struct JointPlacementContext { uint32_t frame,drive; } JointPlacementContext;
static void placement_restore(JointPlacementContext *c)
{g_esp=c->frame;g_ebp=c->drive;}
static void placement_leave(void *opaque)
{
    JointPlacementContext *c=opaque;uint32_t argument=0;
    g_eax=MEM32(g_ecx);method(g_ecx,0x11C,&argument,1);
    placement_restore(c);
}
static void placement_place(void *opaque)
{
    JointPlacementContext *c=opaque;
    uint32_t unit=MEM32(c->drive+0xC),argument=c->frame+0x18;
    g_eax=argument;g_edx=MEM32(unit);method(unit,0x19C,&argument,1);
    placement_restore(c);
}
static void placement_layer(void *opaque)
{(void)opaque;ra2_ground_late_layer_bridge();}
static uint32_t placement_enter(void *opaque)
{
    JointPlacementContext *c=opaque;uint32_t unit=MEM32(c->drive+0xC),argument=1;
    g_ebp=unit;g_edx=MEM32(unit);
    return method(unit,0x11C,&argument,1);
}
static void placement_return(unsigned needs_leave)
{
    JointPlacementContext context={g_esp,g_ebp};
    Ra2CellPlacementServices services={&context,placement_leave,placement_place,
        placement_layer,NULL,placement_enter};
    Ra2CellPlacementResult result=ra2_ground_place_cell(&services,needs_leave);
    ra2_ground_return_frame(context.frame,RA2_FRAME_ADVANCE,result.value&UINT32_C(0xFFFFFF00));
}
void ra2_ground_advance_place_layer_return_bridge(void)
{placement_return(0);}
void ra2_ground_advance_leave_place_return_bridge(void)
{placement_return(1);}

static void template_compare32(uint32_t a,uint32_t b)
{g_flag_k=FK_CMP;g_flag_a=a;g_flag_b=b;g_flag_cf=a<b;}
uint32_t ra2_ground_template_continuation_bridge(unsigned entry)
{
    uint32_t frame=g_esp;
    if(entry==0)
    {
        uint32_t x=g_esi,sentinel=g_edi,index=g_edx,y=MEM32(g_ecx+4);
        g_eax=y;MEM32(frame+0x8C)=x;MEM32(frame+0x90)=y;
        template_compare32(x,sentinel);if(x!=sentinel)return 0x4A2347;
        template_compare32(y,sentinel);if(y!=sentinel)return 0x4A2347;
        template_compare32(index,sentinel);return index!=sentinel?0x4A263A:0x4A2347;
    }
    if(entry==1)
    {
        uint32_t cell=g_eax,source=g_esi,previous=g_edi,position=g_edx;
        template_compare32(cell,source);
        /* 坐标读取与写回相邻，避免重叠局部坐标被提前缓存。 */
        g_ecx=MEM32(position);MEM32(frame+0x18)=g_ecx;
        g_edx=MEM32(position+4);MEM32(frame+0x1C)=g_edx;
        g_ebx=MEM32(position+8);MEM32(frame+0x20)=g_ebx;
        if(cell==source)return 0x4A24DC;
        template_compare32(cell,previous);if(cell==previous)return 0x4A24DC;
        uint32_t progress=MEM32(g_ebp+0x4C);template_compare32(progress,3);
        return (int32_t)progress<=3?0x4A24F4:0x4A24C6;
    }
    uint32_t owner=g_ecx,position=g_edx;
    int32_t x=(int32_t)MEM32(owner+0x88),y=(int32_t)MEM32(position+4);
    MEM32(frame+0x64)=MEM32(position+8);
    int32_t target_x=(int32_t)MEM32(frame+0x18),target_y=(int32_t)MEM32(frame+0x1C);
    Ra2TemplateCells cells=ra2_ground_template_cells(ra2_ground_sample_adjusted(target_x),ra2_ground_sample_adjusted(target_y),x,y);
    g_esi=(uint32_t)cells.current_x;g_edi=(uint32_t)cells.current_y;
    g_ebx=(uint32_t)cells.target_x;g_eax=(uint32_t)cells.target_y;g_edx=target_y<0?255u:0u;
    unsigned same_x=(uint16_t)cells.target_x==(uint16_t)cells.current_x;
    g_flag_k=FK_NARROW(FK_CMP,16);
    g_flag_a=(uint32_t)(uint16_t)(same_x?cells.target_y:cells.target_x)<<16;
    g_flag_b=(uint32_t)(uint16_t)(same_x?cells.current_y:cells.current_x)<<16;
    g_flag_cf=g_flag_a<g_flag_b;
    return cells.same_cell?0x4A2607:0x4A2586;
}
