import json
from matplotlib import pyplot as plt
import traci
from NC import NetworkControl
from junction import junction
from strategy import HCS_strategy, LQ_strategy, DB_strategy


class TrafficSignalControlStrategy(object):

    def __init__(self):
        self.junction_in = {}  # 需调控路口(内部路口)
        self.strategy = {}  # 需调控路口的绿灯配时策略
        with open('param.json', 'r', encoding='utf8') as fp:
            param = json.load(fp)
        self.num_j_in = param["num_j_in"]  # 内部需调控路口数量
        self.T = param["T"]  # time index reflecting corresponding signal cycles,k=0,1,...,159
        self.C = param["C"]  # cycle time(unit:second)
        self.green_wave = param["green_wave"]  # 通过与sumo交互，使用调节offset的算法对green_wave进行调节

    def read_data(self, junction_in_j):
        """
        读入需调控路口demands和vehicle_numbers数据
            demands:车流量(辆/小时){北东南西}
            vehicle_numbers:车辆数(辆){北东南西}
        """
        # sumo生成车流数据
        name_junction = junction_in_j.get_name()
        demands = NetworkControl.getDemand(name_junction)
        vehicle_numbers = NetworkControl.getVehicleNum(name_junction)

        return demands, vehicle_numbers

    def write_data(self, junction_in_j, demands, vehicle_numbers):
        """
        将读入的demands和vehicle_numbers数据写入junction
            demands:车流量(辆/小时){北东南西}
            vehicle_numbers:车辆数(辆){北东南西}
        """
        name_junction = junction_in_j.get_name()
        self.junction_in[name_junction].set_demands(demands)
        self.junction_in[name_junction].set_vehicle_numbers(vehicle_numbers)

    def initNetwork(self):
        """
        初始化路口
            num_j_in = 9 内部需调控路口数量
            junction_in = {}  需调控路口(内部路口)
            strategy = {}  需调控路口的绿灯配时策略
        """
        for j in range(self.num_j_in):
            name_junction = "j_" + str(j + 1)
            self.junction_in[name_junction] = junction(name_junction)
            name_strategy = "s_" + str(j + 1)

            """HCS"""
            self.strategy[name_strategy] = HCS_strategy(name_strategy)
            """DB"""
            # self.strategy[name_strategy] = DB_strategy(name_strategy)
            """LQ"""
            # self.strategy[name_strategy] = LQ_strategy(name_strategy)

            self.junction_in[name_junction].set_num_stage(4)
            self.junction_in[name_junction].set_now_green_time([19, 19, 20, 20])
            self.strategy[name_strategy].set_green_time(self.junction_in[name_junction].get_now_green_time())

            # 读入需调控路口demands和vehicle_numbers数据
            demands, vehicle_numbers = self.read_data(self.junction_in[name_junction])
            # 将读入的demands和vehicle_numbers数据写入junction
            self.write_data(self.junction_in[name_junction], demands, vehicle_numbers)

    def modelStep(self, t):
        """
        模型运行步进一步
            T = 160 time index reflecting corresponding signal cycles,k=0,1,...,159
            C = 90 cycle time(unit:second)
            t = T*C
        """
        for j in range(self.num_j_in):
            name_junction = "j_" + str(j + 1)
            if (t + self.green_wave[j]) % self.C == 0:
                # 进入新周期，切换策略
                name_strategy = "s_" + str(j + 1)
                average_demands = [0, 0, 0, 0]
                # 计算上一相位的average_demands，即根据上一相位的车流量调整策略
                num_count = self.junction_in[name_junction].get_count()
                if self.junction_in[name_junction].get_count() == 0:  # 防止分母为0
                    num_count = 1
                for i in range(self.junction_in[name_junction].get_num_stage()):
                    average_demands[i] = float(
                        self.junction_in[name_junction].get_sum_this_phase_demands()[i]) / num_count
                vehicle_numbers = self.junction_in[name_junction].get_vehicle_numbers()

                """获取green_time和new_strategy DB->DB,LQ->LQ,HCS->DB/LQ"""
                """HCS"""
                last_strategy = self.junction_in[name_junction].get_last_strategy()
                green_time, new_strategy = self.strategy[name_strategy].get_green_time_hcs_strategy(average_demands,
                                                                                                    vehicle_numbers,
                                                                                                    last_strategy)
                """DB/LQ"""
                # green_time, new_strategy = self.strategy[name_strategy].get_green_time(average_demands,
                #                                                                   vehicle_numbers)

                self.junction_in[name_junction].set_hist_strategy(new_strategy)  # 更新hist_strategy
                self.junction_in[name_junction].set_now_green_time(green_time)  # 更新当前绿灯时长
                self.junction_in[name_junction].set_hist_green_time(green_time)  # 保存绿灯时长历史数据
                self.junction_in[name_junction].set_count_0()  # count置零
                self.junction_in[name_junction].set_sum_this_phase_demands_0()  # sum_this_phase_demands置零
            else:
                green_time = self.junction_in[name_junction].get_now_green_time()
                self.junction_in[name_junction].set_now_green_time(green_time)  # 更新当前策略，即保持不变
                self.junction_in[name_junction].set_count(self.junction_in[name_junction].get_count() + 1)
                # 更新junction_in[name_junction]sum_this_phase_demands
                for i in range(self.junction_in[name_junction].get_num_stage()):
                    self.junction_in[name_junction].sum_this_phase_demands[i] = \
                        self.junction_in[name_junction].sum_this_phase_demands[i] + int(
                            self.junction_in[name_junction].get_demands()[i])

            # 读入需调控路口demands和vehicle_numbers数据
            demands, vehicle_numbers = self.read_data(self.junction_in[name_junction])
            # 将读入的demands和vehicle_numbers数据写入junction
            self.write_data(self.junction_in[name_junction], demands, vehicle_numbers)


