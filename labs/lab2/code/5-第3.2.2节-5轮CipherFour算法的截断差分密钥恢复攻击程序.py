"""
第3.2.2节 5轮CipherFour算法的截断差分密钥恢复攻击

本次攻击使用的截断差分为:
    (0000, 0000, 0000, 0001)-3轮->(0???, 0???, 0???, 0???)

攻击步骤:
    (1) 从plaintext.txt和ciphertext.txt读取一一对应的明密文.
    (2) 选择结构体Stru = {(t0, t1, t2, i) | 0 <= i <= 15}.
    (3) 猜测k0,3, 筛选第一轮S盒输出差分为0001的明文对.
    (4) 分别猜测k5的4个半字节, 对密文进行一轮部分解密.
    (5) 保留解密差分均满足0???的密钥猜测.
    (6) 使用多个结构体重复攻击, 对候选密钥集合取交集.

注:
    (1) 输入文件plaintext.txt为所有明文, ciphertext.txt为所有密文且明密文按照顺序对应(固定密钥下)
    (2) 输入文件中的数据可以用逗号, 空格或换行分隔. 每个数可以写成0000或0x0000的形式.
"""

import os
import random


S = [9, 8, 0, 1, 14, 11, 12, 13, 3, 2, 5, 7, 15, 10, 6, 4]
S_reverse = [2, 3, 9, 8, 15, 10, 14, 11, 1, 0, 13, 5, 6, 7, 4, 12]

ROUND_KEYS = [0x0123, 0x4567, 0x89AB, 0xCDEF, 0xFEDC, 0xBA98]
NUMBER_OF_STRUCTURES = 8
RANDOM_SEED = 2026

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
PLAINTEXT_FILE = os.path.join(FILE_PATH, "plaintext.txt")
CIPHERTEXT_FILE = os.path.join(FILE_PATH, "ciphertext.txt")


def read_data(filename):
    """从文件中读取16比特十六进制数据."""
    with open(filename, "r", encoding="utf-8") as file:
        data = file.read().replace(",", " ").split()
    return [int(value, 16) for value in data]


def get_codebook():
    """读取明密文并建立明文到密文的对应关系."""
    plaintext = read_data(PLAINTEXT_FILE)
    ciphertext = read_data(CIPHERTEXT_FILE)

    codebook = {}
    for i in range(len(plaintext)):
        codebook[plaintext[i]] = ciphertext[i]

    return codebook


def get_structures(codebook):
    """选择多个由16个明文组成的结构体."""
    random.seed(RANDOM_SEED)
    structures = []

    for i in range(NUMBER_OF_STRUCTURES):
        t0 = random.randint(0, 15)
        t1 = random.randint(0, 15)
        t2 = random.randint(0, 15)
        prefix = (t0 << 12) | (t1 << 8) | (t2 << 4)

        plaintext = []
        ciphertext = []
        for value in range(16):
            plainText = prefix | value
            plaintext.append(plainText)
            ciphertext.append(codebook[plainText])

        structures.append((prefix, plaintext, ciphertext))

    return structures


def select_pairs(plaintext, ciphertext, first_key):
    """根据k0,3猜测筛选第一轮S盒输出差分为0001的明文对."""
    ciphertext_pairs = []

    for i in range(16):
        for j in range(i + 1, 16):
            input1 = (plaintext[i] & 0xF) ^ first_key
            input2 = (plaintext[j] & 0xF) ^ first_key

            if S[input1] ^ S[input2] == 0x1:
                ciphertext_pairs.append((ciphertext[i], ciphertext[j]))

    return ciphertext_pairs


def get_nibble(value, position):
    """取16比特数从左到右的第position个半字节."""
    return (value >> (12 - 4 * position)) & 0xF


def find_last_key(ciphertext_pairs, position):
    """寻找满足截断差分0???的第position个k5半字节."""
    candidates = set()

    for key in range(16):
        count = 0

        for cipherText1, cipherText2 in ciphertext_pairs:
            nibble1 = get_nibble(cipherText1, position)
            nibble2 = get_nibble(cipherText2, position)

            input1 = S_reverse[nibble1 ^ key]
            input2 = S_reverse[nibble2 ^ key]
            difference = input1 ^ input2

            # 最高位为0, 即差分满足0???.
            if difference & 0x8 == 0:
                count += 1

        if count == len(ciphertext_pairs):
            candidates.add(key)

    return candidates


def attack_one_structure(plaintext, ciphertext):
    """对一个结构体恢复k0,3和k5的候选值."""
    result = {}

    for first_key in range(16):
        ciphertext_pairs = select_pairs(plaintext, ciphertext, first_key)
        last_key = []

        for position in range(4):
            candidates = find_last_key(ciphertext_pairs, position)
            last_key.append(candidates)

        if all(len(candidates) > 0 for candidates in last_key):
            result[first_key] = last_key

    return result


def intersect_results(old_result, new_result):
    """对不同结构体得到的候选密钥集合取交集."""
    if old_result is None:
        return new_result

    result = {}

    for first_key in old_result:
        if first_key in new_result:
            last_key = []

            for position in range(4):
                candidates = old_result[first_key][position]
                candidates = candidates & new_result[first_key][position]
                last_key.append(candidates)

            if all(len(candidates) > 0 for candidates in last_key):
                result[first_key] = last_key

    return result


def format_candidates(candidates):
    """将半字节候选值转换为便于阅读的形式."""
    values = ["0x%X" % key for key in sorted(candidates)]
    return "{" + ", ".join(values) + "}"


def combine_last_key(last_key):
    """将k5的4组半字节候选组合成16比特密钥."""
    keys = []

    for key0 in last_key[0]:
        for key1 in last_key[1]:
            for key2 in last_key[2]:
                for key3 in last_key[3]:
                    key = (key0 << 12) | (key1 << 8) | (key2 << 4) | key3
                    keys.append(key)

    return sorted(keys)


if __name__ == "__main__":
    codebook = get_codebook()
    structures = get_structures(codebook)
    result = None

    print("本题使用的轮密钥:", ["0x%04X" % key for key in ROUND_KEYS])
    print("正确的 k0,3:", "0x%X" % (ROUND_KEYS[0] & 0xF))
    print("正确的 k5:", "0x%04X" % ROUND_KEYS[5])
    print("正确的20比特密钥 k0,3 || k5:", "0x%05X" % (((ROUND_KEYS[0] & 0xF) << 16) | ROUND_KEYS[5]))
    print()

    for i in range(len(structures)):
        prefix, plaintext, ciphertext = structures[i]
        current_result = attack_one_structure(plaintext, ciphertext)
        result = intersect_results(result, current_result)

        print("结构体%d: 固定部分为0x%03X, 剩余k0,3候选数量为%d."
              % (i + 1, prefix >> 4, len(result)))

    print()
    print("最终候选结果:")
    print("k0,3 | k5,0候选 | k5,1候选 | k5,2候选 | k5,3候选")
    print("-" * 65)

    for first_key in sorted(result):
        last_key = result[first_key]
        print("  %X   | %-10s | %-10s | %-10s | %-10s"
              % (first_key,
                 format_candidates(last_key[0]),
                 format_candidates(last_key[1]),
                 format_candidates(last_key[2]),
                 format_candidates(last_key[3])))

    print("-" * 65)
    print("候选20比特密钥k0,3 || k5:")

    for first_key in sorted(result):
        for last_key in combine_last_key(result[first_key]):
            candidate = (first_key << 16) | last_key
            print("0x%05X" % candidate)
