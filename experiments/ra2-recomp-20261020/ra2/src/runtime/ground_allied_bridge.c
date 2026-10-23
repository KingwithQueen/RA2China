#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "state_trace.h"
#include "ground_allied.h"
#include "ground_allied_relation.h"
#include "ground_moving_tail.h"
#include "ground_allied_bridge.h"
#include "x87_arithmetic.h"

typedef struct AlliedContext { uint32_t frame, owner, cell, object; } AlliedContext;

static uint32_t call(uint32_t address, uint32_t object, const uint32_t *args,
    unsigned count, int caller_cleans)
{
    uint32_t stack = g_esp, caller = g_cur_func;
    for (unsigned i=count; i; --i) { g_esp-=4; MEM32(g_esp)=args[i-1]; }
    g_esp-=4; MEM32(g_esp)=RECOMP_RETADDR; g_ecx=object;
    recomp_func_t fn=recomp_lookup_manual(address);
    if (!fn) fn=recomp_lookup(address);
    if (!fn) fn=recomp_lookup_import(address);
    if (!fn) { fprintf(stderr,"[allied-bridge-error] unresolved %08X\n",address); abort(); }
    fn();
    if (caller_cleans) g_esp+=count*4;
    if (g_esp!=stack) { fprintf(stderr,"[allied-bridge-error] unbalanced %08X\n",address); abort(); }
    g_cur_func=caller;
    return g_eax;
}
static uint32_t virtual_call(uint32_t object, uint32_t slot, const uint32_t *args, unsigned count)
{ return call(MEM32(MEM32(object)+slot),object,args,count,0); }

static int locomotor_query(AlliedContext *c, uint32_t slot)
{
    uint32_t locomotor=MEM32(c->object+0x564);
    if (!locomotor)
    {
        uint32_t error=0x80004003;
        call(0x795940,0,&error,1,1);
        locomotor=MEM32(c->object+0x564);
    }
    return (call(MEM32(MEM32(locomotor)+slot),MEM32(locomotor),&locomotor,1,0)&255u)!=0;
}
static int32_t query(void *opaque, Ra2AlliedQuery which)
{
    AlliedContext *c=opaque;
    switch (which)
    {
        case RA2_ALLIED_OWNER_MISSION: return (int32_t)virtual_call(c->owner,0x16C,NULL,0);
        case RA2_ALLIED_IS_OWNER_DESTINATION: return MEM32(c->owner+0x494)==c->object;
        case RA2_ALLIED_IS_OWNER_TARGET: return MEM32(c->owner+0x1B0)==c->object;
        case RA2_ALLIED_OBJECT_KIND: return (int32_t)virtual_call(c->object,0x2C,NULL,0);
        case RA2_ALLIED_OBJECT_HAS_MOVEMENT: return (MEM8(c->object+0x14)&4)!=0;
        case RA2_ALLIED_OBJECT_HAS_DESTINATION: return MEM32(c->object+0x494)!=0;
        case RA2_ALLIED_OBJECT_IS_TURNING: return (call(0x4B8C90,c->object+0x2E0,NULL,0,0)&255u)!=0;
        case RA2_ALLIED_OBJECT_IS_MOVING: return locomotor_query(c,0x10);
        case RA2_ALLIED_OBJECT_IS_ALLIED:
            return (call(0x4E5580,MEM32(c->owner+0x1B4),&c->object,1,0)&255u)!=0;
        case RA2_ALLIED_OBJECT_FLAG_5A0: return MEM8(c->object+0x5A0);
        case RA2_ALLIED_OBJECT_WANTS_MOVING_PASSAGE: return locomotor_query(c,0xA4);
        default: abort();
    }
}
static unsigned quantize(uint32_t value)
{ return (((value>>12)+1u)>>1)&7u; }
static unsigned heading(void *opaque)
{
    AlliedContext *c=opaque; uint32_t arg=c->frame+0x34;
    ra2_state_movement_audit(26,c->owner,c->cell,c->object);
    uint32_t result=call(0x4B8BE0,c->owner+0x2E0,&arg,1,0);
    return quantize(MEM32(result));
}
static unsigned opposite(void *opaque)
{
    AlliedContext *c=opaque; uint32_t arg=c->frame+0x38;
    uint32_t result=call(0x4B8BE0,c->object+0x2E0,&arg,1,0);
    MEM16(c->frame+0x24)=(uint16_t)(MEM16(result)+0x7FFFu);
    return quantize(MEM32(c->frame+0x24));
}
static double read_double(uint32_t address)
{ double value; memcpy(&value,(const void *)(uintptr_t)ADDR(address),8); return value; }
static int32_t convert_top(void)
{ return (int32_t)call(0x77F110,0,NULL,0,0); }
static unsigned relative(void *opaque)
{
    AlliedContext *c=opaque;
    Ra2LegacyReal dx=ra2_real_subtract(ra2_real_from_i32((int32_t)MEM32(c->object+0x88)),
        ra2_real_from_i32((int32_t)MEM32(c->owner+0x88)),g_fpu_cw);
    /* 地图 y 轴与角度函数的 y 轴相反：此参数是 owner.y - object.y。 */
    Ra2LegacyReal dy=ra2_real_subtract(ra2_real_from_i32((int32_t)MEM32(c->owner+0x8C)),
        ra2_real_from_i32((int32_t)MEM32(c->object+0x8C)),g_fpu_cw);
    double args[2]={ra2_real_store_f64(dy,g_fpu_cw),ra2_real_store_f64(dx,g_fpu_cw)};
    uint32_t words[4]; memcpy(words,args,16);
    call(0x4BA600,0,words,4,1);
    Ra2LegacyReal angle=ra2_real_subtract(ra2_real_from_f64(g_st[0]),
        ra2_real_from_f64(read_double(0x79B630)),g_fpu_cw);
    angle=ra2_real_multiply(angle,ra2_real_from_f64(read_double(0x79B628)),g_fpu_cw);
    /* 不在整数转换前落成 double：16383.999... 的扩展精度值会被提前舍成 16384。 */
    fp_pop_impl(g_st,&g_fp_top);
    g_fpu_cw=(uint16_t)MEM32(0x7D8964);
    int32_t value=ra2_real_round_i32(angle,g_fpu_cw);
    MEM16(c->frame+0x28)=(uint16_t)value;
    return quantize(MEM32(c->frame+0x28));
}
static int32_t distance(void *opaque)
{
    AlliedContext *c=opaque; uint32_t arg=c->frame+0x60;
    uint32_t other=virtual_call(c->object,0x48,&arg,1);
    arg=c->frame+0x6C;
    uint32_t actor=virtual_call(c->owner,0x48,&arg,1);
    int32_t delta[3];
    for (unsigned i=0;i<3;++i)
    {
        uint32_t bits=MEM32(actor+i*4)-MEM32(other+i*4);
        memcpy(&delta[i],&bits,4); MEM32(c->frame+0x3C+i*4)=bits;
    }
    /* 原版乘加顺序是 x*x + z*z + y*y，并在调用近似开方前保存为 double。 */
    Ra2LegacyReal x=ra2_real_from_i32(delta[0]), y=ra2_real_from_i32(delta[1]), z=ra2_real_from_i32(delta[2]);
    Ra2LegacyReal sum=ra2_real_add(ra2_real_multiply(x,x,g_fpu_cw),ra2_real_multiply(z,z,g_fpu_cw),g_fpu_cw);
    sum=ra2_real_add(sum,ra2_real_multiply(y,y,g_fpu_cw),g_fpu_cw);
    double squared=ra2_real_store_f64(sum,g_fpu_cw); uint32_t words[2]; memcpy(words,&squared,8);
    call(0x4BA410,0,words,2,1);
    return convert_top();
}
static void remember(void *opaque, int present)
{ AlliedContext *c=opaque; MEM32(c->frame+0x20)=present ? c->object : 0; }

