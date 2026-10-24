"""Promote finite smoothing/postprocess acceptance and preserve exact replay inputs."""
from run_batch_v57 import *
if '--freeze-lineage' in sys.argv:
 lineage=read(S/'checker-lineage.json')
 for e in lineage['entries']:
  e['final_derived_sha256']=sha(R/e['derived']);e['unchanged_after_initial_derivation']=e['final_derived_sha256']==e['derived_sha256']
 (S/'checker-lineage.json').write_text(json.dumps(lineage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Current checker lineage frozen before cleanup.');raise SystemExit(0)
for n in ['native-gates.json','effects.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-functional-impact.json','rng-first-split-window.json','boundary-inheritance.json','service-boundaries.json','infrastructure-status.json','baseline-native-identity.json']:
 assert read(S/n)['passed'],n
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');effects=read(S/'effects.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['smooth','postprocess']];assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results'])
frames=sum(x['frames'] for x in parts)+matrix['production_frames']+matrix['observer_frames']
strict_pairs=sum(x['scene_count'] for x in parts)+sum(x['strict_trace_equal'] for x in matrix['results'])
variations=effects['accepted_baseline_variations'];assert (pairs,frames,strict_pairs,variations)==(15,19065,11,4)
assert native['cases']==16384 and native['groups']==2
p0=read(S/'part-postprocess-path-optimize-0.json');p1=read(S/'part-postprocess-path-optimize-1.json')
report=P/'docs/单位移动第五十六批-路径平滑与后处理服务-20261025.txt'
handoff=P/'交接文档-单位移动第五十六批正式验收-20261025.txt'
policy=P/'docs/项目目标与验收边界-20261024.txt'
report.write_text(f'''单位移动第五十六批（正式56 / 验证57），2026-10-25。
父提交：{read(S/'vcs-context.json')['parent_commit']}。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收边界：{policy}

本轮实现范围
按整体功能、效果、规则解读与资源调用一致验收，不追求逐个BUG复刻。本轮完成ground_path_optimize.c路径平滑与后处理的内部服务整理，仅改一个生产C文件。181个生产C、312项编译输入、37处未实现保护不变；没有新增生产源文件、头文件或CMake改动。生产规则、美术、随机算法、生成入口/指令标签/分发表、runtime桥接、schema12记录器和通用比较器未改。

第一部分smooth：扫描状态与成对转弯服务
以内部Ra2SmoothScan归拢原有首段/次段位置与计数、前方向、配对状态及锚点/当前点，不增加公共字段。入口仍先保存length-1，再分别读取起点用于anchor和point，并保存directions/levels入口指针；服务修改path字段时，不静默改用新数组或新循环上限。
advance_smooth_scan保留原方向识别顺序：先读当前方向、按uint32差值&7判断转弯，再按同向、可配对的两种转向或新首段分流。普通方向推进仍按原direction索引offsets，不额外归一化；方向8才调用connection_exit，使用同一个当前点对象。成对阶段次方向相同只增加second_count并继续，不推进当前点；第二段结束才调用finish_smooth_pair。
finish_smooth_pair先调用shorten_turn，保留原方向/层高两个数组偏移及同一锚点；回调返回后才按其返回的推进量更新first_start，重读被回调修改后的方向，再复位首段计数/配对标记并读取当时的offsets推进当前点。没有在回调前缓存新方向、锚点、偏移表或context。末尾仍只发一次shorten_turn并忽略返回值，不复用会重读方向和推进点的完成阶段，避免新增末尾缓冲读取。

第二部分postprocess：局部改写服务与方向压紧
扫描与几何判断原位保留：以上限last入口快照和index<20扫描前段。方向8仍按offsets[0]推进并重置统计，不改为平滑阶段的特殊连接查询；方向-2只跳索引。发现折返时保留checkpoint、candidate_delta和最大距离的更新顺序，重置参照后仍重试同一个index，不提前推进。
rewrite_postprocess_segment合并两处服务边界。find_anchor先运行，之后才根据其回写的anchor_index/anchor计算delta、覆盖长度和读取levels[anchor_index]，再用实时context调用rewrite_segment。普通段的锚点扫描终点为index、覆盖长度为index-anchor_index+1、final=0；终段仍以index-1为扫描终点、index-anchor_index为覆盖长度、final=1，未把末段错误加一。回调对局部anchor/delta的修改不回写主扫描点，和原先两个局部对象的作用范围一致。
compact_postprocess_directions仍使用入口last压紧方向：跳过-2，遇-1停止；不移动层高槽。补槽阶段保持读取实时path->length，写至原有额外终止槽后，最后才发布written+1的新长度。没有借整理修复高度槽、特殊连接或终止槽的既有规则。

原版片段、分段回退与证据边界
平滑0x428AE0与后处理0x4290C0两个原版映射函数各8192个输入，正式共16384例。改代码前及两部分后均执行同一组输入，不把三次重复计为49152个新用例。原始探针源自v38并按字节保留，原引擎服务用相同桩替代，比较完整path结构、方向/层高缓冲和有序回调参数。
输入包括1..96长度、16位坐标边界、普通方向与特殊连接、成对转弯、回调回写数组/锚点、删除标记-2、提前-1、前20步上限以及终段改写。平滑探针计缩短回调{p0['shorten_callbacks']}、连接回调{p0['connection_callbacks']}；后处理计改写回调{p1['rewrite_callbacks']}、其中终段{p1['final_rewrites']}、保留分支{p1['retained_segments']}。这些累计计数包含该探针中的原版和C两个模式，属于桩服务执行量，不是自然游戏调用数，也不宣称所有ABI字段或全部碰撞感知改写都已覆盖。
改动前探针源码/程序/header另存baseline-probe并由baseline-native-identity.json核对；生产独立基线315项、两部分完整源码/工具/编译收据/程序/探针均保留。每部分默认遭遇战301帧、北桥501帧、南桥501帧，共3配对1303帧，全部严格通过。

自然代表场景与有限回归
mi/sc/aw3/fm四套已验地图、原地形包与规则沿用父批，不新增自然场景、不重复运行改动前游戏基线。最终程序分别重新运行车先登载、南侧Rough/Clear/Beach岸段、八邻格全占位后释放与重发卸载、步兵先登载四场。每种模式的完整轨迹分别等于改代码前该模式；实际登载、同时过水、落格与地形、卸载先后、全程生命、后续Guard目标保持。
mi货车原版2020/C2018卸载、fm步兵原版2219/C2220卸载等旧时序差异原样保留；通用comparison.json的false没有修改，功能检查没有放宽通用比较器。随机快照首差仍mi/sc/aw3为349帧、fm为350帧，只读各首差前后8帧窗口；不加随机钩子、不改种子、不重置/追平随机流，不把快照差异当作随机调用因果证明。
最终程序有限复验桥层列车碰撞、碾压、重复失败、弯曲高差。原版Z436停滞和Z-193未完成等异常的输入、轨迹和基线保留，不转成必须逐BUG复刻的需求。旧未合格岸边、远释放目标、坡型8/飞机、地形名称表及碰撞负控制按boundary-inheritance.json哈希继承，本轮未全部重跑。29非主C候选/86原始入边按哈希继承，当前312项输入无新增直接C调用，无新自然非主副本或隧道入口结论。

验收、保护与清理
本轮合计{pairs}配对{frames}模拟帧：{strict_pairs}严格、{variations}按局部功能通过。最终生产5配对3455帧，独立事件/只读宿主4配对13004帧。固定seed12345，构建串行，最多两条配对通道/四个游戏进程；没有为了无关内部差异扩大矩阵。
父批396项封存、315项独立基线、改动前探针与宿主、两部分回退、原版异常及完整状态轨迹保留。H盘20项原始输入、原版game.exe/SAVE0029、原规则、旧手写引擎、Git配置及远端引用校验不变。批次工具在导入时即按vcs-context.json校验父证据目录，本轮没有父批指针误配或游戏准备失败。
按逐路径/类型/哈希清理{clean['deleted_files']}个可重建中间文件或缓存，共{clean['deleted_bytes']}字节；同目录{clean['protected_files']}项非候选哈希不变。源码、正式程序、资源、基线、回退与轨迹均保留。本地提交、不推送。
复核：{R/'verify_final_movement_v57.py'}；提交收据：{S/'postcommit/git-local-commit.json'}。
接续按功能需要推进ground_path_local的转弯缩短、锚点查找和局部段改写服务，保留通行/威胁/桥层高度的调用边界。其他引擎子系统及完整视觉/资源调用验收仍未覆盖，不宣称全游戏等价。
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式56 / 验证57，2026-10-25。
父提交：{read(S/'vcs-context.json')['parent_commit']}。
政策：{policy}
报告：{report}
程序SHA-256：{digest}
仅整理ground_path_optimize.c：内部平滑扫描状态、advance_smooth_scan/finish_smooth_pair，后处理rewrite_postprocess_segment/compact_postprocess_directions。181C/312输入/37保护不变。入口长度/数组快照、回调后的方向/层高/锚点重读、末尾配对忽略返回、特殊连接两种处理、前20步/同索引重试、终段长度和方向独立压紧/额外终止槽保持。
平滑与后处理各8192原版映射例，正式计16384；改动前和两部分后重复执行不累计。改动前探针程序另存baseline-probe，两部分各3配对1303帧全部严格。总15配对19065帧，11严格、4局部功能。引擎服务仍为桩，不称全部ABI或自然改写覆盖。
mi/sc/aw3/fm本轮复验，基线按父批哈希继承，无新自然场景；每种模式完整轨迹均等于改动前本模式。旧1/2帧差异、严格false和随机首差窗口保留，不追逐个BUG。
列车/碾压/重复失败/高差原版异常有限回归；旧未合格岸边、远目标、坡图/飞机、名称表与29非主C/86入边按哈希继承，无新自然入口结论。
基线：{S/'baseline'}；回退：{S/'parts'}；基线探针：{S/'baseline-probe'}；基线宿主：{S/'baseline-observer'}；封存：{S/'final-source'}。
已清理逐路径哈希核对的可重建缓存；原版、H输入、原规则、旧引擎和历史证据保留。
下一步按功能需要推进ground_path_local转弯缩短/锚点/局部段改写服务，注意通行、威胁及桥层高度的服务顺序；其他子系统与完整视觉/资源调用仍未覆盖。
派生下一批工具时显式更新父证据目录为movement-state-v57，并保留导入时的父目录身份校验。
复核：{R/'verify_final_movement_v57.py'}。本地提交不推送。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第五十六批正式56 / 验证57已验收。\n交接：{handoff}\n政策：{policy}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-25）：原版1.006 C17/x86单位移动第五十六批已验收。路径平滑与后处理服务；[第五十六批交接](交接文档-单位移动第五十六批正式验收-20261025.txt)。遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第五十六批（2026-10-25）\n路径平滑/后处理服务，181C/312输入/37保护，{pairs}配对{frames}帧，平滑和后处理各8192原版片段、共16384例。\n四个既有自然装卸/岸段场景按冻结基线和功能通过；严格false、旧时序及原版异常保留。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=56,verification_round=57,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer)
 x['current_batch']=dict(formal_generation=56,verification_round=57,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=16384,production_c_sources=181,content_inputs=312,strict_all_frames_equal=False,accepted_baseline_variations=variations,strict_game_pairs=strict_pairs,functional_game_pairs=variations)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,natural_alias_dispatch_required=False,candidates_not_confirmed_failures=True,remaining=['ground_path_local turn shortening, anchor lookup and local segment rewriting services','Passage/threat/bridge-level service ordering and natural representative cases as functionally needed','Other engine subsystems and full visual/resource acceptance']))
for e in read(S/'checker-lineage.json')['entries']:assert e['final_derived_sha256']==sha(R/e['derived'])
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v57*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe','.json'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']];documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=read(S/'vcs-context.json')['parent_commit'],state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=181,content_inputs=312,unsupported_guards=37,native_cases=16384,probes=2,capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,accepted_inherited_variations=variations,strict_game_pairs=strict_pairs,strict_all_frames_equal=False,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=56,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames))
