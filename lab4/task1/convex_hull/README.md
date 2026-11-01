# 凸包法

## 1. 在WSL Arch中建立凸包

使用已安装SageMath的系统Python，在 `task1` 目录执行：

```bash
cd /mnt/d/DeskTop/CryptoAnalysis/crypto-analyze/lab4/task1
/usr/bin/python convex_hull/build_hull.py
```

程序分别用DDT、LAT的非零位置构造合法点集，以 `QQ` 精确计算凸包，将完整H表示保存到本目录的 `hull_constraints.json`。

JSON的顶层键是 `DDT`、`LAT`，各自只包含 `inequalities` 和 `equations` 两个系数数组。每行 `[c0,c1,...,c8]` 对应 `c0 + c1*z0 + ... + c8*z7 >= 0` 或 `= 0`，系数均已转成整数。变量位序为 `(a3,a2,a1,a0,b3,b2,b1,b0)`。

## 2. 在Windows中筛选约束并求解

在PowerShell的 `task1` 目录执行：

```powershell
uv run python convex_hull/convex_hull.py
```

程序读取JSON并保留全部等式，每次选择能排除最多剩余非法点的不等式，直到全部非法点被排除，再由Gurobi枚举二进制解。并列时按整数系数的字典序选择。

输出包含原不等式数、贪心保留不等式数、等式数、模型变量数、约束数、解数及全部输入输出对。求解依赖使用 `task1` 现有的uv环境。S盒或合法点集改变后，需要重新运行建立凸包脚本。
