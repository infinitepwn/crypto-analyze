'''
给定明文BESTCIPHER, 按照以下给定参数, 编程实现Enigma机的加密, 并输出对应的密文。

接线板(6条连线)K1: 
S = [2,  1,  0,  4,  3,  5,  7,  6,  8,  9,  24,  11,  20,  13,  14,  15,  16,  17,  22,  19,  12,  21,  18,  23,  10,  25]
即a与c相连, d与e相连, g与h相连, k与y相连, m与u相连, s与w相连

扰频器组合(固定2个转子, 无需从5个中选择2个)
快速转子QUICK = [0,  18,  24,  12,  10,  20,  8,  6,  14,  2,  11,  15,  22,  3,  25,  7,  17,  13,  5,  1,  23,  9,  16,  21,  19,  4]
即快速转子的表格中左侧一列为0, 1, 2, …, 25, 右侧一列0, 18, 24, …, 4; 下同
中速转子MID = [0,  10,  4,  2,  8,  1,  18,  20,  22,  19,  13,  6,  17,  5,  9,  3,  24,  14,  12,  25,  21,  11,  7,  16,  15,  23]
各转子起始点K2: (5,  16), 

反射器
T = [10,  20,  14,  8,  25,  15,  16,  21,  3,  18,  0,  23,  13,  12,  2,  5,  6,  19,  9,  17,  1,  7,  24,  11,  22,  4]
即a与k相连, b与u相连, ……
'''

"""
上述注释是老师给的，下面的实验在原有代码的基础上，依据实验指导，
修改了转子及其初始位置，并将明文改为WETTER，也稍微修改了主函数里面的内容
"""

"""
模拟实现
"""
from copy import *
class myEnigma:
    def __init__(self, rotors, reflector) -> None:
        """
        初始化转子及反射器
        Args:
            rotors: 转子列表, 从高速到低速
            reflector: 反射器
        """
        self.Rotor_left  = [[i for i in range(26)] for j in range(len(rotors))]
        self.Rotor_right = copy(rotors)
        self.rotors      = copy(rotors)
        self.reflector   = reflector

    def setRotor(self, K2):
        """
        设置转子密钥
        Args:
            K2: 转子位置密钥
        """
        self.count = 0
        for i in range(len(self.Rotor_left)):
            self.Rotor_right[i] = self.Rotor_right[i][K2[i]:] + self.Rotor_right[i][:K2[i]]
            self.Rotor_left[i] = self.Rotor_left[i][K2[i]:] + self.Rotor_left[i][:K2[i]]
    
    def resetRotor(self):
        """
        重制转子位置
        """
        self.count = 0
        self.Rotor_left  = [[i for i in range(26)] for j in range(len(self.rotors))]
        self.Rotor_right = copy(self.rotors)
        
    def updateRotor(self):
        """
        模拟转动一次
        """   
        self.count = self.count + 1
        self.Rotor_left[0]  = self.Rotor_left[0][25:] + self.Rotor_left[0][:25]
        self.Rotor_right[0] = self.Rotor_right[0][25:] + self.Rotor_right[0][:25]
        if self.count % 26 == 0:    #快速转子每转26次, 中速转子转一次, 即左移一次
            self.Rotor_left[1] = self.Rotor_left[1][25:] + self.Rotor_left[1][:25]
            self.Rotor_right[1] = self.Rotor_right[1][25:] + self.Rotor_right[1][:25]
        
    def encrypt(self, plaintext,  K1):
        """
        主加密功能
        Args:   
            plaintext: 明文字符串
            K1: 插线板密钥
        Return:
            c: 密文字符串    
        """
        plaintext = plaintext.upper()#统一大写
        plaintext = list(plaintext)
        ciphertext = []
        for m in plaintext:
            m = ord(m) - ord('A')
            m = K1[m]#过接线板
            for i in range(3):
                m = self.Rotor_right[i].index(self.Rotor_left[i][m])#过转子
            m = self.reflector[m]#过反射器
            for i in range(3):
                m = self.Rotor_left[2 - i].index(self.Rotor_right[2 - i][m])#逆向过转子
            m = K1[m]#过接线板
            self.updateRotor()#每加密一个字母, 更新转子
            ciphertext.append(chr(m + ord('A')))
        return ''.join(ciphertext)                
"""
函数式实现
"""    
crypt_once=lambda I, II, III, st0, st1, m:chr((I[(((II[((T[((II.index((((I.index((ord(m)-ord("A")+st0)%26)-st0)%26)+st1)%26)-st1)%26)]+st1)%26)]-st1)%26+st0)%26)]-st0)%26+ord("A"))
#上一行根据实验指导要完成的任务，将Q,M替换为I,II,III

"""
        进行单次加密
        Args:
            I: 快速转子
            II: 中速转子
            III: 慢速转子
            st0: 快速转子当前的转子位置
            st1: 中速转子当前的转子位置
            m: 待通过没有插线板的机器加密的一个字符
        return:
            通过没有插线板的机器加密的一个字符结果
            
"""

rot_once=lambda st0, st1, count:((st0-1, st1-((count+1)%26==0)), count+1)    
#进行转子迭代
    
if __name__=="__main__": 
    S = [21, 18, 6, 3, 4, 5, 2, 7, 8, 9, 10, 11, 13,12, 23, 15, 16, 17, 1, 19, 20, 0, 22, 14, 24, 25]
    
    I = [7, 19, 3, 22, 11, 25, 14, 1, 16, 23, 8, 20, 5,17, 12, 9, 24, 6, 15, 2, 18, 21, 4, 13, 10, 0]
    
    II = [0, 10, 4, 2, 8, 1, 18, 20, 22, 19, 13, 6, 17,5, 9, 3, 24, 14, 12, 25, 21, 11, 7, 16, 15, 23]
    
    III = [0, 23, 5, 12, 18, 3, 21, 9, 14, 1, 17, 6, 24,11, 20, 4, 15, 8, 22, 7, 19, 13, 2, 16, 10, 25]

    T = [5, 3, 7, 1, 8, 0, 9, 2, 4, 6, 12, 14, 10, 15, 11, 13, 18, 20, 16, 21, 17, 19, 24, 25, 22, 23]
    
    K2=(8,9,10)
    #根据实验指导，调整转子及其初始位置，
    E=myEnigma([I, II, III], T)
    
    E.setRotor(K2)
    
    plaintext="WETTER"
    
    ciphertext=E.encrypt(plaintext, S)
    
    print(ciphertext)
    
