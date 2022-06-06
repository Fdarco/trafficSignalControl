# 根据信号配时生成SUMO的信号配时文件，然后运行
# 格式：offsetList: 整数列表，包含 9 个交叉口的相位差
#      controlParaList: 2 维整数列表，包含 9 个整数列表，
#                       每个整数列表内是每个交叉口的相位配时
from xml.dom.minidom import parse
import traci


class PerformIndex:
    @staticmethod
    def runModel(simulationTime):
        traci.start(
            [
                'sumo', '-n', 'GridNetwork.net.xml',
                # 'sumo-gui', '-n', 'GridNetwork.net.xml',  # 显示sumo-gui界面

                # '-r', 'GridNetwork_low.rou.xml',
                # '-r', 'GridNetwork_middle.rou.xml',
                '-r', 'GridNetwork_high.rou.xml',

                '--tripinfo-output', 'GridNetwork.tripinfo.xml',
                '--emission-output', 'GridNetwork.emission.xml',

                # '--mesosim'
            ]
        )

        timestep = 0
        while timestep < simulationTime:
            traci.simulationStep()
            timestep += 1

        traci.close()

    @staticmethod
    def getPI():
        DOMTree = parse("GridNetwork.tripinfo.xml")
        tripinfos = DOMTree.documentElement
        trips = tripinfos.getElementsByTagName("tripinfo")
        waitingTimeSum = 0
        waitingCountSum = 0
        stopTimeSum = 0
        timeLossSum = 0

        for trip in trips:
            waitingTimeSum += float(trip.getAttribute('waitingTime'))
            waitingCountSum += int(trip.getAttribute('waitingCount'))
            stopTimeSum += float(trip.getAttribute('stopTime'))
            timeLossSum += float(trip.getAttribute('timeLoss'))

        # print('sum of waiting time:', waitingTimeSum)
        # print('sum of waiting count:', waitingCountSum)
        # print('sum of stop times', stopTimeSum)
        # print('sum of timeloss', timeLossSum)

        return waitingTimeSum, waitingCountSum, stopTimeSum, timeLossSum