class HCS(TrafficSignalControlStrategy):

    def initNetwork(self):
        """
        初始化路口
            num_j_in = 9 内部需调控路口数量
            junction_in = {}  需调控路口(内部路口)
            strategy = {}  需调控路口的绿灯配时策略
        """
        for j in range(self.num_j_in):
            name_junction = "j_" + str(j + 1)
            self.junction_in[name_junction] = junction(name_junction)
            name_strategy = "s_" + str(j + 1)

            """HCS"""
            self.strategy[name_strategy] = HCS_strategy(name_strategy)

            self.junction_in[name_junction].set_num_stage(4)
            self.junction_in[name_junction].set_now_green_time([19, 19, 20, 20])
            self.strategy[name_strategy].set_green_time(self.junction_in[name_junction].get_now_green_time())

            # 读入需调控路口demands和vehicle_numbers数据
            demands, vehicle_numbers = self.read_data(self.junction_in[name_junction])
            # 将读入的demands和vehicle_numbers数据写入junction
            self.write_data(self.junction_in[name_junction], demands, vehicle_numbers)

    def modelStep(self, t):
        """
        模型运行步进一步
            T = 160 time index reflecting corresponding signal cycles,k=0,1,...,159
            C = 90 cycle time(unit:second)
            t = T*C
        """
        for j in range(self.num_j_in):
            name_junction = "j_" + str(j + 1)
            if (t + self.green_wave[j]) % self.C == 0:
                # 进入新周期，切换策略
                name_strategy = "s_" + str(j + 1)
                average_demands = [0, 0, 0, 0]
                # 计算上一相位的average_demands，即根据上一相位的车流量调整策略
                num_count = self.junction_in[name_junction].get_count()
                if self.junction_in[name_junction].get_count() == 0:  # 防止分母为0
                    num_count = 1
                for i in range(self.junction_in[name_junction].get_num_stage()):
                    average_demands[i] = float(
                        self.junction_in[name_junction].get_sum_this_phase_demands()[i]) / num_count
                vehicle_numbers = self.junction_in[name_junction].get_vehicle_numbers()

                """获取green_time和new_strategy DB->DB,LQ->LQ,HCS->DB/LQ"""
                """HCS"""
                last_strategy = self.junction_in[name_junction].get_last_strategy()
                green_time, new_strategy = self.strategy[name_strategy].get_green_time_hcs_strategy(average_demands,
                                                                                                    vehicle_numbers,
                                                                                                    last_strategy)

                self.junction_in[name_junction].set_hist_strategy(new_strategy)  # 更新hist_strategy
                self.junction_in[name_junction].set_now_green_time(green_time)  # 更新当前绿灯时长
                self.junction_in[name_junction].set_hist_green_time(green_time)  # 保存绿灯时长历史数据
                self.junction_in[name_junction].set_count_0()  # count置零
                self.junction_in[name_junction].set_sum_this_phase_demands_0()  # sum_this_phase_demands置零
            else:
                green_time = self.junction_in[name_junction].get_now_green_time()
                self.junction_in[name_junction].set_now_green_time(green_time)  # 更新当前策略，即保持不变
                self.junction_in[name_junction].set_count(self.junction_in[name_junction].get_count() + 1)
                # 更新junction_in[name_junction]sum_this_phase_demands
                for i in range(self.junction_in[name_junction].get_num_stage()):
                    self.junction_in[name_junction].sum_this_phase_demands[i] = \
                        self.junction_in[name_junction].sum_this_phase_demands[i] + int(
                            self.junction_in[name_junction].get_demands()[i])

            # 读入需调控路口demands和vehicle_numbers数据
            demands, vehicle_numbers = self.read_data(self.junction_in[name_junction])
            # 将读入的demands和vehicle_numbers数据写入junction
            self.write_data(self.junction_in[name_junction], demands, vehicle_numbers)


