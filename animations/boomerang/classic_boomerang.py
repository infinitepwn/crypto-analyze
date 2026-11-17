"""Manim: 经典飞去来器攻击。中文语音在 narration/，可禁用音频单独渲染。"""
from pathlib import Path
import json
import subprocess
from manim import *

config.background_color = '#0B1726'
config.frame_rate = 24

BASE = Path(__file__).resolve().parent
VOICE = BASE / 'narration'
FONT = 'Heiti SC'
WHITE = '#EAF3F7'
MUTED = '#A3B8C7'
TEAL = '#66D9C0'
BLUE = '#7CBCEE'
AMBER = '#F4BD75'
RED = '#F29491'
PANEL = '#12283A'
EDGE = '#36546A'


def txt(s, size=31, color=WHITE, weight=NORMAL):
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def fit(mob, width):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def panel(w, h, color=PANEL, stroke=EDGE, radius=0.15):
    return RoundedRectangle(width=w, height=h, corner_radius=radius,
        stroke_color=stroke, stroke_width=1.4, fill_color=color, fill_opacity=1)


def card(label, position, color=WHITE, width=1.9, height=.68):
    box = panel(width, height)
    text = txt(label, 30, color, BOLD)
    text.move_to(box.get_center())
    return VGroup(box, text).move_to(position)


def rule(x1, y1, x2, y2, color=MUTED, double=False):
    cls = DoubleArrow if double else Arrow
    return cls(np.array([x1,y1,0]), np.array([x2,y2,0]),
               buff=0, stroke_width=2.8, max_tip_length_to_length_ratio=0.14, color=color)


def eqline(s, y, color=WHITE, size=31, x=0, maxwidth=12.8):
    return fit(txt(s, size, color), maxwidth).move_to([x,y,0])


def tag(s, pos, color, width=1.8):
    shape = panel(width,.44,'#1C3648',color,.17)
    label = fit(txt(s,19,color,BOLD),width-.18)
    label.move_to(shape.get_center())
    return VGroup(shape,label).move_to(pos)


