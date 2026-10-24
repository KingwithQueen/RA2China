> 当前研究路线（2026-10-24）：原版1.006 C17/x86单位移动第三十九批已验收。跨格进入、列车链/地表碾压业务与共享定位流程；[第三十九批交接](交接文档-单位移动第三十九批正式验收-20261024.txt)。继续遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)，保留基线、回退和原版异常。

> 此前手写引擎阶段：V3、无畏舰、海空与运输卸载，盟军首关任务链。模拟 11 / RA2RPL13。`build/ra2battle.exe --campaign --map all01t.map` 进入原版首关。原始胜利触发器已在普通命令流程中成立；这不等于完整原版行为与演出验收。范围与待办见 [阶段说明](docs/海空运输与盟军首关.md)，正式结果以 `reports/latest-sea-air.json` 指向的验证为准。此前阶段内容保留为历史记录。

# 红色警戒 2：纯 C 引擎基础

当前实现资源基础库、规则对象与静态引用检查，以及 PAL/SHP/CSF、VXL/HVA/VPL、TMP 和地图解析，提供原生资源、体素和地图查看器，以及实际坦克选择、移动、炮战、固定步与回放的最小战场。
目标平台为 Windows x64，语言为 C17。库、命令行程序、查看器和测试全部使用 C，无 Python、.NET 或 C++ 运行时依赖。构建和验证由 PowerShell 调度；独立参考验收另用 Python，不参与产品运行。

本目录独立开发。现有 `H:\开发` 项目、原始游戏文件、存档和 MOD 均作为只读资料使用；不运行旧项目的生成、安装或补丁脚本。

2026-10-19 调整：后续以原版 1.006 玩法为基线，开发多核与底层升级；中国 MOD 暂缓，仅预留阵营扩展位置。现有中国资源预设和历史验收保留。范围、音视频格式建议及下一阶段顺序见 [重制范围与底层升级方案](docs/重制范围与底层升级方案.md)。

最新显示修复：[终点坦克遮挡修复](docs/终点坦克遮挡修复.md)。桥口单位按像素高度与桥面比较，修正过桥停稳后车身被覆盖的问题；桥下仍保留遮挡。

2026-10-20：当前主线为原版战役与单人遭遇战，菜单暂缓。最新阶段为 [建造、生产、采矿与科技](docs/建造生产采矿与科技.md)：建造/车辆队列、资金与低电力、动态放置和生产、矿车采集与卸货、所属国家与科技前提、运行时对象回放。运行 `build/ra2battle.exe --economy-demo --map MP17T6.map` 进入苏军验证场，增加 `--allied --map MP32S8.map` 可查看盟军雪地流程。模拟版本 **9**，回放 **RA2RPL11**，上一版完整保存在 `build/economy-preserved`。

[建筑实体与原始场景](docs/建筑实体与原始场景.md)的 `--base-demo --map MP05MW.map` 和 `--scenario --map all01t.map` 入口继续保留。当前仍是阶段验证，战役脚本、完整遭遇战、其他单位及未校准行为见新阶段说明。

## 已实现

- 无标志的旧式 MIX 头，以及带标志的 MIX 头。
- Westwood RSA 公共变换与 Blowfish 加密头读取，代码自包含。
- SHA-1 包体摘要校验：有校验标志时必须通过，损坏或缺失则拒绝打开。
- 按 CRC32 或经典算法计算文件名 ID，按名称/ID 查询，按 ID 枚举条目。
- 嵌套 MIX 的只读视图、文件和条目范围检查、重复 ID 拒绝。
- 散装目录和 MIX 的统一资源挂载、显式优先级、来源追踪。
- INI 顺序解析、节/键查找、重复定义保留、来源行号、整数和布尔值转换。
- UTF-8、带 BOM 的 UTF-16 LE/BE；旧编码字节保留。
- 兼容/严格两种 INI 模式；兼容模式对原始文件中的说明文字给出诊断。
- 规则类型表、隐式武器/弹道、单位和美术映射、通用前置组、标量类型与引用检查。
- 缺失目标、声明未定义、未检查资源，以及原文/数据层/运行层字段支持清单。
- PAL 六位 RGB 调色板、TS/RA2 SHP 完整画布与透明游程、CSF 中文文本与附加值解析。
- 原生 Win32/GDI 查看器：原版/MOD 切换、资源目录与手动输入、逐帧/跳转/播放、缩放、调色板选择、中文搜索及 BMP 预览保存。
- VXL 稀疏体素、HVA 多部件帧矩阵、VPL 明暗查色表，以及带深度遮挡的软件体素预览。
- 按实际规则解析中国单位的 Image 与中文名称，合成车体/炮塔/炮管，支持旋转、俯角、缩放、部件选择、阵营换色与实际 HVA 动画。
- TMP 地形与 LZO1X / LCW 地图压缩段解析，实际绘制温带、雪地、城市地图，保留对象布局、覆盖物和来源。
- 原生地图查看器支持中文地图名、缩放拖动、格子查询、图层开关、独立 TMP 查看和完整 BMP 导出。

