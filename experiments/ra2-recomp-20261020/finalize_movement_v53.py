"""Promote batch52: allied blockers, bridge notification, recovery and bounded coast effects."""
from run_batch_v53 import *
for name in ['native-gates.json','effects.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-functional-impact.json','rng-first-split-window.json','occupied-shore-qualification.json']:assert read(S/name)['passed'],name
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');effects=read(S/'effects.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json');rng=read(S/'rng-functional-impact.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['obstacle','recovery']];assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results']);frames=sum(x['frames'] for x in parts)+matrix['production_frames']+matrix['observer_frames']
strict_pairs=sum(x['scene_count'] for x in parts)+sum(x['strict_trace_equal'] for x in matrix['results']);variations=effects['accepted_baseline_variations'];assert pairs==14 and frames==16264 and strict_pairs==11 and variations==3
report=P/'docs/单位移动第五十二批-友军阻挡与失败恢复及岸边等待和多载车-20261025.txt';handoff=P/'交接文档-单位移动第五十二批正式验收-20261025.txt';policy=P/'docs/项目目标与验收边界-20261024.txt'
aw=effects['representative']['aw3']['effect_modes'];mp=effects['representative']['mp']['effect_modes'];a=aw['original']['special'];m=mp['original']['special'];qualification=read(S/'occupied-shore-qualification.json')
text=f'''单位移动第五十二批（正式52 / 验证53），2026-10-25。
父提交：{read(S/'vcs-context.json')['parent_commit']}。第五十一批408项封存逐项核对；本轮315项独立基线保留。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
政策：{policy}

实现与服务边界
目标为整体功能、效果、规则与资源解读一致，不追求逐个BUG复刻。只整理ground_obstacle.c、ground_recovery.c，181个生产C、312项编译内容、37个未实现保护不变；未新增生产文件或修改CMake。
友军阻挡分成close_to_allied_blocker和notify_allied_blocker：先保留方向/地图内判断后的方向重读，通行结果3请求开门，结果6才按友军查询→列车排除→距离与近目标阈值→特殊谓词→原始位置/层高→Z差→地形依次判断。近目标结束时保持目标取消/停止导航及其返回处理；没有走结束分支时才查询桥标记，随后读原始位置、层高、格层级并发桥层通知。
这些阶段仍使用入口绑定的context，字段及函数表按原调用点读取。重建成功的失败预算复位之后再读取实时路径头；原坐标截断、回绕差值和比较边界不变。
失败恢复分成consume_failure_budget和notify_unaccepted_link，用明确的继续/目标已停/所属对象已移除三种内部结果衔接。预算大于0只递减；耗尽时先无效化段末，取消/停止目标，成功停止或所属对象死亡均在音效与共享收尾前返回。音效回调之后清pending；正常收尾再按移动状态→关联对象存在→是否接受的短路顺序通知，最后无效化段末、选择器与旧旗标。
Recovery保留每次原调用点的context读取，未误改成入口缓存；finish_only跳过预算与音效，但仍执行关联对象及共享收尾。停止成功、死亡与正常退出的副作用不合并。
生成标签/入口/分发表、runtime适配、生产记录器schema12、通用比较器、随机算法、规则和美术不变。29非主C候选与86原始入边按哈希继承；312项输入扫描无新直接C调用，无新自然隧道出口或非主副本入口结论。

分部分验证
友军障碍片段包含失败重建65536、重建成功65536；恢复片段包含失败预算65536、共享收尾65536，共262144个不同用例输入，验证探针覆盖的状态、调用序列、返回/栈与控制字边界。探针源复用旧验证器但在当前生产代码上重新构建执行；不把合成片段当自然场景覆盖。
两部分各默认301帧、北桥501帧、南桥501帧，分别3配对1303帧，全部严格通过并保存独立源码/工具/程序回退。运输构造128与Capture64例按哈希继承，不当作本轮新用例。南北桥的移动步兵关系查询、友军等待与绕行按实际事件核对，不冒称所有桥层通知分支均被自然触发。

岸边相邻落格全占用、载员等待与释放重试
aw3保留原版真实水面/沙滩/陆地记录，普通地图放车、正常登载、Move与Unload命令；不写载员链、占用结果、位置/路径或返回值。货车120帧装载，经过593帧实际水面样本后返岸。
车队均从邻格外通过正常Drive移动器驶入，填满运输船[138,102]周围8个陆格：{a['legal_adjacent_cells']}。这些格地形为可通行陆地/道路且无桥，车队Z0，不是初始重叠占位；验证的是此场相邻8格全占用及实际卸载效果，不声称穷举引擎所有候选半径、朝向或其他地形。
1900..2299共{a['full_occupied_frames']}帧8格持续全占用，货车保持载员标记，没有卸下或损失。2300帧释放命令不等于已释放：占位车{a['first_actual_release_motion']}帧才实际移动，{a['first_vacant_cell_frame']}帧第一次腾出邻格。2400帧正常重发Unload，2404帧才在[139,102]卸下，随后货车到[140,104]，占位车到[141,101]。
此处为载员等待、释放后重试成功，不称引擎自动保持卸载任务并自动卸下；占用阶段的实际任务记录见occupied-shore-qualification.json。船300、货车/8辆交通车200、舰船600、步兵125生命全程保持；普通步兵与传送步兵到各自目标。
保留两个未合格控制：b-aw只形成7格占用，且指定释放车没有移走实际占位；b-aw2形成8格占用但较远释放目标未产生位移。没有把未移动的内部原因归为原版BUG；后续货车目标[144,104]确为水格，已校正为已验陆格。第三次只改普通移动目标/路点，不改地形或强制状态，才获得合格释放。前两控制不计正式配对，输入/轨迹原位保留，不继续无功能目标追查较远移动失败原因。

多载车、容量与卸载顺序
mp普通地图中两辆TRUCKA分别133/226帧装上LCRF；{m['simultaneous_loaded_range']}范围同时保持两车载员标记，693帧经过真实水面。原规则LCRF Passengers=12、SizeLimit=6，TRUCKA Size=6、E2 Size=1；两车占满容量12，额外150帧步兵登载请求没有形成载员标记，后续正常地面移动成功。
不将发令当装载，也不宣称直接观测到了容量拒绝服务的返回值。实际只有两车，不冒称两车加步兵三载员或混合登载全部成功。
Unload后先下第二辆1023366，再下第一辆1023363；原版时点{mp['original']['special']['drop_frames']}，C版{mp['generated-c']['special']['drop_frames']}，有1帧旧差异。两车实际落格分别[139,101]/[139,102]且生命保持；随后到[140,104]/[139,104]，未登载步兵到[141,104]、交通车到[138,104]，舰船与传送步兵完成目标。
两车登载/过水/保持、容量上限相容的额外请求结果、先后卸载和最终效果一致；不为1帧差异修改随机数或复制异常。并保留原位步兵/车辆交通组合。

其他移动器与随机分流的有界影响
js沿用第五十一批SUB/JUMPJET/SHAD/E2配方。本轮最终程序重跑完整场景，改动前基线直接引用第五十一批已验原始轨迹，不再次复制或重跑同一基线。两轮空运77/2004、2353/3504，潜艇水路、普通步兵和飞行步兵目标格/生命效果一致；飞行步兵最终高度500、任务2，仍不称Guard完成，不把潜艇Z0当潜航深度。
三场当前原版/C各自完整轨迹逐条等于各自改动前基线；通用comparison.json的false保留。首个随机快照差异分别{ {k:v['rng_first_different_frame'] for k,v in rng['new_variants'].items()} }，每场只读首差前后各8帧窗口，并记录参与对象位置/任务/朝向/生命首差。aw3窗口还包含占位交通车，未把索引差异当实际调用次数或因果来源证明。
完整功能核查覆盖载员保持、合法落格、全占用/真实释放、容量、卸载顺序、目标与生命；未添加随机调用钩子、改种子、重置/追平随机流或放宽通用比较器。不推及战斗随机分配或全游戏等价；只有出现功能影响才继续扩展。

验收、清理与接续
含两部分共{pairs}配对{frames}模拟帧，{strict_pairs}严格、{variations}局部功能通过。最终生产{matrix['production_scenes']}配对{matrix['production_frames']}帧，事件/只读宿主{matrix['observer_scenes']}配对{matrix['observer_frames']}帧。固定seed12345，最多两条配对通道/四个游戏进程，构建串行。
受影响的列车碰撞、碾压、重复失败及弯曲高差Z436停滞/Z-193未完成已有限回归；负对照、旧坡型8控制及独立接桥/飞机异常证据按哈希继承，未全部重跑，不转为必须逐BUG复刻要求。
父批408项封存、本轮315项基线、两部分回退、改动前宿主、全部正式/控制轨迹和异常保留。H盘20项输入、原规则、原版EXE/SAVE0029、旧手写引擎、Git配置与远端引用不变。
清理{clean['deleted_files']}个逐路径/类型/哈希核对的可重建缓存文件，共{clean['deleted_bytes']}字节；同目录{clean['protected_files']}项非候选哈希不变。源文件、正式程序、资源、轨迹、基线与回退保留。
后续按功能需要整理ground_path_prepare的桥层高度、朝向邻格排除及根节点服务；扩展一车加步兵等混合载员、其他岸型/朝向和通知/恢复的自然场景。较远释放目标未移动的内部原因不作为必追旧BUG；其他引擎子系统与完整图像/资源调用验收仍未覆盖。
复核：{R/'verify_final_movement_v53.py'}。本地提交不推送，收据：{S/'postcommit/git-local-commit.json'}。
'''
assert not report.exists() and not handoff.exists();report.write_text(text,encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式52 / 验证53，2026-10-25。
父提交：{read(S/'vcs-context.json')['parent_commit']}。
政策：{policy}
报告：{report}
程序SHA-256：{digest}
只整理ground_obstacle、ground_recovery，181C/312输入/37保护，无新增生产文件或CMake改动。友军近目标结束与桥层通知分开；预算耗尽的成功停目标/死亡/音效/关联对象/共享收尾分开，服务次序和context读取方式保留。
262144原生片段用例（障碍131072、恢复131072），两部分各3配对1303帧；合计{pairs}配对{frames}帧，11严格、3局部功能通过。运输128/Capture64继承，不重复计数。
aw3在真实岸边8个邻格1900..2299全占用400帧，货车保持装载；2300发令，2329实际动、2356腾格；2400重发卸载、2404卸下，货车到[140,104]、释放车[141,101]。未称自动卸载或穷尽所有方向/半径。
b-aw只7格、b-aw2全8格但远释放目标未动，均保留排除；不追未知内部原因。原货车水格目标已改已验陆格，最终只用普通发令取得合格释放。
mp两车133/226装入，容量12/车Size6，额外E2未登载；693帧双车过水；第二车2004先卸，首车原版2019/C2018后卸，各自实际落格、后续目标、生命一致。不是三载员全部成功，直接拒绝服务返回未观察。
js最终程序重跑SUB/JUMPJET/SHAD/E2交通，基线引用父批原始轨迹未重复复制/重跑。三场各模式完整轨迹等于改动前，严格false与随机首差窗口原位保留，按功能有界验收。
列车/碾压/重复失败/高差异常有限回归；旧坡图、飞机异常和29非主C/86入边按哈希继承，无新自然入口结论。
基线：{S/'baseline'}；回退：{S/'parts'}；基线宿主：{S/'baseline-observer'}；封存：{S/'final-source'}。
后续ground_path_prepare桥层/朝向排除/根节点，混合载员和其他岸型、自然通知/恢复组合；其他引擎子系统及视觉/资源调用仍在未覆盖范围。沿用整体功能/效果一致，不追逐个BUG。
复核：{R/'verify_final_movement_v53.py'}。本地提交不推送。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第五十二批正式52 / 验证53已验收。\n交接：{handoff}\n政策：{policy}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-25）：原版1.006 C17/x86单位移动第五十二批已验收。友军阻挡/桥层通知/失败恢复，岸边8邻格占用后的释放重试及多载车；[第五十二批交接](交接文档-单位移动第五十二批正式验收-20261025.txt)。继续遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第五十二批（2026-10-25）\n友军阻挡/桥层通知/失败恢复，181C/312输入/37保护，{pairs}配对{frames}帧、262144原生片段例。\n岸边8邻格全占用后的等待释放重试、多载车/额外请求与移动器交通按冻结基线和功能通过；严格false及随机差异保留。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=52,verification_round=53,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer);x['current_batch']=dict(formal_generation=52,verification_round=53,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=262144,production_c_sources=181,content_inputs=312,strict_all_frames_equal=False,accepted_baseline_variations=variations,strict_game_pairs=strict_pairs,functional_game_pairs=variations);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,natural_alias_dispatch_required=False,percentage_reestimated=False,old_corner_followup_only_for_functional_need=True,rng_exact_call_source_proved=False,candidates_not_confirmed_failures=True,remaining=['ground_path_prepare bridge level, facing exclusions and root service','Mixed vehicle/infantry passenger combinations and other coast directions','Further natural bridge notification/recovery service combinations','Other engine subsystems and full visual/resource acceptance']))
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v53*') if p.is_file())
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
print(dict(passed=True,generation=52,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames))
