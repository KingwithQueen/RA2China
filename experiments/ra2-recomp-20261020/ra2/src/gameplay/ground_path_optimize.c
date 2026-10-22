#include "ground_path_optimize.h"
#include <stdlib.h>

static Ra2PathPoint add(Ra2PathPoint a,Ra2PathPoint b)
{return (Ra2PathPoint){(int16_t)(a.x+b.x),(int16_t)(a.y+b.y)};}
static Ra2PathPoint subtract(Ra2PathPoint a,Ra2PathPoint b)
{return (Ra2PathPoint){(int16_t)(a.x-b.x),(int16_t)(a.y-b.y)};}
static int distance(Ra2PathPoint p){int x=abs(p.x),y=abs(p.y);return x>y?x:y;}
static int nonzero(Ra2PathPoint p){return p.x!=0||p.y!=0;}

void ra2_path_smooth(Ra2RebuiltPath *path,const Ra2PathOptimizationServices *v)
{
    int32_t last=path->length-1,first_start=0,first_count=0,second_start=0,second_count=0;
    int32_t previous=-1,second_direction=-1;
    int pairing=0;Ra2PathPoint anchor=path->start,point=path->start;
    int32_t *directions=path->directions,*levels=path->surface_levels;
    while(first_start+first_count<last && second_start+second_count<last) {
        if(pairing) {
            if(directions[second_start+second_count]==second_direction){++second_count;continue;}
            first_start+=v->shorten_turn(v->context,directions+first_start,levels+first_start,first_count,second_count,&anchor);
            previous=directions[first_start];first_count=1;pairing=0;
            point=add(anchor,v->offsets[previous&7]);
            continue;
        }
        int32_t index=first_start+first_count,direction=directions[index];
        unsigned turn=((uint32_t)direction-(uint32_t)previous)&7;
        if(direction==previous)++first_count;
        else if((turn==2||turn==6) && previous!=-1 && previous!=8 && direction!=8) {
            pairing=1;second_direction=direction;second_start=index;second_count=1;
        } else {
            first_start=index;first_count=1;previous=(direction&1)?direction:-1;anchor=point;
        }
        point=direction==8?v->connection_exit(v->context,&point):add(point,v->offsets[direction]);
    }
    if(pairing)v->shorten_turn(v->context,directions+first_start,levels+first_start,first_count,second_count,&anchor);
}

/* 原版仅扫描前20步寻找折返；局部改写可将方向标成-2。
 * 结束时只压紧方向数组，保留原高度槽，并补到旧长度的额外一个终止槽。 */
void ra2_path_postprocess(Ra2RebuiltPath *path,const Ra2PathOptimizationServices *v)
{
    int32_t *directions=path->directions,*levels=path->surface_levels;
    int32_t last=path->length-1,index=0,segment_start=0,checkpoint_index=0;
    Ra2PathPoint point=path->start,checkpoint={0,0},run_delta={0,0},candidate_delta={0,0};
    int max_x=0,max_y=0,max_distance=0;
    while(index<last && index<20) {
        int32_t direction=directions[index];
        if(direction==8) {
            /* 此处原版走方向0并清空统计；与平滑阶段的特殊连接查询不同。 */
            point=add(point,v->offsets[0]);run_delta=(Ra2PathPoint){0,0};candidate_delta=run_delta;
            checkpoint=run_delta;max_x=max_y=max_distance=0;segment_start=checkpoint_index=++index;continue;
        }
        if(direction==-2){++index;continue;}
        Ra2PathPoint step=v->offsets[direction&7];
        Ra2PathPoint next_run=add(run_delta,step),next_candidate=add(candidate_delta,step);
        if(abs(next_run.x)<max_x || abs(next_run.y)<max_y) {
            if(nonzero(checkpoint)) {
                segment_start=checkpoint_index;candidate_delta=subtract(checkpoint,point);max_distance=distance(candidate_delta);
            }
            checkpoint=point;checkpoint_index=index;max_x=max_y=0;run_delta=(Ra2PathPoint){0,0};
            continue; /* 同一步在重置参照点后重新检查，不能提前推进。 */
        }
        run_delta=next_run;max_x=abs(next_run.x);max_y=abs(next_run.y);point=add(point,step);
        if(distance(next_candidate)>max_distance)max_distance=distance(next_candidate);
        else {
            int32_t anchor_index;Ra2PathPoint anchor=point;
            v->find_anchor(v->context,directions,index,segment_start,&anchor_index,&anchor);
            Ra2PathPoint delta=subtract(point,anchor);
            v->rewrite_segment(v->context,directions+anchor_index,index-anchor_index+1,&anchor,&delta,levels[anchor_index],0);
        }
        candidate_delta=next_candidate;++index;
    }
    if(nonzero(checkpoint) && index-checkpoint_index-1>distance(subtract(point,checkpoint))) {
        int32_t anchor_index;Ra2PathPoint anchor=point;
        v->find_anchor(v->context,directions,index-1,checkpoint_index,&anchor_index,&anchor);
        Ra2PathPoint delta=subtract(point,anchor);
        v->rewrite_segment(v->context,directions+anchor_index,index-anchor_index,&anchor,&delta,levels[anchor_index],1);
    }
    int32_t written=0;
    for(int32_t i=0;i<last && directions[i]!=-1;++i)if(directions[i]!=-2)directions[written++]=directions[i];
    for(int32_t i=written;i<path->length+1;++i)directions[i]=-1;
    path->length=written+1;
}
