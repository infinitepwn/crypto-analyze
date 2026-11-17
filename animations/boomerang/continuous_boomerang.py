"""连续四轨图：经典飞去来器区分器。"""
from pathlib import Path
import subprocess
from manim import *

config.background_color = '#091522'
config.frame_rate = 24
ROOT = Path(__file__).resolve().parent
VOICE = ROOT / 'narration-v2'
FONT = 'Heiti SC'
INK = '#EDF4FA'
MUTED = '#97AEC0'
TEAL = '#67E0C2'
BLUE = '#81C6FF'
ORANGE = '#FFBD74'
VIOLET = '#C5A7FF'
DARK = '#11283A'
BORDER = '#365167'

def text(s, size=27, color=INK, weight=NORMAL):
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)

def fit(obj, width):
    if obj.width > width:
        obj.scale_to_fit_width(width)
    return obj

def rect(w, h, fill=DARK, stroke=BORDER):
    return RoundedRectangle(corner_radius=.10, width=w, height=h,
        fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=1.4)

def center_text(s, x, y, size=25, color=INK):
    return text(s, size, color).move_to([x,y,0])

def small_box(s,x,y,color):
    # Orthographic projection of an extruded block: top and side faces make
    # the depth visible while leaving the equation labels front-facing.
    left,right=x-.43,x+.43
    bottom,top=y-.19,y+.19
    dx,dy=.16,.11
    shadow=Polygon([left+.09,bottom-.09,0],[right+.11,bottom-.09,0],
                   [right+dx+.10,bottom+dy-.09,0],[left+dx+.08,bottom+dy-.09,0],
                   fill_color='#040D15',fill_opacity=.65,stroke_opacity=0)
    top_face=Polygon([left,top,0],[right,top,0],[right+dx,top+dy,0],[left+dx,top+dy,0],
                     fill_color='#385E70',fill_opacity=1,stroke_color=color,stroke_width=1.3)
    side=Polygon([right,bottom,0],[right,top,0],[right+dx,top+dy,0],[right+dx,bottom+dy,0],
                 fill_color='#1A3649',fill_opacity=1,stroke_color=color,stroke_width=1.3)
    front=Polygon([left,bottom,0],[right,bottom,0],[right,top,0],[left,top,0],
                  fill_color='#24475A',fill_opacity=1,stroke_color=color,stroke_width=1.8)
    highlight=Line([left+.05,top-.035,0],[right-.05,top-.035,0],
                   stroke_color='#A2D8E4',stroke_opacity=.37,stroke_width=1)
    t=fit(text(s,22,color),.77).move_to([x,y,0])
    return VGroup(shadow,top_face,side,front,highlight,t)


def rail(x,color):
    # Three nested strokes give the wire a shaded cylindrical appearance.
    start=[x,1.83,0]
    end=[x,-1.41,0]
    shadow=Line([x+.045,1.80,0],[x+.045,-1.44,0],color='#030C14',stroke_width=9,stroke_opacity=.8)
    body=Line(start,end,color=color,stroke_width=5,stroke_opacity=.55)
    glint=Line([x-.02,1.83,0],[x-.02,-1.41,0],color=INK,stroke_width=1.2,stroke_opacity=.55)
    return VGroup(shadow,body,glint)

def label(s,x,y,color=INK):
    return center_text(s,x,y,23,color)

def link(xa,xb,y,s,color):
    a=DoubleArrow([xa+.28,y,0],[xb-.28,y,0],buff=0,color=color,
      stroke_width=3,max_tip_length_to_length_ratio=.14)
    t=center_text(s,(xa+xb)/2,y+.20,23,color)
    return VGroup(a,t)

