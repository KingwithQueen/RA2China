"""Set generation37 promotion checks and documentation before final execution."""
from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'finalize_movement_v38.py';t=p.read_text(encoding='utf-8')
for a,b in [('generation36','generation37'),("O=R/'evidence/movement-state-v36'","O=R/'evidence/movement-state-v37'"),('8f085a069f1efb3d1a84fa1495ba3b0679e89479','6a948c6763d1ec5ce5e9e0911b1620bcf6f53950'),('==123','==126'),('==69','==71'),('==47439','==49241'),('range(9,37)','range(9,38)'),("O/'investigations/template-build-01/receipt.json'","R/'evidence/movement-state-v36/investigations/template-build-01/receipt.json'"),('formal_baseline_generation=36','formal_baseline_generation=37'),('verification_round=37','verification_round=38'),('paired_scenes=69','paired_scenes=71'),('paired_frames=47439','paired_frames=49241'),('probes=123','probes=126'),('independent_bridge_observer_frames=22525','independent_bridge_observer_frames=24327'),('bridge_multiobject_scenes=25','bridge_multiobject_scenes=27'),('bridge_multiobject_frames=22525','bridge_multiobject_frames=24327'),('cleanup_performed_this_round=False','cleanup_performed_this_round=True'),('formal_baseline=36','formal_baseline=37')]:
 assert a in t,a;t=t.replace(a,b)
