#pragma once
#include "ground_path_distance.h"
#include <stdlib.h>

/* Number of straight or diagonal steps spanned by a local grid delta. */
static inline int ra2_ground_path_delta_span(Ra2PathPoint p){int x=abs(p.x),y=abs(p.y);return x>y?x:y;}

/* Apply one local tile offset, retaining the per-axis signed field width. */
static inline Ra2PathPoint ra2_ground_path_point_add(Ra2PathPoint a,Ra2PathPoint b)
{return (Ra2PathPoint){(int16_t)(a.x+b.x),(int16_t)(a.y+b.y)};}
