"""Promote finite layered regional-search acceptance and preserve exact inputs."""
from run_batch_v56 import *
if '--freeze-lineage' in sys.argv:
 lineage=read(S/'checker-lineage.json')
 for e in lineage['entries']:
  e['final_derived_sha256']=sha(R/e['derived']);e['unchanged_after_initial_derivation']=e['final_derived_sha256']==e['derived_sha256']
 (S/'checker-lineage.json').write_text(json.dumps(lineage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Current checker lineage frozen before cleanup.');raise SystemExit(0)
for n in ['native-gates.json','effects.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-functional-impact.json','rng-first-split-window.json','boundary-inheritance.json','service-boundaries.json','infrastructure-status.json','tooling-correction.json']:
 assert read(S/n)['passed'],n
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');effects=read(S/'effects.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['layers','edges']];assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results'])
frames=sum(x['frames'] for x in parts)+matrix['production_frames']+matrix['observer_frames']
strict_pairs=sum(x['scene_count'] for x in parts)+sum(x['strict_trace_equal'] for x in matrix['results'])
variations=effects['accepted_baseline_variations'];assert (pairs,frames,strict_pairs,variations)==(15,19065,11,4)
proof=read(S/'part-edges-region-search.json');assert proof['successes']==3972 and proof['failures']==2172 and proof['final_numeric_control_compared']
report=P/'docs/单位移动第五十五批-分层区域搜索与边代价-20261025.txt'
handoff=P/'交接文档-单位移动第五十五批正式验收-20261025.txt'
policy=P/'docs/项目目标与验收边界-20261024.txt'
text=f'''单位移动第五十五批（正式55 / 验证56），2026-10-25。
父提交：{read(S/'vcs-context.json')['parent_commit']}。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收边界：{policy}

本轮范围与实现
目标为可读、可维护的C17实现，在整体功能、效果、规则解读及资源调用上与原版一致，不追求逐个BUG复刻。本轮完成ground_region_search.c分层区域搜索、边限制和代价服务的内部整理。仅改一个生产C文件，181个生产C、312项编译输入、37处未实现保护不变；没有新增生产源文件、头文件或CMake改动。原版规则、美术、随机算法、生成入口/指令标签/分发表、runtime适配、schema12记录器及通用比较器未改。

第一部分layers
prepare_layer接收每层开始时的heap快照，先清索引0至count的条目与count；历史最高/最低节点地址保留。依次查询start、goal的区域，两个服务分别读取当时v->context；只有两次查询完成后才取得本层cache，再分别发布起终区域的当前连通代次。没有把heap快照延后，也没有把cache快照提前。
publish_same_region保留同区域快捷出口：仅在最细层写根节点region和depth，发布单项route和route_count；不清除节点其余字段，不创建搜索根，不取堆或查询禁行列表，继续下一层。seed_layer_frontier仍先写完整根节点并入区域堆，再发布visited和零代价；随后才设置next_node、取首节点和记录首次禁行列表是否为空。三层仍2→1→0，某层失败立即返回，已完成的粗层路线留存。

第二部分edges
proposed_edge_cost在邻接区域视图取得之后运行。owner_factor与owner_house仍在入口有owner时按原顺序各查询一次，之后才计算factor>0.00001的开关；无owner和临界/零因子路径不新增罚分服务。启用时先调用edge_penalty，再用当时numeric_control计算罚分乘因子，之后才切换到integer_conversion_control并转换整数罚分；不恢复旧控制，后续区域代价继续使用更新后的控制。
代价仍按地形代价+父代价、整数罚分、可选0.001附加值顺序计算并存float。父节点cost在罚分服务之后读取；被缓存、区域或地形限制拒绝的边也先完成代价计算，不用提前过滤省略其数值副作用。
edge_is_eligible依次检查同代visited且旧cost<=proposed、上一层连通限制及terrain==1豁免、terrain_allowed必须严格等于1，最后才检查禁行边。若该层首次禁行列表为空，后续免查；否则只在前面条件均通过时重读列表。禁行无向边仍把两个编号截成uint16、按小编号在高16位规范化，再逆序扫描；未合并查询或把开始列表替代后续实时列表。
合格边仍按原顺序写节点、offer、发布visited/cost、增加next_node。区域堆满时依旧消耗节点池槽位并发布缓存；平分代价保持原堆顺序，区域堆不改用格子搜索的pending规则。三层路线发布函数与路径重建未改。

原版片段、数值控制与分段回退
改代码前及两部分之后均重新构建执行同一组6144原版完整区域搜索片段，正式只计6144输入，不把三次执行累计为新覆盖。12种数值模式、3层、同区域快捷出口、禁行边、地形限制、堆容量及平分输入，3972成功/2172失败。上下文、connected/visited/cost、节点池、堆、路线和有记录的原引擎回调事件均相同。
本轮在继承的探针中增加最终数值控制比较：立即读取原版最终x87控制字，与C例程更新后的逻辑numeric_control比较。改动前和两部分均通过。比较针对逻辑控制状态；不把C宿主物理FPU控制、全部ABI字段或所有可能回调突变宣称为已验证。原版映射代码的引擎服务使用相同桩，属于合成片段证据，不等于自然完整地图覆盖。探针原始来源、改动和当前哈希见checker-lineage.json。
每部分默认遭遇战301帧、北桥501帧、南桥501帧，共3配对1303帧，全部严格通过。各自保留当时源码、编译收据、工具、正式程序与探针程序，可独立回退。桥层行人关系查询、实际等待、障碍车开始移动、绕行及到达目标由功能检查复验。

代表场景与有限回归
本轮复用父批已验的mi/sc/aw3/fm四套配方，原图、地形包和规则按哈希保留；没有新增自然场景，不把继承配方计为新地形或新容量覆盖。四场改动前完整轨迹直接引用父批，冻结父批宿主，未重复运行或复制整套旧轨迹。
最终当前程序重新运行一车再步兵、南侧Rough/Clear/Beach岸段、八邻格全占位后释放并重发卸载、步兵先登载再货车四场。每种模式的完整轨迹分别等于改代码前该模式；实际登载、同时过水、卸载先后、合法落格、全程生命与后续Guard目标保持。fm仍E2在110帧登载、车263帧登载，车2204帧先卸，步兵原版2219/C2220帧后卸；这1帧旧时序差异保留。sc、mi旧瞬时差异及aw3实际腾格/重发卸载行为也原样保留。
四场通用comparison.json的false不改，局部功能检查没有放宽通用比较器。随机快照首差仍mi/sc/aw3为349帧、fm为350帧；本轮只读各首差前后8帧窗口并核对生命/目标，没有添加随机钩子、重置或追平随机流，不把快照差异视为某次随机调用因果证明，也不推及战斗随机行为。
最终程序有限复验列车碰撞、碾压、重复搜索失败及弯曲高差。原版Z436停滞、Z-193未完成等异常保留输入、原始轨迹和基线；当前一致不构成必须逐BUG复刻的要求。旧未合格岸边、远释放目标、坡型8/飞机、地形名称表和碰撞负控制按boundary-inheritance.json追溯原始证据哈希继承，本轮未全部重跑。29非主C候选/86原始入边按哈希继承，当前312项输入无新增直接C调用；无新非主副本或自然隧道入口结论。

验收、保护、清理和接续
本轮合计{pairs}配对{frames}模拟帧，{strict_pairs}严格、{variations}按局部功能通过；最终生产5配对3455帧，独立事件/只读宿主4配对13004帧。固定seed12345，构建串行，最多两条配对通道/四个游戏进程。没有为内部无关差异扩大矩阵，没有新增未合格自然场景。
父批401项封存、315项独立基线、两部分回退、父批宿主、既有完整轨迹及原版异常保留。H盘20项原始输入、原版game.exe/SAVE0029、原规则、旧手写引擎、Git配置与远端引用校验不变。之前的资源链接访问失败记录原位保留，本轮没有同类游戏准备失败。证据检查曾因派生脚本沿用v54父目录而拒绝通过，修正为实际父批v55后重新核对；生产输入、阶段封存及游戏轨迹未变，详见tooling-correction.json。
按逐路径/类型/哈希清理{clean['deleted_files']}个可重建缓存或中间文件，共{clean['deleted_bytes']}字节；同目录{clean['protected_files']}项非候选哈希不变。源码、正式程序、原始资源、状态轨迹、基线与回退保留。
本地提交，不推送。复核：{R/'verify_final_movement_v56.py'}；提交收据：{S/'postcommit/git-local-commit.json'}。
接续按功能需要推进ground_path_optimize的平滑/后处理服务，结合ground_path_rebuild及已有区域路线发布；更多自然交通、容量和岸段是后续候选。其他引擎子系统及完整视觉/资源调用验收仍未覆盖，不宣称全游戏等价。
'''
report.write_text(text,encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式55 / 验证56，2026-10-25。
父提交：{read(S/'vcs-context.json')['parent_commit']}。
政策：{policy}
报告：{report}
程序SHA-256：{digest}
仅整理ground_region_search.c的三层初始化/同区域出口/根准备、边罚分与代价、区域/地形/禁行限制。181C/312输入/37保护不变。heap在查询前快照，cache在两次区域查询后取得；罚分先乘后切整数控制；代价先于限制；禁行列表按原短路重读；堆满仍发布访问代价并耗节点槽；失败保留已完成粗层路线。
改动前及两部分后均重跑同一6144原版映射例，仅计6144：3972成功/2172失败，12数值模式。新增最终原版x87控制字对C逻辑控制的比较，三次均通过；引擎服务仍为探针桩，不称全部ABI/自然入口覆盖。
两部分各3配对1303帧，全部严格；总15配对19065帧，11严格、4局部功能。mi/sc/aw3/fm本轮重跑，基线按父批哈希继承，无新自然场景；四场每种模式完整轨迹均等于改动前本模式，旧1/2帧差异、严格false及随机窗口保留。不追逐个BUG。
列车/碾压/重复失败/高差原版异常有限回归；旧未合格岸边、远目标、坡图/飞机、名称表与29非主C/86入边按哈希继承，无新自然入口结论。
基线：{S/'baseline'}；回退：{S/'parts'}；基线宿主：{S/'baseline-observer'}；封存：{S/'final-source'}。
已清理逐路径哈希核对的可重建缓存；原版、H输入、规则、旧引擎、历史证据保留。
下一步按功能需要推进ground_path_optimize平滑/后处理服务，结合路径重建及区域路线发布；其他子系统与完整视觉/资源调用仍未覆盖。
派生下一批工具时显式更新父证据目录为movement-state-v56，勿只替换脚本后缀。
复核：{R/'verify_final_movement_v56.py'}。本地提交不推送。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第五十五批正式55 / 验证56已验收。\n交接：{handoff}\n政策：{policy}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-25）：原版1.006 C17/x86单位移动第五十五批已验收。分层区域搜索、边限制与代价服务；[第五十五批交接](交接文档-单位移动第五十五批正式验收-20261025.txt)。遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第五十五批（2026-10-25）\n分层区域搜索/边限制/代价服务，181C/312输入/37保护，{pairs}配对{frames}帧，6144原版片段例；最终逻辑数值控制亦对照。\n四个既有自然装卸/岸段场景按冻结基线和功能通过；严格false、旧时序差异及原版异常保留。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=55,verification_round=56,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer)
 x['current_batch']=dict(formal_generation=55,verification_round=56,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=6144,production_c_sources=181,content_inputs=312,strict_all_frames_equal=False,accepted_baseline_variations=variations,strict_game_pairs=strict_pairs,functional_game_pairs=variations)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,natural_alias_dispatch_required=False,candidates_not_confirmed_failures=True,remaining=['ground_path_optimize smoothing/postprocess service boundaries as functionally needed','Path rebuild and region-route publication integration as functionally needed','More natural traffic, capacities and shoreline cases','Other engine subsystems and full visual/resource acceptance']))
lineage=read(S/'checker-lineage.json')
for e in lineage['entries']:
 assert e['final_derived_sha256']==sha(R/e['derived'])
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v56*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe','.json'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']];documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=read(S/'vcs-context.json')['parent_commit'],state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=181,content_inputs=312,unsupported_guards=37,native_cases=6144,probes=1,capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,accepted_inherited_variations=variations,strict_game_pairs=strict_pairs,strict_all_frames_equal=False,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=55,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames))
