"""把本轮扩展实景结论合入早期条件分析，避免旧的未命中描述覆盖新证据。"""
from pathlib import Path
import json,shutil
def reconcile(stage):
    read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    p=stage/'budget-conditions.json';prior=stage/'budget-conditions-before-new-scenes.json'
    if not prior.exists():shutil.copy2(p,prior)
    current=read(p);real=read(stage/'budget-real-scenes.json');assert real['natural_exhaustion_verified']
    if 'original_27_natural_budget_entries' not in current:current['original_27_natural_budget_entries']=current.get('natural_budget_entries',[])
    current['natural_budget_entries']=[dict(scene=tag,**event) for tag in ['m-sk-ai-ring','n-sk-zero-close'] for event in real['scenes'][tag]['modes']['original']['budget_events']]
    current['natural_exhaustion_verified']=True
    current['natural_exhaustion_scope']='Legal-rule skirmish fixture, AI fallback, CloseEnough=0; not the original default-rule game.'
    current['default_rules_full_exhaustion_verified']=False
    current['new_real_scene_evidence']=str(stage/'budget-real-scenes.json')
    current['new_static_followup']='Same active Drive returns failed Prepare with a valid destination. Post-Stop AI callbacks can restore a destination; static candidate chain 4C3895 -> 7053F0 -> 4C8030 -> MoveTo at 4C8165. Callback site itself not separately hooked.'
    ordinary=current['ordinary_drive_failure_analysis']
    ordinary['main_search_failure']='4C371A -> Unit Stop slot 4C4B60 clears the current Drive destination, but later AI failure callbacks may assign another destination before the failed Prepare returns.'
    condition='Stop 之后、Prepare 返回之前的失败回调不会重新赋予有效目的地；本轮 AI 实景不满足这个前提。'
    if condition not in ordinary['assumptions']:ordinary['assumptions'].append(condition)
    ordinary['conclusion']='原来的不扣预算推论还需要回调不恢复目的地的前提。同一 Drive 本身不足以排除扣减；本轮规则实景已验证自然扣减与耗尽。'
    current['unresolved']=['原版默认规则下完整预算耗尽仍未验证。','具体 4C3895 回调点未单独挂钩记录；已有静态链与实景状态支持，后续可补精确调用轨迹。','默认遭遇战第 28 帧步兵坐标差异已在修正前程序重现，尚待整理步兵移动。','全游戏等价和完整移动代码可读化尚未完成。']
    matrices=[read(stage/'d-matrix.json'),read(stage/'e-additional-matrix.json')]
    current['second_search_failure_events']=[]
    for row in [r for m in matrices for r in m['results']]:
        for line in (stage/'runs'/row['tag']/'original/state.jsonl').open(encoding='utf-8'):
            event=json.loads(line)
            if event.get('kind')=='movement-audit' and event.get('stage')==18:current['second_search_failure_events'].append(dict(scene=row['tag'],**event))
    current['second_search_failure_naturally_observed']=True
    condition='路径失败后，AI 回退回调可在同一 Drive 中恢复有效目标；还须避开近距离停止，才会连续扣预算。'
    if condition not in current['necessary_conditions']:current['necessary_conditions'].append(condition)
    write(p,current)
    effects=read(stage/'effects.json');effects['budget']['expanded_legal_rule_natural_exhaustion_verified']=True;effects['budget']['default_rules_full_exhaustion_verified']=False;effects['budget']['expanded_evidence']=str(stage/'budget-real-scenes.json');write(stage/'effects.json',effects)
    strict=read(stage/'strict-acceptance.json');strict['natural_budget_scope']='Original 27 scenes only; later legal-rule natural exhaustion is verified separately in budget-real-scenes.json.';write(stage/'strict-acceptance.json',strict)
if __name__=='__main__':reconcile(Path(__file__).resolve().parent/'evidence/movement-state-v11')
