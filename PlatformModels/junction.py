class junction(object):

    def __init__(self, name):
        self.name = name
        self.now_green_time = {}
        self.next_green_time = {'0': [19.5, 19.5, 19.5, 19.5]}
        self.hist_green_time = {}
        self.hist_strategy = {'0': 'DB'}
        # self.hist_strategy = {'0': 'LQ'}
        self.num_stage = 4
        self.demands = []
        self.vehicle_numbers = []
        self.count = 0  # 用来在求前一阶段流量均值时计录时间数
        self.sum_this_phase_demands = [0, 0, 0, 0]

    def get_name(self):
        return self.name

    def get_now_green_time(self):
        return self.now_green_time

    def get_next_green_time(self):
        return self.next_green_time

    def get_hist_green_time(self):
        return self.hist_green_time

    def get_num_stage(self):
        return self.num_stage

    def get_demands(self):
        return self.demands

    def get_vehicle_numbers(self):
        return self.vehicle_numbers

    def get_count(self):
        return self.count

    def get_sum_this_phase_demands(self):
        return self.sum_this_phase_demands

    def get_hist_strategy(self):
        return self.hist_strategy

    def get_last_strategy(self):
        return self.hist_strategy.get(list(self.hist_strategy.keys())[-1])

    def set_now_green_time(self, new_green_time):
        self.now_green_time = new_green_time

    def set_next_green_time(self, new_green_time):
        self.next_green_time = new_green_time

    def set_hist_green_time(self, new_green_time):
        # 存储历史绿灯时长
        self.hist_green_time[str(len(self.hist_green_time))] = new_green_time

    def set_num_stage(self, new_num_stage):
        self.num_stage = new_num_stage

    def set_demands(self, new_demands):
        self.demands = new_demands

    def set_vehicle_numbers(self, new_vehicle_numbers):
        self.vehicle_numbers = new_vehicle_numbers

    def set_count(self, new_count):
        self.count = new_count

    def set_sum_this_phase_demands(self, new_demands):
        # new_demands为每时刻新增加的车流量，数据格式为list
        for i in range(self.num_stage):
            self.sum_this_phase_demands[i] = self.sum_this_phase_demands[i] + new_demands[i]

    def set_count_0(self):
        # count置零
        self.count = 0

    def set_sum_this_phase_demands_0(self):
        # sum_this_phase_demands置零
        self.sum_this_phase_demands = [0, 0, 0, 0]

    def set_hist_strategy(self, new_strategy):
        self.hist_strategy[str(len(self.hist_strategy))] = new_strategy