uint32_t ra2_ground_allied_bridge(void)
{
    AlliedContext c={g_esp,g_ebp,MEM32(g_esp+0x7C),g_esi};
    ra2_state_movement_audit(25,c.owner,c.cell,c.object);
    Ra2AlliedServices services={&c,query,heading,opposite,relative,distance,remember};
    int32_t passage=(int32_t)MEM32(c.frame+0x8C);
    g_esp=c.frame-0x100;
    Ra2AlliedOutcome outcome=ra2_ground_classify_allied_motion(&passage,&services);
    MEM32(c.frame+0x8C)=(uint32_t)passage;
    g_esp=c.frame; g_ebp=c.owner; g_ebx=c.cell; g_esi=c.object; g_edi=(uint32_t)passage;
    switch (outcome)
    {
        case RA2_ALLIED_CLEAR: return 0x7031B1;
        case RA2_ALLIED_BLOCKED: return 0x703B5A;
        case RA2_ALLIED_CHECK_ENEMY: return 0x70397C;
        case RA2_ALLIED_CHECK_STATIONARY: return 0x70394F;
        default: return 0x7038EF;
    }
}

uint32_t ra2_ground_moving_tail_bridge(void)
{
    uint32_t frame=g_esp,object=g_esi;
    AlliedContext c={frame,MEM32(frame+0x14),MEM32(frame+0x7C),MEM32(frame+0x20)};
    Ra2AlliedServices services={&c,query,heading,opposite,relative,distance,remember};
    g_esp=frame-0x100;
    /* The locomotor callback can update the caller's passage slot. */
    ra2_ground_classify_moving_tail((int32_t *)(uintptr_t)ADDR(frame+0x8C),&services);
    g_esp=frame;g_ebp=MEM32(frame+0x14);g_esi=object;g_edi=c.object;
    return 0x7038EF;
}

uint32_t ra2_ground_allied_relation_bridge(void)
{
    AlliedContext c={g_esp,MEM32(g_esp+0x14),MEM32(g_esp+0x7C),g_esi};
    Ra2AlliedServices services={&c,query,heading,opposite,relative,distance,remember};
    int moving=(g_ebx&255u)!=0;
    int32_t passage=(int32_t)MEM32(c.frame+0x8C);
    g_esp=c.frame-0x100;
    Ra2AlliedOutcome outcome=ra2_ground_classify_allied_relation(moving,&passage,&services);
    MEM32(c.frame+0x8C)=(uint32_t)passage;
    g_esp=c.frame;g_ebp=c.owner;g_ebx=c.cell;g_esi=c.object;g_edi=(uint32_t)passage;
    switch(outcome)
    {
        case RA2_ALLIED_CHECK_ENEMY:return 0x70397C;
        case RA2_ALLIED_CHECK_STATIONARY:return 0x70394F;
        case RA2_ALLIED_BLOCKED:return 0x703B5A;
        default:return 0x7038EF;
    }
}
