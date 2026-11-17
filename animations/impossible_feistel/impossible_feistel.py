"""六轮 Feistel 不可能差分密钥恢复，四比特实算示例。"""
from pathlib import Path
import subprocess
import numpy as np
from manim import *

config.background_color='#10131E'
config.frame_rate=24
HERE=Path(__file__).resolve().parent
VOICE=HERE/'narration'
FONT='Heiti SC'
WHITE='#F2F1EA'; MUTED='#AAB6C7'; TEAL='#67D8B5'; BLUE='#65A8EF'
AMBER='#FFD36A'; VIOLET='#BF9AF2'; RED='#F57775'; PANEL='#10131E'; EDGE='#394658'

def text(s,size=26,color=WHITE,bold=False):
    return Text(s,font=FONT,font_size=size,color=color,weight=BOLD if bold else NORMAL)
def fit(mob,w):
    if mob.width>w: mob.scale_to_fit_width(w)
    return mob
def box(w,h,color=PANEL,stroke=EDGE):
    return RoundedRectangle(corner_radius=.09,width=w,height=h,fill_color=color,fill_opacity=1,stroke_color=stroke,stroke_width=1.2)
def tx(s,x,y,size=24,color=WHITE): return text(s,size,color).move_to([x,y,0])
def block(s,x,y,color):
    w=.76;h=.29;d=.12;e=.08
    l=x-w/2;r=x+w/2;b=y-h/2;t=y+h/2
    top=Polygon([l,t,0],[r,t,0],[r+d,t+e,0],[l+d,t+e,0],fill_color='#375D70',fill_opacity=1,stroke_color=color,stroke_width=1.1)
    side=Polygon([r,b,0],[r,t,0],[r+d,t+e,0],[r+d,b+e,0],fill_color='#19374A',fill_opacity=1,stroke_color=color,stroke_width=1.1)
    front=Polygon([l,b,0],[r,b,0],[r,t,0],[l,t,0],fill_color='#23475B',fill_opacity=1,stroke_color=color,stroke_width=1.5)
    label=fit(text(s,19,color),.66).move_to([x,y,0])
    return VGroup(top,side,front,label)
def wire(a,b,color=MUTED,width=2):
    return Line([*a,0],[*b,0],color=color,stroke_width=width,stroke_opacity=.8)

