# 经典飞去来器攻击动画

视频按课件的经典飞去来器区分器，展示选择明文、加密、构造密文差分、查询解密、中间四元组连接、差分回传与统计判定。中文旁白放在 `narration/`，对应文本为 `narration/script.json`。

- [观看四轨立体图解版](../../assets/animations/classic-boomerang-diagram.mp4)
- [四轨立体图解版源码](continuous_boomerang.py)
- [观看原版动画](../../assets/animations/classic-boomerang.mp4)
- [动画源码](classic_boomerang.py)
- [飞去来器攻击笔记](../../notes/03-差分分析/飞去来器攻击.md)

## 重新渲染

需要 Python 3.12、Manim Community 0.19.2、FFmpeg 和中文字体（脚本使用 `Heiti SC`）。在仓库根目录运行：

```bash
python3.12 -m venv /tmp/boomerang-manim
/tmp/boomerang-manim/bin/pip install manim==0.19.2
/tmp/boomerang-manim/bin/manim -qh --fps 24 \
  animations/boomerang/classic_boomerang.py ClassicBoomerang
```

四轨立体图解版可将上方命令中的脚本和场景名换成 `animations/boomerang/continuous_boomerang.py BoomerangContinuous`；旁白在 `narration-v2/`，使用微软中文神经语音 Xiaoxiao，按课件画出四条完整轨道和对应的 γ、φ 边。

脚本自动读取旁白文件，并根据对应音频长度安排镜头。原版需要静音时，可暂时将 `narration/` 中的 MP3 移出；此时画面使用默认停留时间。四轨版需要保留 `narration-v2/` 中的音频。

## 符号

- $E=E_b\circ A\circ E_f$，连接层 $A$ 为可逆线性或仿射变换。
- 前段正向 $\alpha\to\beta$ 概率 $p_1$，返回时 $\beta\to\alpha$ 概率 $p_2$；后段逆向 $\gamma\to\phi$ 概率 $q$。
- 构造 $C_3=C_1\oplus\gamma$、$C_4=C_2\oplus\gamma$，通过真实解密接口获取 $P_3,P_4$。
- 在课件的独立近似下，视频所示这条路线的成功概率约为 $p_1p_2q^2$；随机置换基准约为 $2^{-n}$，并排除退化四元组。
