#pragma once
#include "x87_arithmetic.h"

/* Order finite legacy values exactly, without first rounding to float or double. */
static inline unsigned ra2_combat_real_top_bit(uint64_t value){unsigned n=0;while(value>>=1)++n;return n;}
static inline int ra2_combat_compare_legacy_real(Ra2LegacyReal a,Ra2LegacyReal b)
{
    if(!a.significand)a.negative=0;
    if(!b.significand)b.negative=0;
    if(a.negative!=b.negative)return a.negative?-1:1;
    int magnitude;
    if(!a.significand || !b.significand)magnitude=(a.significand!=0)-(b.significand!=0);
    else {
        unsigned at=ra2_combat_real_top_bit(a.significand),bt=ra2_combat_real_top_bit(b.significand);
        int32_t ae=a.exponent+(int32_t)at,be=b.exponent+(int32_t)bt;
        if(ae!=be)magnitude=(ae>be)-(ae<be);
        else {uint64_t av=a.significand<<(63-at),bv=b.significand<<(63-bt);magnitude=(av>bv)-(av<bv);}
    }
    return a.negative?-magnitude:magnitude;
}
