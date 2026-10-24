"""Promote batch49 finite functional acceptance; retain strict differences and original evidence."""
from run_batch_v50 import *
for name in ['native-gates.json','effects.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-functional-impact.json']:assert read(S/name)['passed'],name
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');effects=read(S/'effects.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['failure','passage']];assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results']);frames=sum(x['frames'] for x in parts)+matrix['production_frames']+matrix['observer_frames']
strict=all(x['strict_trace_equal'] for x in matrix['results']);variations=effects['accepted_baseline_variations'];assert not strict and variations==2
report=P/'docs/单位移动第四十九批-失败与通行服务及真实水岸和斜角坡面-20261024.txt'
handoff=P/'交接文档-单位移动第四十九批正式验收-20261024.txt';policy=P/'docs/项目目标与验收边界-20261024.txt'
rep=effects['representative'];water=rep['w2']['effect_modes'];air=rep['a2']['effect_modes'];corner6=rep['c6']['modes']['original'];corner8=rep['c8']['modes']['original'];impact=read(S/'rng-functional-impact.json')
text=f'''单位移动第四十九批（正式49 / 验证50），2026-10-24。
父提交：{read(S/'vcs-context.json')['parent_commit']}。第四十八批405项封存逐项核对；本轮313项独立基线保留。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
政策：{policy}

实现与服务边界
继续以整体功能、效果、规则和资源解读一致为目标，不追求逐个BUG复刻。逐模拟帧记录用于判断回归，已有无功能影响的差异有界记录。
新增ground_outcome_policy.h/.c，整理Prepare七类失败分支及对象扫描后最终占用分类。181个生产C、312项编译内容、37个未实现保护；只另改ground_failure、ground_passage_finish及CMake。
失败7的分类出口与其他分类分开：非7先清待处理状态并返回；可重试的揭示障碍保留拒绝方向，分类障碍写-1并启动重试，再递归。其余按直接/保存指针清段后停止，停止单独入口不清段。服务回调、返回值和重读世界状态保留。
最终通行先解释已扫描的通行值、碾压对象及占用低六位；未决分支仍依次查询目标存在→可碾压、owner哨兵→联盟、crusher→能力、列车→首次武器存在→另一次武器清除能力。回调可能改变能力/武器，不能提前读取或合并两次武器服务。
两组原版映射片段各32768例，共65536例，覆盖探针已有状态、回调副作用/次序、结果及栈清理。运输构造128例、Capture64例按源/程序哈希继承，不重跑、不计入本轮65536。
生成入口、runtime适配、生产记录器/schema12、通用比较器、随机实现、生产规则及美术资源未改。原资源和加载路径沿用；本轮真实游戏逻辑/状态对照不等同完整图像或全游戏验收。

真实水岸与其他移动器
w2/a2沿用地图原有水岸，只替换正常初始单位和普通命令，IsoMapPack5解码内容与基图完全相同，未重画假水面或写入运行时坐标/装载结果。
实际格目录区分Water land2、Beach land6、Clear land0与Rough land7。原规则Water允许Hover/Float，Beach允许Hover但Foot为0；规则来源、原字段及哈希见rules-and-locomotors.json。
登陆艇w2：120帧正常装入TRUCKA，470至1462帧带货位于真实水面，共993帧，经过沙滩后返岸；1904帧在实际陆格{water['original']['landing_cell']}、land0卸车，货车继续Move到{water['original']['cargo_final_cell']}。船最后{water['original']['carrier_final_cell']}；船300、货车/交通车200、驱逐舰600、步兵125生命全程保持。
飞行运输a2：77帧正常装入E2，SHAD从陆地升空越过真实水面，原版/C水面飞行分别{air['original']['water_frames']}/{air['generated-c']['water_frames']}帧；高度范围分别{air['original']['water_height_range']}/{air['generated-c']['water_height_range']}。返岸落地，2004帧在实际陆格{air['original']['landing_cell']}、land0卸人，乘员再走到{air['original']['cargo_final_cell']}；运输机175、舰船600、步兵125生命全程保持。
两场DEST均按普通Move在Water land2/Z0往返；分别到达[130,94]与[130,96]。原生观察移动器表：LCRF 7A31EC、DEST 7AB13C、SHAD 7A52A4；另有地面车/普通步兵交通。
CLEG首次300帧收到沙滩[139,96]目标后保持原格；1500帧改为合法陆地[138,105]，1502帧瞬移到达，生命保持。该负/正组合以本场实测为限；详细传送字段未加入生产记录器。
驱逐舰正常构造会先生成ASW附属飞机，后续单位编号顺延。最初b-wa/b-af配方因此未准确指向预期对象，输入和运行保留、排除计数；w2/a2按原版初始状态核对了编号，不通过直接设置状态凑覆盖。

斜角坡型6、8及交通
使用原版完整邻域地图记录移植到桥入口，保留原高程、坡型和桥覆盖层；坡型8的额外接桥探索另补过普通级4路和坡型3过渡，但均未形成主车接桥，未计作接桥通过，不以运行时写Z或路径指针强制过坡。
坡型6：实际角坡[57,57]，移动角坡采样{len(corner6['moving_corner_samples'])}帧，高度范围{corner6['height_range']}；经邻接坡面上下高地、进入桥道后返程，最终{corner6['end']}。
坡型8：实际角坡[57,57]，移动角坡采样{len(corner8['moving_corner_samples'])}帧，高度范围{corner8['height_range']}；角坡及级4/5/6之间往返成立，最终{corner8['end']}。主车900帧的桥目标未形成移动，905至1699帧停在[54,58]；920帧Guard且路径为空。1700帧换为可达高地目标，1730帧恢复实际移动并到达[58,56]。这是普通地图/命令下的受阻与恢复实景，不使用单位环，不宣称已证明具体内部失败入口。
坡型6主车桥层0→1→0→1→0并完成桥道往返；坡型8主车未上桥，只验角坡/受阻恢复。两场其他车辆/步兵均实际通过桥面并完成目标，车辆桥层0→1→0，生命保持。两场原版/C严格逐帧一致。
坡型8完整接桥仍未覆盖；c8、低路d8、加东坡e8的探索输入/轨迹全部保留，不声称已定位根因，不归咎原版BUG，也不继续无限扩展接桥试验。近距离桥上交会/占位/绕行及主车完整桥道行程另由坡型6及两部分南北桥实景覆盖。

随机分流：按功能影响有界处理
旧额外时序b3-dc仅只读复查，不重跑、不计新配对。仍从1029帧起分流，共{impact['old_variant']['rng_different_frames']}帧随机快照不同；原版/C装车145、卸车1504、桥毁430、触发车移除460及最终目标格和生命一致。货车卸载/到达的子格坐标不同，完整原始轨迹及严格false保留。旧同一气垫任务周期调用及前344次原始抽取字的证明按哈希继承，不冒充本轮新随机探针。
新水岸/飞行场景在改动前也已出现349帧起随机分流，早于400/500帧主运输移动命令。舰船到达的相邻帧状态已列出，不能据时间相邻宣称已证明精确调用根因；本轮未增加随机调用钩子、不重置种子或随机状态。
水岸/飞行的装载、卸载帧、实际陆地落格、生命及最终目标一致；返航、通过水岸和合法陆地传送效果成立。瞬时高度、过水时点、子格和后续随机分配仍为记录差异。两场当前原版/C分别与改代码前各自完整轨迹逐条相同，故未发现本次整理引入回归。
两场按局部功能验收通过，严格comparison.json仍为false；通用比较器及随机检查未放宽。该结论只覆盖本轮代表效果，不推及后续战斗随机结果或全游戏等价，不再为这些无功能影响的差异无限追帧。

验证、清理与剩余
两部分各默认301帧、南北桥各501帧，每部分3配对1303帧，独立保存源码/工具/程序回退。最终生产{matrix['production_scenes']}配对{matrix['production_frames']}帧，事件/只读观察宿主{matrix['observer_scenes']}配对{matrix['observer_frames']}帧；含两部分共{pairs}配对{frames}帧，其中13配对严格相同、2配对按冻结基线及功能效果验收。固定seed12345，最多两条配对通道/四个游戏进程，构建串行。
列车碰撞、碾压、重复失败、原版弯曲高差Z436停滞和Z-193未完成已有限回归；负对照沿用已有证据，受控单位环仅用于失败诊断。所有原版异常原位保留，不转化为永久逐BUG要求。
29个非主C候选、86条原始入边按哈希继承，当前312项编译内容扫描无新增直接C调用，原标签/分发表保留，没有新自然入口结论，不强造入口。
父批405项封存、本轮313项基线、两部分回退、改动前宿主、未合格配方及全部异常保留。H盘20项原版输入、只读规则、原版EXE、SAVE0029、旧手写引擎、Git配置和远端引用不变。
清理{clean['deleted_files']}个逐路径/类型/哈希核对的可重建文件或缓存，共{clean['deleted_bytes']}字节；同目录{clean['protected_files']}项非候选文件哈希不变。源文件、程序、原始资源、轨迹、基线和回退保留。
剩余：未覆盖的状态/服务入口、坡型8主车接桥、更多水岸/运输与移动器组合及其他引擎子系统。已记录的非功能差异仅在出现实际功能影响时再有界核查，不追求穷尽内部或异常。
复核：{R/'verify_final_movement_v50.py'}。本地提交不推送，收据：{S/'postcommit/git-local-commit.json'}。
'''
assert not report.exists() and not handoff.exists();report.write_text(text,encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式49 / 验证50，2026-10-24。
父提交：{read(S/'vcs-context.json')['parent_commit']}。
政策：{policy}
报告：{report}
程序SHA-256：{digest}
新增ground_outcome_policy，整理Prepare七类失败及最终占用/通行服务；181C/312输入/37保护。生成入口/runtime/记录器/比较器/规则/美术/随机函数未改。
本轮65536原生例；两部分各3配对1303帧并保留回退；合计{pairs}配对{frames}帧，13严格、2按冻结基线和功能效果通过。运输128/Capture64例按哈希继承。
真实原图水岸：LCRF正常装车120、真实水面993帧、返岸卸车1904；SHAD装人77、起飞过水返岸、卸人2004。DEST水面往返、地面车/步兵交通、CLEG沙滩受阻及合法陆地1502帧瞬移完成；生命/目标格保持。
两运输场景改代码前已有349帧随机/时序/瞬时高度及子格差异。当前两种模式分别等于改动前完整轨迹，严格false保留，仅通过本场功能验收。未增加随机钩子、不强行同步；旧1029样本只读核查生命、目标和装卸效果，不计新配对，不推及全游戏。
坡型6完成主车桥道往返；坡型8完成角坡与级4/5/6、自然受阻后1730帧恢复，主车接桥仍未覆盖。其他车兵实际通桥，两场严格逐帧一致。低路/东坡接桥探索和ASW编号错位配方保留排除。
基线：{S/'baseline'}；分部回退：{S/'parts'}；基线宿主：{S/'baseline-observer'}；封存：{S/'final-source'}。
剩余状态/服务、更多真实运输/移动器组合、其他子系统；维持整体功能、效果一致的有限验收边界，保留原版异常和29候选调查。
复核：{R/'verify_final_movement_v50.py'}。本地提交不推送。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第四十九批正式49 / 验证50已验收。\n交接：{handoff}\n政策：{policy}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-24）：原版1.006 C17/x86单位移动第四十九批已验收。失败与通行服务、真实水岸/飞行装卸、舰船/传送及坡型6/8交通；[第四十九批交接](交接文档-单位移动第四十九批正式验收-20261024.txt)。继续遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第四十九批（2026-10-24）\n新增ground_outcome_policy，整理失败/最终占用服务；181C/312输入/37保护，{pairs}配对{frames}帧、原生65536例。\n真实水岸及飞行运输按冻结基线和功能效果通过，保留严格false和随机差异；坡型6/8严格相同。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=49,verification_round=50,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer);x['current_batch']=dict(formal_generation=49,verification_round=50,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=65536,production_c_sources=181,content_inputs=312,strict_all_frames_equal=strict,accepted_baseline_variations=variations,strict_game_pairs=13,functional_game_pairs=2);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,natural_alias_dispatch_required=False,percentage_reestimated=False,remaining=['Uncovered generated state/service entries','Primary corner8-to-bridge route remains unqualified; retained bounded trials','More natural shore/transport and locomotor combinations','Recorded timing/subcell/RNG variations: revisit only for functional impact','Other engine subsystem integration']))
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v50*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.glob('*fixtures*.json'))
paths.update((S/n).relative_to(R).as_posix() for n in ['bridge-catalog-build-arguments.json','mission-table-proof.json','transport-native-validation-current.json','native-gates.json','service-boundaries.json','rng-functional-impact.json','excluded-explorations.json','unconnected-corner-exploration.json','lower-road-corner-exploration.json','east-transition-exploration.json','corner-qualification.json','rules-and-locomotors.json'])
manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']]
documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=read(S/'vcs-context.json')['parent_commit'],state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=181,content_inputs=312,unsupported_guards=37,native_cases=native['cases'],probes=native['groups'],capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,accepted_inherited_variations=variations,strict_all_frames_equal=strict,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=49,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames))
