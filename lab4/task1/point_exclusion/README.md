# 逐点排除法

本目录使用上一级的 `ddt_lat.py` 计算公共DDT、LAT，并用Gurobi逐个排除表中为0的输入输出对。LAT的负值仍视为合法点。

在 `task1` 目录运行：

```powershell
uv run python point_exclusion/point_exclusion.py
```

程序只打印模型变量数、约束数、解数和全部输入输出对，不保存模型或结果文件，也不进行自动解集比较。环境依赖由 `task1/pyproject.toml` 和 `task1/uv.lock` 管理。
