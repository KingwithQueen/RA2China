"""Create this round's final gates from the previous validated workflow."""
from pathlib import Path
import re
R=Path(__file__).resolve().parent
old_report='单位移动第三十二批-四副本接续与北向移动交会及对象服务出口-20261023.txt'
new_report='单位移动第三十三批-寄存器样本与武器门槛及桥上交会占用组合-20261023.txt'
def adapt(t):
    t=t.replace('v33','ROUND_NEW').replace('v32','v33').replace('ROUND_NEW','v38')
    t=t.replace(old_report,new_report).replace('第三十二批','NEW_BATCH').replace('第三十一批','第三十二批').replace('NEW_BATCH','第三十三批')
    t=t.replace('ccc6e7204cd9deac4e32deadcc263d1f8a2ce4b5','30b30d2dd6ab088c78697fb904fc4ce3fdf74ce0').replace('ccc6e72','30b30d2')
    t=t.replace('d03ef60ce68c447108299d173677ded81af794a8aa5b25b8d184a6efe6c0e45f','19bb89a2f7a69534848b40bdd474c0a44f5788a8b3bb536d8a8650285e8a2104')
    t=t.replace('4390','4684').replace('40231','42033').replace('15317','17119')
    t=re.sub(r'\b111\b','114',t)
    t=t.replace('==61','==63').replace('=61','=63').replace('61场','63场').replace('61个','63个')
    t=t.replace('generation32','generation33').replace('formal_baseline_generation=32','formal_baseline_generation=33').replace("formal_baseline_generation']==32","formal_baseline_generation']==33").replace('formal_baseline=32','formal_baseline=33')
    t=t.replace('verification_round=33','verification_round=34').replace("verification_round']==33","verification_round']==34")
    return t
