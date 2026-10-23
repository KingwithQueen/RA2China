#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "ground_template_entry.h"
#include "ground_passage_entry.h"
#include "ground_joint_bridge.h"
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
    if(!entry){
        int32_t x=(int32_t)g_ecx,y=(int32_t)g_edi;MEM32(c.frame+0x48)=(uint32_t)x;MEM32(c.frame+0x4C)=(uint32_t)y;MEM32(c.frame+0x50)=0;
        g_esi=ra2_ground_sample_adjusted(x);g_eax=ra2_ground_sample_adjusted(y);g_edx=y<0?255:0;g_ecx=owner(&c);return 0x4A17FE;
    }
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
