#pragma once
#include "ground_path_distance.h"
#include <stdlib.h>

/* Number of straight or diagonal steps spanned by a local grid delta. */
static inline int ra2_ground_path_delta_span(Ra2PathPoint p){int x=abs(p.x),y=abs(p.y);return x>y?x:y;}