class DB(TrafficSignalControlStrategy):

    def initNetwork(self):
        """
        初始化路口
            num_j_in = 9 内部需调控路口数量
            junction_in = {}  需调控路口(内部路口)
            strategy = {}  需调控路口的绿灯配时策略
        """
        for j in range(self.num_j_in):
            name_junction = "j_" + str(j + 1)
            self.junction_in[name_junction] = junction(name_junction)
            name_strategy = "s_" + str(j + 1)

            """DB"""
            self.strategy[name_strategy] = DB_strategy(name_strategy)

            self.junction_in[name_junction].set_num_stage(4)
            self.junction_in[name_junction].set_now_green_time([19, 19, 20, 20])
            self.strategy[name_strategy].set_green_time(self.junction_in[name_junction].get_now_green_time())

            # 读入需调控路口demands和vehicle_numbers数据
            demands, vehicle_numbers = self.read_data(self.junction_in[name_junction])
            # 将读入的demands和vehicle_numbers数据写入junction
            self.write_data(self.junction_in[name_junction], demands, vehicle_numbers)

    def modelStep(self, t):
        """
        模型运行步进一步
            T = 160 time index reflecting corresponding signal cycles,k=0,1,...,159
            C = 90 cycle time(unit:second)
            t = T*C
        """
        for j in range(self.num_j_in):
            name_junction = "j_" + str(j + 1)
            if (t + self.green_wave[j]) % self.C == 0:
                # 进入新周期，切换策略
                name_strategy = "s_" + str(j + 1)
                average_demands = [0, 0, 0, 0]
                # 计算上一相位的average_demands，即根据上一相位的车流量调整策略
                num_count = self.junction_in[name_junction].get_count()
                if self.junction_in[name_junction].get_count() == 0:  # 防止分母为0
                    num_count = 1
                for i in range(self.junction_in[name_junction].get_num_stage()):
                    average_demands[i] = float(
                        self.junction_in[name_junction].get_sum_this_phase_demands()[i]) / num_count
                vehicle_numbers = self.junction_in[name_junction].get_vehicle_numbers()

                """获取green_time和new_strategy DB->DB,LQ->LQ,HCS->DB/LQ"""
                """DB"""
                green_time, new_strategy = self.strategy[name_strategy].get_green_time(average_demands,
                                                                                       vehicle_numbers)

                self.junction_in[name_junction].set_hist_strategy(new_strategy)  # 更新hist_strategy
                self.junction_in[name_junction].set_now_green_time(green_time)  # 更新当前绿灯时长
                self.junction_in[name_junction].set_hist_green_time(green_time)  # 保存绿灯时长历史数据
                self.junction_in[name_junction].set_count_0()  # count置零
                self.junction_in[name_junction].set_sum_this_phase_demands_0()  # sum_this_phase_demands置零
            else:
                green_time = self.junction_in[name_junction].get_now_green_time()
                self.junction_in[name_junction].set_now_green_time(green_time)  # 更新当前策略，即保持不变
                self.junction_in[name_junction].set_count(self.junction_in[name_junction].get_count() + 1)
                # 更新junction_in[name_junction]sum_this_phase_demands
                for i in range(self.junction_in[name_junction].get_num_stage()):
                    self.junction_in[name_junction].sum_this_phase_demands[i] = \
                        self.junction_in[name_junction].sum_this_phase_demands[i] + int(
                            self.junction_in[name_junction].get_demands()[i])

            # 读入需调控路口demands和vehicle_numbers数据
            demands, vehicle_numbers = self.read_data(self.junction_in[name_junction])
            # 将读入的demands和vehicle_numbers数据写入junction
            self.write_data(self.junction_in[name_junction], demands, vehicle_numbers)


