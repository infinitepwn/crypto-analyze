# 实验代码与报告

四组实验按 `lab1` 到 `lab4` 保留各自的代码、数据、报告和结果。想先理解实验结论，可从[实验复习指南](../review/实验复习/README.md)进入；本页用于查找原始材料与运行入口。

| 实验 | 代码入口 | 报告与结果 | 复习笔记 |
| --- | --- | --- | --- |
| **Lab 1：Enigma** | [加密](lab1/encrypt.py) · [已知明文恢复](lab1/decrypt.py) · [完整目录](lab1/) | [报告源码](lab1/report/main.tex) · [实验图](lab1/report/figures/) | [Enigma 与已知明文](../review/实验复习/01-Enigma与已知明文.md) |
| **Lab 2：差分分析** | [DDT](lab2/task1/DDT.py) · [路线枚举](lab2/task2/find_all_routes.py) · [末轮恢复](lab2/task4/denoise_and_recover_k6.py) | [报告 PDF](lab2/report/main.pdf) · [报告源码](lab2/report/main.tex) | [差分路径与密钥恢复](../review/实验复习/02-差分路径与密钥恢复.md) |
| **Lab 3：线性分析** | [LAT](lab3/code/task1.py) · [迭代路线](lab3/code/task2.py) · [PHILOX](lab3/code/task3.py) | [报告 PDF](lab3/report/main.pdf) · [报告源码](lab3/report/main.tex) | [线性分析与自动化建模](../review/实验复习/03-线性分析与自动化建模.md) |
| **Lab 4：自动化搜索** | [公共表](lab4/code/task1/ddt_lat.py) · [四种建模方法](lab4/code/task1/) · [多轮配置](lab4/code/task2/) | [报告 PDF](lab4/report/main.pdf) · [报告源码](lab4/report/main.tex) · [平台输出](lab4/result_of_task2/) | [线性分析与自动化建模](../review/实验复习/03-线性分析与自动化建模.md) |

## 从小例子开始

以下命令均在**仓库根目录**运行，只需要 Python 3 标准库：

```bash
# 计算 CipherFour 的 S 盒 DDT
python3 labs/lab2/task1/DDT.py

# 计算 LAT：本实验存储“成立次数减去 8”
python3 labs/lab3/code/task1.py

# 搜索四轮固定点线性路线，得到路线偏差 1/32
python3 labs/lab3/code/task2.py

# 查看实验四共用的 DDT 和 LAT
python3 -m labs.lab4.code.task1.ddt_lat

# 读取已有码本，筛选密文对并给末轮半字节候选计数
python3 labs/lab2/task4/denoise_and_recover_k6.py
```

最后一个例子从 `labs/lab2/code/` 读取明密文数据，保留 4028 个有序对，候选 `8` 和 `9` 均得到 3172 分。同分原因见对应的[实验复习笔记](../review/实验复习/02-差分路径与密钥恢复.md)。

## 各目录怎么读

- **`lab1/`**：Python 加解密与环路约束实现；C 程序用于性能实验；`report/` 保存报告源文件和插图。
- **`lab2/`**：`task1`—`task5` 对应实验任务，`code/` 保存参考实现与码本；学习密钥恢复时优先运行上面的 `denoise_and_recover_k6.py`。
- **`lab3/code/`**：三个任务分别计算 LAT、搜索迭代路线、分析一轮线性关系。
- **`lab4/code/task1/`**：`one_hot`、`point_exclusion`、`logic_minimization`、`convex_hull` 是四种局部传播编码；`ddt_lat.py` 提供共用表格与位序。
- **`lab4/code/task2/`**：多轮差分和线性搜索配置；求解结果保存在 `lab4/result_of_task2/`。

## 环境与报告

| 内容 | 所需工具 |
| --- | --- |
| 上方五个小例子 | Python 3 标准库 |
| 实验二的完整差分搜索 | NumPy、tqdm，具体见对应脚本导入 |
| 实验四优化模型 | Python 3.12+、Gurobi；逻辑化简另需 PyEDA |
| 重新生成凸包数据 | SageMath |
| 编译实验报告 | XeLaTeX、latexmk |

实验四依赖定义见 [pyproject.toml](lab4/code/task1/pyproject.toml)，已有凸包数据为 [hull_constraints.json](lab4/code/task1/convex_hull/hull_constraints.json)。五个模型脚本按自身位置导入公共表，直接运行脚本时不依赖当前工作目录。

报告在各自 `report/` 目录中编译。例如从仓库根目录执行：

```bash
make -C labs/lab3/report
```

生成文件位于对应报告的 `output/` 目录。报告中的图与附录源码保持实验内部的相对路径。

[返回项目首页](../README.md) · [课程笔记](../notes/README.md) · [复习资料](../review/README.md)
