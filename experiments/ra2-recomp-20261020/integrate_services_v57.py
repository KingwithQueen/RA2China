"""Two content-checked, reversible phases in the existing optimization unit."""
from run_batch_v57 import *
p=R/'ra2/src/gameplay/ground_path_optimize.c';part=sys.argv[1]
t=p.read_text(encoding='utf-8')
if part=='smooth':
 assert sha(p)==sha(S/'baseline/ra2/src/gameplay/ground_path_optimize.c')
 a=t.index('void ra2_path_smooth(');b=t.index('/* 原版仅扫描前20步',a)
 block='''typedef struct Ra2SmoothScan {
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

'''
 t=t[:a]+block+t[b:]
elif part=='postprocess':
 assert 'finish_smooth_pair' in t and 'rewrite_postprocess_segment' not in t
 old='''            int32_t anchor_index;Ra2PathPoint anchor=point;
            v->find_anchor(v->context,directions,index,segment_start,&anchor_index,&anchor);
            Ra2PathPoint delta=subtract(point,anchor);
            v->rewrite_segment(v->context,directions+anchor_index,index-anchor_index+1,&anchor,&delta,levels[anchor_index],0);'''
 assert t.count(old)==1
 t=t.replace(old,'            rewrite_postprocess_segment(v,directions,levels,index,segment_start,point,0);')
 old='''        int32_t anchor_index;Ra2PathPoint anchor=point;
        v->find_anchor(v->context,directions,index-1,checkpoint_index,&anchor_index,&anchor);
        Ra2PathPoint delta=subtract(point,anchor);
        v->rewrite_segment(v->context,directions+anchor_index,index-anchor_index,&anchor,&delta,levels[anchor_index],1);'''
 assert t.count(old)==1
 t=t.replace(old,'        rewrite_postprocess_segment(v,directions,levels,index,checkpoint_index,point,1);')
 a=t.index('    int32_t written=0;',t.index('void ra2_path_postprocess('));b=t.index('\n}',a)
 compact=t[a:b]
 t=t[:a]+'    compact_postprocess_directions(path,directions,last);'+t[b:]
 helpers='''static void rewrite_postprocess_segment(const Ra2PathOptimizationServices *v,
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
'''+compact+'''
}

'''
 t=t.replace('/* 原版仅扫描前20步',helpers+'/* 原版仅扫描前20步',1)
else:raise ValueError(part)
eol=b'\r\n' if b'\r\n' in p.read_bytes() else b'\n';p.write_bytes(t.encode('utf-8').replace(b'\n',eol))
print(dict(passed=True,part=part,source_sha256=sha(p)))