class BoomerangContinuous(Scene):
    def caption(self,s):
        bg=rect(13,.54,'#172D3F','#29485B').move_to([0,-3.52,0])
        t=fit(text(s,23,INK),12.5).move_to(bg)
        group=VGroup(bg,t)
        if hasattr(self,'capt'):
            self.play(ReplacementTransform(self.capt,group),run_time=.25)
        else:
            self.play(FadeIn(group),run_time=.25)
        self.capt=group

    def stage(self,num,title,lines,formula,caption):
        bg=rect(4.75,4.53,'#102638','#2D4A60').move_to([4.05,.13,0])
        badge=text(f'{num:02d} / 08',20,TEAL).move_to([2.0,2.02,0],aligned_edge=LEFT)
        hd=fit(text(title,31,INK,BOLD),4.05).move_to([2.0,1.52,0],aligned_edge=LEFT)
        sep=Line([2.0,1.22,0],[6.10,1.22,0],color=BORDER,stroke_width=1)
        content=VGroup(*[fit(text(line,23,MUTED),4.05) for line in lines])
        content.arrange(DOWN,aligned_edge=LEFT,buff=.22).move_to([2.0,.8,0],aligned_edge=UL)
        fbg=rect(4.14,1.02,'#1B394A','#45687B').move_to([4.05,-1.28,0])
        flines=VGroup(*[fit(text(s,25,TEAL),3.8) for s in formula])
        flines.arrange(DOWN,buff=.13).move_to(fbg)
        panel=VGroup(bg,badge,hd,sep,content,fbg,flines)
        if hasattr(self,'side'):
            self.play(FadeOut(self.side),FadeIn(panel),run_time=.4)
        else:
            self.play(FadeIn(panel),run_time=.4)
        self.side=panel
        self.caption(caption)
        self.add_sound(str(VOICE/f'{num:02}.mp3'))
        self.start=self.time
        self.voice_duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(VOICE/f'{num:02}.mp3')],text=True))

    def pause_to(self,portion):
        t=self.start + self.voice_duration*portion-self.time
        if t>0: self.wait(t)

    def flow(self,indices,down=True):
        animations=[]
        dots=[]
        for i in indices:
            x=self.xs[i]
            a=np.array([x,2.00 if down else -1.60,0])
            b=np.array([x,-1.60 if down else 2.00,0])
            dot=Dot(a,radius=.075,color=TEAL if down else VIOLET).set_z_index(10)
            dots.append(dot)
            animations.append(MoveAlongPath(dot,Line(a,b),rate_func=linear))
        self.add(*dots)
        self.play(*animations,run_time=3.1)
        self.play(*[FadeOut(d) for d in dots],run_time=.2)

    def construct(self):
        title=text('飞去来器攻击 · 四轨全流程',36,INK,BOLD).move_to([-6.45,3.53,0],aligned_edge=LEFT)
        subtitle=text('前进、折返，再观察是否回到原来的差分',21,MUTED).move_to([6.35,3.53,0],aligned_edge=RIGHT)
        bar=Line([-6.5,3.12,0],[6.5,3.12,0],color=BORDER,stroke_width=1)
        self.add(title,subtitle,bar)
        self.xs=[-5.95,-4.12,-2.29,-.46]
        xs=self.xs
        # The middle values are analytical states. The four lanes remain visible throughout.
        self.add(text('正向加密',19,TEAL).move_to([-5.95,2.83,0]),text('逆向解密',19,VIOLET).move_to([-4.12,2.83,0]),text('正向加密',19,TEAL).move_to([-2.29,2.83,0]),text('逆向解密',19,VIOLET).move_to([-.46,2.83,0]))
        sub=['₁','₃','₂','₄']
        for j,x in enumerate(xs):
            down=j in (0,2)
            c=TEAL if down else VIOLET
            self.add(rail(x,c))
            for name,y in [('P',2.04),('x',.84),('y',-.36),('C',-1.56)]:
                obj=label(name+sub[j],x,y,INK)
                backing=BackgroundRectangle(obj,color=config.background_color,fill_opacity=1,buff=.05)
                self.add(backing,obj)
            self.add(small_box('E_f' if down else 'E_f⁻¹',x,1.44,c),small_box('A' if down else 'A⁻¹',x,.24,c),small_box('E_b' if down else 'E_b⁻¹',x,-.96,c))
        note=fit(text('x、y 为分析用的内部状态',20,MUTED),7).move_to([-3.20,-2.43,0])
        self.add(note)
        self.stage(1,'先看四条路径',['密码分为前段、连接层、后段','两条正向，两条用于分析逆向','连接层 A 可逆且为线性或仿射'],['E = E_b ∘ A ∘ E_f'],'四条轨道始终对应四组明文、密文和内部状态。')
        self.pause_to(1)
        self.stage(2,'选择明文并加密',['主动选取 P₁、P₂，差分为 α','将两者送进完整加密接口','前段命中时，x₁ 与 x₂ 差分为 β'],['P₁ ⊕ P₂ = α','x₁ ⊕ x₂ = β  ·  概率 p₁'],'主动设定 α；前段出现 β 是概率事件。')
        # Horizontal arcs span the two forward lanes, as on the lecture slide.
        alpha=ArcBetweenPoints([xs[0],2.28,0],[xs[2],2.28,0],angle=-.38,color=TEAL,stroke_width=3)
        alabel=center_text('α', (xs[0]+xs[2])/2,2.50,24,TEAL)
        self.play(Create(alpha),FadeIn(alabel),run_time=.8)
        self.pause_to(.30);self.flow([0,2],True)
        self.pause_to(.68)
        beta=ArcBetweenPoints([xs[0]+.15,1.01,0],[xs[2]-.15,1.01,0],angle=-.34,color=BLUE,stroke_width=3)
        blabel=center_text('β', (xs[0]+xs[2])/2+.55,1.17,22,BLUE)
        self.play(Create(beta),FadeIn(blabel),run_time=.7)
        self.pause_to(1)
        self.stage(3,'构造回程密文',['对 C₁ 和 C₂ 分别异或 γ','得到密文 C₃ 和 C₄','γ 连接 1–3 与 2–4'],['C₃ = C₁ ⊕ γ','C₄ = C₂ ⊕ γ'],'两条 γ 边由攻击者主动构造。')
        self.pause_to(.24)
        gammas=VGroup(link(xs[0],xs[1],-1.56,'γ',ORANGE),link(xs[2],xs[3],-1.56,'γ',ORANGE))
        self.play(Create(gammas),run_time=1.1)
        self.pause_to(1)
        self.stage(4,'解密回程',['将 C₃、C₄ 送入完整解密接口','得到 P₃、P₄','图中的内部状态用于解释传播'],['P₃ = D(C₃)','P₄ = D(C₄)'],'查询的是完整解密接口；图中的内部状态只用于分析。')
        self.pause_to(.18);self.flow([1,3],False);self.pause_to(1)
        self.stage(5,'观察两条 φ 边',['两次后段逆向差分分别命中','两条内部差分都等于 φ','相同的 φ 在异或中抵消'],['y₁ ⊕ y₃ = y₂ ⊕ y₄ = φ','y₁ ⊕ y₂ ⊕ y₃ ⊕ y₄ = 0'],'两次后段逆向差分命中时，中间两条边都是 φ。')
        self.pause_to(.28)
        phis=VGroup(link(xs[0],xs[1],-.36,'φ',BLUE),link(xs[2],xs[3],-.36,'φ',BLUE))
        self.play(Create(phis),run_time=1.0)
        self.pause_to(1)
        self.stage(6,'跨过连接层',['仿射连接层保持四值异或和为零','四个 x 状态的异或和也为零','所以两组 x 差分相同'],['x₁ ⊕ x₂ ⊕ x₃ ⊕ x₄ = 0','x₃ ⊕ x₄ = x₁ ⊕ x₂ = β'],'利用连接层的结构，把 y 的四元组关系传到 x。')
        self.pause_to(.60)
        x34=ArcBetweenPoints([xs[1]+.12,.73,0],[xs[3]-.12,.73,0],angle=.32,color=BLUE,stroke_width=3)
        x34label=center_text('β',(xs[1]+xs[3])/2+.62,.66,22,BLUE)
        self.play(Create(x34),FadeIn(x34label),run_time=.8);self.pause_to(1)
        self.stage(7,'回到明文端',['前段反向差分命中','P₃ 与 P₄ 的差分回到 α','整条路线包含四次差分命中'],['P₃ ⊕ P₄ = α','概率约 p₁ · p₂ · q²（独立近似）'],'β 反向传播为 α，四条差分路径共同组成飞去来器。')
        self.pause_to(.32)
        alpha2=ArcBetweenPoints([xs[1],2.16,0],[xs[3],2.16,0],angle=-.38,color=VIOLET,stroke_width=3)
        a2=center_text('α',(xs[1]+xs[3])/2+.35,2.39,23,VIOLET)
        self.play(Create(alpha2),FadeIn(a2),run_time=.8);self.pause_to(1)
        self.stage(8,'统计与区分',['重复构造并查询加密、解密','统计 P₃ ⊕ P₄ = α 的频率','与随机置换的对应概率比较'],['差分概率有明显偏差 → 区分器','扩展轮数、猜测子密钥 → 密钥恢复'],'重复实验并统计结果；扩展轮数后可进一步尝试恢复密钥。')
        self.pause_to(1)
        self.wait(.5)
