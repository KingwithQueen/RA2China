"""Promote one finite batch with source, document and rollback identities."""
from run_batch_v45 import *
for name in ['native-gates.json','effects.json','preservation.json','alias-evidence-inheritance.json','cleanup.json','final-scene-matrix.json']:
 assert read(S/name)['passed'],name
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');effects=read(S/'effects.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['commit','continuation']]
assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results'])
frames=sum(x['frames'] for x in parts)+matrix['production_frames']+matrix['observer_frames']
strict=all(x['strict_trace_equal'] for x in matrix['results']);variations=effects['accepted_baseline_variations']
report=P/'docs/单位移动第四十四批-路段接入与接续服务边界及动态交通-20261024.txt'
handoff=P/'交接文档-单位移动第四十四批正式验收-20261024.txt';policy=P/'docs/项目目标与验收边界-20261024.txt'
rep=effects['representative'];repair=rep['reverse-restored-bridge-traffic'];detour=rep['mixed-locomotor-detour']
text=f'''单位移动第四十四批（正式44 / 验证45），2026-10-24。
父提交：{read(S/'vcs-context.json')['parent_commit']}。
第四十三批367项封存已逐项核对，当前303项独立基线及两部分回退保留。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收政策：{policy}

实现与服务边界
整体功能、效果、规则与资源解读一致；只验证本次功能和受影响的有限回归，不以穷尽标签或复制原版每个BUG为目标。
新增ground_segment_admission.h/.c，集中候选是否有效、写入路段/驾驶状态、接受服务、限制标志、开始服务及失败后owner存活检查，返回NO_CANDIDATE/STARTED/REJECTED_ALIVE/OWNER_REMOVED。
接受服务返回false时短路限制标志查询；成功进入后不新增owner查询。失败且owner仍在才清路段/驾驶状态；owner被服务移除时不覆盖服务留下的状态。
Prepare的ground_template提交仍先处理方向队列、目标格与采样字段，再清已有路段；接受/开始服务使用按值传入的候选。未进入路段时仍按原策略清方向并归零速度，包括owner失效路径。
Advance的ground_continuation保留提交模板、刷新对象、驾驶标志与三项对象检查顺序；候选由刷新后的实时状态取得，接受/开始回调继续从实时上下文读取，不能替换成Prepare按值候选。STARTED后依次恢复速度并弹出旧方向，普通受阻仍返回原有继续收尾结果。
两处共有接入判断，各自后续策略保留。未改模板选择算法、对象分类规则、路径结果、生成入口、runtime适配、生产记录器/schema12、比较器、规则或美术资源。
176个生产C，302项实际编译内容输入，37个未实现保护；新增一C一头文件，另改ground_template.c、ground_continuation.c及CMake。

验证与分部回退
Prepare提交与Advance接续两部分，各默认遭遇战301帧、南北桥上移动步兵/车辆交会及占位出口各501帧；每部分3配对1303帧，保存各自源码、构建工具与程序清单。
三个受影响原生片段组共196608例：Prepare主提交与共享提交入口各65536，Advance接续65536。接续包含全部八种通行分类，60545次继续、4991次中止、154次方向移除；服务次序、服务可见状态、返回/栈及探针覆盖的边界均与原版核对。
Prepare的phase1初次独立构建已通过；为让两组收据对应同一保留程序，又复核phase1。旧收据保留，重复例不增加唯一用例计数。Capture普通命令构造器64例证明沿用第四十三批，源/程序哈希一致，本轮未重跑或计入196608。
最终生产程序{matrix['production_scenes']}配对{matrix['production_frames']}帧，普通Capture输入/只读桥格功能宿主{matrix['observer_scenes']}配对{matrix['observer_frames']}帧；连同两部分共{pairs}配对、{frames}帧。最终矩阵全部严格逐模拟帧相同：{strict}；本轮功能例外数量：{variations}。
三个选定新场景同时要求本轮改动前后各模式的完整记录逐条相同。随机数、普通命令、目标对象身份及负注入检测也核对。固定seed12345，最多两条配对通道、四个真实游戏进程，所有构建串行。

修桥后的反向动态交通
普通地图中陷桥车辆先令桥断，工程师正常进入维修屋修复；桥格200帧[0,0]、900/1800帧[1,1]，工程师消耗于{repair['engineer_consumed_frame']}帧。
北行车辆重新发令，与南行步兵在桥上发生关系查询；实际查询帧{sorted({q['frame'] for q in repair['meeting_query_events']})}，同帧多条事件不当成多个模拟帧。车辆也分类查询了出口占位车，并出现{len(repair['waiting_sample_frames'])}个等待采样，这些采样不声称是连续区间。
占位车普通Move发令1350/1450帧，实际运动时点{[x['first_motion_frame'] for x in repair['blocker_releases']]}。车辆最后{repair['car_final']}，请求[60,56]，实际停格{repair['actual_goal_cell']}；原版目标邻格停止按实际效果保留。步兵最后{repair['foot_final']}，两者生命不损失。
气垫作为附近静止横向占位，正常悬浮升降；没有声称它完成横向移动。相同地图仅省去工程师Capture命令的负对照桥格仍断、工程师仍在，车辆/步兵没有跨越断口。

毁桥后的混合移动器绕行
主车仅一次Move命令，自行使用普通地图的替代通道绕过断口及停放车辆。车辆/步兵/气垫的普通移动输入与真实效果见{S/'effects.json'}。
主车最后{detour['car_final']}，步兵最后{detour['foot_final']}，气垫最后{detour['hover_final']}；停放车辆仍在原位。共同移动采样{len(detour['simultaneous_motion_frames'])}帧，只按水平位移判断，不把悬浮升降当成通行。无桥、路径、速度、对象链或最终结果直接写入。
前两条气垫路线在原版未能水平抵达，原版/C均只悬浮而未前进；初次配方、输入、轨迹及比较全部保留，不计作气垫移动效果。最终选用此前已证实可达的南侧入口，并调整气垫发令时序；没有修改原始规则或通用比较器。气垫混类绕行改动前已存在X13/Y21世界单位的最大水平差、方向5316/5324、计时88/4差异；只有气垫六项字段与stage27地形查询时点变化，其余状态、普通命令、随机数、地面车辆和步兵一致。严格comparison.json保留false，局部功能验收冻结到本轮基线的同模式完整记录，不追平瞬时数值。

原版异常、合法入口与范围限制
两项弯曲高差原版异常（Z436停滞、Z-193未完成）按有限回归保留，未来不要求逐BUG复制。列车真实碰撞与步兵碾压继续回归，关闭规则的负对照沿用既有受保护证据；重复重建失败的受控单位环仅用于诊断回归，与普通地图实景分开。
第四十二/四十三批Jumpjet及气垫瞬时数值差异和各自严格false报告原地保留，本轮不重复其未受影响矩阵，不把旧差异改记为通过或追平每个BUG。
29个非主C候选、86条原始入边的有界来源调查沿用，当前302项输入扫描无新增直接C调用；生成标签与分发表保留。没有证明新的合法自然入口，不强造入口扩充覆盖。
本批只整理剩余服务边界的一部分，不代表全地面移动可读化或全游戏完成。下一步按具体状态入口、其他移动器/运输/上下桥及引擎子系统集成继续推进；只在新功能或重要回归出现时扩大验证，不估算缺少可靠分母的全项目百分比。

保留、清理与本地提交
父批封存、当前独立基线、两部分回退、改动前功能宿主及探索/异常记录保留；当前封存只含实际编译内容、当前工具和有限选用配方。
删除{clean['deleted_files']}个逐项路径/类型/哈希核对的可再生成中间文件或缓存，共{clean['deleted_bytes']}字节；同目录{clean['protected_files']}个非候选文件哈希不变。没有删除源文件、程序、原始资源、存档、轨迹或回退。
H盘20项原版输入、只读提取规则、原版EXE、SAVE0029及旧手写引擎指纹不变；Git配置及远端引用不变。
复核：{R/'verify_final_movement_v45.py'}。
本地提交，不推送；提交身份见{S/'postcommit/git-local-commit.json'}。
'''
assert not report.exists() and not handoff.exists();report.write_text(text,encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式44 / 验证45，2026-10-24。
政策：{policy}
报告：{report}
程序SHA-256：{digest}
共享ground_segment_admission；Prepare按值候选与失败归零、Advance实时候选与成功恢复速度/移除方向的差别保留。176C/302输入/37保护，生成入口/runtime/比较器/生产记录器未改。
原生3组196608唯一例；2部分各3配对1303帧，最终连同分部共{pairs}配对{frames}帧。Capture64例证明继承，不重复计数。
修桥两场严格逐帧相同；混类绕行保留气垫数值差异，当前每个模式与改动前完整轨迹相同。
已补北行修桥交通与南行步兵交会、出口两车1350/1450先后离开；不修桥负对照未跨越。原版目标邻格停止保留。毁桥绕行中包含真实水平移动气垫、车辆与步兵；初次气垫仅悬浮未前进的探索保留，不计成功。
旧气垫/Jumpjet差异、原版高差异常和29候选调查原地保留，不追求逐BUG复刻。
基线：{S/'baseline'}；回退：{S/'parts'}；基线功能宿主：{S/'baseline-observer'}；封存：{S/'final-source'}。
后续按剩余具体状态分支、其他移动器与运输/上下桥及其他子系统继续，有界验证，保留回退，清理可重建缓存，本地提交不推送。
复核：{R/'verify_final_movement_v45.py'}。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第四十四批正式44 / 验证45已验收。\n交接：{handoff}\n政策：{policy}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-24）：原版1.006 C17/x86单位移动第四十四批已验收。共享路段接入与接续服务边界、反向修桥交通及混合移动器绕行；[第四十四批交接](交接文档-单位移动第四十四批正式验收-20261024.txt)。继续遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)，保留基线、回退和原版异常。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt'
p.write_bytes(f'第四十四批（2026-10-24）\n新增ground_segment_admission，共用路段接入判断；保留Prepare按值候选/失败归零与Advance实时候选/成功接续的不同服务顺序。\n反向修桥交通与混合移动器绕行已实测；176C、302输入、37保护，{pairs}配对{frames}帧，原生196608例。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=44,verification_round=45,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer);x['current_batch']=dict(formal_generation=44,verification_round=45,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=196608,production_c_sources=176,content_inputs=302,strict_all_frames_equal=strict,accepted_baseline_variations=variations);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
exploratory=[]
for folder in sorted((S/'runs').glob('b-*')):
 if folder.is_dir() and (folder/'comparison.json').is_file():
  q=read(folder/'comparison.json');exploratory.append(dict(tag=folder.name,strict_passed=q['passed'],frames=q['comparison']['frames_compared'],selected=folder.name in [x['baseline_tag'] for x in read(S/'dynamic-fixtures.json')['fixtures']],counted_in_final_matrix=False))
write(S/'exploration-summary.json',dict(passed=True,results=exploratory,failed_horizontal_hover_recipes=['b-ds','b-d2'],initial_probe_link_failure_log='build-part-commit-template-1.log',all_original_reports_retained=True))
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,natural_alias_dispatch_required=False,percentage_reestimated=False,remaining=['Other generated state entries and service boundaries','Other locomotors and transport/bridge transition combinations','Other engine subsystems and integration']))
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP','evidence/movement-state-v45/service-boundaries.json'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v45*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.glob('*fixtures*.json'))
manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']]
documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=read(S/'vcs-context.json')['parent_commit'],state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=176,content_inputs=302,unsupported_guards=37,native_cases=native['cases'],probes=native['groups'],capture_packet_cases_inherited=64,accepted_inherited_variations=variations,strict_all_frames_equal=strict,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=44,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames))