class ImpossibleFeistel(Scene):
    def panel_stage(self,n,title,lines,formulas,caption):
        # A clean board replaces stacked cards. Each line is revealed in time with the voice.
        index=text(f'{n:02d}  /  09',19,MUTED).move_to([1.48,2.17,0],aligned_edge=LEFT)
        heading=fit(text(title,33,WHITE,True),4.65).move_to([1.48,1.70,0],aligned_edge=LEFT)
        sep=Line([1.48,1.35,0],[6.20,1.35,0],color=EDGE,stroke_width=1)
        accent=Line([1.48,-.56,0],[2.30,-.56,0],color=TEAL,stroke_width=2.4)
        header=VGroup(index,heading,sep,accent)
        if hasattr(self,'stage_objects'):
            self.play(*[FadeOut(obj) for obj in self.stage_objects],FadeIn(header,shift=UP*.05),run_time=.30)
        else:
            self.play(FadeIn(header,shift=UP*.05),run_time=.30)
        self.stage_objects=[header]
        body=VGroup(*[fit(text(line,24,MUTED),4.72) for line in lines]).arrange(DOWN,aligned_edge=LEFT,buff=.20).move_to([1.48,1.08,0],aligned_edge=UL)
        self.body_items=list(body)
        palette={'α':AMBER, 'β':BLUE, 'γ':VIOLET, 'δ':RED, 'κ':AMBER, '↛':RED}
        eq=VGroup(*[fit(Text(line,font=FONT,font_size=27,color=WHITE,t2c=palette),4.70) for line in formulas]).arrange(DOWN,buff=.16).move_to([3.86,-1.35,0])
        self.formula_items=list(eq)
        cb=Line([-6.45,-3.17,0],[6.45,-3.17,0],color=EDGE,stroke_width=1)
        ct=fit(text(caption,22,WHITE),12.6).move_to([0,-3.47,0])
        cap=VGroup(cb,ct)
        if hasattr(self,'cap'):self.play(ReplacementTransform(self.cap,cap),run_time=.20)
        else:self.play(FadeIn(cap),run_time=.20)
        self.cap=cap
        self.add_sound(str(VOICE/f'{n:02d}.mp3'))
        self.audio_start=self.time
        self.audio_duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(VOICE/f'{n:02}.mp3')],text=True))
        self.reveal_body(0)
    def show_line(self, mob):
        self.play(FadeIn(mob,shift=UP*.06),run_time=.28)
        self.stage_objects.append(mob)
    def reveal_body(self,i): self.show_line(self.body_items[i])
    def reveal_eq(self,i): self.show_line(self.formula_items[i])
    def cue(self,fraction):
        t=self.audio_start+fraction*self.audio_duration-self.time
        if t>0:self.wait(t)
    def marker(self,top,bottom,color,label):
        yy=(top+bottom)/2
        a=RoundedRectangle(corner_radius=.08,width=4.12,height=top-bottom,stroke_color=color,stroke_width=2.4,fill_color=color,fill_opacity=.045).move_to([-4.08,yy,0])
        tag=fit(text(label,18,color,True),1.2).move_to([-1.22,yy,0])
        obj=VGroup(a,tag)
        if hasattr(self,'highlight'):
            self.play(FadeOut(self.highlight),FadeIn(obj),run_time=.5)
        else:self.play(FadeIn(obj),run_time=.5)
        self.highlight=obj
    def flow(self, rounds, reverse=False):
        # Two tokens follow the Feistel branches, one round at a time.
        xL, xR = -5.42, -2.70
        for i in rounds:
            top, bottom = self.bounds[i], self.bounds[i+1]
            mid = (top + bottom) / 2
            # The first five rounds exchange branches; round six does not.
            out_l, out_r = (xR, xL) if i < 5 else (xL, xR)
            paths = [
                [[xL,top,0], [xL,mid,0], [out_l,bottom,0]],
                [[xR,top,0], [xR,mid,0], [out_r,bottom,0]],
            ]
            if reverse:
                paths = [list(reversed(path)) for path in paths]
            dots = [Dot(path[0], radius=.06, color=VIOLET if reverse else TEAL).set_z_index(10) for path in paths]
            curves = [VMobject().set_points_as_corners([np.array(p) for p in path]) for path in paths]
            self.add(*dots)
            self.play(*[MoveAlongPath(dot,curve,rate_func=linear) for dot,curve in zip(dots,curves)], run_time=.62)
            self.remove(*dots)
    def diagram(self):
        self.add(text('不可能差分 · 六轮 Feistel 密钥恢复',35,WHITE,True).move_to([-6.45,3.52,0],aligned_edge=LEFT))
        self.add(text('找到矛盾 → 逆推末轮 → 排除候选',20,MUTED).move_to([6.35,3.52,0],aligned_edge=RIGHT))
        self.add(Line([-6.5,3.13,0],[6.5,3.13,0],color=EDGE,stroke_width=1))
        xL=-5.42; xR=-2.70; xf=-3.90
        bounds=[2.28-i*.67 for i in range(7)]
        self.add(tx('mᵢᴸ',xL,2.55,24,TEAL),tx('mᵢᴿ',xR,2.55,24,TEAL))
        self.add(fit(text('每个 f(·, kᵢ) 为双射',19,MUTED),3.8).move_to([-4.06,2.83,0]))
        for i in range(6):
            top=bounds[i];bottom=bounds[i+1];mid=(top+bottom)/2; col=TEAL if i<5 else AMBER
            # f takes the right branch; its output is XORed into the left.
            # The first five rounds swap; the sixth goes straight to ciphertext.
            out_l, out_r = (xR, xL) if i < 5 else (xL, xR)
            pieces=[wire((xL,top),(xL,mid+.11)),wire((xR,top),(xR,mid)),wire((xR,mid),(xf+.38,mid)),wire((xf-.38,mid),(xL+.13,mid)),wire((xL,mid-.11),(out_l,bottom)),wire((xR,mid),(out_r,bottom))]
            self.add(*pieces)
            self.add(Dot([xR,mid,0],radius=.033,color=col))
            xor=Circle(radius=.11,stroke_color=col,stroke_width=1.6,fill_color=config.background_color,fill_opacity=1).move_to([xL,mid,0])
            cross=tx('+',xL,mid,18,col)
            self.add(xor,cross,block('f',xf,mid,col))
            self.add(tx('k'+'₁₂₃₄₅₆'[i],xf,mid+.28,15,col))
            self.add(tx(f'第 {i+1} 轮',-6.25,mid,19,col))
        self.add(tx('cᵢᴸ',xL,-1.99,22,AMBER),tx('cᵢᴿ',xR,-1.99,22,AMBER))
        self.add(fit(text('第六轮不交换，直接输出密文',20,MUTED),4.8).move_to([-4.06,-2.36,0]))
        self.bounds=bounds
    def construct(self):
        self.diagram(); b=self.bounds
        self.panel_stage(1,'先找五轮的禁忌',['单独五轮：第 5 轮不交换','扩展六轮：第 5 轮后交叉','分析第 5 轮交叉后的状态'],['单独五轮： (α, 0) ↛ (α, 0)','六轮中前五轮： (α, 0) ↛ (0, α)'],'单独五轮与扩展六轮的观察位置不同：第 5 轮之后是否交叉。')
        self.marker(b[0]+.07,b[5]-.04,TEAL,'五轮核心')
        self.cue(.20);self.reveal_body(1)
        self.cue(.40);self.reveal_body(2)
        self.cue(.55);self.reveal_eq(0)
        self.cue(.73);self.reveal_eq(1);self.cue(1)

        self.panel_stage(2,'从输入正推两轮',['选输入差分 (α, 0)，α ≠ 0','第一轮后： (0, α)','第二轮后： (α, β)，β ≠ 0'],['第二轮末左支差分 = α'],'前向两轮：在第二轮结束时，左半支差分必定为 α。')
        self.marker(b[0]+.07,b[2]-.03,TEAL,'正推两轮')
        self.cue(.22);self.flow(range(1));self.reveal_body(1)
        self.cue(.42);self.flow(range(1,2));self.reveal_body(2)
        self.cue(.60);self.reveal_eq(0)
        self.forward_proof=fit(text('正推：α',22,TEAL,True),1.65).move_to([-1.08,1.04,0])
        self.play(FadeIn(self.forward_proof),run_time=.35);self.cue(1)

        self.panel_stage(3,'从输出逆推三轮',['假设第五轮末差分为 (0, α)','逆推： (α, 0) → (γ, α)','再逆推： (α ⊕ δ, γ)，δ ≠ 0'],['同一位置左支： α ≠ α ⊕ δ','因此五轮差分不可能'],'正推与逆推对第二轮末左半支提出矛盾要求。')
        self.marker(b[2]+.04,b[5]-.04,VIOLET,'逆推三轮')
        self.cue(.24);self.flow(range(4,2,-1),True);self.reveal_body(1)
        self.cue(.47);self.flow([2],True);self.reveal_body(2)
        self.reverse_proof=fit(text('逆推：α ⊕ δ',22,VIOLET,True),2.05).move_to([-1.08,.69,0])
        self.play(FadeIn(self.reverse_proof),run_time=.35)
        self.cue(.69);self.reveal_eq(0)
        self.play(Indicate(self.forward_proof,color=RED,scale_factor=1.10),Indicate(self.reverse_proof,color=RED,scale_factor=1.10),run_time=.8)
        self.cue(.85);self.reveal_eq(1);self.cue(1)
        self.play(FadeOut(self.forward_proof),FadeOut(self.reverse_proof),run_time=.3)

        self.panel_stage(4,'扩展一轮并采样',['选择明文 mᵢ、mⱼ','明文对差分：mᵢ ⊕ mⱼ = (α, 0)','查询六轮加密得到 cᵢ、cⱼ'],['前五轮交叉，第六轮不交换'],'选择明文对并加密；第六轮两支直接输出为密文。')
        self.marker(b[0]+.07,b[6]-.04,BLUE,'六轮加密')
        self.cue(.20);self.reveal_body(1)
        self.cue(.35);self.flow(range(6));self.reveal_body(2)
        self.cue(.74);self.reveal_eq(0);self.cue(1)

        self.panel_stage(5,'先筛选数据对',['先检查密文右半支差分','不符合条件的数据对直接跳过','此时还没有猜测任何密钥'],['ΔR₅ = cᵢᴿ ⊕ cⱼᴿ','只保留： cᵢᴿ ⊕ cⱼᴿ = α'],'只有密文右半边差分为 α 的数据对，才可能触发禁忌差分。')
        self.marker(b[5]+.05,b[6]-.04,AMBER,'数据预筛')
        self.cue(.18);self.reveal_body(1)
        self.cue(.30);self.reveal_eq(0)
        self.cue(.58);self.reveal_eq(1)
        self.cue(.75);self.reveal_body(2);self.cue(1)

        self.panel_stage(6,'猜测末轮子密钥',['枚举第六轮子密钥候选 k₆','用候选值逆去 cᵢ 和 cⱼ 的第六轮','左支差分为 0 时，删除候选'],['R₅,ᵢ = cᵢᴿ','L₅,ᵢ = cᵢᴸ ⊕ f(cᵢᴿ, k₆)','f(cᵢᴿ,k₆) ⊕ f(cⱼᴿ,k₆) = cᵢᴸ ⊕ cⱼᴸ'],'对每个子密钥候选，逆推末轮并检查左半支差分。')
        self.marker(b[5]+.05,b[6]-.04,VIOLET,'逆推末轮')
        self.cue(.26);self.reveal_body(1);self.flow([5],True)
        self.cue(.48);self.reveal_eq(0)
        self.cue(.62);self.reveal_body(2)
        self.cue(.68);self.reveal_eq(1)
        self.cue(.84);self.reveal_eq(2);self.cue(1)

        self.panel_stage(7,'具体算一对数据',['四比特半支；数字均为十六进制','mᵢ = (0,0)，mⱼ = (9,0)，α = 9','cᵢ = (3,1)，cⱼ = (F,8)'],['cᵢᴿ ⊕ cⱼᴿ = 1 ⊕ 8 = 9','k₆ = 6：f(1,6) ⊕ f(8,6) = D ⊕ 1 = C','cᵢᴸ ⊕ cⱼᴸ = 3 ⊕ F = C'],'通过数据预筛后，候选 6 满足末轮排除方程。')
        self.cue(.13);self.reveal_body(1)
        self.cue(.28);self.reveal_body(2)
        self.cue(.46);self.reveal_eq(0)
        self.cue(.64);self.reveal_eq(1)
        self.cue(.85);self.reveal_eq(2)
        flag=fit(text('命中排除方程',19,RED,True),1.8).move_to([-1.24,-.99,0])
        self.play(FadeIn(flag),run_time=.4);self.cue(1);self.play(FadeOut(flag),run_time=.2)

        self.panel_stage(8,'命中禁忌：删除',['猜测 k₆ = 6：逆推得 (E,1)、(E,8)','第五轮末差分变成 (0,9)','与五轮不可能差分矛盾'],['ΔL₅ = 0，ΔR₅ = 9','因此删除候选 k₆ = 6'],'触发禁忌差分的候选密钥一定错误，直接删除。')
        self.marker(b[5]+.05,b[6]-.04,RED,'删除 k₆ = 6')
        self.cue(.26);self.reveal_body(1);self.reveal_eq(0)
        self.cue(.56);self.reveal_body(2)
        self.cue(.78);self.reveal_eq(1)
        self.play(Indicate(self.formula_items[1],color=RED,scale_factor=1.06),run_time=.7);self.cue(1)

        self.panel_stage(9,'继续筛选与验证',['本数据对排除 6、F；真实 9 留存','更多数据对继续排除错误候选','结合其余密钥进行完整加密验证'],['满足排除方程 → 删除候选','剩余候选 → 完整加密验证'],'更多数据对继续筛选，结合其余密钥验证剩余候选。')
        self.marker(b[5]+.05,b[6]-.04,TEAL,'继续验证')
        self.cue(.34);self.reveal_eq(0)
        self.cue(.53);self.reveal_body(1)
        self.cue(.68);self.reveal_body(2)
        self.cue(.80);self.reveal_eq(1);self.cue(1);self.wait(.5)
