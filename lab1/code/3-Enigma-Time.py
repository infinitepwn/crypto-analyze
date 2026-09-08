"""
如果改用从4个转子中选择3个再进行加密,请理论分析需要猜测多少密钥?
对题目1中实现的加密算法进行1000次加密,统计每秒可进行的加密次数,
判断在个人电脑上直接进行穷举攻击是否可行？
"""

import time

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

S = [21, 18, 6, 3, 4, 5, 2, 7, 8, 9, 10, 11, 13,12, 23, 15, 16, 17, 1, 19, 20, 0, 22, 14, 24, 25]
    
I = [7, 19, 3, 22, 11, 25, 14, 1, 16, 23, 8, 20, 5,17, 12, 9, 24, 6, 15, 2, 18, 21, 4, 13, 10, 0]
    
II = [0, 10, 4, 2, 8, 1, 18, 20, 22, 19, 13, 6, 17,5, 9, 3, 24, 14, 12, 25, 21, 11, 7, 16, 15, 23]
    
III = [0, 23, 5, 12, 18, 3, 21, 9, 14, 1, 17, 6, 24,11, 20, 4, 15, 8, 22, 7, 19, 13, 2, 16, 10, 25]

T = [5, 3, 7, 1, 8, 0, 9, 2, 4, 6, 12, 14, 10, 15, 11, 13, 18, 20, 16, 21, 17, 19, 24, 25, 22, 23]
    
K2=(8,9,10)

plaintext = "WETTER"

E = myEnigma([I, II, III], S)

if __name__=="__main__":
    test_times = 1000  #加密1000次

    start_time = time.perf_counter() #开始计时

    for t in range(test_times):
        E.resetRotor()
        E.setRotor(K2)
        E.encrypt(plaintext, S)

    end_time = time.perf_counter() #结束计时

    total_time = end_time - start_time  #计算总时长

    encryptions_per_second = test_times / total_time  #计算每秒加密次数

    print("加密次数:", test_times)
    print("总耗时:", total_time, "秒")
    print("每秒加密次数:", encryptions_per_second, "次/秒")


