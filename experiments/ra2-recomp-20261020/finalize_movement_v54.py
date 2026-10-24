"""Promote batch53: path preparation and mixed passengers at two natural shores."""
from run_batch_v54 import *
for name in ['native-gates.json','effects.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-functional-impact.json','rng-first-split-window.json','land-type-table-proof.json','shore-comparison.json']:assert read(S/name)['passed'],name
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');effects=read(S/'effects.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json');rng=read(S/'rng-functional-impact.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['levels','exclusions']];assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results']);frames=sum(x['frames'] for x in parts)+matrix['production_frames']+matrix['observer_frames']
strict_pairs=sum(x['scene_count'] for x in parts)+sum(x['strict_trace_equal'] for x in matrix['results']);variations=effects['accepted_baseline_variations'];assert pairs==14 and frames==15664 and strict_pairs==11 and variations==3
report=P/'docs/单位移动第五十三批-路径准备与混合载员及南侧岸段-20261025.txt';handoff=P/'交接文档-单位移动第五十三批正式验收-20261025.txt';policy=P/'docs/项目目标与验收边界-20261024.txt'
mi=effects['representative']['mi']['effect_modes'];sc=effects['representative']['sc']['effect_modes'];aw=effects['representative']['aw3']['effect_modes'];stops=read(S/'part-exclusions-path_lifecycle-0.json')['stop_cases']
text=f'''单位移动第五十三批（正式53 / 验证54），2026-10-25。
父提交：{read(S/'vcs-context.json')['parent_commit']}。第五十二批412项封存逐项核对；本轮315项独立基线保留。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
政策：{policy}

路径准备实现
目标为整体功能、效果、规则和资源解读一致，不追求逐个BUG复刻。仅整理ground_path_prepare.c，181个生产C、312项编译内容、37个未实现保护不变；无新增生产文件、头文件或CMake改动。
分为resolve_bridge_levels、create_root_state、seed_start_exclusions三个内部阶段。入口仍先计算起点与终点两个引用，再按短路顺序校验格；桥层阶段保留目标类别/目标格/桥标记，再独立查询起点类别/起点格/所在桥层。类别2的桥层查询短路保留；高度修正先查第一次类型、重读起格，再按条件查询高度。
重复格读取仍使用入口校验时同一组start/target局部对象，未把后续忽略的读取失败改成新退出，也未用新空缓冲代替旧值；三个类型查询不合并。各服务保留原调用点的实时v->context读取，没有新增入口context缓存。
根节点阶段独立进行第二次类型查询、写移动区域、清区域游标、复制起点并保存connected_regions快照，再调用create_root。起终同格同层的判断在根节点回调之后；空根的最终结果也在原本的排除/阻挡目标服务之后读取，不提前返回或缓存结果。
排除阶段在根节点服务后才检查障碍模式、切换障碍、重读起点格并发布起点缓存，再进行第三次类型查询。启用朝向排除时仍查询九次朝向，第九次只查询，不排邻格；方向差3..5的判断不额外环绕归一化，邻格读取与发布保持顺序。最后独立读对象类别，短路查询阻挡目标标记，再归一化负扩展上限，决定空根/可继续结果。
原层高补偿、坐标/缓存索引转换、重复服务调用和条件边界保留。未改变生产规则、美术、随机算法、生成入口/标签/分发表、runtime适配、生产记录器schema12或通用比较器。

分部分验证与回退
两部分分别为levels（桥层与根节点）和exclusions（起点及朝向排除），每部分默认301帧、北桥501帧、南桥501帧，共3配对1303帧，全部严格通过，源码/工具/程序各自封存回退。
两部分均重新构建执行同一组8192个原版映射片段用例，原引擎服务由探针桩替代，比较上下文、缓存/代价数组、回调顺序及准备结果。四出口为无效格{stops[0]}、已到达{stops[1]}、空根{stops[2]}、可继续{stops[3]}例；正式覆盖仅计8192例，不把重跑累计成16384，不宣称所有ABI字段或自然完整搜索都已覆盖。
运输构造128、Capture64按哈希继承，不计本轮新增；29非主C候选/86原始入边证据继承，当前312项输入扫描无新直接C调用，无新非主副本或自然隧道入口结论。

一车加步兵的真实混合装卸
mi使用已验原图与正常初始对象，只改变普通登载/移动/卸载命令。TRUCKA于133帧、E2于197帧实际装入LCRF；两类载员同时保持标记，693帧经过真实水面、49帧经过Beach邻域。原规则车Size6、步兵Size1，总7，运输容量12、SizeLimit6；这次是车兵都实际登载，区别于上一批双车装满后额外步兵未登载。
返原岸[138,102]，步兵2004帧先在[139,101]卸下，货车原版2020/C2018帧后在[139,102]卸下；两帧旧时序差异保留。随后货车[139,104]、步兵[140,104]、交通车[141,104]/[138,104]、舰船[130,106]、传送步兵[138,105]均到目标格并Guard5，参与对象生命全程保持。
船300、货车/交通车200、舰船600、步兵/传送步兵125生命不变；用实际旗标、类别和位置判断登载/卸载，不把发令或同一任务编号当作装载完成。

南侧真实岸段及交通占格
sc沿用完全相同的地图记录和原规则，将返岸中心改为[138,107]，没有改IsoMapPack、地形、层高或岸线。原岸中心地形0，相邻八格[7,0,0,0,0,0,0,0]；南侧中心地形7，相邻八格[0,0,0,7,7,6,6,6]。顺序为西北/北/东北/西/东/西南/南/东南，是同图两个不同真实邻域，不冒称新增地形类型、所有岸型或全部朝向覆盖。
两类载员仍133/197帧装载，同时带货过水原版{sc['original']['special']['water_with_both_frames']}/C版{sc['generated-c']['special']['water_with_both_frames']}帧、两模式均89帧Beach。2200帧卸载时交通车已实际在[139,106]和[137,106]占据北侧邻格；步兵2204帧在西侧[137,107]的Rough格落地，货车2218帧在北侧[138,106]的Clear格落地。
两类载员的实际落格、先后顺序、生命及后续目标一致；瞬时位置/高度、过水样本数和子格差异单列。货车[139,104]、步兵[140,104]、交通车[141,104]/[137,106]、舰船[130,106]、传送步兵[138,99]均到目标格并Guard5。没有强行写载员列表、位置、占用、路径或返回结果。

原版地形名称核对与文字补正
本批只读核对原版EXE的0x7D3878和0x7EEBBC两组名称指针表：0=Clear、1=Road、2=Water、6=Beach、7=Rough。地形7应称粗糙地，不是Road；以前报告将0/7泛称“陆地/道路”的文字不作为正确名称依据。
land-type-table-proof.json保留原版哈希、两个表的实际指针和名称。此前基线、历史报告封存、轨迹、编号与规则文件原位保留；本批交接补正名称，生产代码原本按整数地形判断，未改规则或旧验证结果。南侧步兵确在Rough7卸下，不误写成道路卸载。

既有岸边等待释放回归与随机分流
aw3本轮最终程序重新运行第五十二批配方，改动前基线直接引用父批原始轨迹，不重复复制/重跑同一基线。相邻八格1900..2299全占用400帧，载员保持；2329实际移动、2356腾格、2400重发卸载、2404落地、后续目标/生命均保持原结果，不称自动卸载。
三场当前每种模式的完整轨迹逐条等于改代码前本模式轨迹，通用comparison.json的false保留。随机快照首差见rng-functional-impact.json：{ {k:v['rng_first_different_frame'] for k,v in rng['new_variants'].items()} }。每场只读首差前后各8帧固定窗口，包含载员、舰船、传送步兵及交通车，记录位置/任务/朝向/生命首差。
完整功能检查覆盖混合载员、合法落地、占格/释放、先后顺序、生命和目标。未把快照/索引差异当某次随机调用的因果证明，不加随机钩子、不改种子、不重置/追平随机流、不放宽通用比较器；只在出现功能影响时进一步核查，不推及战斗随机分配或全游戏等价。

验收、保留、清理与接续
含两部分共{pairs}配对{frames}模拟帧，{strict_pairs}严格、{variations}按局部功能通过。最终生产{matrix['production_scenes']}配对{matrix['production_frames']}帧，事件/只读宿主{matrix['observer_scenes']}配对{matrix['observer_frames']}帧。固定seed12345，最多两条配对通道/四个游戏进程，构建串行。
受影响列车碰撞、碾压、重复失败和弯曲高差Z436停滞/Z-193未完成已有限回归。旧未合格岸边控制、较远释放目标未动、坡型8/飞机及随机诊断按哈希继承，未全部重跑，不转成必须逐BUG复刻要求；本批两项新岸段均首次配方即通过，无新增未合格游戏场景。
父批412项封存、本轮315项基线、两部分回退、改动前宿主、完整轨迹和原版异常保留；H盘20项输入、原规则、原版EXE/SAVE0029、旧手写引擎、Git配置/远端引用不变。
清理{clean['deleted_files']}个逐路径/类型/哈希核对的可重建缓存文件，共{clean['deleted_bytes']}字节；同目录{clean['protected_files']}项非候选哈希不变，源文件、正式程序、资源、轨迹、基线与回退保留。
本轮完成ground_path_prepare三块服务边界整理。后续候选为ground_path_search的邻域扩展、区域限制和节点/缓存服务，以及更多自然混合容量/岸段/桥层交通。其他引擎子系统及完整图像/资源调用验收仍未覆盖，不因未穷尽所有内部差异而阻止本批交付。
复核：{R/'verify_final_movement_v54.py'}。本地提交不推送，收据：{S/'postcommit/git-local-commit.json'}。
'''
assert not report.exists() and not handoff.exists();report.write_text(text,encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式53 / 验证54，2026-10-25。
父提交：{read(S/'vcs-context.json')['parent_commit']}。
政策：{policy}
报告：{report}
程序SHA-256：{digest}
只整理ground_path_prepare.c：桥层高度、根节点状态、起点/朝向排除三个阶段，181C/312输入/37保护不变，无新增生产文件/头文件/CMake改动。重复格/类型/context查询、根创建后再判同格、connected_regions创建前快照、九次朝向和最后空根判断保持。
同一组8192原版片段例在两部分均复验，四出口{stops}；只计8192不重复累计。两部分各3配对1303帧，合计{pairs}配对{frames}帧，11严格、3局部功能通过。运输128/Capture64继承。
mi一车加E2于133/197帧实际登载，总Size7/容量12，693帧同时过水；步兵2004先卸、货车原版2020/C2018后卸，实际落格/生命/后续Guard目标一致。
sc原图南侧[138,107]中心Rough7、邻格含Beach6，交通车卸载时实际占[139,106]/[137,106]；E2于2204在Rough[137,107]先卸，车2218在Clear[138,106]后卸，均到后续目标。没有改岸线或地形。
地形名称补正：原版两个表核对1=Road、7=Rough，旧文把7称道路的用词不沿用；历史报告/封存/编号/规则/轨迹原位保留，本批land-type-table-proof.json记录来源。
aw3全8格占用后的等待、实际腾格及重发卸载最终回归通过，基线直接引用父批未重复复制/运行。三场各模式完整轨迹等于改动前本模式，严格false和随机首差窗口保留，不追平随机或逐BUG。
列车/碾压/重复失败/高差原版异常有限回归；旧岸边未合格、远目标、坡图/飞机与29非主C/86入边按哈希继承，无新自然入口结论。
基线：{S/'baseline'}；回退：{S/'parts'}；基线宿主：{S/'baseline-observer'}；封存：{S/'final-source'}。
下一步按功能需要整理ground_path_search邻域扩展/区域限制/节点缓存；更多自然混合容量、岸段和桥层交通，其他子系统及视觉/资源调用仍未覆盖。整体功能/效果一致，不追逐个BUG。
复核：{R/'verify_final_movement_v54.py'}。本地提交不推送。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第五十三批正式53 / 验证54已验收。\n交接：{handoff}\n政策：{policy}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-25）：原版1.006 C17/x86单位移动第五十三批已验收。路径准备桥层/根节点/朝向排除，一车加步兵与南侧岸段装卸；[第五十三批交接](交接文档-单位移动第五十三批正式验收-20261025.txt)。继续遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第五十三批（2026-10-25）\n路径准备桥层/根节点/朝向排除，181C/312输入/37保护，{pairs}配对{frames}帧、8192原生片段例。\n一车加步兵、南侧Clear/Rough/Beach岸段及已有全占位释放重试按冻结基线和功能通过；严格false及随机差异保留。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=53,verification_round=54,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer);x['current_batch']=dict(formal_generation=53,verification_round=54,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=8192,production_c_sources=181,content_inputs=312,strict_all_frames_equal=False,accepted_baseline_variations=variations,strict_game_pairs=strict_pairs,functional_game_pairs=variations);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,natural_alias_dispatch_required=False,percentage_reestimated=False,old_corner_followup_only_for_functional_need=True,rng_exact_call_source_proved=False,candidates_not_confirmed_failures=True,remaining=['ground_path_search neighbor expansion, region restrictions and node/cache services','More natural mixed passenger capacities, shore directions and bridge-layer traffic','Other engine subsystems and full visual/resource acceptance']))
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v54*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe','.json'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']];documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=read(S/'vcs-context.json')['parent_commit'],state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=181,content_inputs=312,unsupported_guards=37,native_cases=native['cases'],probes=native['groups'],capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,accepted_inherited_variations=variations,strict_all_frames_equal=False,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=53,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames))