运行 `build/ra2battle.exe` 进入最小战斗：实际灰熊/犀牛坦克、原版选择与编队、移动/攻击/停止、生命条、炮弹和爆炸动画。当前支持桥上/桥下独立占格与桥口通行、桥梁损坏与修复、原版桥梁图像、静态坡面底盘与炮口矩阵、常规炮弹碰撞退场、基础索敌候选过滤。固定模拟为 15 步/秒，模拟版本为 **9**，回放标识为 **RA2RPL11**，全部新增状态参与逐步校验。

桥梁层的历史实现见[桥梁分层与碰撞生命周期](docs/桥梁分层与碰撞生命周期.md)。当前实现和边界以[建造、生产、采矿与科技](docs/建造生产采矿与科技.md)及 `reports/latest-battle.json` 为准；完整战役、遭遇战、其他单位、精确采卸矿/工厂时序和多核任务系统仍需继续开发。中国内容只保留扩展接口；旧版代码和程序保留于 `build/stage10-preserved`。

```powershell
.\build\ra2battle.exe --map MP06T2.map
.\build\ra2battlecheck.exe --map MP06T2.map --layers --output build\桥梁.rpl
.\scripts\verify-layers.ps1 -AddressSanitizer -ConcurrentDesignDirectory 'H:\开发\研究资料\中国阵营重设计'
```

## 构建

在 PowerShell 中运行：

```powershell
Set-Location -LiteralPath 'D:\Program\红色警戒2'
.\build.ps1
.\build\ra2tests.exe
.\build\ra2rulestests.exe
.\build\ra2assettests.exe
.\build\ra2voxeltests.exe
.\build\ra2maptests.exe
.\build\ra2battletests.exe
.\build\ra2combattests.exe
.\build\ra2missiontests.exe
.\build\ra2physicstests.exe
.\build\ra2locomotortests.exe
```

需要安装 Visual Studio / Build Tools 的 x64 C 工具链和 Windows SDK。脚本通过 `vswhere` 查找编译器，使用 C17、`/W4 /WX`，输出静态库、工具和测试程序；编译临时文件留在本目录。

```powershell
.\build.ps1 -AddressSanitizer
.\build\asan\ra2tests.exe
```

也提供标准 CMake 工程：

```powershell
cmake -S . -B build/cmake-vs -G "Visual Studio 18 2026" -A x64
cmake --build build/cmake-vs --config Release
ctest --test-dir build/cmake-vs -C Release --output-on-failure
```

本环境另提供 `.\scripts\verify-cmake.ps1`，使用 Ninja 和嵌入调试信息，并实际检查 MSVC 头文件依赖；可处理只安装中文编译器诊断资源时的提示前缀编码差异。

## 使用真实资源

地图预览运行 `build\ra2mapviewer.exe`，可切换原版 / 中国预设，查看温带、雪地、城市地图和单独 TMP，支持缩放、平移、格子查询与布局图层。建筑和单位目前显示位置标记。操作见 [地图预览](docs/地图预览.md)，验收见 `reports/latest-maps.json` 和 [第五阶段验收](docs/第五阶段验收.md)。

```powershell
.\build\ra2mapviewer.exe
.\scripts\verify-maps.ps1 -AddressSanitizer
```

体素预览运行 `build\ra2voxelviewer.exe`。可选 `CNAPOC` 查看中国天启坦克，`CARRIER2` 查看航母，`J10` 查看战机，`SEEK` 查看带真实 HVA 帧的直升机；右侧显示实际图像映射和文件来源。详细用法见 [体素预览](docs/体素预览.md)，验收见 `reports/latest-voxels.json`。

```powershell
.\build\ra2voxelviewer.exe
.\scripts\verify-voxels.ps1 -AddressSanitizer
```

双击 `build\ra2viewer.exe` 打开资源查看器，默认使用本机已经确认的原版与中国运行目录。首次挂载会核对 MIX 摘要，需要几秒钟；不写入游戏目录。用法与支持范围见 [资源查看器](docs/资源查看器.md)，正式结果见 `reports/latest-assets.json`。

```powershell
.\build\ra2viewer.exe --original 'H:\开发\运行版本\原版1.006' --mod 'H:\开发\运行版本\中国开局验证'
.\scripts\verify-assets.ps1
```

