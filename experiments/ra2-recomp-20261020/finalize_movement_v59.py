"""Promote bounded heap improvement and finite node/publication acceptance."""
from run_batch_v59 import *
if '--freeze-lineage' in sys.argv:
 lineage=read(S/'checker-lineage.json')
 for e in lineage['entries']:
  e['final_derived_sha256']=sha(R/e['derived']);e['unchanged_after_initial_derivation']=e['final_derived_sha256']==e['derived_sha256']
 (S/'checker-lineage.json').write_text(json.dumps(lineage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Current checker lineage frozen before cleanup.');raise SystemExit(0)
for n in ['native-gates.json','effects.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-functional-impact.json','rng-first-split-window.json','boundary-inheritance.json','service-boundaries.json','infrastructure-status.json','baseline-native-identity.json','community-reference-review.json']:
 assert read(S/n)['passed'],n
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');effects=read(S/'effects.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['heap','nodes']];assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results'])
frames=sum(x['frames'] for x in parts)+matrix['production_frames']+matrix['observer_frames']
strict_pairs=sum(x['scene_count'] for x in parts)+sum(x['strict_trace_equal'] for x in matrix['results'])
variations=effects['accepted_baseline_variations'];assert (pairs,frames,strict_pairs,variations)==(15,19065,11,4)
h=read(S/'part-nodes-heap.json');n=read(S/'part-nodes-nodes.json');m=read(S/'part-nodes-model.json')
assert native['groups']==2 and native['cases']==h['cases']+n['cases']
assert h['intentional_capacity_changes']>0 and h['unexpected_differences']==0
assert m['passed'] and m['synthetic_not_natural'] and m['goal_cost']==m['bfs_distance']==1 and m['cases']==65541
old=read(S/'part-baseline-model.json');assert old['passed'] and not old['zero_slot_heap_reached_goal'] and old['cases']==2
refs=read(S/'community-reference-review.json');assert len(refs['sources'])==5 and not refs['third_party_engine_code_imported']
assert sha(S/'community-reference-review.json')==sha(O/'community-reference-review.json')
reference_lines='\n'.join(x['repository']+' @ '+x['revision']+' / '+x['path']+'\n'+x['url']+'\nSHA-256 '+x['sha256'] for x in refs['sources'])
report=P/'docs/单位移动第五十八批-堆容量与节点分配发布-20261025.txt'
handoff=P/'交接文档-单位移动第五十八批正式验收-20261025.txt'
policy=P/'docs/项目目标与验收边界-20261024.txt';addendum=P/'docs/寻路机制改进验收补充-20261025.txt'
parent=read(S/'vcs-context.json')['parent_commit']
samples='\n'.join(f"例{x['case']}，count={x['count']} / capacity={x['capacity']}：原版选分数{x['original_selected_priority']}，本轮选{x['new_selected_priority']}" for x in h['samples'])
report.write_text(f'''单位移动第五十八批（正式58 / 验证59），2026-10-25。
父提交：{parent}。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收边界：{policy}
本轮用户授权补充：{addendum}

本轮结果与边界
完成ground_path_heap的固定容量候选保留，以及ground_path_nodes的节点/链分配、状态初始化和代次清理服务整理。用户明确允许寻路机制与原版有所不同，按整体功能、效果、合法通行与规则验收，不追求逐个BUG复刻。本批增加一项有意的容量选择改进，原版1.006结果、原始严格差异及改动前控制均保留。
生产改动仅ground_path_heap.c、ground_path_heap.h注释和ground_path_nodes.c；181个生产C、312项编译输入、37处未实现保护不变，无新增生产源文件或CMake改动。评分、随机算法、生产规则/美术、生成入口/标签/分发表、runtime桥接、schema12记录器和通用比较器未改。原验收政策字节不变，新授权另附补充文件。

第一部分heap：容量与有限候选改进
capacity包含闲置0号槽，pending是堆外独立暂存的一项候选。有可用槽时，旧pending按原筛升规则入堆，再暂存新candidate；队列未满的选择、计数、地址界限和共享收尾保持。
原版满堆时无法存入旧pending，却总选新candidate，可能丢弃更低分候选。本轮try_push返回是否成功；满堆时在旧pending与新candidate之间保留priority较低者，同分仍选新candidate。不扩堆、不增加候选预算或更改评分；堆内已有元素不受影响。has_free_slot先判断capacity>0和count<capacity-1再加一，零容量或计数回绕不产生非法写入。
这只改善满堆时两项候选的局部选择，不保证所有地图、所有预算下的全局最优路径。既有缓存发布/搜索剪枝没有改写，较低priority也不等于所有情形最终路程更短。

第二部分nodes：分配与延迟发布
initialize_node_state归拢原有根节点/子节点初始化。仍先取节点地址并递增节点计数，再取路径链并递增链计数；先写链的引用/父链，再初始化高度、累计代价、长度等状态，最后发布node->path_link。priority留给既有距离服务生成，保留原始未写字节；x87数值控制、中间计算和32位长度回绕保持。
原节点/链存储布局及运行时桥接未改，容量仍由既有搜索上下文保证。没有新增通用分配器逐项越界检查或声称节点池已全面加固；本轮节点服务的结论是既有分配/发布语义保持。
搜索重置仍依次清链计数、节点计数、两个堆，再递增generation。仅generation回绕为零时进入clear_wrapped_generation，清上下层和三组区域代次标记，再升到1；保留旧代价、旧节点内容及堆历史地址界限。缓存发布仍先写代次再写代价，层选择与索引保持。

原版1.006片段对照
堆offer {h['offer_cases']}、take {h['take_cases']}、共享收尾{h['tail_cases']}次，共{h['cases']}次映射操作。满堆保留较低分的有意返回差异{h['intentional_capacity_changes']}次，未分类差异{h['unexpected_differences']}；原版与本轮选择分数样本如下：
{samples}
只有“堆满、存在旧pending且其有限priority严格更低、原版返回新candidate而本轮返回旧pending”允许分类通过。每例堆数组、计数、容量、地址历史仍逐项比较，take和共享收尾无放宽。原版返回规则、逐例比较、确定性输入和8项差异样本保留在源码/程序/收据中，不把主动差异改写成严格相等。
节点{n['node_cases']}、缓存发布{n['publish_cases']}、代次重置{n['reset_cases']}次，共{n['cases']}次映射操作，逐字节状态一致；覆盖12种数值控制、根/子节点、长度边界、桥层及代次回绕。两组正式原版映射操作合计{native['cases']}；改动前、第一部分后、第二部分后重跑同组输入，不累计成三倍新覆盖。这是有限输入的映射片段证据，不宣称全部ABI、无穷输入或所有自然入口覆盖。

独立的完整搜索见证（合成，非自然地图）
capacity_witness.c用三格有向图调用实际ra2_path_search_neighbors、节点、缓存、堆和代价代码，服务桩仅提供简单图/通行/代价。独立广度优先搜索给出目标距离1；方向顺序先生成一步可达目标，后生成死路。
capacity=1时，堆内无槽、仅能暂存一项：改动前丢目标而耗尽，本轮保留目标并到达，累计代价1、路径长度2（含起点）。capacity=2的控制中两版本均到达、代价1。基线程序与两张控制收据保留，未强制游戏状态或直接伪造到达结果。
另外65536组有限分数独立检查满堆选择不劣于两个输入、同分选新，以及3项零容量/无槽/计数回绕写入保护，共{m['cases']}项合成检查。它们与上述{native['cases']}次原版映射操作分开计数；不构成自然游戏已经触发满堆改进、普遍路线最短或普遍性能提升的证明。

社区源码线索
继续采用父批已核对的5项固定提交/内容哈希，community-reference-review.json逐字节继承，没有本轮新下载或引入第三方引擎代码。
gagarin的YR gamemd.exe 1.001 AStar声明、FootClass::FindPath包装及单位调用方用于结构/符号定位，不能直接套到本项目RA2 1.006地址或规则。EA旧Red Alert的通行检查与路径优化组织供服务拆分参考，其算法不等同本项目；Phobos是原引擎扩展。本轮依据本项目原版映射控制、明确授权的候选改进及功能回归作结论，不把社区声明当已实现独立尤里引擎或同版证明。
{reference_lines}

自然代表场景与有限回归
两部分各默认遭遇战301帧、北桥501帧、南桥501帧，共3配对1303帧，均严格通过。最终重新运行既有mi/sc/aw3/fm四套自然代表配方，基线按父批完整轨迹哈希继承；原地形/规则不改，无新增自然场景。每种模式完整轨迹等于改动前本模式，装卸、同时过水、合法落格、先后顺序、全程生命及后续Guard目标保持。
旧mi货车原版2020/C2018、fm步兵原版2219/C2220等时序差异，通用comparison.json的false及随机首差窗口保留；首差仍mi/sc/aw3为349帧、fm为350帧。只读前后8帧，不钩随机调用、不改种子、不重置/追平随机流，快照差异不作为某次随机调用的因果证明。
最终有限复验列车碰撞、碾压、重复失败和弯曲高差，原版Z436停滞与Z-193未完成等异常保留输入/轨迹/基线，不作为必须复刻的BUG。旧未合格岸边、远目标、坡型8/飞机、名称表和碰撞负控制按boundary-inheritance.json继承，未全量重跑。29非主C候选/86原始入边按哈希继承，当前输入无新增直接C调用，无新自然非主副本或隧道入口结论。
合计{pairs}配对{frames}模拟帧，{strict_pairs}严格、{variations}局部功能通过；最终生产5配对3455帧、独立事件/只读宿主4配对13004帧。固定seed12345，构建串行、最多两条配对通道/四个游戏进程。

保护、回退、清理和提交
父批405项封存、315项独立生产基线、baseline-probe和baseline-observer、heap/nodes两部分回退均保留。H盘20项原始输入、原版game.exe/SAVE0029、原规则、旧手写引擎、Git配置及远端引用哈希不变。
受限命令启动器枚举Q盘失败，使用常规执行完成构建/验收，未改变游戏输入。逐路径/类型/哈希清理{clean['deleted_files']}个可重建中间文件/缓存，共{clean['deleted_bytes']}字节；同目录{clean['protected_files']}项非候选哈希不变。源码、正式程序、资源、基线、回退、完整轨迹和原版异常保留。
只做本地提交，不推送。复核：{R/'verify_final_movement_v59.py'}；提交收据：{S/'postcommit/git-local-commit.json'}。
下一步按功能需要连接路径完成/重建与更多自然交通，并仅在可度量的功能/效果收益下继续改进搜索；其他引擎子系统与完整视觉/资源调用验收未覆盖，不宣称全游戏等价或全局最短。
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式58 / 验证59，2026-10-25。
父提交：{parent}。
政策：{policy}
寻路机制改进授权补充：{addendum}
报告：{report}
程序SHA-256：{digest}
ground_path_heap满堆保留pending/candidate中较低priority，同分选新；正常入堆/取堆不变，固定容量/内存不增加，先比界限再加一防计数回绕。不保证全地图最短路径，也不声称自然场景已触发改进。
ground_path_nodes拆分状态初始化与回绕代次清理；先节点后链分配、各自取址时递增、最后发布path_link、priority留待距离服务、缓存先代次后代价、回绕只清代次均保持。节点/链布局及上下文容量合同不变，未增加逐项分配越界检查。
181C/312输入/37保护，改动2个C及1个头注释。原版映射两组{native['cases']}次操作；满堆选择有意差异{h['intentional_capacity_changes']}次、未分类0，节点{n['cases']}次严格一致。三轮重复不累计。
独立三格完整搜索：capacity1基线丢目标/耗尽，新版到达成本1，独立BFS确认1；capacity2两者均到达。另65536有限分数检查及3边界检查，合成总{m['cases']}，与原版映射计数分开，非自然地图证据。
两部分各3配对1303帧严格；总15配对19065帧，11严格、4局部功能。mi/sc/aw3/fm完整轨迹等于改动前本模式；旧时序、严格false、随机窗口及Z436/Z-193等原版异常保留。原版1.006为比较依据，但验收不要求寻路机制或逐个BUG相同。
社区5项固定提交/哈希继续继承：{S/'community-reference-review.json'}。gagarin YR1.001用于结构符号、EA旧Red Alert用于组织、Phobos为扩展；未引入外部引擎代码，不直接套地址/规则。
旧未合格岸边/远目标/坡图飞机及29非主C/86入边按哈希继承，无新自然入口结论。
基线：{S/'baseline'}；回退：{S/'parts'}；基线探针：{S/'baseline-probe'}；基线宿主：{S/'baseline-observer'}；封存：{S/'final-source'}。
已逐路径哈希清理{clean['deleted_files']}项可重建缓存；H输入、原版、规则、旧引擎及历史证据保留。本地提交，不推送。
下一步按功能需要连接路径完成/重建和更多自然交通，或以实际效果支持的搜索改进；其他子系统/完整视觉资源验收未覆盖，不宣称全游戏等价或普遍最短。
派生下一批工具须显式使用父证据movement-state-v59并保留导入校验；复核：{R/'verify_final_movement_v59.py'}。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第五十八批正式58 / 验证59已验收。\n交接：{handoff}\n政策：{policy}\n寻路机制改进补充：{addendum}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-25）：原版1.006 C17/x86单位移动第五十八批已验收。固定容量候选改进、节点分配与发布；[第五十八批交接](交接文档-单位移动第五十八批正式验收-20261025.txt)。遵守[整体功能与效果一致边界](docs/项目目标与验收边界-20261024.txt)及[寻路机制改进补充](docs/寻路机制改进验收补充-20261025.txt)。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第五十八批（2026-10-25）\n满堆保留较低分候选，固定预算；节点/链分配发布和代次重置整理。181C/312输入/37保护，{pairs}配对{frames}帧；原版映射{native["cases"]}次操作，合成{m["cases"]}项分开记录。\n按用户授权允许寻路机制改进，不保证全地图最短；旧严格差异/原版异常及全部基线回退保留。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=58,verification_round=59,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy),pathfinding_policy_addendum=str(addendum),path_mechanism_identity_required=False,globally_shortest_paths_verified=False)
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer)
 x['current_batch']=dict(formal_generation=58,verification_round=59,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=native['cases'],native_groups=2,synthetic_cases=m['cases'],intentional_capacity_changes=h['intentional_capacity_changes'],production_c_sources=181,content_inputs=312,strict_all_frames_equal=False,accepted_baseline_variations=variations,strict_game_pairs=strict_pairs,functional_game_pairs=variations)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,path_mechanism_identity_required=False,globally_shortest_paths_verified=False,natural_alias_dispatch_required=False,candidates_not_confirmed_failures=True,community_references_available=True,remaining=['Path completion/rebuild integration and additional natural traffic as functionally needed','Further pathfinding changes only with bounded functional/effect evidence; no global optimality claim','Other engine subsystems and full visual/resource acceptance']))
for e in read(S/'checker-lineage.json')['entries']:assert e['final_derived_sha256']==sha(R/e['derived'])
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v59*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe','.json'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy,addendum]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']];documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=parent,state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=181,content_inputs=312,unsupported_guards=37,native_cases=native['cases'],probes=2,synthetic_cases=m['cases'],intentional_capacity_changes=h['intentional_capacity_changes'],unexpected_native_differences=0,capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,accepted_inherited_variations=variations,strict_game_pairs=strict_pairs,strict_all_frames_equal=False,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=58,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames,native_cases=native['cases'],synthetic_cases=m['cases']))
