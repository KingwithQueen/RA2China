"""Promote finite local-path acceptance, community reference receipts and replay inputs."""
from run_batch_v58 import *
if '--freeze-lineage' in sys.argv:
 lineage=read(S/'checker-lineage.json')
 for e in lineage['entries']:
  e['final_derived_sha256']=sha(R/e['derived']);e['unchanged_after_initial_derivation']=e['final_derived_sha256']==e['derived_sha256']
 (S/'checker-lineage.json').write_text(json.dumps(lineage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Current checker lineage frozen before cleanup.');raise SystemExit(0)
for n in ['native-gates.json','effects.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-functional-impact.json','rng-first-split-window.json','boundary-inheritance.json','service-boundaries.json','infrastructure-status.json','baseline-native-identity.json','community-reference-review.json','environment-note.json']:
 assert read(S/n)['passed'],n
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');effects=read(S/'effects.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['turns','segments']];assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results'])
frames=sum(x['frames'] for x in parts)+matrix['production_frames']+matrix['observer_frames']
strict_pairs=sum(x['scene_count'] for x in parts)+sum(x['strict_trace_equal'] for x in matrix['results'])
variations=effects['accepted_baseline_variations'];assert (pairs,frames,strict_pairs,variations)==(15,19065,11,4)
assert native['cases']==32768 and native['groups']==3
p1=read(S/'part-segments-path-local-1.json');p2=read(S/'part-segments-path-local-2.json')
refs=read(S/'community-reference-review.json');assert len(refs['sources'])==5 and not refs['third_party_engine_code_imported']
reference_lines='\n'.join(x['repository']+' @ '+x['revision']+' / '+x['path']+'\n'+x['url']+'\nSHA-256 '+x['sha256'] for x in refs['sources'])
report=P/'docs/单位移动第五十七批-局部路径与锚点及段改写-20261025.txt'
handoff=P/'交接文档-单位移动第五十七批正式验收-20261025.txt'
policy=P/'docs/项目目标与验收边界-20261024.txt'
report.write_text(f'''单位移动第五十七批（正式57 / 验证58），2026-10-25。
父提交：{read(S/'vcs-context.json')['parent_commit']}。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收边界：{policy}

本轮范围
按整体功能、效果、规则解读和资源调用一致验收，不追求逐个BUG复刻。本轮完成ground_path_local.c锚点查找、转弯缩短和局部段改写服务整理，仅改一个生产C文件。181个生产C、312项编译输入、37处未实现保护不变，没有新增生产源文件、头文件或CMake改动。生产规则、美术、随机算法、生成入口/标签/分发表、runtime桥接、schema12记录器和通用比较器未改。

第一部分turns：锚点与转弯候选
锚点反扫改用reverse_delta、candidate_anchor、maximum_extent、passed_peak、reverse_direction等描述状态的局部名称，算法与发布顺序保持。跳过-2槽；方向8在这里仍按低三位普通回退，不查特殊连接。同步回退位移和候选点，越过峰值并再扩大时选择上一格；先写anchor_index，再按原时点读取偏移写anchor。空反扫区间仍写start和原候选点，不新增错误出口。
can_shorten_run分离候选走廊检查。起点origin仍是外层同一局部对象，首格从origin沿middle方向推进；先查passage，未受阻才查0x40000属性，仍未受阻才查询origin的威胁，按原scaled_at_least表达式与1.0比较。不能把此处威胁点替换成正在推进的point，也不能与段改写的查询顺序合并。
每次检查后先减remaining，再推进下一格、cell_at、读取属性和更新层高；即使本次受阻或刚好到段尾也保留下一格探测。层高仍以previous-ground_level==4和桥标志0x100决定是否保持上层。owner_factor和owner_house仍在候选循环前按原顺序各查询一次，numeric_control按原表达式读取。
候选完整通过后才写中间方向，再按实际方向数组walk推进锚点并返回前缀长度；失败候选不发布方向。原有first/second含特殊连接的回退、首段较长时的origin预行走、每次失败后的origin推进和最终走完整首段均保持。

第二部分segments：两段候选与延迟发布
Ra2SegmentRewritePlan只归拢原先已存在的两方向、两段长度、factor、house和use_threat快照，不缓存context或格属性。方向/长度仍先从delta计算，再依次查询owner_factor/owner_house，随后判断factor>0.00001。
segment_is_passable检查完整候选。每次尝试从当时anchor、原level和high_threat=0开始；首段长度为0仍按既有条件拒绝。每步先推进point/cell_at，启用威胁时在当前point查询并按0.01累计，再调用passage；不能因威胁已超限而跳过通行服务。passage之后总会读取properties，通行成功才合并0x40000、high_threat>3和非终段有威胁的限制，最后总会更新current_level。通行桩可修改桥层和高度，后读属性的顺序保留。
final_segment仍按低8位判断，256与0、257与1分别走对应路径。失败后交换两方向及长度再试，第二次重新初始化point/层高/威胁累计；最多两次。两次都失败时方向缓冲不变。publish_segment_directions仅在完整候选通过后按两段顺序发布方向，并把剩余旧槽填-2；不改anchor/delta，也不增加截断或新规则。
scaled_at_least的x87兼容中间计算、乘法控制与0x037F差值比较保持原样，没有先落为普通double或改变阈值边界。

原版片段与回退
锚点0x429570共8192例；转弯0x428CF0和段改写0x4296F0各12288例，正式合计32768。改代码前、第一部分后和第二部分后均执行相同三组输入，不把重复累计成98304个新用例。原始探针按v38源字节保留，phase3完成流程未重跑、不计本批覆盖。
转弯正前缀返回{p1['successes']}例、零前缀{p1['failures_or_zero_prefix']}例；零前缀可能是合法缩短结果，不作为测试失败。段改写返回成功{p2['successes']}、不改写{p2['failures_or_zero_prefix']}例，两类结果均与原版一致。锚点函数返回void，其通用success/failure计数字段不作成败解释。
比较完整方向/层高缓冲、锚点/差量/索引、格数组、上下文、返回结果及有记录的有序引擎回调。转弯比对{p1['event_words_compared']}个事件字、段改写{p2['event_words_compared']}个事件字，不能把事件字称作相同数量的服务调用。两者含12种数值控制，覆盖0/临界/负因子、威胁边界、16位坐标边界、特殊连接和passage修改桥层的输入。原版返回栈平衡逐例核对；这些是桩服务映射片段证据，不宣称全部寄存器/ABI或全部自然地图入口覆盖。
改动前探针源码/程序/header独立留在baseline-probe，生产基线315项、两部分源码/工具/编译收据/正式程序/探针均保留。每部分默认遭遇战301帧、北桥501帧、南桥501帧，共3配对1303帧，全部严格通过。

社区引擎参考核对与应用
按用户建议核对了gagarin、EA公开Red Alert源码和Phobos的5项固定提交资料，保存内容SHA-256和定位行号；未引入第三方引擎实现代码，生产仍为本项目C17。
gagarin目标是Yuri Revenge gamemd.exe 1.001。检查的AStar声明、FootClass::FindPath包装和单位AStar调用方提供结构、名称和桥层标记线索，不构成本工程RA2 1.006局部路径函数的已验证同版地址/规则映射。EA旧Red Alert源码提供先检查通行再发布优化方向、-2空槽等组织线索，但其视线/沿边搜索及命令对优化不同于本项目分层搜索和局部规则。Phobos定位为原引擎扩展，不能作为独立C17替代引擎。
本批据此把候选检查和成功发布清楚分开，后续可直接从固定链接定位相关结构，减少重复检索；不声称已经量化开发提速。阈值、威胁查询位置、桥层读取及返回栈仍以本项目原版探针和功能验证为依据。
{reference_lines}

自然代表场景与有限回归
沿用父批mi/sc/aw3/fm四套已验配方和原地形/规则，无新增自然场景；改动前完整轨迹按父批哈希继承，不重复运行基线。最终程序重新运行车先登载、南侧Rough/Clear/Beach岸段、全8邻格占位后释放并重发卸载、步兵先登载四场。每种模式完整轨迹分别等于改代码前本模式；实际装卸、同时过水、合法落格、先后顺序、全程生命及后续Guard目标保持。
mi货车原版2020/C2018、fm步兵原版2219/C2220等旧时序差异、通用comparison.json的false和随机首差窗口原样保留。首差仍mi/sc/aw3为349帧、fm为350帧，只读前后8帧窗口，不加随机钩子、不改种子、不重置/追平随机流，不把快照差异当作某次随机调用的因果证明。
最终程序有限复验列车碰撞、碾压、重复失败、弯曲高差。原版Z436停滞和Z-193未完成等异常保留输入、轨迹及基线，不转为必须逐BUG复刻的要求。旧未合格岸边、远释放目标、坡型8/飞机、名称表和碰撞负控制按boundary-inheritance.json哈希继承，未全部重跑。29非主C候选/86原始入边按哈希继承，当前312项输入无新增直接C调用，无新自然非主副本或隧道入口结论。

验收、保护与清理
合计{pairs}配对{frames}模拟帧，{strict_pairs}严格、{variations}局部功能通过；最终生产5配对3455帧，独立事件/只读宿主4配对13004帧。固定seed12345，构建串行，最多两条配对通道/四个游戏进程，没有为无关内部差异扩大矩阵。
父批399项封存、315项独立基线、改动前探针与宿主、两部分回退、完整轨迹及原版异常保留。H盘20项原始输入、原版game.exe/SAVE0029、原规则、旧手写引擎、Git配置和远端引用校验不变。
开场受限命令启动器枚举Q盘失败，改用常规执行；首次Python读取公开资料时TLS连接中止，改用系统HTTP接口成功。详见environment-note.json；均属于工具环境问题，未改变生产输入，不是游戏回归差异。公开源码临时下载文件逐个删除。
逐路径/类型/哈希清理{clean['deleted_files']}个可重建中间文件或缓存，共{clean['deleted_bytes']}字节；同目录{clean['protected_files']}项非候选哈希不变。源码、正式程序、资源、基线、回退与轨迹保留。本地提交，不推送。
复核：{R/'verify_final_movement_v58.py'}；提交收据：{S/'postcommit/git-local-commit.json'}。
下一步按功能需要推进ground_path_heap/nodes的堆容量、节点分配及发布服务，或连接路径完成/重建与更多自然交通；其他引擎子系统及完整视觉/资源调用验收仍未覆盖，不宣称全游戏等价。
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式57 / 验证58，2026-10-25。
父提交：{read(S/'vcs-context.json')['parent_commit']}。
政策：{policy}
报告：{report}
程序SHA-256：{digest}
仅整理ground_path_local.c：锚点反扫状态命名/原发布顺序；can_shorten_run候选走廊；Ra2SegmentRewritePlan/segment_is_passable/publish_segment_directions。181C/312输入/37保护不变。转弯查origin威胁，段改写查point威胁；通行/属性/威胁与阻挡后下一格/层高顺序保持，最终标志低8位和成功后发布/剩余-2保持。
锚点8192、转弯12288、段改写12288原版映射例，共32768；改动前及两部分重跑不累计。转弯/段改写12数值模式、原版返回栈平衡均通过。零前缀不是失败，锚点void计数字段不作成败解释；phase3完成流程未重跑。改动前探针另存baseline-probe。
两部分各3配对1303帧全部严格；总15配对19065帧，11严格、4局部功能。mi/sc/aw3/fm本轮复验，基线引用父批，无新自然场景；各模式完整轨迹等于改动前本模式，旧1/2帧差异、严格false、随机窗口和原版异常保留，不追逐个BUG。
社区参考已核对：gagarin的YR1.001结构/符号、EA旧Red Alert优化检查、Phobos扩展定位；5项固定提交/哈希/行号见{S/'community-reference-review.json'}。只用于结构和定位，未引入外部引擎代码或直接套地址/阈值。原版1.006验收仍为依据。
列车/碾压/重复失败/高差有限回归；旧未合格岸边、远目标、坡图/飞机及29非主C/86入边按哈希继承，无新自然入口结论。
基线：{S/'baseline'}；回退：{S/'parts'}；基线探针：{S/'baseline-probe'}；基线宿主：{S/'baseline-observer'}；封存：{S/'final-source'}。
已清理逐路径哈希核对的可重建缓存；H输入、原版、规则、旧引擎及历史证据保留。工具启动器Q盘问题用常规执行解决，公开资料读取用系统HTTP接口；详见environment-note.json。
下一步按功能需要推进ground_path_heap/nodes堆容量、节点分配/发布，或路径完成/重建服务；其他子系统与完整视觉/资源调用仍未覆盖。
派生下一批工具时显式更新父证据目录为movement-state-v58，并保留导入校验。
复核：{R/'verify_final_movement_v58.py'}。本地提交不推送。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第五十七批正式57 / 验证58已验收。\n交接：{handoff}\n政策：{policy}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-25）：原版1.006 C17/x86单位移动第五十七批已验收。局部转弯、锚点与段改写服务及社区参考核对；[第五十七批交接](交接文档-单位移动第五十七批正式验收-20261025.txt)。遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第五十七批（2026-10-25）\n局部转弯/锚点/段改写，181C/312输入/37保护，{pairs}配对{frames}帧，三个原版片段组共32768例。\n社区5项固定来源仅供结构/定位参考；既有自然场景按冻结基线和功能通过，严格false、旧时序和原版异常保留。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=57,verification_round=58,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer)
 x['current_batch']=dict(formal_generation=57,verification_round=58,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=32768,production_c_sources=181,content_inputs=312,strict_all_frames_equal=False,accepted_baseline_variations=variations,strict_game_pairs=strict_pairs,functional_game_pairs=variations)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,natural_alias_dispatch_required=False,candidates_not_confirmed_failures=True,community_references_available=True,remaining=['ground_path_heap/nodes capacity, allocation and publication services as functionally needed','Path completion/rebuild integration and additional natural traffic as functionally needed','Other engine subsystems and full visual/resource acceptance']))
for e in read(S/'checker-lineage.json')['entries']:assert e['final_derived_sha256']==sha(R/e['derived'])
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v58*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe','.json'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']];documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=read(S/'vcs-context.json')['parent_commit'],state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=181,content_inputs=312,unsupported_guards=37,native_cases=32768,probes=3,capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,accepted_inherited_variations=variations,strict_game_pairs=strict_pairs,strict_all_frames_equal=False,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=57,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames))
