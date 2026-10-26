#include "combat_damage.h"
#include "x87_arithmetic.h"
#include <stdlib.h>
#include <string.h>

static unsigned leading_bit(uint64_t value)
{unsigned n=0;while(value>>1){value>>=1;++n;}return n;}
static int increment(uint64_t retained,uint64_t remainder,uint64_t divisor,
    unsigned negative,uint16_t control)
{
    if(!remainder)return 0;
    switch((control>>10)&3) {
        case 0:return remainder>divisor-remainder ||
            (remainder==divisor-remainder && (retained&1));
        case 1:return negative!=0;
        case 2:return negative==0;
        default:return 0;
    }
}
/* 逐位商保留完整余数；不借助宿主double先舍入，覆盖原版64位精度除法。 */
static Ra2LegacyReal divide_integer(Ra2LegacyReal value,int32_t divisor,uint16_t control)
{
    Ra2LegacyReal d=ra2_real_from_i32(divisor),out={0,0,value.negative^d.negative};
    if(!d.significand)abort();
    if(!value.significand)return out;
    unsigned precision;
    switch((control>>8)&3){case 0:precision=24;break;case 2:precision=53;break;case 3:precision=64;break;default:abort();}
    unsigned a=leading_bit(value.significand),b=leading_bit(d.significand);
    int32_t exponent=value.exponent+(int32_t)a-d.exponent-(int32_t)b;
    uint64_t numerator=value.significand<<(63-a),denominator=d.significand<<(63-b),remainder,quotient=1;
    if(numerator>=denominator)remainder=numerator-denominator;
    else {remainder=(numerator<<1)-denominator;--exponent;}
    for(unsigned bit=1;bit<precision;++bit) {
        unsigned carry=(unsigned)(remainder>>63);remainder<<=1;quotient<<=1;
        if(carry || remainder>=denominator){remainder-=denominator;quotient|=1;}
    }
    if(increment(quotient,remainder,denominator,out.negative,control)) {
        ++quotient;
        if(!quotient){quotient=UINT64_C(1)<<63;++exponent;}
        else if(precision<64 && quotient==(UINT64_C(1)<<precision)){quotient>>=1;++exponent;}
    }
    out.significand=quotient;out.exponent=exponent-(int32_t)(precision-1);return out;
}
static int64_t convert_integer(Ra2LegacyReal value,uint16_t control)
{
    uint64_t magnitude;
    if(value.exponent>=0) {
        if(value.exponent>=64 || value.significand>(UINT64_MAX>>value.exponent))return INT64_MIN;
        magnitude=value.significand<<value.exponent;
    } else {
        unsigned shift=(unsigned)-value.exponent;
        magnitude=shift<64?value.significand>>shift:0;
        uint64_t remainder=shift<64?value.significand&((UINT64_C(1)<<shift)-1):value.significand;
        unsigned mode=(control>>10)&3;int round=0;
        if(remainder) {
            if(mode==0 && shift<=64) {
                uint64_t half=UINT64_C(1)<<(shift-1);
                round=remainder>half || (remainder==half && (magnitude&1));
            } else if(mode==1)round=value.negative!=0;
            else if(mode==2)round=value.negative==0;
        }
        magnitude+=(unsigned)round;
    }
    if(magnitude>(UINT64_C(1)<<63) || (magnitude==(UINT64_C(1)<<63) && !value.negative))return INT64_MIN;
    uint64_t bits=value.negative?0-magnitude:magnitude;int64_t result;memcpy(&result,&bits,8);return result;
}
static int32_t low_word(int64_t value)
{uint32_t bits=(uint32_t)value;int32_t out;memcpy(&out,&bits,4);return out;}
static int32_t subtract_wrapped(int32_t a,int32_t b)
{uint32_t bits=(uint32_t)a-(uint32_t)b;int32_t out;memcpy(&out,&bits,4);return out;}
Ra2CombatDamageResult ra2_combat_adjust_damage(const Ra2CombatDamageInput *in)
{
    Ra2CombatDamageResult out={0};out.final_control=in->arithmetic_control;
    if(!in->damage || in->disabled || !in->warhead_present)return out;
    if(in->damage<0){out.damage=in->distance<8?in->damage:0;return out;}
    out.positive_path=1;
    out.initial_damage=ra2_real_store_f32(ra2_real_from_i32(in->damage),in->arithmetic_control);
    out.edge_damage=ra2_real_store_f32(ra2_real_multiply(ra2_real_from_i32(in->damage),
        ra2_real_from_f32(in->percent_at_max),in->arithmetic_control),in->arithmetic_control);
    Ra2LegacyReal extent=ra2_real_multiply(ra2_real_from_f32(in->cell_spread),
        ra2_real_from_f32(in->units_per_cell),in->arithmetic_control);
    out.spread_distance=low_word(convert_integer(extent,in->conversion_control));
    out.final_control=in->conversion_control;
    int32_t damage=in->damage;
    if(out.initial_damage!=out.edge_damage && out.spread_distance) {
        Ra2LegacyReal falloff=ra2_real_subtract(ra2_real_from_f32(out.initial_damage),
            ra2_real_from_f32(out.edge_damage),out.final_control);
        falloff=ra2_real_multiply(falloff,ra2_real_from_i32(subtract_wrapped(out.spread_distance,in->distance)),out.final_control);
        falloff=divide_integer(falloff,out.spread_distance,out.final_control);
        falloff=ra2_real_add(falloff,ra2_real_from_f32(out.edge_damage),out.final_control);
        damage=low_word(convert_integer(falloff,out.final_control));out.distance_interpolated=1;
    }
    out.before_armor=damage>0?damage:0;
    int64_t adjusted=convert_integer(ra2_real_multiply(ra2_real_from_i32(out.before_armor),
        ra2_real_from_f64(in->armor_multiplier),out.final_control),out.final_control);
    int32_t result=low_word(adjusted);out.conversion_high=(uint32_t)((uint64_t)adjusted>>32);
    out.damage=result<in->maximum_damage?result:in->maximum_damage;return out;
}
