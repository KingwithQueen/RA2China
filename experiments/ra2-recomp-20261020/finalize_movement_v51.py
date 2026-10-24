"""Promote batch50: finite service boundaries, independent corner8 bridge and transport cycles."""
from run_batch_v51 import *
for name in ['native-gates.json','effects.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-functional-impact.json','corner-boundary-findings.json']:assert read(S/name)['passed'],name
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');effects=read(S/'effects.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['gate','exit']];assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results']);frames=sum(x['frames'] for x in parts)+matrix['production_frames']+matrix['observer_frames']
strict=all(x['strict_trace_equal'] for x in matrix['results']);variations=effects['accepted_baseline_variations'];assert not strict and variations==3
report=P/'docs/单位移动第五十批-模板与共享出口及坡型8接桥和水岸循环-20261024.txt'
handoff=P/'交接文档-单位移动第五十批正式验收-20261024.txt';policy=P/'docs/项目目标与验收边界-20261024.txt'
rep=effects['representative'];corner=rep['cm']['modes']['original'];water=rep['cw']['effect_modes']['original'];air=rep['ca']['effect_modes'];plane=rep['of']['effect_modes']
text=f'''单位移动第五十批（正式50 / 验证51），2026-10-24。
父提交：{read(S/'vcs-context.json')['parent_commit']}。第四十九批402项封存逐项核对；本轮315项独立基线保留。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
政策：{policy}

实现与服务边界
以整体功能、效果、规则和资源解读一致为目标，不追求逐个BUG复刻。未改变生产规则、美术、随机算法、生成入口/runtime适配、生产记录器schema12或通用比较器。
保持181个生产C、312项编译内容、37个未实现保护，只整理ground_template_transition.c与ground_tube_state.c；未增加生产文件或改CMake。
模板门分成类型门和覆盖层门。入口绑定context一次；第一分类>=7时跳过第一类型查询，类型门不清理时第二阶段重新读取分类，只有4/5才依次读第二类型标志和overlay。类型/覆盖层服务的副作用不能用预读或缓存合并。
共享出口分成原对象链快照、快照让路与空出口落位三个阶段。先完整复制原链再发让路请求；每次迭代重读快照数量，非类别1再查一次类别，仅类别1/15查询移动状态并请求静止对象让路；速度服务之后释放快照。空出口按落位→入格→目标格查询→必要自让路→恢复任务→速度复位→朝向执行。
两类服务均保留原版入口绑定的context值，context内部世界字段和函数表仍按原调用点访问。初版出口回退另存parts/exit-before-context；最终版本按入口绑定复验。
正式原生覆盖98304个不同用例输入：模板65536、共享出口32768，核对探针覆盖的回调值/顺序、状态、结果和栈清理；同组重跑不重复计数。运输构造128/Capture64例按源/程序哈希继承。本轮未新增自然隧道出口进入/清场实景，片段验证不冒称自然入口覆盖。

坡型8：有界控制与独立合法组合
历史地图只新增两项正常命令控制：cf把主车从低处[54,58]直接出发，仍未上桥；cs保留到达历史并以高、低路点分段，可到[60,58]级5和[62,58]级4，但桥目标仍未成行。两控制原版/C严格一致，不计正式配对，说明不能仅用原先下坡到达历史解释受阻；未证明具体内部原因，不归咎原版BUG。
另只新增一个独立集成模块cm：在已验c6地图旁放置原版坡型8完整邻域和原版坡型3过渡，桥入口及桥面[59..61,60..73]记录保持原字节不变。只用普通初始位置、地图记录与Move路点，不调用位置、路径或通行结果设置函数。
主车实际角坡[54,56]、级4/5/6范围416至624，移动角坡采样{len(corner['moving_corner8_samples'])}帧；1900/2299帧在[60,80]完成南行，返程后2999帧到角坡，最终{corner['end']}。桥层0→1→0→1→0，进出时点{corner['bridge_layers']}。
车兵对向移动及出口占位组合中，主车绕行{len(corner['exit_detour_frames'])}帧，其他车兵都完成目标且生命保持。该新场景没有宣称取得主车对移动步兵的新关系查询证明；近距离移动步兵关系查询由两部分的南北桥实景另验。
cm严格逐模拟帧一致，当前两模式各自完整轨迹亦等于改代码前各自轨迹。它证明新的合法坡型8主车接桥往返，不等于已修复或定位历史c8地图的直接接桥失败；旧地图、控制与异常全部保留。旧现象只在影响具体功能时再查，避免反复追同一未知内部边界。

水岸占用及两轮运输
cw使用原图真实水面/沙滩/陆地，terrain pack不变；把一辆交通车正常放在[138,101]占用原卸载点。两轮装/卸分别为{[(x['board_frame'],x['drop_frame']) for x in water['cycles']]}帧，货车两轮在船上时持续保持装载标记；水面带货分别{[x['water_frames'] for x in water['cycles']]}帧。
首次1404帧原落点仍被车占用，货车改在合法陆格[139,102]卸下，无需等占位车离开。1500帧第一条让路命令未产生位置移动，2250帧换目标后2261帧才实际移动；不能把命令时点当作已释放。第二轮3004帧原落点已空，货车在[138,101]卸下，随后到[139,104]。船300、货车/交通车200、舰船600、步兵125生命全程保持。
ca的SHAD与E2两轮装/卸为{[(x['board_frame'],x['drop_frame']) for x in air['original']['cycles']]}帧，两轮带人经过真实水面后返岸落地卸载，最后E2到[140,104]。原版/C两轮实际落格相同，飞行过水时点/瞬时高度等差异单列保留；舰船、地面步兵及传送步兵的多条交通命令也完成，生命保持。
运输地图只改变正常初始单位位置或命令；没有运行时写载员列表、卸载格、Z、修复/破桥或路径指针。

其他移动器与对象语义
无机场oc中，原版/C的ORCA均在305帧移除，记录中此前生命已为0，800帧后续命令因对象不存在被输入检查拒绝；输入与完整轨迹保留，未计作成功飞行流程，也不称为C独有崩溃。
再以正常GAAIRC及GAPOWR建筑作一次条件对照of，不覆盖原规则。飞机150和机场600生命保持，普通Move请求触发四段飞行；原版/C高于50的飞行区间分别{plane['original']['airborne_groups']}/{plane['generated-c']['airborne_groups']}，最高1500。最终双方均在[34944,26240,0]、Guard5返场停靠；舰船到[130,94]、步兵到[140,100]。
请求过的水面格未冒称已到达；该场验证的是实际飞行、返场和机场使用效果。飞机出现的任务7按进场/停靠解释，货车/步兵的任务7则用实际装载标记解释，不把相同编号当成同一种对象效果。飞机详细移动器字段未加入生产schema，规则GUID和真实位置/状态观测分开记录；两次短身份确认窗口不计正式配对。

随机分流与有限验收
cw、ca、of改代码前已有随机快照和瞬时数值/时点/子格差异，严格comparison.json的false保留。当前每种模式分别与其改代码前完整轨迹逐条相同，再核对两轮载员保持、合法落格、生命、目标、飞行与返场效果，三场局部功能验收通过。
未增加随机调用钩子、改种子、重置/追平随机流或放宽通用比较器。旧1029与349帧分析按哈希继承，不当作本轮新探针或新配对；当前差异帧范围见rng-functional-impact.json。不推及后续战斗随机分配或全游戏等价，也不为无功能影响的数值差异无限追帧。
两部分各默认301帧、南北桥各501帧，每部分3配对1303帧并保存源码/工具/程序回退；最终生产{matrix['production_scenes']}配对{matrix['production_frames']}帧、事件/只读宿主{matrix['observer_scenes']}配对{matrix['observer_frames']}帧，含两部分共{pairs}配对{frames}帧，12严格、3局部功能通过。固定seed12345、最多两条配对通道/四个游戏进程，构建串行。
列车碰撞、碾压、重复失败及原版弯曲高差Z436停滞/Z-193未完成已有限回归，负对照继承旧证据，单位环只用于旧失败诊断。原版异常原位保留，不转化为永久逐BUG要求。
29非主C候选与86原始入边按哈希继承，当前312项内容扫描无新直接C调用，生成标签/分发表保留，无新自然入口结论。

保留、清理与接续
父批402项封存、本轮315项基线、两部分及初版出口回退、改动前宿主、全部控制/未合格试验/原版异常保留。H盘20项输入、原规则、原版EXE、SAVE0029、旧手写引擎、Git配置/远端引用不变。
清理{clean['deleted_files']}个逐路径/类型/哈希核对的可重建文件或缓存，共{clean['deleted_bytes']}字节；同目录{clean['protected_files']}项非候选哈希不变。源文件、正式程序、资源、轨迹和回退保留。
剩余：未覆盖状态/服务、更多真实运输/移动器组合、其他引擎子系统；旧地图接桥原因未定位，但新的合法坡型8往返已验证，不把旧边界当成必须继续逐BUG追踪项。本批游戏逻辑/状态验证不等同完整图像或全游戏验收。
复核：{R/'verify_final_movement_v51.py'}。本地提交不推送，收据：{S/'postcommit/git-local-commit.json'}。
'''
assert not report.exists() and not handoff.exists();report.write_text(text,encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式50 / 验证51，2026-10-24。
父提交：{read(S/'vcs-context.json')['parent_commit']}。
政策：{policy}
报告：{report}
程序SHA-256：{digest}
整理ground_template_transition与ground_tube_state两阶段服务边界，181C/312输入/37保护，未新增生产文件或改CMake；生成入口/runtime/记录器/比较器/随机/规则/美术不变。
正式98304原生用例（模板65536、出口32768，复验不重复计数），两部分各3配对1303帧；共{pairs}配对{frames}帧，12严格、3局部功能通过。运输128/Capture64按哈希继承。初版出口在parts/exit-before-context保留，最终按入口context一次绑定复验。
坡型8独立模块cm保留已验桥入口，原版/C严格逐帧相同，完成级4/5/6、主车桥道往返、车兵交通及绕行。历史地图cf低处重新出发也受阻，cs高低路点可达但桥目标仍受阻；原因未定位，仅有界记录，不再默认继续追旧地图内部边界。
cw真实水岸两轮装/卸201/1404、1955/3004；首卸原点被占改选[139,102]，占位车1500命令未动、2250换目标后2261实际移动，第二卸[138,101]；ca两轮77/2004、2353/3504后乘员继续移动。生命/目标保持。
无机场ORCA于305帧移除，后续命令无对象的试验保留排除；正常GAAIRC/GAPOWR条件of完成四段飞行和返场停靠，生命/结果一致，不冒称已到达请求水格。飞机任务7与货车/步兵装载语义分开。
三功能场景已有随机、时点/瞬时高度/子格差异，严格false保留，当前各模式等于改动前完整轨迹；不改随机数、不追平旧BUG、不推及全游戏。
基线：{S/'baseline'}；回退：{S/'parts'}；基线宿主：{S/'baseline-observer'}；封存：{S/'final-source'}。
后续剩余状态/服务、更多运输/移动器及其他子系统，维持整体功能与效果一致的有限验收。
复核：{R/'verify_final_movement_v51.py'}。本地提交不推送。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第五十批正式50 / 验证51已验收。\n交接：{handoff}\n政策：{policy}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-24）：原版1.006 C17/x86单位移动第五十批已验收。模板/共享出口服务、坡型8独立接桥往返、水岸两轮装卸及正常机场飞行；[第五十批交接](交接文档-单位移动第五十批正式验收-20261024.txt)。继续遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第五十批（2026-10-24）\n整理模板/共享出口服务，181C/312输入/37保护，{pairs}配对{frames}帧、98304正式原生例。\n坡型8独立模块接桥往返严格一致；三运输/机场场景按冻结基线与功能效果通过，保留严格false及随机差异。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=50,verification_round=51,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer);x['current_batch']=dict(formal_generation=50,verification_round=51,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=98304,production_c_sources=181,content_inputs=312,strict_all_frames_equal=strict,accepted_baseline_variations=variations,strict_game_pairs=12,functional_game_pairs=3);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,natural_alias_dispatch_required=False,percentage_reestimated=False,new_corner8_bridge_roundtrip_verified=True,old_corner8_map_internal_cause_proved=False,old_corner_followup_only_for_functional_need=True,remaining=['Uncovered generated state/service entries','More natural transport and locomotor combinations','Other engine subsystem integration']))
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v51*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.glob('*fixtures*.json'))
paths.update((S/n).relative_to(R).as_posix() for n in ['bridge-catalog-build-arguments.json','mission-table-proof.json','transport-native-validation-current.json','native-gates.json','service-boundaries.json','rng-functional-impact.json','excluded-explorations.json','rules-and-locomotors.json','context-refinement.json','corner-boundary-findings.json','aircraft-pilot-fixture.json','airfield-pilot-fixture.json'])
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
print(dict(passed=True,generation=50,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames))
