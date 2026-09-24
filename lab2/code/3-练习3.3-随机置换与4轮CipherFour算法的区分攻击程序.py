"""
练习3.3 随机置换与4轮CipherFour算法的区分攻击程序

实验1: 统计4轮CipherFour中差分 0001 -> 0001 出现的频率.
实验2: 统计随机置换中差分 0001 -> 0001 出现的频率.
"""

import random


S = [9, 8, 0, 1, 14, 11, 12, 13, 3, 2, 5, 7, 15, 10, 6, 4]
P = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]

DIFFERENCE = 0x0001
TRIALS = 20
SEED = 20260802


def S_box(value):
    """对16比特状态并行使用4个S盒."""
    output = 0
    for shift in [12, 8, 4, 0]:
        output = output | (S[(value >> shift) & 0xF] << shift)
    return output


def P_box(value):
    """对16比特状态进行P置换."""
    input_bits = bin(value)[2:].zfill(16)
    output_bits = ""
    for i in range(16):
        output_bits = output_bits + input_bits[P[i]]
    return int(output_bits, 2)


def cipherFourEnc(plainText, keys, SP_table):
    """进行4轮CipherFour加密, 最后一轮仍包含P置换."""
    state = plainText
    for i in range(4):
        state = SP_table[state ^ keys[i]]
    return state ^ keys[4]


def run_experiment(trials=TRIALS, seed=SEED):
    rng = random.Random(seed)
    SP_table = [P_box(S_box(x)) for x in range(2 ** 16)]
    cipher_frequencies = []
    random_frequencies = []

    for _ in range(trials):
        # 实验1: 4轮CipherFour
        keys = [rng.randrange(2 ** 16) for _ in range(5)]
        cipherText = [
            cipherFourEnc(x, keys, SP_table)
            for x in range(2 ** 16)
        ]

        count = 0
        for x in range(2 ** 16):
            if cipherText[x] ^ cipherText[x ^ DIFFERENCE] == DIFFERENCE:
                count += 1
        cipher_frequencies.append(count / (2 ** 16))

        # 实验2: 随机置换
        random_permutation = list(range(2 ** 16))
        rng.shuffle(random_permutation)

        count = 0
        for x in range(2 ** 16):
            if random_permutation[x] ^ random_permutation[x ^ DIFFERENCE] == DIFFERENCE:
                count += 1
        random_frequencies.append(count / (2 ** 16))

    return cipher_frequencies, random_frequencies


if __name__ == "__main__":
    cipher_frequencies, random_frequencies = run_experiment()

    print("输入差分: %04X" % DIFFERENCE)
    print("目标输出差分: %04X" % DIFFERENCE)
    print("实验次数:", TRIALS, "(随机选取20组不同的密钥)")
    print()
    print("序号 | CipherFour频率 | 随机置换频率")
    print("-" * 42)

    for i in range(TRIALS):
        print(
            "%4d | %16.6f | %14.6f"
            % (i + 1, cipher_frequencies[i], random_frequencies[i])
        )

    print("-" * 42)
    print(
        "平均 | %16.6f | %14.6f"
        % (
            sum(cipher_frequencies) / TRIALS,
            sum(random_frequencies) / TRIALS,
        )
    )
