import traci
from xml.dom.minidom import parse
from TrafficSignalControlStrategy import HCS, DB, LQ


class PerformIndex:
    @staticmethod
    def runModel(simulationTime, str_strategy):
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

        if str_strategy == "DB":
            """DB"""
            db = DB()
            db.initNetwork()
            # 路网仿真并进行信号控制
            for t in range(1, simulationTime + 1):
                traci.simulationStep()
                db.modelStep(t)
        elif str_strategy == "LQ":
            """LQ"""
            lq = LQ()
            lq.initNetwork()
            # 路网仿真并进行信号控制
            for t in range(1, simulationTime + 1):
                traci.simulationStep()
                lq.modelStep(t)
        else:
            """HCS"""
            hcs = HCS()
            hcs.initNetwork()
            # 路网仿真并进行信号控制
            for t in range(1, simulationTime + 1):
                traci.simulationStep()
                hcs.modelStep(t)
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
