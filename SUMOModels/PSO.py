import matplotlib.pyplot as plt
import numpy as np
from SUMOModels.tuningObjectFunction import fit_fun_PSO, update_json


class Particle:

    def __init__(self, dim, max_param, min_param, max_vel, min_vel):
        self.pos = np.random.uniform(min_param, max_param, (1, dim))  # 粒子的位置
        self.vel = np.random.uniform(min_vel, max_vel, (1, dim))  # 粒子的速度
        self.bestPos = np.zeros((1, dim))  # 粒子最好的位置
        self.fitnessValue = fit_fun_PSO(self.pos)  # 适应度函数值

    def set_pos(self, value):
        self.pos = value

    def get_pos(self):
        return self.pos

    def set_best_pos(self, value):
        self.bestPos = value

    def get_best_pos(self):
        return self.bestPos

    def set_vel(self, value):
        self.vel = value

    def get_vel(self):
        return self.vel

    def set_fitness_value(self, value):
        self.fitnessValue = value

    def get_fitness_value(self):
        return self.fitnessValue


class Pso:

    def __init__(self, dim, size, iter_num, max_param, min_param, max_vel, min_vel, tol=1e-4,
                 best_fitness_value=float('Inf'), C1=1.49445, C2=1.49445, W=1):
        self.dim = dim  # 粒子的维度
        self.size = size  # 粒子个数
        self.iter_num = iter_num  # 迭代次数
        self.max_param = max_param
        self.min_param = min_param
        self.max_vel = max_vel  # 粒子最大速度
        self.min_vel = min_vel
        self.tol = tol  # 截止条件
        self.best_fitness_value = best_fitness_value
        self.C1 = C1
        self.C2 = C2
        self.W = W
        self.best_position = (max_param - min_param) / 2  # 种群最优位置
        self.fitness_val_list = []  # 每次迭代最优适应值

        # 对种群进行初始化
        self.Particle_list = [Particle(self.dim, self.max_param, self.min_param, self.max_vel, self.min_vel) for i in
                              range(self.size)]

    def set_bestFitnessValue(self, value):
        self.best_fitness_value = value

    def get_bestFitnessValue(self):
        return self.best_fitness_value

    def set_bestPosition(self, value):
        self.best_position = value

    def get_bestPosition(self):
        return self.best_position

    # 更新速度
    def update_vel(self, part):
        vel_value = self.W * part.get_vel() + self.C1 * np.random.rand() * (part.get_best_pos() - part.get_pos()) \
                    + self.C2 * np.random.rand() * (self.get_bestPosition() - part.get_pos())
        vel_value = np.minimum(vel_value, self.max_vel)
        vel_value = np.maximum(vel_value, self.min_vel)
        part.set_vel(vel_value)

    # 更新位置
    def update_pos(self, part):
        pos_value = part.get_pos() + part.get_vel()
        pos_value = np.minimum(pos_value, self.max_param)
        pos_value = np.maximum(pos_value, self.min_param)
        part.set_pos(pos_value)
        value = fit_fun_PSO(part.get_pos())
        if value < part.get_fitness_value():
            part.set_fitness_value(value)
            part.set_best_pos(pos_value)
        if value < self.get_bestFitnessValue():
            self.set_bestFitnessValue(value)
            self.set_bestPosition(pos_value)

    def update_Pso(self):
        for i in range(self.iter_num):
            for part in self.Particle_list:
                self.update_vel(part)  # 更新速度
                self.update_pos(part)  # 更新位置
            self.fitness_val_list.append(self.get_bestFitnessValue())  # 每次迭代完把当前的最优适应度存到列表
            print('第{}次最佳适应值为{}'.format(i, self.get_bestFitnessValue()))
            if self.get_bestFitnessValue() < self.tol:
                break
        return self.fitness_val_list, self.get_bestPosition()


def tuning_hyperparameters(size, iter_num):
    """
    参数空间：
        "green_wave": [0, 10, 20, 30, 40, 10, 20, 30, 40],
        "HCS_b1": 0.3,
        "HCS_b2": 0.5,
        "DB_b3": 0.75,
        "LQ_r": 0.5,
        "LQ_scale": 0.2
    """
    dim = 14
    size = size
    iter_num = iter_num
    max_param = np.array([90, 90, 90, 90, 90, 90, 90, 90, 90, 0.40, 0.65, 0.9, 1, 0.5])
    min_param = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15, 0.45, 0.6, 0.1, 0.1])
    max_param = max_param.reshape((1, dim))
    min_param = min_param.reshape((1, dim))
    max_vel = (max_param - min_param) / 10  # 粒子最大速度
    min_vel = -(max_param - min_param) / 10  # 粒子最大速度
    max_vel = max_vel.reshape((1, dim))
    min_vel = min_vel.reshape((1, dim))

    pso = Pso(dim, size, iter_num, max_param, min_param, max_vel, min_vel)
    fit_var_list, best_pos = pso.update_Pso()
    best_pos = best_pos.reshape([dim, ]).tolist()
    result = {'target': fit_var_list,
              'params': {'green_wave_1': best_pos[0], 'green_wave_2': best_pos[1], 'green_wave_3': best_pos[2],
                         'green_wave_4': best_pos[3], 'green_wave_5': best_pos[4], 'green_wave_6': best_pos[5],
                         'green_wave_7': best_pos[6], 'green_wave_8': best_pos[7], 'green_wave_9': best_pos[8],
                         'HCS_b1': best_pos[9], 'HCS_b2': best_pos[10], 'DB_b3': best_pos[11],
                         'LQ_r': best_pos[12], 'LQ_scale': best_pos[13]}
              }

    # 更新param.json文件
    opt_params = result['params']
    green_wave_1 = opt_params['green_wave_1']
    green_wave_2 = opt_params['green_wave_2']
    green_wave_3 = opt_params['green_wave_3']
    green_wave_4 = opt_params['green_wave_4']
    green_wave_5 = opt_params['green_wave_5']
    green_wave_6 = opt_params['green_wave_6']
    green_wave_7 = opt_params['green_wave_7']
    green_wave_8 = opt_params['green_wave_8']
    green_wave_9 = opt_params['green_wave_9']
    HCS_b1 = opt_params['HCS_b1']
    HCS_b2 = opt_params['HCS_b2']
    DB_b3 = opt_params['DB_b3']
    LQ_r = opt_params['LQ_r']
    LQ_scale = opt_params['LQ_scale']
    x = np.asarray([green_wave_1, green_wave_2, green_wave_3, green_wave_4, green_wave_5,
                    green_wave_6, green_wave_7, green_wave_8, green_wave_9, HCS_b1,
                    HCS_b2, DB_b3, LQ_r, LQ_scale]).reshape([14, ])
    update_json(x)

    return result