t=adapt((R/'finalize_movement_v33.py').read_text(encoding='utf-8'))
t=t.replace('range(9,33)','range(9,34)').replace('destination-copy-contract.json','new-fragment-contract.json')
t=t.replace("'internal-alias-sources.json','alias-natural-scenes.json'","'internal-alias-sources.json','alias-natural-scenes.json','bridge-occupied-real-scenes.json'")
t=t.replace("assert native['passed']", "assert read(S/'native-round34-identity.json')['passed']\nassert native['passed']",1)
t=t.replace("bridge_multiobject_scenes=17,bridge_multiobject_frames=17119","bridge_multiobject_scenes=19,bridge_multiobject_frames=17119,bridge_meeting_occupied_scenes=2,bridge_meeting_occupied_frames=1802,bridge_meeting_occupied_verified=True")
t=t.replace("prepare_stop_service_exits_shared_readable=True)","prepare_stop_service_exits_shared_readable=True,register_sample_internal_shared_readable=True,enemy_weapon_internal_shared_readable=True,owner_stop_service_shared_readable=True)")
t=t.replace("preservation['original_preframe_startup_failures_preserved']=", "prelaunch=read(S/'prelaunch-failures.json');assert prelaunch['passed']\nfor attempt in prelaunch['attempts']:\n    assert not attempt['game_launched'] and attempt['simulation_frames']==0 and sha(R/attempt['log'])==attempt['sha256']\n    assert read(S/'runs'/attempt['tag']/'comparison.json')['passed']\npreservation['prelaunch_path_refusals_preserved']=len(prelaunch['attempts'])\npreservation['original_preframe_startup_failures_preserved']=",1)
a=t.index("body=f'''");b=t.index('report.write_text(body',a)
body="""body=f'''单位移动第三十三批正式验收（2026-10-23）
正式代次33 / 验证轮次34
父提交：30b30d2dd6ab088c78697fb904fc4ce3fdf74ce0
程序：{exe}
SHA-256：{digest}
证据：{S}

第三十二批提交30b30d2、程序19bb89a2f7a69534848b40bdd474c0a44f5788a8b3bb536d8a8650285e8a2104与4684项源封存先只读核对通过，原工作区干净。完整baseline、旧文档、程序及指针均保留。

1. 三部分与原版逐帧对照及回退
内部模板：4A2314八处接续共用已有样本选择服务，入口3从传入EDX读取样本下标，其他入口仍从drive缓存读取。65536例特意使寄存器下标与缓存不同，核对原版内存、活跃结果、非易失寄存器及栈。旧原生标签、注解、跳转与37处保护均保留，没有增加原生分派入口；不等于八个C副本已有自然入口证明。
具体对象：7039EC三处共用武器零查询、列车属性门槛和既有建筑/地形/其他分类。65536例包含武器回调改变列车属性，保留短路和调用顺序。
服务出口：4A449B七处共用410服务与Prepare返回，服务对象来自传入ECX而不是提前重读drive.owner。65536例包含不同入口对象、回调替换owner、改写保存寄存器及EAX高位，核对服务参数、完整返回和出栈。
每部分六场3406帧：默认901、短包围101、独立真实AI预算901、双向隧道各501及出口占用501；状态、RNG、命令及有序事件一致。三份完整源、程序、探针及场景回退：
'''+''.join(n+' : '+v['exe_sha256']+'\\n' for n,v in parts.items())+f'''
171个C源、292项内容输入；最终内容构建刷新0并与returns回退相同。正式记录器、公共比较器、schema12、0010的LF和0046的CRLF保持。七项生产源、三项探针、一项观察器和两份新地图从本批baseline独立重放逐字节一致。原63份地图/规则逐字节继承。

2. 最终回归
114组原版片段门禁通过，包含既有111组完整重跑及本轮三项各65536例。生产清单实际求和63场42033帧，包含上一批61场40231帧及两场交会占用各901帧。短包围检查、探索试验和观察程序不重复计入生产。
独立默认预算901、内部观察4054、连接及高差占用9116、桥观察19场17119、非主入口观察3604帧分别统计。坐标扰动与缺帧负控均拒绝差异；存档使用私有副本。

3. 桥上移动步兵与车辆交会加出口占用
沿用原版桥跨及普通地图对象，分别在北向70格、南向63格放置本方TRUCKA占住桥出口内侧，E2与主车辆正常对向移动，300帧仅向占位车辆下达正常驶离命令。未写路径、链指针、运动状态或桥层。
生产/原版、独立观察/原版、生产/观察的状态和有序事件全部相等。要求双方在416桥面同帧反向移动时有实际关系与几何查询，主车辆确实查询占位车辆并在出口附近等待，占位车辆按令驶离后主车辆恢复移动。到达与查询分别统计，保留原版最终行为。
新增两场结果：{ {n:v['modes']['original'] for n,v in evidence['bridge-occupied-real-scenes.json']['scenes'].items()} }
上一批北向移动查询108帧、既有交会/跟行、友方和原生AI敌方交通、上下层三对象链均已重跑。观察器原字节检查和CPU/FPU保存与上一批相同，替换十二项测试对象，完整状态身份单独核对。

4. 非主自然入口与原版异常
继续检查28个非主别名、三个主入口和85条原生入边，扫描171源与292输入；全部原生入边逐字节核对。没有新增独立原生入口或强行调用非主C副本。主入口正控有记录，扩展十九个候选加既有九个在合法桥实景中仍未观察到自然首次调用。函数内部边界命中不等于独立C入口命中；任意计算目标、运行时指针和未覆盖场景仍未排除。
4→6上行停滞及7→4下行至-193的异常继续与原版一致，只计异常一致性。四组既有成功高差加占用继续保留原等待和退出；旧错误桥端摆放、缺Tags及敌方命令拒绝、旧逐帧失败和上一批零帧CSF失败记录均保留，未修改原版异常。
本批第一次短包围启动在创建私有目录前被路径检查拒绝，尚未启动游戏或产生模拟帧；prelaunch-failures.json及原日志完整保留，同一路径补跑通过。比较器和路径保护完全未改。当前游戏首帧前失败{len(startup['attempts'])}次。

5. 保留、范围及继续工作
v9..v33旧封存、本批4684项baseline和三份parts均逐项核对；H盘原版允许列表20项、原游戏、SAV及旧手写引擎哈希保持。只声称核对的允许列表，不扩大成整个H盘未变化。
本批对应八处寄存器接续、三处武器门槛、七处服务出口以及两场交会占用组合完成验收。其他内部模板、更多具体对象/移动器/建筑/地形/碾压/毁桥、其他服务与递归写回出口、28个非主自然入口、更广高差和占用组合仍需继续；完整移动、寻路、对象分类及全游戏等价未完成。没有重新估算百分比，旧估算仅为历史记录。
完成后只本地提交，不推送。下批先运行verify_final_movement_v38.py核对，再建立新回退；不要原地重跑本轮封存写入脚本。
'''
"""
t=t[:a]+body+t[b:]
# Keep concise entry pointers aligned with the actual final scope.
t=t.replace('四副本接续、敌方接触、后续服务出口','寄存器样本接续、武器门槛、入口对象服务出口').replace('四副本接续、敌方接触与后续服务出口','寄存器样本接续、武器门槛与入口对象服务出口')
t=t.replace("formal_baseline_generation=32","formal_baseline_generation=33").replace("verification_round=33","verification_round=34")
(R/'finalize_movement_v38.py').write_text(t,encoding='utf-8',newline='\n')
for name in ['stage_movement','audit_git','audit_git_bytes','verify_final_movement']:
    p=R/(name+'_v38.py');t=adapt((R/(name+'_v33.py')).read_text(encoding='utf-8'))
    if name=='stage_movement':t=t.replace("'ground_joint_bridge.c','ground_allied_bridge.c'","'ground_joint_bridge.c','ground_allied_bridge.c','ground_tube_state_bridge.c'")
    if name=='audit_git':t=t.replace("map_names={","map_names={'bridge-occupied-north.MAP','bridge-occupied-south.MAP',")
    p.write_text(t,encoding='utf-8',newline='\n')
print('Created formal generation33 finalization and commit gates')
