"""Publish formal71 / verification72 and a continuation-ready bounded lifecycle handoff."""
from combat_batch_v72 import *
roll=read(S/'evidence-rollup.json');clean=read(S/'cleanup.json');review=read(S/'baseline-review.json');assert roll['passed'] and clean['passed'] and review['passed']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe');assert receipt['executable_sha256']==digest==read(S/'parts/lifecycle/validation.json')['exe_sha256']
parent=read(S/'vcs-context.json')['parent_commit'];policy=P/'docs/项目目标与验收边界-20261024.txt'
report=P/'docs/战斗与对象生命周期第四批-派生死亡与对象移除-20261026.txt';handoff=P/'交接文档-战斗与对象生命周期第四批正式验收-20261026.txt';progress=P/'docs/当前进度与剩余内容-20261026-战斗第四批.txt'
summary=f"{roll['accepted_pairs']}配对、{roll['accepted_frames']}帧，{roll['strict_pairs']}组全记录严格通过；9组按已核对边界功能验收，含既有维修/比例1差异、两场攻击方1HP差及附带对象清理5帧差。七个原版片段229376例，加2730个不重复的初始死亡帧补充例，共232106例；不累计失败或重复运行。"
scenes='\n'.join(f"{i+1}. {x['tag']}：目标{x['targets']}，结束仍在对象表{x['remaining']}，最大待删队列{x['maximum_delete_queue']}，首次析构帧{x['first_death_frame']}；生命周期调用{x['lifecycle_counts']}。" for i,x in enumerate(review['fixtures']))
for p in [report,handoff,progress]:assert not p.exists(),p
report.write_text(f'''战斗与对象生命周期第四批：Unit/Infantry派生死亡衔接与对象移除，2026-10-26
全项目正式71 / 验证72；父提交：{parent}
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收继续以原版1.006为准，整体功能、规则与效果一致，不追求逐个BUG复刻。基线、有效回退、原版异常和失败输入保留。

实际服务与衔接
新增combat_lifecycle及桥接适配器，190个C、139个头、329个内容绑定编译输入；23117生成入口、37全局保护点不变。
Unit在父受伤结果后保留5的提前返回，非死亡状态进入原存活处理；死亡状态按DeathFrames条件判断是否初始化死亡帧与归属通知，并恢复1生命/活动位进入延迟表现，其余进入原死亡效果。
Infantry保留0和5的直接返回、非死亡分支；死亡时按原顺序通知击杀来源、清理占用与动作、先清任务再设死亡任务并提交，调用死亡通知后进入原表现分支。没有把派生死亡和共享生命结算混成一次删除。
Unit/Infantry在尾部按Sinkable调用原开始沉没接口，成功则延后移除；车辆另外保留当前延迟死亡标志。不能把“已死亡”统一解释成“立即释放内存”。
Foot解除关联和离队后调用对象层移除。对象层先处理成员0x38的挂接解除回调、解除引用、调用原Limbo，再标记失效并加入延迟删除队列。入队按原容量/动态分配/增长量条件处理；扩容失败仍保留原失效状态，不擅自强行析构。
延迟删除服务重新读取当前队列长度和数组，跳过尚不允许删除的项；删除当前对象的所有有效重复条目并按顺序搬移，再检查原类别/类型条件、按原要求临时恢复活动位并调用删除析构接口。析构可能新增队列项，循环继续使用最新数量；析构后不再读取已释放对象。
七个接入点：006FCA7E、004FFBD6、006FD17D、004FFF61、004CCE40、005D4E90、006ECF10。五个既有生成文件只增桥接块与包含；仅在各主入口函数内匹配接入点，其他重复提升的内部地址及别名函数原样保留，全部原始语句和标签保留；CMake只追加2C严格C17 /W4 /WX。生命/治疗、装甲弹头距离、共享死亡尾段、移动、共享数值层、生产记录器/比较器/跟踪器全部内容不变。

原版片段对照
直接执行锁定1.006的七个片段，各32768例、合计229376；生命周期控制使用实际C服务和适配器。类虚调用、团队/关联、向量扩容/查找、RTTI和析构用可记录替身隔离，不能将该门禁称为全部真实回调实现的验收。
核对返回/后继、对象与队列状态、重复项清除/搬移顺序、回调参数顺序、栈、非易失寄存器及正常收尾标志。主矩阵覆盖死亡状态0..5，另补2730个正DeathFrames且初始死亡帧未设置的Unit用例，消除state模6与标志模2的相关性漏检；与主矩阵的对象输入不同，不重复计数。覆盖死亡帧已初始化/未初始化、沉没低字节返回、关联回调改变团队、满队列/零容量/不可增长/扩容失败、未到删除时机、重复条目、查找失败/越界返回及析构新增待删对象。
首次探针把无this的cdecl typeid调用的ECX记作语义接收者，仅规范该诊断字段；一次工具改写重复CRLF被严格编译拒绝，换行规范后重建。随后原版drain例2抓到搬移源末项必须包含新count位置的边界错误，主接入前修正。失败探针、首版适配器和原始失败日志保留，未作为有效候选封存。

自然战斗
固定seed=12345，普通Attack命令、原地图触发标签/NoAction动作；不直接注入生命、伤害、路径、寿命或队列。新增四场：MTNK触发DeathFrames=8的美术控制、SREF触发DeathFrames=8/MaxDeathCounter=40的美术控制、E2 NotHuman=yes规则控制、四车攻击四辆卡车的队列控制；各0..1200帧。另重跑前批五场（0..900），含普通车辆/步兵、Cyborg重复恢复、无标签和密集来火。
{scenes}
初始DeathFrames规则控制虽严格通过，但没有触发延迟；按原0070AE04/10的ART.INI读取点，只在私有目录替换原美术配置的TRUCKA段，实际观察到移除前1生命阶段后才纳入；不能将这些输入解释为一定延迟8或40帧。初始无效控制原样保留并排除。NotHuman步兵在475帧致死、491帧析构，普通步兵476帧析构，实际覆盖了延后释放。另有默认SHK电击E2场景在改前C就存在RNG/附带对象时序差，目标析构同为211帧；保留其前后诊断，不计入已验收自然场景。
九场十八路完整记录在主接入前后分别保持。原版与C其中6场严格相同；MTNK美术控制及四车控制各仅攻击方一项生命相差1，SREF控制1201帧状态/RNG/其他记录完全相同，仅附带对象1023359入队与随后drain晚5帧。三场原始严格比较失败保留，使用明确字段/对象/帧界限的独立功能收据验收，不改严格比较器。只带普通命令的独立宿主与观测宿主四路生产记录完全一致；严格比较器不放宽。
观测只在隔离宿主中增加入口日志：原版对五个无相对转移的入口搬移完整指令，对两类析构通过已核对的虚表槽跳板观察后跳至原入口，保留寄存器/标志/FPU；C端沿用已有入口跟踪。上一批共享死亡结果观测仍用独立重命名生成块，美术控制的第二份私有副本同时规范了换行，TRUCKA段以外的配置文本保持；生产资源和记录器不修改。工具继承的旧install_hook指针类型警告保留，新产品与片段探针严格编译通过。

回归、存储与保留
{summary}
八种既有战斗十六路生产记录保持父证据，默认遭遇战、南北桥、列车、碾压、Stop后Move六个移动回归十二路保持父证据；前批原版Cyborg姿态复位后的重复恢复和密集来火死亡不改。父正式70封存413项、28项继承保护输入（含H盘20项、锁定原镜像/存档与旧手写x64）保持；另验证所读原ART.INI与锁定ra2.mix内字节一致并单独保护。
继承上一批evidence默认NTFS压缩，新增证据也按目录继承，避免重新快速增长；本轮没有删除历史数据。清理{clean['deleted_files']}项可再生成中间对象/缓存，共{clean['deleted_bytes']}字节，受保护文件清理前后相同。基线{S/'baseline'}为329项，有效回退{S/'parts/lifecycle'}为332项，最终封存{S/'final-source'}。失败稿和原版异常仍保留。本地提交，不推送。

剩余边界
本批完成派生受伤后的死亡衔接、对象失效入队与待删队列调度。原死亡表现、残骸爆炸、载员与连锁、沉没具体实现、各类析构内部和全局引用系统仍由原翻译代码执行，不能宣称完整对象生命周期或整个战斗域已全部可读重写。
下一批继续死亡表现、载员释放与连锁效果的有限服务提取，并按需核查电击战斗RNG及附带对象时序差；武器/投射物、建造经济科技、AI战役、普通交互、保存载入和长期游戏体验仍需后续。
交接：{handoff}
进度：{progress}
复核：{R/'verify_lifecycle_v72.py'}
提交收据：{S/'postcommit/git-local-commit.json'}
''',encoding='utf-8',newline='\n')
progress.write_text(f'''当前进度与剩余内容，2026-10-26（正式71 / 验证72，战斗第四批）
主线190C、139头、329编译输入；23117提升入口、37全局保护点。代码计数不是总体功能完成率，旧手写x64不计入主线。
移动域有限范围已收口；共享生命/治疗、装甲弹头距离、共享死亡尾段已验收。本批继续完成Unit/Infantry派生死亡衔接、Foot/Object失效入队及延迟删除调度。
{summary}
新增四个自然场景，前批五个生命周期场景、八个战斗场景与六个移动回归保持。入队与实际析构分开，原死亡衔接、沉没、Cyborg恢复及既有差异保留。电击战斗的改前RNG/附带清理差保留诊断，未计入自然等价验收。
下一项：死亡表现、载员释放及连锁效果；原残骸/爆炸、沉没和析构内部未全部可读化。完整触发器执行器、武器投射物、建造经济科技、AI、战役、用户交互、保存载入、长期游戏和视听体验仍未全量验收。
新增证据继承无损压缩，历史基线、回退、异常保留；不虚构总体完成百分比。
报告：{report}
交接：{handoff}
下一父证据：{S}
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''正式71 / 验证72，战斗与对象生命周期第四批，2026-10-26
父提交：{parent}
程序SHA-256：{digest}
完成Unit/Infantry派生死亡衔接、死亡尾部移除选择、Foot/Object失效入队和延迟删除队列调度；原效果与析构实现继续委托原代码。
{summary}
九场十八路分别保持改前记录，原始严格差异及限定功能收据保留；新增两种美术DeathFrames控制、规则NotHuman=yes与多目标队列四场。190C/329输入/37保护。
基线：{S/'baseline'}（329项）
有效回退：{S/'parts/lifecycle'}（332项）
最终封存：{S/'final-source'}
原版、H盘输入、旧手写引擎、父封存和异常不改。新证据继承压缩，清理{clean['deleted_files']}项可再生成中间文件；本地提交，不推送。
报告：{report}
进度：{progress}
复核：{R/'verify_lifecycle_v72.py'}
提交收据：{S/'postcommit/git-local-commit.json'}
下批以combat-state-v4为父，继续死亡表现、载员释放及连锁效果；维持整体功能/效果一致、不逐BUG复刻边界，不重开已解释的相同移动范围。
''',encoding='utf-8',newline='\n')
reading=R/'ra2/src/gameplay/阅读说明-战斗.txt';reading.write_bytes(f'战斗第四批（正式71 / 验证72，2026-10-26）\ncombat_lifecycle及bridge处理Unit/Infantry死亡衔接与延迟删除生命周期，原表现与析构实现仍委托。\n{summary}\n报告：{report}\n交接：{handoff}\n\n'.encode()+reading.read_bytes())
roots=['README.md','交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']+['reports/'+n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']]
for n in roots:assert git('show','HEAD:'+n)==(P/n).read_bytes()==(S/'baseline-project'/n).read_bytes(),n
lead=f'最新接续：正式71 / 验证72，战斗第四批派生死亡衔接与对象移除服务已验收。\n交接：{handoff}\n程序：{digest}\n以下历史原地保留。\n\n'.encode()
for n in roots[1:3]:p=P/n;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';lines=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if lines[0].endswith(b'\r\n') else b'\n';p.write_bytes('> 当前研究路线（2026-10-26）：原版1.006 C17/x86第七十一批（战斗第四批）派生死亡衔接与对象移除服务已验收。[交接](交接文档-战斗与对象生命周期第四批正式验收-20261026.txt)、[进度](docs/当前进度与剩余内容-20261026-战斗第四批.txt)。以下旧手写引擎阶段不计入本主线完成度。'.encode()+eol+b''.join(lines[1:]))
pointer=dict(passed=True,status='promoted',domain='combat-lifecycle',formal_baseline_generation=71,verification_round=72,combat_batch=4,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),report=str(report),handoff=str(handoff),progress_report=str(progress),full_original_equivalence_verified=False,scoped_movement_acceptance_closed=True,complete_combat_rewrite=False,all_locomotors_readably_rewritten=False,acceptance_policy=str(policy),combat_parent_evidence=str(O))
batch=dict(formal_generation=71,verification_round=72,combat_batch=4,accepted_game_pairs=roll['accepted_pairs'],accepted_frames=roll['accepted_frames'],strict_game_pairs=roll['strict_pairs'],functional_game_pairs=roll['functional_pairs'],native_cases=232106,native_programs=2,native_fragments=7,production_c_sources=190,content_inputs=329,unsupported_guards=37,whole_game_acceptance=False,strict_all_frames_equal=False,complete_combat_rewrite=False)
for n in roots[3:]:
    p=P/n;x=read(p);x['previous_accepted_batch']=x.get('current_batch');x.update(pointer);x['current_batch']=batch;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
