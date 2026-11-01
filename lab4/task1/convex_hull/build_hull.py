"""用SageMath计算DDT、LAT合法点集的凸包，保存完整H表示。"""

import json
import sys
from math import gcd, lcm
from pathlib import Path

# 配置导入路径，复用task1中的表格计算与八位编码函数。
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sage.all import Polyhedron, QQ

from ddt_lat import SIZE, bits, compute_ddt, compute_lat


def integer_row(row):
    """乘以正的公分母，再约去最大公因数，得到同向的整数系数。"""
    scale = lcm(*(int(value.denominator()) for value in row))
    coefficients = [int(value * scale) for value in row]
    divisor = gcd(*coefficients) or 1
    return [value // divisor for value in coefficients]


def build_hull(table):
    """将非零表项编码为合法点，并提取其凸包的等式与不等式。"""
    points = [bits(a, b) for a in range(SIZE) for b in range(SIZE)
              if table[a][b] != 0]

    # QQ使用精确有理数；坐标依次为(a3,a2,a1,a0,b3,b2,b1,b0)。
    hull = Polyhedron(vertices=points, base_ring=QQ)

    # 每行按[c0,c1,...,c8]保存，对应c0+sum(cj*zj)>=0或=0。
    return {
        "inequalities": sorted(integer_row(row)
                               for row in hull.inequalities_list()),
        "equations": sorted(integer_row(row)
                            for row in hull.equations_list()),
    }


if __name__ == "__main__":
    hulls = {}
    for name, table in (("DDT", compute_ddt()), ("LAT", compute_lat())):
        hulls[name] = build_hull(table)
        print(f"{name}凸包：不等式数={len(hulls[name]['inequalities'])}，"
              f"等式数={len(hulls[name]['equations'])}")

    # 将两种模型的完整H表示写入同一份JSON，供求解脚本读取。
    output = Path(__file__).resolve().with_name("hull_constraints.json")
    output.write_text(json.dumps(hulls, indent=2) + "\n", encoding="utf-8")
    print(f"约束已保存到：{output}")
