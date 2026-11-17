# 六轮 Feistel 不可能差分动画

[观看立体图解动画](../../assets/animations/impossible-feistel-recovery.mp4) · [Manim 源码](impossible_feistel.py) · [相关笔记](../../notes/03-差分分析/不可能差分分析.md)

动画采用深色背景、逐步呈现的数学板书与彩色高亮，按轮内状态顺序 $(L_i,R_i)$ 讲解前五轮不可能差分，再扩展第六轮进行密钥筛选。前五轮交叉，第六轮不交换，直接得到密文 $c_i=(c_i^L,c_i^R)$。单独五轮的第 5 轮不交换，扩展为六轮后第 5 轮成为中间轮并交叉。音频由微软中文神经语音生成，旁白文字在 `narration/script.json`。

## 重现动画

在仓库根目录使用 Python 3.12、Manim Community 0.19.2、FFmpeg 和 `Heiti SC` 字体运行：

```bash
manim -qh --disable_caching animations/impossible_feistel/impossible_feistel.py ImpossibleFeistel
```

动画依赖 `narration/` 里的 MP3 文件，并按各段长度同步画面。

## 数值例子

每半支 4 比特，$f(x,k)=S(x\oplus k)$，S 盒以十六进制表示为

```text
S = [C, 5, 6, B, 9, 0, A, D, 3, E, F, 8, 4, 7, 1, 2]
轮密钥 = [1, 5, 3, 7, 2, 9]
```

对于 $m_i=(0,0)$、$m_j=(9,0)$，直接输出的密文为 $c_i=(3,1)$、$c_j=(F,8)$。猜测 $k_6=6$ 时，$f(1,6)=D$、$f(8,6)=1$，逆推第五轮末状态为 $(E,1)$ 和 $(E,8)$，其差分为 $(0,9)$，因此删除候选 6。枚举全部 16 个末轮候选可知，这一对还会排除 F；真实末轮子密钥 9 留存。其余候选需要更多数据继续筛选，并结合其他密钥做完整加密验证。
