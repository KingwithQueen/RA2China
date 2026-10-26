"""Combat first batch, formal68/verification69: bounded delivery and continuation."""
from combat_batch_v69 import *
roll=read(S/'evidence-rollup.json');clean=read(S/'cleanup.json');source=read(S/'source-preservation.json')
assert all(d['passed'] for d in [roll,clean,source])
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe');assert receipt['executable_sha256']==digest==read(S/'parts/health/validation.json')['exe_sha256']
parent=read(S/'vcs-context.json')['parent_commit'];policy=P/'docs/项目目标与验收边界-20261024.txt'
report=P/'docs/战斗与对象生命周期第一批-伤害接纳与生命结算-20261026.txt'
handoff=P/'交接文档-战斗与对象生命周期第一批正式验收-20261026.txt'
progress=P/'docs/当前进度与剩余内容-20261026-战斗第一批.txt'
summary=f"{roll['accepted_pairs']}配对、{roll['accepted_frames']}帧，{roll['strict_pairs']}严格通过，{roll['functional_pairs']}维修既有差异按功能接受；原版片段131072例，重复运行不累计。"
for p in [report,handoff,progress]:assert not p.exists(),p
report.write_text(f'''战斗与对象生命周期第一批：伤害接纳与生命结算，2026-10-26
全项目正式68 / 验证69，父提交：{parent}
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收沿用整体功能、规则解读和效果一致；保留基线、回退与原版异常，不追求逐个BUG复刻。此前移动域收口按movement-state-v68继承，本批转入实际战斗功能。

实际修改
combat_health以命名状态和服务表达受伤接纳、免疫、有效伤害交付、治疗封顶、致命伤害钳制、半血和规则比例状态分级。combat_health_bridge只承担1.006对象布局、实时查询/回调、参数、寄存器、标志和原段衔接。
005D3D20是共享基础受伤入口；提升器的WaveClass__virtual_86名字来自共享虚表，不能据此认为只有Wave会调用。仅在入口插入桥接，并在原005D3E68续接指令前增加标签；原来的全部语句、内部标签和死亡尾段原字节保留，无内部独立函数入口被删除。
0047E1C0弹头/装甲/距离换算仍调用原实现；死亡、特殊步兵、通知和事件尾段仍为原提升实现。本批没有宣称整个战斗系统或死亡服务已可读重写。
实际184C、133头、317编译输入；仅一个既有生成块加入9行，新增2C/2头，CMake追加严格C17编译项。23117个生成入口、37个全局保护调用点保持，移动源、记录器、严格比较器和原版规则不改。

原版片段验证
执行锁定的1.006机器码受伤前段，与新可读服务及实际适配器对照，共131072例：68458提前返回、62614进入正伤害尾段；状态1/2/3分别36616/3993/22005，治疗刷新16001次。
覆盖零生命/零伤害、免疫/忽略防御、负治疗封顶、致死钳制、半血/比例严格边界；回调改写生命/伤害/类型/控制字、距离在第三次GetType前捕获、24/53/64位精度和四种舍入。验证状态、调用顺序、栈、续接活跃寄存器和标志；合法规则比例为有限数，不声称复制无效规则或无用x87状态字/死栈字节。
片段探针将装甲换算替换为有记录的确定服务，以隔离生命结算；下面自然场景使用真正原装甲换算。两类证据分开，不把模拟换算称为真实伤害公式对照。

自然场景和效果
五个相同地形、固定seed=12345、0..1500帧的普通命令场景，逐个在接入前后与原版运行。独立命令适配器只将Attack/Enter目标写入原MEGAMISSION事件，不直接改生命、伤害、路径或预算；初始受伤值来自原地图单位生命比例。
1. MTNK对TRUCKA，5次基础伤害入口，200生命最终死亡移除，原版/当前C严格一致。
2. MTNK对E2，8次基础伤害入口，125生命最终死亡移除，严格一致。
3. 工程师Enter FV后维修友方MTNK，Mechanical -50三次，150回到300。
4. 同一维修配方仅初始地图比例128改200，234到284后第二次-50封顶300，真实过量治疗得到覆盖。
5. 显式Immune=yes的TRUCKA规则控制，25次攻击，生命始终200，原版/当前C严格一致。该规则控制单列，不冒充原版默认免疫单位。
两组维修在未接入的父C中就有RNG从260帧开始、对象编号计数差异；维修完成回Guard分别晚2帧和1帧，其余记录的生命、位置、朝向和对象状态相同。编号差异原因未完全证明，也没有对粒子/完整视觉作等价承诺。原始严格比较保持失败；改前已冻结有限效果边界，当前C的每一路完整记录与改前C原字节相同，差异没有扩大。
五场共十路完整记录前后相同；有/无健康观测器的坦克场景四路全部生产记录相同。基线初始只去掉RNG的视图仍有编号/任务差异，该未通过视图原地保留；最终按原始完整记录和明确效果验收，没有放宽严格比较器。

受影响回归与证据
{summary}
默认遭遇战301帧、南北桥通行各501帧、列车/碾压各501帧、Stop后新Move1801帧严格通过，十二路完整回归记录也与移动域收口父证据相同。既往交通、异常、全局保护和非主入口证据按原范围继承，不重复计入本批。
新探针最初因记录返回后标志时占用了已返回的调用栈参数而失败；先切回宿主栈后取标志修正，初始探针与复核保留。首次主程序编译因续接指令原来没有单独标签而失败，增加标签后成功；未封存失败候选。命令宿主重复生成的LF/CRLF校验问题只修正工具比较，源和完整轨迹仍单独绑定。
原H盘20项、D盘原game.exe/固定存档、旧手写x64引擎、正式记录器/比较器/跟踪器及父档426项均核对。社区固定寻路线索及哈希按原审查继承，本批生命结算直接以本机1.006机器码为依据，未将旧引擎的寻路实现外推为伤害公式。

保留、清理和接续
基线：{S/'baseline'}（317项，接入前313编译输入及构建绑定等）；改前观测/命令宿主分别在baseline-observer、baseline-command。
有效回退：{S/'parts/health'}（当前317编译输入、CMake、EXE及构建收据）；最终封存：{S/'final-source'}。
清理{clean['deleted_files']}项、{clean['deleted_bytes']}字节可再生成对象和缓存；清理前后受保护文件不变。原版、有效EXE、基线、回退、轨迹、异常及诊断不删除。
下一批优先整理0047E1C0有效伤害换算及其距离/装甲边界，再推进005D3E68后的死亡、特殊步兵和事件/通知服务；每项先补有限原版/自然对照，不重开已解释的移动边界。战斗全域、投射物/武器、完整对象生命周期及整机体验仍未验收完成。
本地提交但不推送；提交收据：{S/'postcommit/git-local-commit.json'}
复核：{R/'verify_combat_v69.py'}
交接：{handoff}
进度：{progress}
''',encoding='utf-8',newline='\n')
progress.write_text(f'''当前进度与剩余内容，2026-10-26（正式68 / 验证69，战斗第一批）
当前C17/x86主线184C、133头、317编译输入；23117个提升入口，37个全局保护调用点。计数不是功能完成率，旧手写x64阶段不混入主线。
已验收：移动域可达性/占位/停止与有限公平性按正式67收口；本批新增共享受伤入口的免疫接纳、生命结算、治疗封顶、致死钳制和生命状态分级可读服务。
{summary}
五种自然攻击/维修/免疫控制、十路完整前后轨迹和受影响移动回归闭环。保留两组维修既有RNG/编号与1-2帧完成差异，不要求逐BUG复制。
紧邻剩余：有效伤害的弹头/装甲/距离计算；死亡、特殊步兵和通知事件；武器投射物、对象生命周期。
后续系统剩余：建造/经济/科技、AI、战役触发和任务目标的逐步可读化/验收；普通用户交互、保存载入、长期游戏、视听和资源调用整体体验。其它移动器的完整可读重写随实际功能需要推进，37点按可达风险处理；当前不宣称整机等价或虚构整体百分比。
下一父证据：{S}；移动域既有证据仍为{O}。
报告：{report}
交接：{handoff}
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''正式68 / 验证69，战斗与对象生命周期第一批，2026-10-26
父提交：{parent}
程序SHA-256：{digest}
已完成：共享受伤接纳与生命结算服务；保留0047E1C0装甲/弹头/距离计算和005D3E68后的原死亡/通知尾段。
{summary}
184C/317输入/37保护点；五个自然场景及十路前后完整轨迹相同，两个维修的既有内部计数和1-2帧完成差异原地保留。默认、桥面、列车碾压和Stop回归严格通过且与父记录相同。
边界依然是整体功能、规则与效果一致；不追求逐个BUG复刻，也不将本批称为全战斗或死亡域完成。
基线：{S/'baseline'}
有效回退：{S/'parts/health'}
最终封存：{S/'final-source'}
报告：{report}
进度：{progress}
复核：{R/'verify_combat_v69.py'}
本地提交收据：{S/'postcommit/git-local-commit.json'}
清理{clean['deleted_files']}项可再生成对象和缓存，原版/基线/回退/异常保留，不推送。
继续时使用combat-state-v1为父证据，先推进0047E1C0有效伤害换算的有限原版/自然对照，再整理死亡/事件尾段。此前movement-state-v68已经收口的移动范围仅因明确回归或实际需求重开。
''',encoding='utf-8',newline='\n')
reading=R/'ra2/src/gameplay/阅读说明-战斗.txt';assert not reading.exists();reading.write_text(f'''战斗第一批（正式68 / 验证69，2026-10-26）
combat_health是共享受伤入口的命名生命结算服务，combat_health_bridge处理1.006布局与005D3E68续接。
0047E1C0有效伤害计算和死亡/特殊步兵/通知事件仍保留原提升实现。有限规则/自然效果边界见报告。
{summary}
报告：{report}
交接：{handoff}
''',encoding='utf-8',newline='\n')
roots=['README.md','交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']+['reports/'+n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']]
for n in roots:assert git('show','HEAD:'+n)==(P/n).read_bytes()==(S/'baseline-project'/n).read_bytes(),n
lead=f'最新接续：正式68 / 验证69，战斗第一批生命结算已验收；移动域正式67收口范围继承。\n交接：{handoff}\n程序：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for n in roots[1:3]:p=P/n;p.write_bytes(lead+p.read_bytes())
p=P/roots[0];lines=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if lines[0].endswith(b'\r\n') else b'\n';p.write_bytes('> 当前研究路线（2026-10-26）：原版1.006 C17/x86第六十八批（战斗第一批）生命结算已验收；移动域收口范围继承。[交接](交接文档-战斗与对象生命周期第一批正式验收-20261026.txt)、[进度](docs/当前进度与剩余内容-20261026-战斗第一批.txt)。以下旧手写引擎阶段不计入本主线完成度。'.encode('utf-8')+eol+b''.join(lines[1:]))
pointer=dict(passed=True,status='promoted',domain='combat-health',formal_baseline_generation=68,verification_round=69,combat_batch=1,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),report=str(report),handoff=str(handoff),progress_report=str(progress),full_original_equivalence_verified=False,scoped_movement_acceptance_closed=True,all_locomotors_readably_rewritten=False,complete_combat_rewrite=False,acceptance_policy=str(policy),movement_parent_evidence=str(O))
batch=dict(formal_generation=68,verification_round=69,combat_batch=1,accepted_game_pairs=roll['accepted_pairs'],accepted_frames=roll['accepted_frames'],strict_game_pairs=roll['strict_pairs'],functional_game_pairs=roll['functional_pairs'],native_cases=131072,native_programs=1,native_fragments=1,production_c_sources=184,content_inputs=317,unsupported_guards=37,whole_game_acceptance=False,strict_all_frames_equal=False,complete_combat_rewrite=False)
for n in roots[3:]:
    p=P/n;x=read(p);x['previous_accepted_batch']=x.get('current_batch');x.update(pointer);x['current_batch']=batch;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,next='0047E1C0 effective damage: warhead/armor/distance',subsequent=['Death, special infantry and notification/events tail','Weapons/projectiles and complete object lifecycle','Production, economy, AI, campaigns and whole user experience'],movement_scope_closed_inherited=True,complete_combat_rewrite=False,full_original_equivalence_verified=False,bug_for_bug_required=False))
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']};paths|={'ra2/CMakeLists.txt','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-战斗.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py'}
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v69*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.exe','.json'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());manifest=[]
for rel in sorted(paths):
    p=S/'final-source'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,p);manifest.append(dict(path=rel,sha256=sha(p)))
write(S/'source-manifest.json',manifest)
documents=[]
for p in [P/n for n in roots]+[report,handoff,progress,policy,P/'docs/寻路机制改进验收补充-20261025.txt']:
    q=S/'current-project'/p.relative_to(P);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(q)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(pointer|batch,parent_commit=parent,state_schema=12,source_files=len(manifest),rollback_parts=['health'],protected_baseline_and_originals=True,cleanup_performed=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,exe_sha256=digest,source_files=len(manifest),pairs=roll['accepted_pairs'],frames=roll['accepted_frames']))
