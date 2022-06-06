import numpy as np


def produce_demands(param):
    # 以一秒为单位，生成各车道实时车流量(辆/时)，仅为了跑通程序
    num_j_in = param["num_j_in"]
    num_stage = param["num_stage"]
    # 驶入的车辆数
    in_ji_lmr = np.zeros((num_j_in, num_stage, 3))
    for j in range(num_j_in):
        for i in range(num_stage):
            for k in range(3):
                in_ji_lmr[j][i][k] = np.random.randint(0, 1200)
    '''
    # 初始化每个道路上的车辆数，设为0
    # 以需调控路口为索引，制定车道车辆数的数据结构
    # TODO:以一定规律生成(随机或分布)。生成[a,b]间的随机整数:np.random.randint(0, 10)
    # TODO:在路网运行过程中，我们要考虑路网内部车辆的转移及路网周边车辆的输入与输出，该步骤须在T>0时实现
    # ???d_ji = np.zeros((num_J_i, num_stage, 3))  # link demands (in vehicles per hour)
    # ???需要s_out_ji_lmr,out_ji_lmr的数据吗
    # 驶出的车辆数
    out_ji_lmr = np.zeros((num_J_i, num_stage, 3))
    # 驶入和驶出在中间的路径重叠
    # 更新in_ji_lmr
    for j in range(num_J_i):
        for i in range(num_stage):
            for k in range(3):
                pass
    # 更新out_ji_lmr
    for j in range(num_J_i):
        for i in range(num_stage):
            for k in range(3):
                pass
    '''
    return in_ji_lmr
