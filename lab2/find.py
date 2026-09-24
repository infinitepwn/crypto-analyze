import numpy as np


def make_probability_table(sbox):
    """构造S盒差分概率表 probability_table[dx][dy]."""
    table = np.zeros((16, 16), dtype=np.float32)

    for dx in range(16):
        for x in range(16):
            dy = sbox[x] ^ sbox[x ^ dx]
            table[dx][dy] += 1

    return table / 16.0


def state_to_int(state):
    """(a,b,c,d) -> 16位整数."""
    a, b, c, d = state
    return (a << 12) | (b << 8) | (c << 4) | d


def int_to_state(x):
    """16位整数 -> (a,b,c,d)."""
    return ((x >> 12) & 0xf, (x >> 8) & 0xf, (x >> 4) & 0xf, x & 0xf)


def build_pmap(pbox):
    """
    预计算所有65536个状态经过拉线后的结果.

    这里规定：
    pbox[i] = j
    表示输入第i位 -> 输出第j位，
    第0位是最高位.
    """
    x = np.arange(65536, dtype=np.uint16)
    y = np.zeros(65536, dtype=np.uint16)

    for i, j in enumerate(pbox):
        bit = (x >> (15 - i)) & 1
        y |= bit.astype(np.uint16) << (15 - j)

    return y


def update_one_sbox_fast(score, origin, probability_table, position):
    """
    对一个S盒进行传播.

    score[a,b,c,d]:
        当前到达该差分的最高概率

    origin[a,b,c,d]:
        这条最高概率路线在本轮开始时来自哪个状态
    """

    # 把正在处理的半字节移到第0维
    s = np.moveaxis(score, position, 0)
    o = np.moveaxis(origin, position, 0)

    # s:
    #   (16,16,16,16)
    #
    # probability_table:
    #   (16,16)
    #
    # candidate:
    #   (diff_in, diff_out, 其余三个半字节)
    candidate = s[:, None, :, :, :] * probability_table[:, :, None, None, None]

    # 对所有diff_in取最大值
    best_in = np.argmax(candidate, axis=0)
    new_s = np.max(candidate, axis=0)

    # 找到最大值对应路线原本来自哪个状态
    o_flat = o.reshape(16, -1)
    best_flat = best_in.reshape(16, -1)

    cols = np.arange(o_flat.shape[1])[None, :]
    new_o = o_flat[best_flat, cols].reshape(best_in.shape)

    # 把轴移回原位置
    new_s = np.moveaxis(new_s, 0, position)
    new_o = np.moveaxis(new_o, 0, position)

    return new_s, new_o


def one_round_fast(score, probability_table, pmap):
    """
    一轮：
        4个S盒
          ↓
        拉线P

    返回：
        下一轮score
        predecessor：下一轮每个状态的最佳路线来自上一轮哪个状态
    """

    # 当前轮开始时，每个状态的来源就是它自己
    origin = np.arange(65536, dtype=np.uint16).reshape(16, 16, 16, 16)

    for position in range(4):
        score, origin = update_one_sbox_fast(score, origin, probability_table, position)

    score_flat = score.reshape(-1)
    origin_flat = origin.reshape(-1)

    new_score = np.zeros(65536, dtype=np.float32)
    predecessor = np.zeros(65536, dtype=np.uint16)

    # P置换是一一映射，所以可以直接搬过去
    new_score[pmap] = score_flat
    predecessor[pmap] = origin_flat

    return new_score.reshape(16, 16, 16, 16), predecessor


def generate_start_states():
    """
    枚举只有一个活跃S盒的输入差分.

    共：
        4 * 15 = 60个
    """
    states = []

    for position in range(4):
        for diff in range(1, 16):
            state = [0, 0, 0, 0]
            state[position] = diff
            states.append(tuple(state))

    return states


def recover_path(final_state, predecessors):
    """根据predecessor从第4轮倒推回初始差分."""
    path = [final_state]
    current = final_state

    for predecessor in reversed(predecessors):
        current = int(predecessor[current])
        path.append(current)

    path.reverse()

    return [int_to_state(x) for x in path]


def search_best_trail(probability_table, pbox, rounds=4):
    """
    同时从60个单活跃S盒输入开始搜索，
    找概率最高的一条4轮差分路线.
    """

    pmap = build_pmap(pbox)

    score = np.zeros(65536, dtype=np.float32)

    # 所有60个起点同时放进去
    for state in generate_start_states():
        score[state_to_int(state)] = 1.0

    score = score.reshape(16, 16, 16, 16)

    predecessors = []

    for r in range(rounds):
        score, predecessor = one_round_fast(score, probability_table, pmap)
        predecessors.append(predecessor)

        print(f"第 {r + 1} 轮完成，当前最大概率 = {score.max()}")

    final_score = score.reshape(-1)

    # 按最终概率从大到小检查
    order = np.argsort(final_score)[::-1]

    for final_state in order:
        probability = float(final_score[final_state])

        if probability == 0:
            break

        path = recover_path(int(final_state), predecessors)

        # 排除题目已经给出的：
        # (0,0,0,1) -> 4轮 -> (0,0,0,1)
        if path[0] == (0, 0, 0, 1) and path[-1] == (0, 0, 0, 1):
            continue

        return probability, path

    return None, None


def print_trail(probability, path):
    print("\n============================")
    print("找到的最高概率差分路线")
    print("============================")

    print("概率 =", probability)
    print("log2(P) =", np.log2(probability))

    print("\n输入   :", path[0])

    for i in range(1, len(path)):
        print(f"第{i}轮 :", path[i])
# CipherFour算法的S盒定义
S = [9, 8, 0, 1, 14, 11, 12, 13, 3, 2, 5, 7, 15, 10, 6, 4]

# CipherFour算法的P置换定义
P = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]



probability_table = make_probability_table(S)

probability, path = search_best_trail(probability_table, P, rounds=4)

print_trail(probability, path)