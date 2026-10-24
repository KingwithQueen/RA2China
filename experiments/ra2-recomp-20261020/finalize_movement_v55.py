"""Promote the finite functional search/transport batch and preserve exact inputs."""
from run_batch_v55 import *
for n in ['native-gates.json','effects.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-functional-impact.json','rng-first-split-window.json','boundary-inheritance.json','service-boundaries.json']:
 assert read(S/n)['passed'],n
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');effects=read(S/'effects.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['neighbors','frontier']];assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results'])
frames=sum(x['frames'] for x in parts)+matrix['production_frames']+matrix['observer_frames']
strict_pairs=sum(x['scene_count'] for x in parts)+sum(x['strict_trace_equal'] for x in matrix['results'])
variations=effects['accepted_baseline_variations'];assert (pairs,frames,strict_pairs,variations)==(15,19065,11,4)
report=P/'docs/单位移动第五十四批-路径搜索与步兵先登载-20261025.txt'
handoff=P/'交接文档-单位移动第五十四批正式验收-20261025.txt'
policy=P/'docs/项目目标与验收边界-20261024.txt'
fm=effects['representative']['fm']['effect_modes'];stops=read(S/'part-frontier-path-search.json')['stop_cases']
text=f'''单位移动第五十四批（正式54 / 验证55），2026-10-25。
父提交：{read(S/'vcs-context.json')['parent_commit']}。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收边界：{policy}

本轮实现与结束条件
以整体功能、效果、规则解读和资源调用一致为目标，不追求逐个BUG复刻。本轮完成ground_path_search.c邻域、区域限制、代价和搜索前沿的内部服务整理。只改一个生产C文件，181个生产C、312项编译输入、37个未实现保护不变；无新增头文件、生产源文件或CMake改动。生产规则、美术、随机算法、生成入口/指令标签/分发表、runtime桥接、schema12记录器及通用比较器均未改。
第一部分neighbors：resolve_neighbor先查询邻格，再校验格；普通八方向按当前索引加偏移，第九项特殊连接按实际落格计算索引。桥层/高度判断完成后才查询区域。candidate_region_allows保留区域服务之后重读同一候选格，沿用原来不根据重复读取的返回值新增退出的处理；连接标记、区域代次、上下层豁免与限制开关按原条件读取。
第二部分frontier：score_candidate_step在通行服务之后计算代价。软障碍模式只归一化passage<7；第九项重读当前与候选两个原局部缓冲后算距离，普通方向调用地形代价后读取实时权重、方向偏置和数值控制。即使passage>=7仍先算代价，再判断阻挡目标出口。未缓存context、层高、权重或代次。
缓存先排除同代较低代价候选，再查询通行和代价，passage<7时在创建节点前第二次读标记，允许服务已经发布该格。建节点之后仍依次提交待选堆、发布缓存，再按当时的区域游标推进路线；未提前快照游标或节点代价。advance_frontier先取堆、按新节点发布层高、增加展开数，空堆也增加计数后退出。每轮仍先判断展开限额，再判断当前是否到达目标；目标同格同层、阻挡目标和空前沿出口保留。

原版片段与分段回退
两部分均串行重建并执行同一组8192原版完整搜索循环用例，正式计8192，不重复累计。四出口顺序为限额{stops[0]}、到达{stops[1]}、阻挡目标{stops[2]}、空前沿{stops[3]}。比较311395次有序服务事件、17661个创建节点及上下文、堆、路径链接、两层缓存；12种数值控制，并含区域服务改变连接标记、通行服务改变权重或提前写缓存的输入。原引擎四类服务使用相同探针桩，属于合成映射片段证据，不宣称全部ABI字段或自然搜索入口穷尽。
每部分默认遭遇战301帧、北向桥层交通501帧、南向桥层交通501帧，共3配对1303帧，全部严格通过。两部分分别封存源码、当前工具、编译收据及程序，可独立回退。桥层行人关系查询、实际等待、障碍车移动腾空、绕行及到目标由现有功能检查复验。

步兵先登载的自然混合场景fm
沿用上一批sc同一原始地图、地形包和原规则，仅改变普通命令：50帧要求E2登载，180帧要求TRUCKA登载，其余过水、返南岸、交通占格和后续移动命令保留。用实际装载旗标及对象类别判断完成，不把命令提交当作成功，不强写载员列表、占用、位置或寻路结果。
两模式E2均在{fm['original']['cycles']['1023368'][0]['board_frame']}帧实际登载，货车均在{fm['original']['cycles']['1023363'][0]['board_frame']}帧登载。与上一批车先登载相比，最后登载的货车先于步兵卸下：两模式货车{fm['original']['cycles']['1023363'][0]['drop_frame']}帧在Rough7[137,107]落地；E2原版{fm['original']['cycles']['1023368'][0]['drop_frame']}/C版{fm['generated-c']['cycles']['1023368'][0]['drop_frame']}帧在Clear0[138,106]落地。1帧步兵时序差异在改代码前基线中已存在并保留。
同时带两类载员经过Water的采样原版{fm['original']['special']['water_with_both_frames']}/C版{fm['generated-c']['special']['water_with_both_frames']}帧，两模式经过Beach均{fm['original']['special']['beach_with_both_frames']}帧。全程船300、货车/交通车200、舰船600、步兵/传送步兵125生命不变；货车到[139,104]、E2到[140,104]，其他交通与舰船/传送步兵按原目标结束并Guard5。完整逐模式结果另见effects.json及functional-acceptance.json。
两类载员均实际登载，总Size7、容量12、SizeLimit6；同时装载状态经过Water2和Beach6，返[138,107]原图Rough7中心，北侧交通车在[139,106]/[137,106]占格。实际卸载先后、落格/地形、全程生命及后续Guard5目标一致。1=Road、7=Rough的原版两组名称表证据按哈希继承，不重新解释旧报告用词，也不改旧图或旧轨迹。
fm改代码前用冻结的父批宿主独立运行3401帧基线；最终程序原版/C每种模式完整轨迹分别等于各自改动前轨迹。mi一车再步兵、sc南侧岸段、aw3八邻格全占位/释放/重发卸载沿用父批完整轨迹为基线，本轮最终程序重新运行。四场通用comparison.json的false、随机首差及瞬时差异原样保留；局部功能检查不放宽通用比较器。随机首差前后各8帧只读核查，未加随机钩子、重置/追平随机流或宣称随机调用因果已证明。

有限回归与继承边界
本轮正式计{pairs}配对{frames}模拟帧，{strict_pairs}严格通过、{variations}按局部功能通过。另运行1配对3401帧改动前基线，覆盖不重复累计。最终生产5配对3455帧，独立事件/只读宿主4配对13004帧。固定seed12345，最多两条配对通道/四个游戏进程，构建串行。
最终程序有限复验列车碰撞、碾压、重复失败，以及弯曲高差原版Z436停滞/Z-193未完成；原版异常及输入保留，当前一致不转为必须复刻BUG。旧未合格岸边、远释放目标、坡型8/飞机、碰撞负控制等按boundary-inheritance.json哈希继承，本轮未全部重跑。29非主C候选/86原始入边按哈希继承，当前312项输入无新直接C调用；没有新非主副本或自然隧道入口结论。

保留、清理与提交
父批407项封存、独立315项基线、两部分回退、父批观察宿主、完整状态轨迹、原版异常及首轮资源链接访问失败记录保留。首次访问失败发生于创建资源链接、未启动游戏，提权重试与游戏验收分开记录。
H盘20项原始输入、原版game.exe/SAVE0029、原规则、旧手写引擎、Git配置及远端引用均校验不变。仅清理{clean['deleted_files']}个逐路径/类型/哈希核对的可重建中间文件和缓存，共{clean['deleted_bytes']}字节，同目录{clean['protected_files']}项非候选哈希不变；没有删除源码、正式程序、资源、基线、回退或轨迹。
本地提交，不推送。复核：{R/'verify_final_movement_v55.py'}。提交收据：{S/'postcommit/git-local-commit.json'}。
后续按功能需要继续ground_region_search分层区域搜索、边限制和代价服务，配合已有ground_region_route发布及ground_path_rebuild路径重建，或更多自然容量/岸段/桥层交通；其他引擎子系统及完整视觉/资源调用仍未覆盖，不宣称全游戏等价。
'''
report.write_text(text,encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式54 / 验证55，2026-10-25。
父提交：{read(S/'vcs-context.json')['parent_commit']}。
政策：{policy}
报告：{report}
程序SHA-256：{digest}
只整理ground_path_search.c：邻域解析/区域限制/实时步进代价/搜索前沿，181C/312输入/37保护不变。原顺序保留：区域回调后重读格；通行与代价后第二次读缓存；建节点→堆→缓存→区域游标；取堆→层高→展开数；限额先于到达判断。
两部分各8192同组原版映射例，正式仅计8192，四出口{stops}，311395有序服务事件/17661节点。每部分3配对1303帧，全部严格。合计{pairs}配对{frames}帧，11严格、4局部功能；另1配对3401帧改动前基线不重复计覆盖。
新增fm为50帧E2先请求登载、180帧货车后请求，原图南岸及原规则不变。实际登载/卸载见报告，车兵总Size7/容量12，均带货过水、合法落地并到后续Guard目标。mi/sc/aw3有限回归，四场逐模式完整轨迹均等于改动前本模式，严格false和随机首差窗口原样保留。不追逐个BUG。
列车/碾压/重复失败/高差原版异常有限回归；旧未合格岸边、远目标、坡图/飞机及29非主C/86入边按哈希继承，不宣称新自然入口。
基线：{S/'baseline'}；回退：{S/'parts'}；基线宿主：{S/'baseline-observer'}；封存：{S/'final-source'}。
清理逐路径哈希核对的可重建缓存；H输入、原版、原规则、旧引擎、历史证据保留。
下一步按功能需要整理ground_region_search分层区域搜索/边限制/代价服务，配合区域路线发布及路径重建；更多自然容量/岸段/桥层交通，其他子系统及完整视觉/资源调用仍未覆盖。
复核：{R/'verify_final_movement_v55.py'}。本地提交不推送。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第五十四批正式54 / 验证55已验收。\n交接：{handoff}\n政策：{policy}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-25）：原版1.006 C17/x86单位移动第五十四批已验收。路径搜索邻域/区域/代价/前沿，步兵先登载及南岸混合装卸；[第五十四批交接](交接文档-单位移动第五十四批正式验收-20261025.txt)。遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第五十四批（2026-10-25）\n路径搜索邻域/区域限制/代价/前沿，181C/312输入/37保护，{pairs}配对{frames}帧，8192原版片段例。\n步兵先登载、两岸段和全占位释放重试按冻结基线与功能通过；严格false及随机差异保留。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=54,verification_round=55,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer)
 x['current_batch']=dict(formal_generation=54,verification_round=55,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=8192,production_c_sources=181,content_inputs=312,strict_all_frames_equal=False,accepted_baseline_variations=variations,strict_game_pairs=strict_pairs,functional_game_pairs=variations)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,natural_alias_dispatch_required=False,candidates_not_confirmed_failures=True,remaining=['ground_region_search layer initialization, edge restrictions and penalty/cost services','Regional route publication and path rebuild integration as functionally needed','More natural mixed capacities, shore directions and bridge-layer traffic','Other engine subsystems and full visual/resource acceptance']))
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v55*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe','.json'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']];documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=read(S/'vcs-context.json')['parent_commit'],state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=181,content_inputs=312,unsupported_guards=37,native_cases=8192,probes=1,capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,accepted_inherited_variations=variations,strict_game_pairs=strict_pairs,strict_all_frames_equal=False,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=54,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames))
