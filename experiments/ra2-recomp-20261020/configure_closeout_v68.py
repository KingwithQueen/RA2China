"""Readonly diagnosis and legal counterfactuals; never inject paths, budgets or targets."""
from run_batch_v68 import *
import re
def section(t,key,value):
    pat=rf'(?ms)^\[{key}\]\n.*?(?=^\[|\Z)';new='['+key+']\n'+value+'\n'
    return re.sub(pat,lambda _:new,t) if re.search(pat,t) else t+'\n'+new
items=[]
parent=read(O/'traffic-fixtures.json')['fixtures']
for old in parent:
    x=dict(old);x['path']=(S/'fixtures'/Path(x['path']).name).relative_to(R).as_posix()
    x['tag']='rq-boundary' if x['kind']=='reverse' else 'bm-stop';x['last']=5400
    x['parent_tag']=old['tag'];x['classification']='retained-boundary'
    items.append(x)
x=dict(items[0]);x.update(tag='rq-valid',classification='corrected-legal-targets')
# Change only the four out-of-area requests; keep starts, timing, terrain and blockers.
replacements={1022585:[66,110],1022588:[67,112],1022589:[67,116],1022590:[68,118]}
x['events']=[dict(e,cell=replacements[e['id']]) if e['id'] in replacements and e['stage']=='request' else dict(e) for e in x['events']]
x['orders']=[f"{e['frame']}:{e['id']}:2:{e['cell'][0]}:{e['cell'][1]}" for e in x['events']]
x['goals']={str(e['id']):e['cell'] for e in x['events']};items.append(x)
source=S/'fixtures/traffic-bm.MAP';t=source.read_text(encoding='ascii')
for tag,occupied in [('stop-free',False),('stop-occupied',True)]:
    rows='0=Player House,TRUCKA,256,77,76,0,Guard,None,0,-1,0,-1,1,1\n'
    if occupied:rows+='1=Player House,TRUCKA,256,57,76,0,Sleep,None,0,-1,0,-1,1,1\n'
    out=section(section(t,'Units',rows),'Infantry','');p=S/'fixtures'/(tag+'.MAP');p.write_text(out,encoding='ascii',newline='\n')
    strip=lambda z:section(section(z,'Units',''),'Infantry','')
    assert strip(out)==strip(t)
    # Unit identity is calibrated from frame zero, rather than guessed from editor order.
    items.append(dict(tag=tag,path=p.relative_to(R).as_posix(),last=2400,orders=[],calibrate=True,occupied=occupied,classification='stop-occupation-control'))
rules_source=Path(read(O/'collision-acceptance-fixtures.json')['original_rules_source'])
rules=rules_source.read_text(encoding='cp936');assert len(re.findall(r'(?m)^CloseEnough=2\.25(?=[ \t;]|$)',rules))==1
zero=re.sub(r'(?m)^CloseEnough=2\.25(?=[ \t;]|$)', 'CloseEnough=0',rules)
rp=S/'fixtures/rules-zero-close.ini';rp.write_text(zero,encoding='cp936',newline='\n')
x=dict(items[1]);x.update(tag='bm-zero',rules=rp.relative_to(R).as_posix(),classification='explicit-zero-distance-counterfactual');items.append(x)
write(S/'scene-recipes-pending.json',dict(passed=True,fixtures=items,corrections=replacements,rules_original=str(rules_source),rules_original_sha256=sha(rules_source),zero_rule_sha256=sha(rp),zero_rule_is_override=True))
# Extend only the independent observer. All diagnostics read memory and write the trace file.
block=r'''
    if(frame==first_frame)
        fprintf(state_file,"{\"kind\":\"fixture-map-area\",\"frame\":%u,\"width\":%d,\"local\":[%d,%d,%d,%d],\"close_enough\":%d}\n",frame,
            I32(0x8325D0),I32(0x8325D8),I32(0x8325DC),I32(0x8325E0),I32(0x8325E4),I32(U32(0x839848)+0x1380));
    for(uint32_t index=0;index<U32(0xA40C30);++index)
    {
        uint32_t actor=U32(U32(0xA40C24)+index*4);
        if(U32(actor)!=0x7ADDF8)continue;
        uint32_t active=U32(actor+0x564);
        if(!active || U32(active)!=0x7A04CC)continue;
        uint32_t id=U32(actor+0x10),target=U32(actor+0x494),last=MAX_ORDERS;
        for(int k=0;k<order_count;++k)if(orders[k].mission==2 && orders[k].id==id && orders[k].frame<=frame)last=(uint32_t)k;
        if(last==MAX_ORDERS)continue;
        int x=(int)orders[last].x,y=(int)orders[last].y,slot=y*512+x;
        uint32_t cell=slot>=0 && slot<262144 ? U32(U32(0x832618)+(uint32_t)slot*4):0;
        fprintf(state_file,"{\"kind\":\"fixture-move-boundary\",\"frame\":%u,\"id\":%u,\"requested\":[%d,%d],\"goal_cell\":[%d,%u,%u],\"navigation\":[%u,%d,%d],\"destination\":[%d,%d,%d]}\n",frame,id,x,y,
            cell?(int8_t)U8(cell+0x11B):0,cell?U8(cell+0x11C):0,cell?U32(cell+0x124):0,
            target?U32(target):0,target?(int16_t)U16(target+0x24):0,target?(int16_t)U16(target+0x26):0,
            I32(active+0x30),I32(active+0x34),I32(active+0x38));
    }
'''
p=R/'make_bridge_catalog_v68.py';text=p.read_text(encoding='utf-8');marker="q=S/'bridge_catalog_observer.c'";assert text.count(marker)==1
text=text.replace(marker,"t=t.replace('    write_cell_catalog(frame);','    write_cell_catalog(frame);'+"+repr(block)+")\n"+marker)
p.write_text(text,encoding='utf-8')
write(S/'observer-scope.json',dict(passed=True,production_recorder_sha256=sha(R/'ra2/src/runtime/state_trace.c'),additional_records=['fixture-map-area','fixture-move-boundary'],engine_queries=False,game_memory_writes=False,scope='Raw map/local area, CloseEnough, latest ordinary order, ground occupation bits and current navigation cell/destination. No causal claims from mere proximity.'))
print(dict(passed=True,recipes=len(items),corrected_targets=4,readonly_observer=True))
