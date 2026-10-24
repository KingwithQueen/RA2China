"""Small reversible phase extraction; service reads stay at their original call sites."""
from run_batch_v52 import *
name=sys.argv[1]
if name=='prepare':
 p=R/'ra2/src/gameplay/ground_prepare.c';before=S/'baseline/ra2/src/gameplay/ground_prepare.c'
 assert sha(p)==sha(before)
 t=p.read_text(encoding='utf-8')
 start=t.index('    if (*cached_path_head != -1)');end=t.index('\nint ra2_ground_retry_timer_ready',start)
 block=t[start:end];assert block.endswith('    return RA2_PREPARE_RETRY_PATH;\n}\n')
 helper='static Ra2PreparePhase prepare_queued_path(int32_t *cached_path_head,\n    const Ra2PrepareServices *services)\n{\n'+block
 t=t[:start]+'    return prepare_queued_path(cached_path_head, services);\n}\n'+t[end:]
 marker='Ra2PreparePhase ra2_ground_prepare_entry('
 t=t.replace(marker,helper+'\n'+marker,1)
 start=t.index('    if (!query(services, RA2_PREPARE_OWNER_EXISTS))',t.index('Ra2PreparePhase ra2_ground_retry_path'))
 block=t[start:];assert block.endswith('    return RA2_PREPARE_INSPECT_OBSTACLE;\n}\n')
 helper='static Ra2PreparePhase finish_failed_rebuild(Ra2GroundPrepareState *state,\n    Ra2WorldPoint invalid_position, const Ra2PrepareServices *services)\n{\n'+block
 t=t[:start]+'    /* 重建服务可能移除所属对象或改变目标，失败后的判断留在服务之后。 */\n    return finish_failed_rebuild(state, invalid_position, services);\n}\n'
 marker='Ra2PreparePhase ra2_ground_retry_path('
 t=t.replace(marker,helper+'\n'+marker,1)
elif name=='advance':
 p=R/'ra2/src/gameplay/ground_advance.c';before=S/'baseline/ra2/src/gameplay/ground_advance.c'
 assert sha(p)==sha(before)
 t=p.read_text(encoding='utf-8')
 start=t.index('    int32_t index = s->query(c, RA2_ADVANCE_SAMPLE_INDEX, 0);',t.index('int ra2_ground_advance_sample('))
 end=t.index('    Ra2WorldPoint raw_position = s->raw_position(c);',start)
 old=t[start:end]
 expected='''    int32_t index = s->query(c, RA2_ADVANCE_SAMPLE_INDEX, 0);
    Ra2AdvanceCell previous;
    if (!index) previous = s->current_cell(c);
    else
    {
        Ra2PathSample prior_sample = s->sample(c, index - 1, 1);
        previous = cell_of(s->transform_sample(c, &prior_sample, 1));
    }
    index = s->query(c, RA2_ADVANCE_SAMPLE_INDEX, 0);
    Ra2PathSample sample = s->sample(c, index, 0);
    Ra2WorldPoint position = s->transform_sample(c, &sample, 0);
    position.z = 0;
'''
 assert old==expected
 replacement='''    Ra2AdvanceCell previous = previous_sample_cell(s, c);
    Ra2PathSample sample;
    Ra2WorldPoint position = current_sample_position(s, c, &sample);
'''
 t=t[:start]+replacement+t[end:]
 helper='''static Ra2AdvanceCell previous_sample_cell(const Ra2AdvanceServices *s, void *c)
{
    int32_t index = s->query(c, RA2_ADVANCE_SAMPLE_INDEX, 0);
    if (!index) return s->current_cell(c);
    Ra2PathSample prior_sample = s->sample(c, index - 1, 1);
    return cell_of(s->transform_sample(c, &prior_sample, 1));
}

static Ra2WorldPoint current_sample_position(const Ra2AdvanceServices *s, void *c,
    Ra2PathSample *sample)
{
    /* 前一采样的变换服务可改索引；当前索引必须在服务之后重新查询。 */
    int32_t index = s->query(c, RA2_ADVANCE_SAMPLE_INDEX, 0);
    *sample = s->sample(c, index, 0);
    Ra2WorldPoint position = s->transform_sample(c, sample, 0);
    position.z = 0;
    return position;
}

'''
 t=t.replace('int ra2_ground_advance_sample(',helper+'int ra2_ground_advance_sample(',1)
else:raise ValueError(name)
eol=b'\r\n' if b'\r\n' in p.read_bytes() else b'\n'
p.write_bytes(t.replace('\r\n','\n').encode('utf-8').replace(b'\n',eol))
print(dict(passed=True,phase=name,source=p.relative_to(R).as_posix(),sha256=sha(p)))
