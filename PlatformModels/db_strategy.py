"""
    DB策略:文章“A Hybrid Strategy for Real-Time Traffic Signal Control of Urban Road Networks”中的公式(7)
    DB可被单独调用，也可在HCS里调用
"""
import json

import lq_strategy
from modify_green_time import modify_green_time


def get_green_time(average_demands, vehicle_numbers, last_strategy='DB'):
    with open('param.json', 'r', encoding='utf8') as fp:
        param = json.load(fp)
    green_time = []
    S_z = param["S_z"]  # saturation flow
    C = param["C"]
    L_j = param["Loss_j"]
    b3 = param["DB_b3"]  # DONE:通过实验获取合适的b3(0.7,...,0.8)
    sum_d_s = 0
    d_z = average_demands
    for i in range(len(d_z)):
        sum_d_s = sum_d_s + float(d_z[i]) / float(S_z[i])
    for i in range(len(d_z)):
        try:
            green_time.append(float(d_z[i]) / float(S_z[i]) / float(sum_d_s) * (C - L_j))
        except:
            green_time.append(1)
    green_time = modify_green_time(green_time)

    # step3
    if last_strategy == 'HCS':
        G_z = sum(green_time)
        for i in range(len(d_z)):
            if float(green_time[i]) * C / float(G_z) / S_z[i] > b3:
                return lq_strategy.get_green_time(average_demands, vehicle_numbers), 'LQ'
        else:
            return green_time, 'DB'
    else:
        return green_time
