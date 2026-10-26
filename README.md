# 红色警戒 2 C17 复刻代码

当前主线位于 `experiments/ra2-recomp-20261020/ra2`：基于原版 1.006 的 Windows x86 静态重编译及可读 C 服务。目标是整体功能、规则和效果一致，不要求逐个复现原版缺陷。

目录内容：

- `experiments/ra2-recomp-20261020/ra2/src`：当前 C17 产品与运行时代码。
- `experiments/ra2-recomp-20261020/pcrecomp`：构建与静态提升所需的运行时、工具及上游授权声明。
- `src`、`include`、`tests`：保留的早期 C17/x64 引擎、资源解析及测试代码。
- `scripts`：通用构建检查、测试及代码生成工具。

在配置好 MSVC x86 C 工具链、Windows SDK、CMake 和 Ninja 后，可运行：

```powershell
Set-Location experiments/ra2-recomp-20261020
.\build-faithful.ps1
```

该脚本使用本机 Visual Studio 路径，首次使用时应核对脚本中的安装位置；产物位于 `ra2/build-original-c`。原版程序、游戏素材与私有存档由使用者自行准备，放在本地 `ra2/game`，不纳入版本控制。

早期 x64 代码可通过根目录 `build.ps1` 或 `CMakeLists.txt` 构建；它与当前 x86 主线分开维护。

提交前检查：

```powershell
python -B scripts/verify-source-scope.py
python -B scripts/verify-staged-recomp.py
```

仓库仅跟踪源码、构建/通用测试工具及必要授权声明。交接文档、接续说明、分批验收记录、原始对照数据、回退产物、临时缓存及一次性整理脚本仅在本地保留。