下列 `ra2tool` 命令只读输入，结果输出为 JSON；错误写入标准错误。退出码 0 表示成功，3 表示未找到，其他错误为 1。

查看加密包或嵌套包的条目：

```powershell
.\build\ra2tool.exe mix 'H:\开发\运行版本\原版1.006\ra2.mix'
.\build\ra2tool.exe mix 'H:\开发\运行版本\原版1.006\ra2.mix|local.mix'
```

查看 INI 结构、重复项数量和忽略文本的诊断：

```powershell
.\build\ra2tool.exe ini 'H:\开发\运行版本\中国开局验证\rules.ini'
```

从原版包和 MOD 目录统一查询：中国目录优先级 100，原版嵌套包优先级 10。

```powershell
.\build\ra2tool.exe query rules.ini CNLTNK Strength `
  --mix 10 'H:\开发\运行版本\原版1.006\ra2.mix|local.mix' `
  --dir 100 'H:\开发\运行版本\中国开局验证'
```

结果包含最终来源、优先级、实际定义行号和值。`resolve` 查询任意资源的来源、长度和 SHA-1；`scan-ini` 解析挂载后的 INI；`compare` 与指定参考文件进行逐字节比较。

```powershell
.\build\ra2tool.exe resolve ai.ini `
  --mix 10 'H:\开发\运行版本\原版1.006\ra2.mix|local.mix' `
  --dir 100 'H:\开发\运行版本\中国开局验证'
```

挂载规则：优先级数值越大越优先；相同优先级后挂载者优先。嵌套路径用 `|` 分隔并在命令行中加引号。挂载指定包的直接成员；不会自动扫描其他包，也不会隐式挂载所有子包。覆盖的单位是完整资源文件，尚不合并不同 INI 文件中的节/键。

## 完整验证

```powershell
.\scripts\verify.ps1
.\scripts\verify-rules.ps1
```

验证包含 C 测试、真实包校验、既有资源索引对照、28 个原版配置文件的逐字节对照与解析、MOD 覆盖和原版回退。每次运行生成独立报告目录，入口在 `reports\latest-release.json`。

现有 `MOVIES01.MIX` 的包体 SHA-1 与存储摘要不一致，独立计算已确认。严格读取器拒绝该文件；验证按完整文件 SHA-256 精确识别这一已有异常并记录预期拒绝，不将它计为资源校验通过。原文件保持不变，视频内容能否播放尚未判断。

保存证据包括旧项目全体文件的路径/长度/修改时间清单，以及参与验证的输入文件 SHA-256 前后记录。检查只覆盖报告所载验证时间段；输入文件没有被作为输出打开。

规则阶段另由 `reports\latest-rules.json` 指向正式记录，分别列出原版与中国 MOD 的缺失引用和全部未实现字段。该阶段检查使用的 4 份 INI 和原版 MIX 均进行前后 SHA-256 对照。

## 开发接口与后续

- 公共接口：`include/ra2/ra2.h`。
- 格式与兼容边界：`docs/格式与接口约定.md`。
- 路线与当前交接：`docs/开发顺序与交接.md`。
- 本次结果与保存证据：`docs/第一阶段验收.md`。
- 规则模型、状态定义和使用方式：`docs/规则对象与引用检查.md`。
- 本阶段真实文件结果：`docs/第二阶段验收.md`。
- 新增代码规范：`docs/编码规范.md`。

资源、地图、最小炮战、战场任务和桥梁损毁/修复基础已经建立；下一步补原版实机边界验证，接入建筑、工程师维修屋与经济闭环。固定步、可重放命令和逐步摘要继续作为多核优化的参考。



桥梁损毁/修复阶段已提供可回放的桥段状态、动态通行与坦克坠桥结算，详见 [桥梁损毁修复与坠桥](docs/桥梁损毁修复与坠桥.md)。运行 `build\ra2battle.exe --bridge-demo` 可查看演示；正式证据入口为 `reports/latest-bridges.json`。原版实机校准、工程师与维修屋玩家交互仍按该文档列项待验。

桥梁与单位显示修复见 [修复说明](docs/桥梁与单位显示修复.md)：高桥按方向校正锚点，坦克统一车身、炮塔与坡面变换，使用固定比例和原点，按剧场切换单位调色板。直接运行 `D:\Program\红色警戒2\build\ra2battle.exe`，参数为 `--map MP06T2.map` 或 `--bridge-demo`。显示验证通过后由 `reports/latest-rendering.json` 和 `reports/latest-battle.json` 指向本轮记录；桥梁模拟的历史入口继续保留。


