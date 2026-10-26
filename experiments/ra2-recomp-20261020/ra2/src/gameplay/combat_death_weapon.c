#include <string.h>
#include "combat_death_weapon.h"
#include "x87_arithmetic.h"

Ra2DeathWeaponSelection ra2_select_death_weapon(const Ra2DeathWeaponServices *s)
{
    Ra2DeathWeaponSelection result;unsigned fallback=0;
    /* 虚调用可以改变类型或武器槽；保留原版第二次查询，不能复用首次资格检查的值。 */
    if(s->query(s->context,RA2_DW_EXPLICIT_WEAPON))result.weapon=s->query(s->context,RA2_DW_EXPLICIT_WEAPON);
    else if(s->query(s->context,RA2_DW_SLOT_HAS_WEAPON))result.weapon=s->query(s->context,RA2_DW_SLOT_WEAPON);
    else {result.weapon=s->query(s->context,RA2_DW_DEFAULT_WEAPON);fallback=1;}
    result.damage=s->damage(s->context,result.weapon,fallback);return result;
}
int32_t ra2_death_weapon_damage(int32_t base,double multiplier,uint16_t arithmetic_control,uint16_t conversion_control)
{
    uint64_t bits;memcpy(&bits,&multiplier,sizeof(bits));
    /* 屏蔽异常的x87整数转换：非有限数或64位溢出产生不定值，其低32位为零。 */
    if((bits&UINT64_C(0x7FF0000000000000))==UINT64_C(0x7FF0000000000000))return 0;
    Ra2LegacyReal value=ra2_real_multiply(ra2_real_from_i32(base),ra2_real_from_f64(multiplier),arithmetic_control);
    uint64_t top=value.significand;int32_t exponent=value.exponent;
    while(top>1){top>>=1;++exponent;}
    if(top && exponent>=63)return 0;
    return ra2_real_round_i32(value,conversion_control);
}