t=t.replace("assert read(S/'native-round37-identity.json')['passed']","assert read(S/'native-round38-identity.json')['passed']")
marker="evidence['bridge-lane-release-motion.json']=";i=t.index(marker)
t=t[:i]+"evidence.update({n:read(S/n) for n in ['bridge-neighbor-release-real-scenes.json','bridge-neighbor-release-motion.json']})\nassert evidence['bridge-neighbor-release-real-scenes.json']['production_executable_sha256']==digest\n"+t[i:]
marker="preservation['previous_cleanup_verified']=True;preservation['cleanup_performed_this_round']=False"
assert marker in t
t=t.replace(marker,"""current_cleanup=read(S/'cleanup.json');plan=read(S/'cleanup-plan.json')
assert current_cleanup['passed'] and current_cleanup['protected_files_unchanged'] and current_cleanup['plan_sha256']==sha(S/'cleanup-plan.json')
assert current_cleanup['deleted_files']==len(plan['files']) and current_cleanup['deleted_bytes']==sum(e['bytes'] for e in plan['files'])
for e in plan['files']:assert not (R/e['path']).exists(),e['path']
for e in plan['protected_files']:assert sha(R/e['path'])==e['sha256'],e['path']
preservation['previous_cleanup_verified']=True;preservation['cleanup_performed_this_round']=True;preservation['current_cleanup']=current_cleanup""")
old_report='单位移动第三十六批-4A24F0与弹头门槛及桥上主车道先放行组合-20261024.txt'
new_report='单位移动第三十七批-桥层写回与武器分类及桥上相邻车道放行组合-20261024.txt'
t=t.replace(old_report,new_report).replace('交接文档-单位移动第三十六批正式验收-20261024.txt','交接文档-单位移动第三十七批正式验收-20261024.txt')
a=t.index("body=f'''");b=t.index("report.write_text(body",a)
body="""body=f'''单位移动第三十七批正式验收（2026-10-24）
正式代次37 / 验证轮次38
父提交：{vcs['parent_commit']}
程序：{exe}
SHA-256：{digest}
证据：{S}

本轮先只读核对第三十六批6a948c6、程序4db5d31b232480adb2f7aa7142e71add8d3721bf4b75c9b21bdf17c882487c73、5980项封存和干净工作区；完整baseline、旧程序和三部分回退保留。
内部模板：4A25A0桥层写回共十三段（八处原生标签、五处嵌入段），复用纯C桥层判断，保持已取格子指针、符号高度与重复读取标志顺序。65536例覆盖全部有符号高度字节组合和写回与标志/保存指针重叠；不新增原生入口。
具体对象：703A45三处从已载入武器检查可空弹头及146字节，复用已验纯C分类，不重选武器或查询kind。65536例包含空弹头、256种字节值和有符号通行边界，零服务调用。
共享出口：4A2586十三处离格11C(0)→定位19C→桥层写回→进入11C(1)→Advance出栈。首次使用入口ECX，后续在回调后重读owner和两个格子；65536例检查回调改换owner、坐标、格子、保存槽及返回EAX。
四项生产C源改动；七项相关源、三项探针、观察器和两份新地图由基线独立重放，逐字节相同。旧标签、指令注解、尾部、37处保护保留。
每部分六场3406帧：默认901、短包围101、独立预算901、双向隧道各501及出口占用501。状态、RNG和有序事件逐帧一致。三部分封存回退：
'''+''.join(n+' : '+v['exe_sha256']+chr(10) for n,v in parts.items())+f'''
最终126组原版片段门禁通过，旧123组重跑，本轮新增196608例。生产共71场49241帧（原69场47439帧及新两场1802帧）。独立默认预算901、内部4054、连接及高差占用9116、桥观察27场24327帧；入口观察3604+5406帧单列，不重复计入生产。
最多两路、四个游戏进程；编译/探针构建串行。171个C源、292项内容输入，最终刷新0且与returns回退一致。公共比较器、schema12、CPU/FPU方式和0010 LF、0046 CRLF保持。71份既有地图/规则逐字节继承，新两份地图为普通地图副本，只改变正常命令时序。

新增桥组合：主车与E2在第5帧各一次对向移动；两普通占位车先到桥出口。北210/南226帧放行61列相邻车道，60列主车道占位车到北420/南436帧才收到离开命令。必须从实际逐帧位置确认相邻车先运动、主车绕行跨出口时主车道仍占用，并同时存在主车与早放行占位车的动态交通。放行命令、实际开始运动、跨出口和到达分别记录；没有写入路径、链、运动或桥层。
新增结果：{ {n:v['modes']['original'] for n,v in evidence['bridge-neighbor-release-real-scenes.json']['scenes'].items()} }
实际放行运动：{evidence['bridge-neighbor-release-motion.json']['scenes']}
旧主车道先放行、错峰放行、持续占用到600帧、300/320清空与重发、友敌混类、移动步兵和弯曲高差出口占用全部重跑。旧主车道先放行的命令到实际运动延迟仍按原版保留，不将命令发出当作车道清空。

29个非主C副本及三个主入口继续核查；{evidence['internal-alias-sources.json']['unique_native_edges']}条原生入边逐字节核对。新组合六场观察覆盖29候选，4A24F0配置南北向，主入口正控均须出现。未观察到非主C副本合法自然首次调用；不是每个候选在每个方向穷尽，计算目标、运行时指针和未跑场景仍待核。原生内部跳转不等于独立C首次调用。
原版4→6上行停滞和7→4下行到-193异常保留，4→7和6→4完成组单列；曲线长组每场实际601帧。完整移动与全游戏等价未完成。
本轮首帧前失败{len(startup['attempts'])}，公共路径拒绝{len(prelaunch['attempts'])}；旧v34不达标试验、v35拒绝和v36首次模板编译失败原地核对保留。
v9..v37旧封存、5980项本轮baseline和三部分回退逐项核对；H盘允许列表20项、D盘原游戏、SAV和旧引擎指纹保持。清理仅删v36/v37根目录{current_cleanup['deleted_files']}个可再生探针obj（{current_cleanup['deleted_bytes']}字节），其余{current_cleanup['protected_files']}个文件逐项未变；不含fixture链接对象、程序、日志、轨迹和封存。v35已批准清理记录及旧2428项缺失状态保持。

剩余：{read(S/'progress-estimate.json')['remaining_zh']}
本轮没有重新估算百分比；旧工程估算明确标作历史，不能由批次/行数推算完成率。
完成后只本地提交，不推送。下批先只读运行verify_final_movement_v38.py，再保存新回退；不要原地重跑封存写入脚本。
'''
"""
t=t[:a]+body+t[b:]
t=t.replace('第三十六批','第三十七批').replace('正式36 / 验证37','正式37 / 验证38').replace('69场47439帧、123组','71场49241帧、126组').replace('69场47439帧，123组','71场49241帧，126组').replace('4A24F0、已载入弹头门槛、进入服务出口','4A25A0桥层写回、703A45武器分类、4A2586离格定位出口').replace('4A24F0、弹头门槛与进入服务出口','桥层写回、武器分类与离格定位出口').replace('桥上主车道先放行组合通过','桥上相邻车道先放行且主车道持续占用组合通过')
# The predecessor sentence in the report must still identify generation36.
t=t.replace('本轮先只读核对第三十七批6a948c6','本轮先只读核对第三十六批6a948c6')
marker="flags.update(loaded_destination_internal_shared_readable=True"
i=t.index(marker);t=t[:i]+"flags.update(late_layer_internal_shared_readable=True,loaded_weapon_internal_shared_readable=True,leave_place_mark_service_shared_readable=True)\n"+t[i:]
t=t.replace('bridge_main_lane_release_verified=True,','bridge_neighbor_lane_release_verified=True,bridge_neighbor_lane_release_runtime_evidence=str(S/"bridge-neighbor-release-real-scenes.json"),bridge_main_lane_release_verified=True,')
t=t.replace('Remaining loaded-table and register-sourced template continuations','Other loaded-table, coordinate-selection and template continuations')
compile(t,str(p),'exec');p.write_text(t,encoding='utf-8',newline='\n')
for name in ['stage_movement_v38.py','audit_git_v38.py','verify_final_movement_v38.py','commit_movement_v38.py']:
 p=R/name;t=p.read_text(encoding='utf-8').replace(old_report,new_report).replace('第三十六批','第三十七批').replace('generation36','generation37').replace("generation']==36","generation']==37").replace("round']==37","round']==38").replace('==69','==71').replace('==47439','==49241').replace('==123','==126')
 if name=='audit_git_v38.py':t=t.replace("map_names={","map_names={'bridge-neighbor-release-north.MAP','bridge-neighbor-release-south.MAP',")
 if name=='commit_movement_v38.py':t=t.replace('Refactor 4A24F0, loaded warheads and mark exits; validate main-lane bridge release (batch 36)','Refactor late bridge layers, loaded weapons and leave-place exits; validate neighboring traffic (batch 37)')
 if name=='verify_final_movement_v38.py':
  i=t.index("assert v['content_inputs']")
  t=t[:i]+"assert all(v[k] for k in ['late_layer_internal_shared_readable','loaded_weapon_internal_shared_readable','leave_place_mark_service_shared_readable','bridge_neighbor_lane_release_verified'])\nassert read(S/'bridge-neighbor-release-motion.json')['passed'] and read(S/'bridge-neighbor-release-real-scenes.json')['passed']\nassert v['cleanup_performed_this_round'] and read(S/'cleanup.json')['passed']\n"+t[i:]
 compile(t,str(p),'exec');p.write_text(t,encoding='utf-8',newline='\n')
p=R/'finish_acceptance_v38.py';t=p.read_text(encoding='utf-8').replace('Generation36 accepted','Generation37 accepted');p.write_text(t,encoding='utf-8',newline='\n')
print('Generation37 promotion configured')