def tuning_offset(size, iter_num):
    # 参数空间："green_wave": [0, 10, 20, 30, 40, 10, 20, 30, 40]
    dim = 9
    size = size
    iter_num = iter_num
    max_param = np.array([90, 90, 90, 90, 90, 90, 90, 90, 90])
    min_param = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    max_param = max_param.reshape((1, dim))
    min_param = min_param.reshape((1, dim))
    max_vel = (max_param - min_param) / 10  # 粒子最大速度
    min_vel = -(max_param - min_param) / 10  # 粒子最大速度
    max_vel = max_vel.reshape((1, dim))
    min_vel = min_vel.reshape((1, dim))

    pso = Pso(dim, size, iter_num, max_param, min_param, max_vel, min_vel)
    fit_var_list, best_pos = pso.update_Pso()
    best_pos = best_pos.reshape([dim, ]).tolist()
    result = {'target': fit_var_list,
              'params': {'green_wave_1': best_pos[0], 'green_wave_2': best_pos[1], 'green_wave_3': best_pos[2],
                         'green_wave_4': best_pos[3], 'green_wave_5': best_pos[4], 'green_wave_6': best_pos[5],
                         'green_wave_7': best_pos[6], 'green_wave_8': best_pos[7], 'green_wave_9': best_pos[8]}
              }

    # 更新param.json文件
    opt_params = result['params']
    green_wave_1 = opt_params['green_wave_1']
    green_wave_2 = opt_params['green_wave_2']
    green_wave_3 = opt_params['green_wave_3']
    green_wave_4 = opt_params['green_wave_4']
    green_wave_5 = opt_params['green_wave_5']
    green_wave_6 = opt_params['green_wave_6']
    green_wave_7 = opt_params['green_wave_7']
    green_wave_8 = opt_params['green_wave_8']
    green_wave_9 = opt_params['green_wave_9']
    x = np.asarray([green_wave_1, green_wave_2, green_wave_3, green_wave_4, green_wave_5,
                    green_wave_6, green_wave_7, green_wave_8, green_wave_9]).reshape([9, ])
    update_json(x)

    return result


if __name__ == '__main__':
    """
    单独运行Part1 调节超参数(offset+HCS中的参数)
    单独运行Part2 调节offset(注:需要先找到合适的tuningObjectFunction.fit_fun_PSO中的controlParaList及"HCS_b1"等五个参数)
    """

    """
    Part1
        基于PSO调节超参数
        Args:
            size:粒子个数 {int}
            iter_num:最大迭代次数 {int}
        Returns:
            result: {dict:2}
                target:每代的最优适应度值 {list:iter_num}
                params:最优参数 {dict:14}
    """
    size = 1
    iter_num = 2
    result = tuning_hyperparameters(size, iter_num)
    # 输出结果并绘图
    best_pos = list(
        [result['params']['green_wave_1'], result['params']['green_wave_2'], result['params']['green_wave_3'],
         result['params']['green_wave_4'], result['params']['green_wave_5'], result['params']['green_wave_6'],
         result['params']['green_wave_7'], result['params']['green_wave_8'], result['params']['green_wave_9'],
         result['params']['HCS_b1'], result['params']['HCS_b2'], result['params']['DB_b3'],
         result['params']['LQ_r'], result['params']['LQ_scale']])
    fit_var_list = result['target']
    print("最优位置:" + str(best_pos))
    print("最优解:" + str(fit_var_list[-1]))
    plt.plot(range(len(fit_var_list)), fit_var_list, alpha=0.5)
    plt.show()

    """
    Part2
        基于PSO调节offset
        Args:
            size:粒子个数 {int}
            iter_num:最大迭代次数 {int}
        Returns:
            result: {dict:2}
                target:每代的最优适应度值 {list:iter_num}
                params:最优offset参数 {dict:9}
    """
    # size = 2
    # iter_num = 3
    # result = tuning_offset(size, iter_num)
    # # 输出结果并绘图
    # best_pos = list(
    #     [result['params']['green_wave_1'], result['params']['green_wave_2'], result['params']['green_wave_3'],
    #      result['params']['green_wave_4'], result['params']['green_wave_5'], result['params']['green_wave_6'],
    #      result['params']['green_wave_7'], result['params']['green_wave_8'], result['params']['green_wave_9']])
    # fit_var_list = result['target']
    # print("最优位置:" + str(best_pos))
    # print("最优解:" + str(fit_var_list[-1]))
    # plt.plot(range(len(fit_var_list)), fit_var_list, alpha=0.5)
    # plt.show()
