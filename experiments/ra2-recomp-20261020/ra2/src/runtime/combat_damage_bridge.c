#include <string.h>
#include "recomp_types.h"
#include "combat_damage.h"
#include "combat_damage_bridge.h"

static float read_float(uint32_t address)
{float value;memcpy(&value,(void *)(uintptr_t)ADDR(address),4);return value;}
void ra2_combat_damage_bridge(void)
{
    uint32_t entry=g_esp,frame=entry-20,warhead=g_edx;
    Ra2CombatDamageInput in={0};in.damage=(int32_t)g_ecx;in.distance=(int32_t)MEM32(entry+8);
    in.arithmetic_control=g_fpu_cw;in.warhead_present=warhead!=0;
    if(in.damage)in.disabled=(MEM8(MEM32(0xA3D290))&0x20)!=0;
    if(in.damage>0 && !in.disabled && in.warhead_present) {
        in.cell_spread=read_float(warhead+0x124);in.percent_at_max=read_float(warhead+0x12C);
        in.units_per_cell=read_float(0x79B0AC);
        memcpy(&in.armor_multiplier,(void *)(uintptr_t)ADDR(warhead+MEM32(entry+4)*8+0xA0),8);
        in.maximum_damage=(int32_t)MEM32(MEM32(0x839848)+0x1330);in.conversion_control=MEM16(0x7D8964);
    }
    Ra2CombatDamageResult out=ra2_combat_adjust_damage(&in);
    MEM32(frame)=g_edi;MEM32(frame+4)=g_esi;MEM32(frame+12)=(uint32_t)in.damage;
    if(out.positive_path) {
        memcpy((void *)(uintptr_t)ADDR(frame+8),&out.initial_damage,4);
        memcpy((void *)(uintptr_t)ADDR(frame+12),&out.edge_damage,4);
        MEM32(frame+16)=(uint32_t)out.spread_distance;MEM32(entry+8)=(uint32_t)out.before_armor;
        g_ecx=(uint32_t)in.maximum_damage;g_edx=out.conversion_high;
    }
    g_eax=(uint32_t)out.damage;g_fpu_cw=out.final_control;g_esp=entry+12;
    g_flag_k=FK_ADD;g_flag_a=entry-12;g_flag_b=12;g_flag_cf=entry<entry-12;
}
