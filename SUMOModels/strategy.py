import db_strategy
import lq_strategy
import hcs_strategy


class strategy(object):

    def __init__(self, name):
        self.name = name
        self.green_time = []

    def get_green_time(self, average_demands, vehicle_numbers):
        green_time = []
        return green_time

    def set_green_time(self, new_green_time):
        self.green_time = new_green_time


class DB_strategy(strategy):
    def get_green_time(self, average_demands, vehicle_numbers):
        return db_strategy.get_green_time(average_demands, vehicle_numbers, last_strategy='DB'), 'DB'


class LQ_strategy(strategy):
    def get_green_time(self, average_demands, vehicle_numbers):
        return lq_strategy.get_green_time(average_demands, vehicle_numbers, last_strategy='LQ'), 'LQ'


class HCS_strategy(strategy):
    def get_green_time_hcs_strategy(self, average_demands, vehicle_numbers, last_strategy):
        return hcs_strategy.get_green_time_hcs_strategy(average_demands, vehicle_numbers, last_strategy)
