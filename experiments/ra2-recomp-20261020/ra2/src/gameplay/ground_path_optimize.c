#include "ground_path_optimize.h"
#include <stdlib.h>

static Ra2PathPoint add(Ra2PathPoint a,Ra2PathPoint b)
{return (Ra2PathPoint){(int16_t)(a.x+b.x),(int16_t)(a.y+b.y)};}
static Ra2PathPoint subtract(Ra2PathPoint a,Ra2PathPoint b)
{return (Ra2PathPoint){(int16_t)(a.x-b.x),(int16_t)(a.y-b.y)};}
static int distance(Ra2PathPoint p){int x=abs(p.x),y=abs(p.y);return x>y?x:y;}
static int nonzero(Ra2PathPoint p){return p.x!=0||p.y!=0;}

typedef struct Ra2SmoothScan {
    int32_t first_start,first_count,second_start,second_count;
    int32_t previous,second_direction;
    int pairing;
    Ra2PathPoint anchor,point;
} Ra2SmoothScan;

static void finish_smooth_pair(Ra2SmoothScan *s,const Ra2PathOptimizationServices *v,
    int32_t *directions,int32_t *levels)
{
    s->first_start+=v->shorten_turn(v->context,directions+s->first_start,levels+s->first_start,
        s->first_count,s->second_count,&s->anchor);
    /* 服务可改方向、层高和锚点；返回后才重读新起点方向与偏移表。 */
    s->previous=directions[s->first_start];s->first_count=1;s->pairing=0;
    s->point=add(s->anchor,v->offsets[s->previous&7]);
}

static void advance_smooth_scan(Ra2SmoothScan *s,const Ra2PathOptimizationServices *v,
    const int32_t *directions)
{
    int32_t index=s->first_start+s->first_count,direction=directions[index];
    unsigned turn=((uint32_t)direction-(uint32_t)s->previous)&7;
    if(direction==s->previous)++s->first_count;
    else if((turn==2||turn==6) && s->previous!=-1 && s->previous!=8 && direction!=8) {
        s->pairing=1;s->second_direction=direction;s->second_start=index;s->second_count=1;
    } else {
        s->first_start=index;s->first_count=1;s->previous=(direction&1)?direction:-1;s->anchor=s->point;
    }
    /* 平滑阶段的特殊连接查询使用同一当前点；普通方向不额外归一化。 */
    s->point=direction==8?v->connection_exit(v->context,&s->point):add(s->point,v->offsets[direction]);
}

void ra2_path_smooth(Ra2RebuiltPath *path,const Ra2PathOptimizationServices *v)
{
    int32_t last=path->length-1;
    Ra2SmoothScan scan={0};scan.previous=-1;scan.second_direction=-1;
    scan.anchor=path->start;scan.point=path->start;
    int32_t *directions=path->directions,*levels=path->surface_levels;
    while(scan.first_start+scan.first_count<last && scan.second_start+scan.second_count<last) {
        if(scan.pairing) {
            if(directions[scan.second_start+scan.second_count]==scan.second_direction){++scan.second_count;continue;}
            finish_smooth_pair(&scan,v,directions,levels);continue;
        }
        advance_smooth_scan(&scan,v,directions);
    }
    /* 末尾配对只发服务调用，沿用忽略返回值、不再重读方向或推进点的行为。 */
    if(scan.pairing)v->shorten_turn(v->context,directions+scan.first_start,levels+scan.first_start,
        scan.first_count,scan.second_count,&scan.anchor);
}

static void rewrite_postprocess_segment(const Ra2PathOptimizationServices *v,
    int32_t *directions,int32_t *levels,int32_t index,int32_t start,Ra2PathPoint point,int final_segment)
{
    int32_t anchor_index;Ra2PathPoint anchor=point;
    v->find_anchor(v->context,directions,final_segment?index-1:index,start,&anchor_index,&anchor);
    /* 锚点服务可修改索引、锚点和缓冲；之后才算差量、长度并读取该槽层高。 */
    Ra2PathPoint delta=subtract(point,anchor);
    int32_t count=final_segment?index-anchor_index:index-anchor_index+1;
    v->rewrite_segment(v->context,directions+anchor_index,count,&anchor,&delta,levels[anchor_index],final_segment);
    /* 改写服务对局部锚点/差量的反馈不回写扫描点，保持原有服务边界。 */
}

static void compact_postprocess_directions(Ra2RebuiltPath *path,int32_t *directions,int32_t last)
{
    /* last是入口快照；补槽时仍读取实时length，只压方向、不搬层高。 */
    int32_t written=0;
    for(int32_t i=0;i<last && directions[i]!=-1;++i)if(directions[i]!=-2)directions[written++]=directions[i];
    for(int32_t i=written;i<path->length+1;++i)directions[i]=-1;
    path->length=written+1;
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
            rewrite_postprocess_segment(v,directions,levels,index,segment_start,point,0);
        }
        candidate_delta=next_candidate;++index;
    }
    if(nonzero(checkpoint) && index-checkpoint_index-1>distance(subtract(point,checkpoint))) {
        rewrite_postprocess_segment(v,directions,levels,index,checkpoint_index,point,1);
    }
    compact_postprocess_directions(path,directions,last);
}
