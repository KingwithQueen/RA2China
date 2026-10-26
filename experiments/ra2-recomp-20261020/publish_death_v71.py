"""Formal70 / verification71: bounded lifecycle delivery and storage continuation."""
from combat_batch_v71 import *
roll=read(S/'evidence-rollup.json');clean=read(S/'cleanup.json');disk=read(S/'storage-review.json');assert roll['passed'] and clean['passed'] and disk['passed']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe');assert digest==receipt['executable_sha256']==read(S/'parts/death/validation.json')['exe_sha256']
parent=read(S/'vcs-context.json')['parent_commit'];policy=P/'docs/项目目标与验收边界-20261024.txt'
report=P/'docs/战斗与对象生命周期第三批-死亡特殊步兵与通知事件-20261026.txt';handoff=P/'交接文档-战斗与对象生命周期第三批正式验收-20261026.txt';progress=P/'docs/当前进度与剩余内容-20261026-战斗第三批.txt';storage=P/'docs/存储占用核查与无损整理-20261026.txt'
summary=f"{roll['accepted_pairs']}配对、{roll['accepted_frames']}帧，{roll['strict_pairs']}全记录严格通过，{roll['functional_pairs']}组保留既有维修/1HP差异按功能验收；131072原版尾段用例，重复运行不累计。"
for p in [report,handoff,progress]:assert not p.exists(),p
report.write_text(f'''战斗与对象生命周期第三批：死亡、特殊步兵与通知事件，2026-10-26
全项目正式70 / 验证71；父提交：{parent}
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
边界仍为整体功能、规则和效果一致，不追求逐个BUG复刻；以原版1.006为准，保留基线、回退和原版异常。

先完成的存储整理
历史封存的大头是独立EXE与生成源码；目录约7TiB的逻辑累加另包含大量硬链接，不能当作真实占用。25,731个单链接证据文件采用NTFS透明压缩，逐项压缩前后SHA-256相同、路径保持，释放{disk['saved_bytes']/2**30:.2f} GiB；D盘从约179GiB提高到约384GiB。没有删除历史基线、有效回退、原版异常、轨迹或录像。
压缩后的封存EXE完成原版/当前C的31帧严格对照，新私有存档继承压缩并保持单独链接；旧正式69/验证70复核通过后才开始本批开发。evidence根目录的新文件继承压缩，降低后续增长；活动源码与构建目录原布局保留。当前有明显余量，不急于另备磁盘。详见：{storage}

实际代码
combat_death提供共享受伤尾段的命名控制：特殊步兵恢复条件、实时存活/生命/标签读取、首伤与生命状态通知、攻击来源载荷、零生命处理、移除及末尾通知；combat_death_bridge只处理1.006布局、回调/分配/效果构造、栈和寄存器/控制字适配。
仅在005D3E68插入桥接返回。该751字节原尾段全部语句、标签及原5D3D20入口仍保留；生命接纳和装甲/弹头/距离数值服务、移动与共享数值层不改。188C、137头、325编译输入；新增2C/2头，一个既有生成块增加7行，CMake追加C17 /W4 /WX编译项；23117生成入口、37全局保护点保持。
特殊路径依次检查非正生命、Infantry类别、忽略防御、类型Cyborg位和当前0x5C3姿态位；效果分配失败仍按原路径继续恢复。恢复量为类型Strength乘本机常量0.25，经原转换控制舍入且至少1；先写姿态、调用状态动作6，再发布伤害状态3。
0x5C3不能缓存为“一生是否恢复过”。观测器历史字段special_applied仅表示当时该原始位；本批服务明确命名SPECIAL_POSTURE。控制场景会因姿态复位反复恢复，密集来火维持该位时则直接进入死亡，不能擅自加永久一次性限制。
通知后逐次读取对象/标签状态，攻击者在原时点捕获；保留0x26/0x27/0x28/0x29/0x2A/0x2B/6/0x2C事件与有/无来源载荷的区别。对象在前段失效或正生命被回调改成非正生命时返回5；正常零生命先通知来源、写状态4、再调用移除接口。死亡状态4分别抑制后面的6和0x2C，末尾活动对象且标志允许时调用0x11C(2)。晚期取消仍按原收尾状态返回，不与返回5混为一类。

原版片段与ABI
直接执行锁定1.006的005D3E68尾段和真实0077F110转换，对照新服务及实际适配器131072例。引擎类回调、分配和通知用可记录替身隔离，覆盖当前生命/姿态/类型/来源/标签/忽略防御组合、分配失败、GetType为空、回调取消对象或改写生命/标签/来源、转换控制变化。
结果：特殊恢复8739次、移除回调20048次、触发通知279778次；返回0..5分别17310/17313/16963/24451/39230/15805。核对对象/类型状态、调用参数及顺序、栈平衡、非易失寄存器、返回和算术标志/控制字。该片段证据不等于所有真实回调实现或整机验收。
首版探针把硬件CW当作翻译模式的记录来源，修正为模拟器CW；数值/最终CW当时已相同。随后原版例25抓到初稿漏掉0x2C的状态4抑制，在主程序接入前补齐。初稿、原始失败及复核保留，未封存无效候选。

自然场景
固定seed=12345、模拟帧0..900，普通Attack命令和原地图触发标签/NoAction动作，无直接生命、伤害、路径或预算注入。
1. 附标签TRUCKA受MTNK攻击，五次受伤后移除；首伤、状态变化、命中及来源通知真实发出。
2. 附标签E2，八次受伤后死亡；捕获全部八类尾段事件和来源载荷。
3. 同一E2显式Cyborg=yes规则控制，原版和改前C在475/598/719/840帧恢复31生命；姿态复位后会重复恢复，900帧仍存活。这是该非默认规则控制的实际边界，未改成另一种恢复机制。
4. 同图未挂标签控制，生命/死亡流程正常，不发出目标的Tag事件。
5. 三辆MTNK持续来火，特殊E2在致死前已保持姿态位，299帧返回4，随后移除；与单车低频控制共同限定恢复与死亡条件。
五场十路完整记录接入前后逐字节相同，原版与当前C也全部严格相同。独立观测器与只带普通命令适配的宿主四路全部生产记录相同；原始严格比较器未放宽。原版观测用保存/恢复寄存器、标志和FPU的返回跳板，C端只重命名独立构建中一个函数定义再包返回观察，实际生产记录器、分发和资源不改。
首版地图把Trigger所属国家误写为House实例名BadGuy1 House，两端均在6ED7AD读00000135异常；无观测的命令宿主也复现。只将该字段改为国家BadGuy1后全场通过。无效地图、日志和失败原样保留并排除，不能把它们冒充有效自然场景或原版默认规则缺陷。
独立观测器首编译的名称冲突和naked前置声明问题只修正工具，保留原稿和失败；继承的旧install_hook类型警告不影响新产品C17严格编译。

回归、封存与接续
{summary}
八个父场景含车辆/步兵死亡、维修、治疗封顶、免疫、步枪重甲、默认V3波及和比例1控制；十六路生产记录保持父证据。既有维修RNG/编号/1-2帧完成差异和原比例控制1HP差异保留。默认遭遇战、南北桥、列车、碾压、Stop后新Move六个回归严格通过，十二路记录保持父证据。旧交通与非主入口按原范围继承，不重复加总。
原H盘20项、D盘1.006镜像/固定存档、旧手写x64程序、记录器/比较器/跟踪器及父封存392项均核对。社区固定源码线索按既有审查和哈希继承，本批直接以本机1.006控制流为据。
基线：{S/'baseline'}（325项）；有效回退：{S/'parts/death'}（328项）；观测/命令基线：baseline-observer、baseline-command；最终封存：{S/'final-source'}。
当批再清理{clean['deleted_files']}项、{clean['deleted_bytes']}字节可再生成中间对象和缓存，受保护文件清理前后不变。保留全部原版、基线、回退、异常、失败输入与原始轨迹。本地提交，不推送。
本批完成共享受伤尾段，尚不等于所有派生死亡处理、残骸/爆炸/载员/连锁及完整对象生命周期已经可读重写。下一批继续派生Unit/Infantry死亡衔接及对象移除生命周期，按实际风险补有限场景；完整触发器执行器、武器/投射物、建造经济AI战役和普通用户体验仍需后续验收。
交接：{handoff}
进度：{progress}
复核：{R/'verify_death_v71.py'}
提交收据：{S/'postcommit/git-local-commit.json'}
''',encoding='utf-8',newline='\n')
progress.write_text(f'''当前进度与剩余内容，2026-10-26（正式70 / 验证71，战斗第三批）
C17/x86主线188C、137头、325编译输入；23117提升入口，37全局保护点。计数不是功能完成率，旧手写x64不计入主线。
已验收：移动域有限范围收口、共享生命接纳/治疗结算、装甲弹头距离换算、本批共享受伤尾段的特殊步兵恢复/死亡与通知服务。
{summary}
五种新场景十路完整前后记录相同；八种父战斗及六种生产回归保持。Cyborg控制中姿态复位导致的重复恢复与密集来火死亡均保留原版边界。
存储已无损释放约{disk['saved_bytes']/2**30:.0f}GiB，D盘整理后约384GiB余量，新证据继承压缩；历史资料未删。报告：{storage}
下一项：Unit/Infantry派生死亡衔接、对象移除和生命周期；继续残骸/爆炸/载员/连锁及触发器执行器的有限可读化和验收。其余完整武器投射物、建造经济科技、AI、战役目标、普通交互、保存载入、长期游戏和视听资源体验尚未全量验收。
移动器其余可读化和全局保护点按实际风险推进，不宣称全部完成或虚构总体百分比。
下一父证据：{S}
交接：{handoff}
报告：{report}
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''正式70 / 验证71，战斗与对象生命周期第三批，2026-10-26
父提交：{parent}
程序SHA-256：{digest}
完成005D3E68共享受伤尾段：特殊步兵恢复、姿态边界、实时取消检查、返回5/正常死亡4及通知事件衔接。保留原语句、派生虚调用和已有生命/伤害服务。
{summary}
五场十路前后完整记录相同，单车Cyborg重复恢复及三车密集来火死亡均与原版一致。188C/325输入/37保护。
存储先无损整理25,731个独立文件并逐项验哈希，释放{disk['saved_bytes']/2**30:.2f}GiB，余量从179提高到约384GiB；基线、回退、原版异常和录像均保留。新证据默认压缩。
当批另清理{clean['deleted_files']}项中间文件。本地提交，不推送。
基线：{S/'baseline'}
有效回退：{S/'parts/death'}
最终封存：{S/'final-source'}
报告：{report}
进度：{progress}
存储报告：{storage}
复核：{R/'verify_death_v71.py'}
提交收据：{S/'postcommit/git-local-commit.json'}
下批以combat-state-v3为父，推进派生Unit/Infantry死亡衔接和对象移除生命周期；保留不逐BUG复刻的整体功能/效果边界，不重开已解释的相同移动范围。
''',encoding='utf-8',newline='\n')
reading=R/'ra2/src/gameplay/阅读说明-战斗.txt';reading.write_bytes(f'战斗第三批（正式70 / 验证71，2026-10-26）\ncombat_death与bridge处理共享死亡、特殊姿态和通知尾段；0x5C3不是一生只恢复一次的标记。\n{summary}\n报告：{report}\n交接：{handoff}\n\n'.encode('utf-8')+reading.read_bytes())
roots=['README.md','交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']+['reports/'+n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']]
for n in roots:assert git('show','HEAD:'+n)==(P/n).read_bytes()==(S/'baseline-project'/n).read_bytes(),n
lead=f'最新接续：正式70 / 验证71，战斗第三批死亡、特殊步兵与通知尾段已验收；存储无损整理释放约205GiB。\n交接：{handoff}\n程序：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for n in roots[1:3]:p=P/n;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';lines=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if lines[0].endswith(b'\r\n') else b'\n';p.write_bytes('> 当前研究路线（2026-10-26）：原版1.006 C17/x86第七十批（战斗第三批）死亡、特殊步兵与通知服务已验收；存储无损整理释放约205GiB。[交接](交接文档-战斗与对象生命周期第三批正式验收-20261026.txt)、[进度](docs/当前进度与剩余内容-20261026-战斗第三批.txt)。以下旧手写引擎阶段不计入本主线完成度。'.encode('utf-8')+eol+b''.join(lines[1:]))
pointer=dict(passed=True,status='promoted',domain='combat-death',formal_baseline_generation=70,verification_round=71,combat_batch=3,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),report=str(report),handoff=str(handoff),progress_report=str(progress),storage_report=str(storage),full_original_equivalence_verified=False,scoped_movement_acceptance_closed=True,complete_combat_rewrite=False,all_locomotors_readably_rewritten=False,acceptance_policy=str(policy),combat_parent_evidence=str(O))
batch=dict(formal_generation=70,verification_round=71,combat_batch=3,accepted_game_pairs=roll['accepted_pairs'],accepted_frames=roll['accepted_frames'],strict_game_pairs=roll['strict_pairs'],functional_game_pairs=roll['functional_pairs'],native_cases=131072,native_programs=1,native_fragments=1,production_c_sources=188,content_inputs=325,unsupported_guards=37,whole_game_acceptance=False,strict_all_frames_equal=False,complete_combat_rewrite=False,storage_saved_bytes=disk['saved_bytes'])
for n in roots[3:]:
    p=P/n;x=read(p);x['previous_accepted_batch']=x.get('current_batch');x.update(pointer);x['current_batch']=batch;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,next='Derived Unit/Infantry death handoff and object removal lifecycle',subsequent=['Debris, explosions, passengers, chained effects and event executor','Full weapons/projectiles, production, economy, AI, campaign and user experience'],posture_sensitive_special_control_preserved=True,whole_object_lifecycle_rewritten=False,movement_scope_closed_inherited=True,complete_combat_rewrite=False,full_original_equivalence_verified=False,bug_for_bug_required=False))
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']};paths|={'ra2/CMakeLists.txt','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-战斗.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py'}
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v71*') if p.is_file());paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.exe','.json'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());paths.add((S/'observer-build/death_generated.c').relative_to(R).as_posix());manifest=[]
for rel in sorted(paths):
    p=S/'final-source'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,p);manifest.append(dict(path=rel,sha256=sha(p)))
write(S/'source-manifest.json',manifest);documents=[]
for p in [P/n for n in roots]+[report,handoff,progress,storage,policy,P/'docs/寻路机制改进验收补充-20261025.txt']:
    q=S/'current-project'/p.relative_to(P);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(q)))
write(S/'document-manifest.json',documents);write(S/'validation.json',dict(pointer|batch,parent_commit=parent,state_schema=12,source_files=len(manifest),rollback_parts=['death'],protected_baseline_and_originals=True,cleanup_performed=True,pushed=False));write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,exe_sha256=digest,source_files=len(manifest),pairs=roll['accepted_pairs'],frames=roll['accepted_frames']))
