"""Promote finite bridge-plane, vehicle transport and actual slope acceptance."""
from run_batch_v48 import *
for name in ['native-gates.json','effects.json','preservation.json','alias-evidence-inheritance.json','cleanup.json','final-scene-matrix.json']:
 assert read(S/name)['passed'],name
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');effects=read(S/'effects.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['transition','approach']];assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results']);frames=sum(x['frames'] for x in parts)+matrix['production_frames']+matrix['observer_frames']
strict=all(x['strict_trace_equal'] for x in matrix['results']);variations=effects['accepted_baseline_variations']
report=P/'docs/单位移动第四十七批-高度转换与接近服务及毁桥运输和多向坡面-20261024.txt'
handoff=P/'交接文档-单位移动第四十七批正式验收-20261024.txt';policy=P/'docs/项目目标与验收边界-20261024.txt'
rep=effects['representative'];dc=rep['dc']['modes']['original'];rd=rep['rd']['modes']['original'];south=rep['ss']['modes']['original'];east=rep['es']['modes']['original']
text=f'''单位移动第四十七批（正式47 / 验证48），2026-10-24。
父提交：{read(S/'vcs-context.json')['parent_commit']}。第四十六批380项封存已逐项核对，本轮309项独立基线保留。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
政策：{policy}

实现与状态/服务边界
以整体功能、效果、规则和资源解读一致为目标，不追求逐个BUG复刻。只固定本批实现、代表效果和受影响的有限回归。
新增ground_transition_rules.h/.c，集中上/下层参考高度与同高、一级坡面、四级桥层的判断。32位加减回绕按原x86位模式解释，不依赖C有符号溢出。
ground_passage保留direction=-1特殊入口、空来路/去路返回、未知参考高度的初始化。参考高度已经写入后再遇阻挡时仍保留该写入；changing_layer只在原版允许的四级向下分支写1，不因普通失败清旧值。
同高保留桥标志和未知/相等参考判断；一级高差下行查去格坡面、上行查来格坡面；四级变化复用已核对的桥面高度匹配，保留桥与参考高度、0x300标志检查；其他高差阻挡。
ground_internal_next共用层参考计算，保留重置预算、方向8连接早退、首次目标构造、重新读位置、格与参考高度，以及第二次重新读位置/偏移/格/桥标志/上层状态再标记过渡的顺序。首次世界回调可改变owner和坐标，不能缓存给第二组查询。
179个生产C、308项编译内容输入、37个未实现保护；新增一C一头文件，仅另改ground_passage、ground_internal_next及CMake。生成入口、runtime适配、比较器、生产记录器/schema12、生产规则与美术资源不变。

验证
高度转换片段32768例、完整采样收尾/接近片段32768例，共65536个本轮原生用例；服务回调值与顺序、状态/局部量、返回与栈清理按探针已覆盖范围核对。运输构造器128例、Capture64例证明按源/程序哈希继承，不重复运行或计入65536。
转换与接近两部分各默认遭遇战301帧、南北桥上移动交会/占位出口各501帧，每部分3配对1303帧，分别封存源码/工具/程序回退。
最终生产程序{matrix['production_scenes']}配对{matrix['production_frames']}帧，普通事件/只读观察功能宿主{matrix['observer_scenes']}配对{matrix['observer_frames']}帧；连同分部共{pairs}配对、{frames}帧。清地运输一场有改代码前即存在的气垫数值/关系查询时点差异，单列功能验收；其余严格逐模拟帧相同。
选定四场动态场景同时要求当前原版/C分别与本轮改动前各自完整轨迹逐条相同。正式矩阵最多两条配对通道/四个真实游戏进程，构建串行，固定seed12345；随机数检查保持。

毁桥时的载车运输与不同卸载地形
两场都以普通Enter把TRUCKA装入LCRF，另一辆车正常驶上原版CellTag触发桥毁。桥标志逐模拟帧只读观察；被毁后一直保持断口。没有直接调用破桥、装卸、落位或路径结果函数。
清地场景：{dc['board_frame']}帧已装载，{dc['collapse_frame']}帧桥毁，触发车{dc['trap_removed_frame']}帧移除；此刻船还在起步转向，未发生水平位移，随后完成运输。{dc['drop_frame']}帧卸车，实际货车落格{dc['landing_cell']}、地形land={dc['landing_land']}；货车继续普通Move到{dc['cargo_final']}。
道路场景：{rd['board_frame']}帧已装载，{rd['collapse_frame']}帧桥毁，此刻登陆艇确实带货水平移动；触发车{rd['trap_removed_frame']}帧移除。{rd['drop_frame']}帧卸车，实际货车落格{rd['landing_cell']}、land={rd['landing_land']}；货车继续普通Move到{rd['cargo_final']}。
清地使用普通地图记录替换卸载区域的清地图块，并保持平台原有级4；道路保留原图地形。比较实际货车落点，不把船所在格当作货车落格。两场船300、货车和另一辆交通车200、步兵125生命保持；另一辆车与步兵也实际完成普通移动。
运输路线位于桥旁既有可达通道，船不在断裂桥面上；验证的是桥毁事件期间的载车状态、运动和卸载，不宣称验证了船在坍塌桥面上的坠落或直接伤害。

其他坡型和方向
采用原版只读格目录已观察到的坡型2（原54,44）和坡型3（原69,40），只用普通IsoMapPack5记录铺设，保留原桥覆盖层；未运行时改Z、坡型、桥层或路径。
南侧坡型2：主车从北侧级4进入桥道，在南侧上坡至级5后返程下坡；高度416↔520。坡面中间采样分别{[len(q['samples']) for q in south['ramps']]}帧，桥层0→1→0→1→0，最后{south['end']}。
东西向坡型3：主车从西侧高地向东下坡，再转入南北桥道，返程向西上坡；高度520↔416。中间采样分别{[len(q['samples']) for q in east['ramps']]}帧，桥层同样完成两次进出，最后{east['end']}。
两场都含对向车辆、步兵和450帧后离开的出口占位车，往返及反向移动效果已核对，生命未损失；详细帧、坡面坐标和桥层时点见effects.json。

差异、未合格探索与原版异常
清地场景的原版/C气垫坐标最大差X13/Y21/Z5世界单位，方向8315/5545、内部转向计时240/6；同一船对同一步兵在同格的三条关系查询相差1帧，值和次序一致。除此之外状态和非地形记录一致，地形规则值计数一致、随机数一致。
严格comparison.json保留false；局部功能验收冻结到本轮改动前完整的同模式轨迹。通用比较器未修改，不追平无功能影响的瞬时数值。
低海拔岸线初试b-dc/b-wg没有形成有效运输移动，不计作水面卸载验证，输入/轨迹保留。后来把清地毁桥触发延后20帧的b3-dc，在改业务代码前就出现1029帧起随机数分流，根因未定，未计入正式通过；未放宽随机数检查。道路b3-rd可证明水平移动中毁桥，清地采用已核对的b2-dc时序。
两项原版弯曲高差异常Z436停滞、Z-193未完成继续保留并有限回归，不自动变成永久逐BUG需求。列车碰撞、步兵碾压与重复失败已回归；受控单位环只用于重复失败诊断，装卸/坡面场景仅用普通地图和普通命令。关闭规则负对照继承既有证据。
29个非主C候选、86条原始入边沿用；当前308项编译内容扫描无新增直接C调用，原始标签/分发表保留；没有新自然入口结论，不强造入口。

保留、清理、后续
父批380项封存、本批309项独立基线、两部分回退、改动前功能宿主、全部差异/未合格探索和原版异常保留。当前封存只含实际编译内容、工具、必要探针与有限配方。
清理{clean['deleted_files']}个路径/类型/哈希逐项核对的可重建中间文件或缓存，共{clean['deleted_bytes']}字节；同目录{clean['protected_files']}个非候选文件哈希不变。原始资源、源文件、存档、程序、轨迹和回退保留。
H盘20项原版输入、只读规则、原版EXE、SAVE0029、旧手写引擎及Git配置/远端引用不变。
仍需后续有界核查改动前的额外时序随机数分流、水面/其他装卸地形、贴近坍塌区的载具伤害、更多坡型/移动器和其他子系统。本批不代表全游戏等价或全部移动状态完成，不估算缺少可靠分母的总体百分比。
复核：{R/'verify_final_movement_v48.py'}。
本地提交，不推送；提交身份见{S/'postcommit/git-local-commit.json'}。
'''
assert not report.exists() and not handoff.exists();report.write_text(text,encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式47 / 验证48，2026-10-24。
政策：{policy}
报告：{report}
程序SHA-256：{digest}
新增ground_transition_rules，整理同高/一级坡面/四级桥层判断和上层参考高度；Prepare接近阶段保留两组实时世界查询，不缓存第一次结果。
179C/308输入/37保护；生成入口/runtime/生产记录器/比较器/规则与美术未改。
两部分各3配对1303帧并保留回退；正式矩阵共{pairs}配对{frames}帧，原生65536例。运输构造器128例及Capture64例证明继承，不重复计数。
毁桥载车的清地与道路卸载已核对实际落格land0/1；道路场景桥毁瞬间船正带货水平移动，清地桥毁时处于起步转向阶段，随后完整运输/卸车/独立移动。
南侧坡型2、东西向坡型3往返及动态交通完成，实际高差416↔520、桥层两进两出。船不在断裂桥面上，不冒称验证了坠落/直接伤害。
清地气垫瞬时数值和三条关系查询1帧时点差异单列功能验收，当前各模式与基线完整轨迹相同，严格false保留。
额外b3-dc在改代码前即有1029帧起随机数分流，根因未定、未计通过；b-dc/b-wg低岸试验未形成移动，也不计水面卸载验证。全部输入/轨迹与原版高差异常/旧差异及29候选调查保留。
基线：{S/'baseline'}；回退：{S/'parts'}；基线宿主：{S/'baseline-observer'}；封存：{S/'final-source'}。
后续优先有界核查额外时序的随机数差异、其他装卸地形、贴近坍塌区的载具伤害，再推进剩余状态服务、坡型/移动器及其他子系统。
复核：{R/'verify_final_movement_v48.py'}。本地提交不推送。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第四十七批正式47 / 验证48已验收。\n交接：{handoff}\n政策：{policy}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-24）：原版1.006 C17/x86单位移动第四十七批已验收。高度转换/接近服务边界、毁桥载车与清地/道路卸载、南向及东西向坡面交通；[第四十七批交接](交接文档-单位移动第四十七批正式验收-20261024.txt)。继续遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)，保留基线、回退和原版异常。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt'
p.write_bytes(f'第四十七批（2026-10-24）\n新增ground_transition_rules，统一高度转换与上层参考，保留Prepare接近阶段的两组实时查询。\n毁桥载车、清地/道路落点及坡型2/3交通已核对；179C/308输入/37保护，{pairs}配对{frames}帧，原生65536例。额外改动前随机数探索未计通过，记录见报告。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=47,verification_round=48,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer);x['current_batch']=dict(formal_generation=47,verification_round=48,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=65536,production_c_sources=179,content_inputs=308,strict_all_frames_equal=strict,accepted_baseline_variations=variations);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,natural_alias_dispatch_required=False,percentage_reestimated=False,remaining=['Other generated state/service entries','Pre-change timed clear RNG divergence at1029; water/unload terrain and direct collapse damage; more slopes/locomotors','Other locomotors and engine subsystem integration']))
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v48*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.glob('*fixtures*.json'))
paths.update((S/n).relative_to(R).as_posix() for n in ['bridge-catalog-build-arguments.json','mission-table-proof.json','transport-native-validation-current.json','native-gates.json','service-boundaries.json','excluded-explorations.json'])
manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']]
documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=read(S/'vcs-context.json')['parent_commit'],state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=179,content_inputs=308,unsupported_guards=37,native_cases=native['cases'],probes=native['groups'],capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,accepted_inherited_variations=variations,strict_all_frames_equal=strict,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=47,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames))
