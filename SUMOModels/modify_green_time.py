import json
import numpy as np


def make_int(green_time):
    with open('./param.json', 'r', encoding='utf8') as fp:
        param = json.load(fp)
    C = param["C"]
    L_j = param["Loss_j"]
    for i in range(len(green_time)):
        green_time[i] = round(green_time[i])
    num = sum(green_time) - (C - L_j)

    while num > 0:
        while 1:
            index = np.random.randint(0, 4)
            if green_time[index] > 10:
                break
        green_time[index] = green_time[index] - 1
        num = num - 1

    while num < 0:
        index = np.random.randint(0, 4)
        green_time[index] = green_time[index] + 1
        num = num + 1

    return green_time


def modify_green_time(green_time):
    """
        TODO:改进版中采用这篇文章的方法(A POLYNOMIALLY BOUNDED ALGORITHM FOR A SINGLY CONSTRAINED QUADRATIC PROGRAM)
    """
    with open('./param.json', 'r', encoding='utf8') as fp:
        param = json.load(fp)
    g_ijmin = param["g_ijmin"]
    C = param["C"]
    L_j = param["Loss_j"]

    # 第一次修正：根据比例修正绿灯时长
    scale = float(C - L_j) / float(sum(green_time))
    for i in range(len(green_time)):
        green_time[i] = scale * green_time[i]

    # 第二次修正step1：将小于g_ijmin的置为g_ijmin
    index_bound_modified = []
    for i in range(len(green_time)):
        if green_time[i] < g_ijmin:
            green_time[i] = g_ijmin
            index_bound_modified.append(i)
    index_bound_unmodified = list(set(list(range(len(green_time)))) - set(index_bound_modified))

    # 第二次修正step2：修正其他的green_time[i]
    scale = float(C - L_j - len(index_bound_modified) * g_ijmin) / float(
        sum(green_time) - len(index_bound_modified) * g_ijmin)
    for i in range(len(green_time) - len(index_bound_modified)):
        green_time[index_bound_unmodified[i]] = scale * green_time[index_bound_unmodified[i]]

    return make_int(green_time)
