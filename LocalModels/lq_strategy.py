"""
    LQ策略:文献“A Hybrid Strategy for Real-Time Traffic Signal Control of Urban Road Networks”中的公式(3)
    LQ可被单独调用，也可在HCS里调用
    适用场景：saturated traffic conditions
"""
import json
import numpy as np
from modify_green_time import modify_green_time

'''
def get_green_time(average_demands, vehicle_numbers, last_strategy='LQ'):
    green_time = [19, 19, 20, 20]
    C = 90  # cycle time(unit:second)
    L_j = 12
    L = 0.15*np.eye(4)
    delta_green_time = np.dot(L, np.transpose(np.array(vehicle_numbers)))
    green_time = green_time + delta_green_time
    green_time = modify_green_time(green_time, C, L_j)
    return green_time
'''


def riccati(B, Q, R):
    P_k = Q
    tolerance = 0.01
    max_num_iteration = 100
    err = 0
    iteration_num = 0
    while err > tolerance and iteration_num < max_num_iteration:
        iteration_num = iteration_num + 1
        P_temp = Q + P_k - P_k * B * (B.T * P_k * B + R).I * B.T * P_k
        err = sum(sum(P_temp - P_k))
        P_k = P_temp
    return P_k


def get_green_time(average_demands, vehicle_numbers, last_strategy='LQ'):
    """
        此处使用的公式为g_{k+1}=g_k+delta_g_k
        而不是g_k=g^N-L*x_k
    """
    with open('param.json', 'r', encoding='utf8') as fp:
        param = json.load(fp)
    green_time = param["green_time_g_N"]
    r = param["LQ_r"]  # DONE:调参
    B = -np.eye(4)
    Q = np.eye(4)
    R = r * np.eye(4)
    P_k = riccati(B, Q, R)
    delta_green_time = -np.dot(
        np.dot(np.linalg.inv(np.dot(np.dot(np.transpose(B), P_k), B) + R), np.dot(np.transpose(B), P_k)),
        np.transpose(np.array(vehicle_numbers)))
    # delta_green_time = np.linalg.inv(-np.transpose(B) * P_k * B + R) * (np.transpose(B) * P_k) * (np.array(average_demands)).T
    scale = param["LQ_scale"]
    green_time = green_time + scale * delta_green_time
    green_time = modify_green_time(green_time)
    return green_time
