"""
    HCS策略:参考文献“A Hybrid Strategy for Real-Time Traffic Signal Control of Urban Road Networks”
    HCS->DB/LQ
"""
import json
import db_strategy
import lq_strategy


def get_green_time_hcs_strategy(average_demands, vehicle_numbers, last_strategy):
    with open('param.json', 'r', encoding='utf8') as fp:
        param = json.load(fp)
    b1 = param["HCS_b1"]
    b2 = param["HCS_b2"]
    x_z = vehicle_numbers
    xz_max = param["xz_max"]
    # 文献中的step1
    if last_strategy == 'DB':
        for i in range(len(average_demands)):
            if float(x_z[i]) / float(xz_max) >= b2:
                return lq_strategy.get_green_time(average_demands, vehicle_numbers), 'LQ'
        return db_strategy.get_green_time(average_demands, vehicle_numbers, 'HCS')
    # 文献中的step2
    if last_strategy == 'LQ':
        for i in range(len(average_demands)):
            if float(x_z[i]) / float(xz_max) > b1:
                return lq_strategy.get_green_time(average_demands, vehicle_numbers), 'LQ'
        return db_strategy.get_green_time(average_demands, vehicle_numbers, 'HCS')