class ClassicBoomerang(Scene):
    def title(self, number, heading, sub):
        left = txt(heading, 37, WHITE, BOLD).move_to([-6.50,3.43,0], aligned_edge=LEFT)
        right = txt(f'{number:02d}  /  07', 23, TEAL).move_to([6.45,3.43,0],aligned_edge=RIGHT)
        bar = Line([-6.5,3.04,0],[6.5,3.04,0],stroke_width=1,color=EDGE)
        context = txt(sub, 21, MUTED).move_to([-6.50,2.76,0],aligned_edge=LEFT)
        self.play(FadeIn(left,shift=DOWN*.08),FadeIn(right),Create(bar),FadeIn(context),run_time=.55)

    def caption(self, s):
        shape=panel(12.9,.58,'#172D3D','#254356',.11).move_to([0,-3.43,0])
        content=fit(txt(s,23,WHITE),12.35).move_to(shape.get_center())
        nxt=VGroup(shape,content)
        if getattr(self,'cap',None) is None:
            self.play(FadeIn(nxt),run_time=.3)
        else:
            self.play(ReplacementTransform(self.cap,nxt),run_time=.3)
        self.cap=nxt

    def voice(self,n):
        path=VOICE/f'{n:02d}.mp3'
        self.vstart=self.time
        if path.exists():
            self.add_sound(str(path))
            raw=subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(path)],text=True)
            self.dur=float(raw.strip())
        else:
            self.dur=15

    def cue(self, portion):
        remaining = self.vstart + self.dur * portion - self.time
        if remaining > 0: self.wait(remaining)

    def finish_act(self):
        self.cue(1.03)
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)],run_time=.4)
        self.cap=None

    def quartet(self, prefix, positions=None, colors=None):
        if positions is None:
            positions=[[-2.45,1.25,0],[2.45,1.25,0],[-2.45,-.75,0],[2.45,-.75,0]]
        if colors is None: colors=[WHITE]*4
        indices = ['₁', '₂', '₃', '₄']
        return [card(f'{prefix}{indices[i]}',positions[i],colors[i],width=2.0,height=.78) for i in range(4)]

    def construct(self):
        self.cap=None
        self.part1();self.part2();self.part3();self.part4();self.part5();self.part6();self.part7()

    def part1(self):
        self.title(1,'飞去来器攻击','把两段短差分连接成一个四元组')
        self.voice(1)
        self.caption('将加密过程拆成前段、连接层和后段。')
        formula=eqline('E = E_b  ∘  A  ∘  E_f',2.12,WHITE,35)
        boxes=[card('前段  E_f',[-4.15,.66,0],TEAL,3.0,.9),card('连接层  A',[0,.66,0],WHITE,3.0,.9),card('后段  E_b',[4.15,.66,0],AMBER,3.0,.9)]
        arrows=[rule(-2.5,.66,-1.65,.66),rule(1.65,.66,2.5,.66)]
        self.play(Write(formula),*[FadeIn(b,shift=UP*.15) for b in boxes],*[GrowArrow(a) for a in arrows],run_time=1.5)
        self.cue(.34); self.caption('两段有各自的差分，中间不必在同一对文本上直接相接。')
        left=eqline('α  →  β',-.64,TEAL,43,-4.15)
        right=eqline('φ  →  γ',-.64,AMBER,43,4.15)
        hint=eqline('四个文本 · 上段横边 · 下段竖边',-1.74,MUTED,27)
        self.play(Write(left),Write(right),FadeIn(hint),run_time=1)
        self.finish_act()

    def part2(self):
        self.title(2,'第一步 · 选择明文并加密','已知：前段差分 α → β，正向概率 p₁')
        self.voice(2);self.caption('选择 P₁、P₂，使它们的输入差分等于 α。')
        p1=card('P₁',[-3.15,1.45,0],TEAL);p2=card('P₂',[3.15,1.45,0],TEAL)
        edge=rule(-2.08,1.45,2.08,1.45,TEAL,True); el=eqline('α',1.86,TEAL,29)
        self.play(FadeIn(p1),FadeIn(p2),GrowArrow(edge),Write(el),run_time=1)
        self.cue(.27); self.caption('查询完整加密算法，得到 C₁ 和 C₂。')
        e1=card('E',[-3.15,.35,0],WHITE,.8,.56);e2=card('E',[3.15,.35,0],WHITE,.8,.56)
        c1=card('C₁',[-3.15,-.85,0],AMBER);c2=card('C₂',[3.15,-.85,0],AMBER)
        arrows=[rule(-3.15,1.02,-3.15,.68),rule(3.15,1.02,3.15,.68),rule(-3.15,.02,-3.15,-.42),rule(3.15,.02,3.15,-.42)]
        self.play(FadeIn(e1),FadeIn(e2),*[GrowArrow(a) for a in arrows],FadeIn(c1),FadeIn(c2),run_time=1.2)
        self.cue(.61);self.caption('前段命中时，x₁ ⊕ x₂ = β；这是概率事件。')
        note=tag('命中事件', [0,-.72,0], BLUE,1.8)
        detail=eqline('x₁ ⊕ x₂ = β     概率 p₁',-1.60,BLUE,31)
        internal=eqline('xᵢ = E_f(Pᵢ)  ·  内部状态用于分析',-2.16,MUTED,23)
        self.play(FadeIn(note),Write(detail),FadeIn(internal),run_time=.9)
        self.finish_act()

    def part3(self):
        self.title(3,'第二步 · 主动构造密文差分','伽马 γ 是上下对应密文之间的差分')
        self.voice(3);self.caption('将 C₁、C₂ 分别异或 γ，构造 C₃、C₄。')
        q=self.quartet('C',colors=[AMBER]*4)
        arrows=[rule(-2.45,.80,-2.45,-.30,AMBER,True),rule(2.45,.80,2.45,-.30,AMBER,True)]
        labels=[eqline('γ',.24,AMBER,28,-3.28),eqline('γ',.24,AMBER,28,3.28)]
        self.play(FadeIn(q[0]),FadeIn(q[1]),run_time=.6)
        self.cue(.25); self.play(FadeIn(q[2]),FadeIn(q[3]),*[GrowArrow(a) for a in arrows],*[Write(t) for t in labels],run_time=1.3)
        self.cue(.55); self.caption('C₁ ⊕ C₃ = γ，C₂ ⊕ C₄ = γ；两条竖边由我们主动设定。')
        eq=eqline('C₃ = C₁ ⊕ γ        C₄ = C₂ ⊕ γ',-1.75,WHITE,29)
        caution=eqline('C₁ 与 C₂ 的差分未被指定为 γ',-2.27,MUTED,24)
        self.play(Write(eq),FadeIn(caution),run_time=1)
        self.finish_act()

    def part4(self):
        self.title(4,'第三步 · 解密并分析后段','解密接口给出明文；中间状态仅用于分析')
        self.voice(4);self.caption('把 C₃、C₄ 送入解密接口，得到 P₃、P₄。')
        left=eqline('C₃   ── D ──→   P₃',1.75,WHITE,36,-3.05,5.7)
        right=eqline('C₄   ── D ──→   P₄',1.75,WHITE,36,3.05,5.7)
        self.play(Write(left),Write(right),run_time=1.2)
        self.cue(.31); self.caption('两条后段逆向差分命中时，内部 y 状态的竖边均为 φ。')
        q=self.quartet('y',positions=[[-2.45,.65,0],[2.45,.65,0],[-2.45,-1.10,0],[2.45,-1.10,0]],colors=[BLUE]*4)
        arrows=[rule(-2.45,.2,-2.45,-.65,AMBER,True),rule(2.45,.2,2.45,-.65,AMBER,True)]
        labels=[eqline('φ',-.22,AMBER,29,-3.3),eqline('φ',-.22,AMBER,29,3.3)]
        self.play(*[FadeIn(x,shift=UP*.1) for x in q],*[GrowArrow(x) for x in arrows],*[Write(x) for x in labels],run_time=1.4)
        self.cue(.67)
        note=eqline('y₁ ⊕ y₃ = y₂ ⊕ y₄ = φ     每条概率 q',-2.13,AMBER,27)
        definition=eqline('yᵢ = A(xᵢ) = E_b⁻¹(Cᵢ)   ·   内部状态',-2.65,MUTED,22)
        self.play(Write(note),FadeIn(definition),run_time=.9)
        self.finish_act()

    def part5(self):
        self.title(5,'第四步 · 中间四元组连接','连接层 A 为可逆线性或仿射变换')
        self.voice(5);self.caption('两条竖边差分相同，四个 y 状态异或和为 0。')
        top=eqline('y₁ ⊕ y₃ = φ      y₂ ⊕ y₄ = φ',1.93,AMBER,33)
        eq=eqline('y₁ ⊕ y₂ ⊕ y₃ ⊕ y₄ = 0',1.18,WHITE,33)
        self.play(Write(top),Write(eq),run_time=1.3)
        self.cue(.35);self.caption('通过可逆线性或仿射连接层，x 状态也满足四元组关系。')
        bridge=tag('跨越连接层 A', [0,.48,0],TEAL,2.5)
        xeq=eqline('x₁ ⊕ x₂ ⊕ x₃ ⊕ x₄ = 0',-.16,BLUE,33)
        self.play(FadeIn(bridge),Write(xeq),run_time=1)
        self.cue(.67);self.caption('因此 x₃ ⊕ x₄ = x₁ ⊕ x₂；前段命中时它等于 β。')
        bottom=eqline('x₃ ⊕ x₄  =  x₁ ⊕ x₂  =  β',-1.15,TEAL,38)
        note=eqline('两段差分成立时，在连接处形成平行四边形',-2.02,MUTED,23)
        self.play(Write(bottom),FadeIn(note),run_time=1.1)
        self.finish_act()

    def part6(self):
        self.title(6,'第五步 · 回到明文','前段逆向：β → α，概率记为 p₂')
        self.voice(6);self.caption('x₃ ⊕ x₄ = β 时，前段逆向差分命中可得到 α。')
        upper=eqline('x₃ ⊕ x₄ = β    ── E_f⁻¹ ──→    P₃ ⊕ P₄ = α',1.67,BLUE,32)
        self.play(Write(upper),run_time=1)
        self.cue(.38); self.caption('前段正向一条、后段逆向两条、前段反向一条。')
        tags=VGroup(tag('正向  p₁',[-4.6,.36,0],TEAL,2.0),tag('逆向  q',[-1.55,.36,0],AMBER,2.0),tag('逆向  q',[1.55,.36,0],AMBER,2.0),tag('反向  p₂',[4.6,.36,0],BLUE,2.0))
        self.play(LaggedStart(*[FadeIn(t,shift=UP*.15) for t in tags],lag_ratio=.2),run_time=1.2)
        self.cue(.61); self.caption('课件的独立近似下，整条成功路线约为 p₁p₂q²。')
        formula=eqline('P ≈ p₁ · p₂ · q²',-1.02,WHITE,44)
        simpl=eqline('若 p₁ = p₂ = p，则 P ≈ p²q²',-1.79,TEAL,29)
        self.play(Write(formula),FadeIn(simpl,shift=UP*.1),run_time=1.1)
        self.finish_act()

    def part7(self):
        self.title(7,'第六步 · 统计与验证','重复测试四元组，建立飞去来器区分器')
        self.voice(7);self.caption('统计 P₃ ⊕ P₄ = α 的命中次数，并与随机基准比较。')
        question=eqline('检验：P₃ ⊕ P₄  是否等于  α ?',1.89,WHITE,36)
        left=card('目标密码 · 此路线',[-3.12,.66,0],TEAL,3.8,.78)
        right=card('随机置换',[3.12,.66,0],BLUE,3.8,.78)
        lval=eqline('≈ p₁p₂q²',-.12,TEAL,35,-3.12)
        rval=eqline('≈ 2⁻ⁿ',-.12,BLUE,35,3.12)
        self.play(Write(question),FadeIn(left),FadeIn(right),Write(lval),Write(rval),run_time=1.4)
        self.cue(.43);self.caption('排除重复文本造成的退化情形；差异明显则可以区分。')
        n1=eqline('非零 α、γ；排除 C₁ ⊕ C₂ = γ 的退化对',-1.01,MUTED,24)
        self.play(FadeIn(n1),run_time=.6)
        self.cue(.7);self.caption('进一步扩轮、猜子密钥并统计候选，才能进行密钥恢复。')
        result=eqline('区分器   →   扩展轮   →   猜密钥   →   验证',-2.10,TEAL,29)
        self.play(Write(result),run_time=1.0)
        self.finish_act()
