# Espresso逻辑化简法

程序先用PyEDA调用Espresso，把DDT或LAT表中为0的位置化简为逻辑立方体；再将每个立方体转换成Gurobi排除约束，枚举剩余的合法输入输出对。全过程在内存中完成，不保存PLA、模型、日志或结果文件。

在 `task1` 目录运行：

```powershell
uv run python logic_minimization/logic_minimization.py
```

依赖由上一级的 `pyproject.toml` 和 `uv.lock` 管理；此方法使用 `pyeda`（Espresso）和 `gurobipy`。