class LQ(TrafficSignalControlStrategy):

    def initNetwork(self):
        """
        初始化路口
            num_j_in = 9 内部需调控路口数量
            junction_in = {}  需调控路口(内部路口)
            strategy = {}  需调控路口的绿灯配时策略
        """
        for j in range(self.num_j_in):
            name_junction = "j_" + str(j + 1)
            self.junction_in[name_junction] = junction(name_junction)
            name_strategy = "s_" + str(j + 1)

            """LQ"""
            self.strategy[name_strategy] = LQ_strategy(name_strategy)

            self.junction_in[name_junction].set_num_stage(4)
            self.junction_in[name_junction].set_now_green_time([19, 19, 20, 20])
            self.strategy[name_strategy].set_green_time(self.junction_in[name_junction].get_now_green_time())

            # 读入需调控路口demands和vehicle_numbers数据
            demands, vehicle_numbers = self.read_data(self.junction_in[name_junction])
            # 将读入的demands和vehicle_numbers数据写入junction
            self.write_data(self.junction_in[name_junction], demands, vehicle_numbers)

    def modelStep(self, t):
        """
        模型运行步进一步
            T = 160 time index reflecting corresponding signal cycles,k=0,1,...,159
            C = 90 cycle time(unit:second)
            t = T*C
        """
        for j in range(self.num_j_in):
            name_junction = "j_" + str(j + 1)
            if (t + self.green_wave[j]) % self.C == 0:
                # 进入新周期，切换策略
                name_strategy = "s_" + str(j + 1)
                average_demands = [0, 0, 0, 0]
                # 计算上一相位的average_demands，即根据上一相位的车流量调整策略
                num_count = self.junction_in[name_junction].get_count()
                if self.junction_in[name_junction].get_count() == 0:  # 防止分母为0
                    num_count = 1
                for i in range(self.junction_in[name_junction].get_num_stage()):
                    average_demands[i] = float(
                        self.junction_in[name_junction].get_sum_this_phase_demands()[i]) / num_count
                vehicle_numbers = self.junction_in[name_junction].get_vehicle_numbers()

                """获取green_time和new_strategy DB->DB,LQ->LQ,HCS->DB/LQ"""
                """LQ"""
                green_time, new_strategy = self.strategy[name_strategy].get_green_time(average_demands,
                                                                                       vehicle_numbers)

                self.junction_in[name_junction].set_hist_strategy(new_strategy)  # 更新hist_strategy
                self.junction_in[name_junction].set_now_green_time(green_time)  # 更新当前绿灯时长
                self.junction_in[name_junction].set_hist_green_time(green_time)  # 保存绿灯时长历史数据
                self.junction_in[name_junction].set_count_0()  # count置零
                self.junction_in[name_junction].set_sum_this_phase_demands_0()  # sum_this_phase_demands置零
            else:
                green_time = self.junction_in[name_junction].get_now_green_time()
                self.junction_in[name_junction].set_now_green_time(green_time)  # 更新当前策略，即保持不变
                self.junction_in[name_junction].set_count(self.junction_in[name_junction].get_count() + 1)
                # 更新junction_in[name_junction]sum_this_phase_demands
                for i in range(self.junction_in[name_junction].get_num_stage()):
                    self.junction_in[name_junction].sum_this_phase_demands[i] = \
                        self.junction_in[name_junction].sum_this_phase_demands[i] + int(
                            self.junction_in[name_junction].get_demands()[i])

            # 读入需调控路口demands和vehicle_numbers数据
            demands, vehicle_numbers = self.read_data(self.junction_in[name_junction])
            # 将读入的demands和vehicle_numbers数据写入junction
            self.write_data(self.junction_in[name_junction], demands, vehicle_numbers)