write(S/'remaining-work.json',dict(passed=True,next='Death presentation, passenger release and chained effects',whole_object_lifecycle_rewritten=False,complete_combat_rewrite=False,full_original_equivalence_verified=False,bug_for_bug_required=False,derived_effects_and_destructors_still_delegated=True,known_diagnostic_gap='Pre-existing electric attack RNG/auxiliary cleanup divergence, preserved per mode and excluded from accepted natural equivalence',movement_scope_closed_inherited=True))
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']};paths|={'ra2/CMakeLists.txt','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-战斗.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py'}
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v72*') if p.is_file());paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.exe','.json'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());paths.add((S/'observer-build/death_generated.c').relative_to(R).as_posix());manifest=[]
for rel in sorted(paths):
    p=S/'final-source'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,p);manifest.append(dict(path=rel,sha256=sha(p)))
write(S/'source-manifest.json',manifest);documents=[]
for p in [P/n for n in roots]+[report,handoff,progress,policy,P/'docs/寻路机制改进验收补充-20261025.txt',P/'docs/存储占用核查与无损整理-20261026.txt']:
    q=S/'current-project'/p.relative_to(P);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(q)))
write(S/'document-manifest.json',documents);write(S/'validation.json',dict(pointer|batch,parent_commit=parent,state_schema=12,source_files=len(manifest),rollback_parts=['lifecycle'],protected_baseline_and_originals=True,cleanup_performed=True,pushed=False));write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,exe_sha256=digest,source_files=len(manifest),pairs=roll['accepted_pairs'],frames=roll['accepted_frames']))