if __name__ == "__main__":
    from SUMOModels import PSO
    """
    单独运行Part1 调节超参数(offset+HCS中的参数)
    单独运行Part2 调节offset(注:需要先找到合适的tuningObjectFunction.fit_fun_PSO中的controlParaList及"HCS_b1"等五个参数)
    单独运行Part3 sumo仿真(注:建议当调节完超参数或offset后运行Part3)
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
    result = PSO.tuning_hyperparameters(size, iter_num)
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
    # result = PSO.tuning_offset(size, iter_num)
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

    """
    Part3
        sumo仿真
        HCS\DB\LQ 三种选择其中一种运行
    """
    # traci.start(
    #     [
    #         'sumo', '-n', 'GridNetwork.net.xml',
    #         # 'sumo-gui', '-n', 'GridNetwork.net.xml',  # 显示sumo-gui界面
    #
    #         # '-r', 'GridNetwork_low.rou.xml',
    #         # '-r', 'GridNetwork_middle.rou.xml',
    #         '-r', 'GridNetwork_high.rou.xml',
    #
    #         '--tripinfo-output', 'GridNetwork.tripinfo.xml',
    #         '--emission-output', 'GridNetwork.emission.xml',
    #     ]
    # )

    """HCS"""
    # hcs = HCS()
    # hcs.initNetwork()
    # # 路网仿真并进行信号控制
    # for t in range(1, hcs.T * hcs.C + 1):
    #     print('=' * 50)
    #     print('timestep:', t)
    #     traci.simulationStep()
    #     hcs.modelStep(t)
    #     print('now green time:', hcs.junction_in['j_5'].get_now_green_time())
    # traci.close()
    #
    # print('history strategy:', hcs.junction_in['j_1'].get_hist_strategy())
    # print('history strategy:', hcs.junction_in['j_2'].get_hist_strategy())
    # print('history strategy:', hcs.junction_in['j_3'].get_hist_strategy())
    # print('history strategy:', hcs.junction_in['j_4'].get_hist_strategy())
    # print('history strategy:', hcs.junction_in['j_5'].get_hist_strategy())
    # print('history strategy:', hcs.junction_in['j_6'].get_hist_strategy())
    # print('history strategy:', hcs.junction_in['j_7'].get_hist_strategy())
    # print('history strategy:', hcs.junction_in['j_8'].get_hist_strategy())
    # print('history strategy:', hcs.junction_in['j_9'].get_hist_strategy())

    """DB"""
    # db = DB()
    # db.initNetwork()
    # # 路网仿真并进行信号控制
    # for t in range(1, db.T * db.C + 1):
    #     print('=' * 50)
    #     print('timestep:', t)
    #     traci.simulationStep()
    #     db.modelStep(t)
    #     print('now green time:', db.junction_in['j_5'].get_now_green_time())
    # traci.close()
    #
    # print('history strategy:', db.junction_in['j_1'].get_hist_strategy())
    # print('history strategy:', db.junction_in['j_2'].get_hist_strategy())
    # print('history strategy:', db.junction_in['j_3'].get_hist_strategy())
    # print('history strategy:', db.junction_in['j_4'].get_hist_strategy())
    # print('history strategy:', db.junction_in['j_5'].get_hist_strategy())
    # print('history strategy:', db.junction_in['j_6'].get_hist_strategy())
    # print('history strategy:', db.junction_in['j_7'].get_hist_strategy())
    # print('history strategy:', db.junction_in['j_8'].get_hist_strategy())
    # print('history strategy:', db.junction_in['j_9'].get_hist_strategy())

    """LQ"""
    # lq = LQ()
    # lq.initNetwork()
    # # 路网仿真并进行信号控制
    # for t in range(1, lq.T * lq.C + 1):
    #     print('=' * 50)
    #     print('timestep:', t)
    #     traci.simulationStep()
    #     lq.modelStep(t)
    #     print('now green time:', lq.junction_in['j_5'].get_now_green_time())
    # traci.close()
    #
    # print('history strategy:', lq.junction_in['j_1'].get_hist_strategy())
    # print('history strategy:', lq.junction_in['j_2'].get_hist_strategy())
    # print('history strategy:', lq.junction_in['j_3'].get_hist_strategy())
    # print('history strategy:', lq.junction_in['j_4'].get_hist_strategy())
    # print('history strategy:', lq.junction_in['j_5'].get_hist_strategy())
    # print('history strategy:', lq.junction_in['j_6'].get_hist_strategy())
    # print('history strategy:', lq.junction_in['j_7'].get_hist_strategy())
    # print('history strategy:', lq.junction_in['j_8'].get_hist_strategy())
    # print('history strategy:', lq.junction_in['j_9'].get_hist_strategy())
