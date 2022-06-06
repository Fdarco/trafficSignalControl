# ****************************************************************************
# created at: [2022-04-06 09:49]
# fudaocheng@pjlab.org.cn 
# ****************************************************************************
# 建立信号控制模型与仿真模型间的数据传输通道


from statistics import mean
import traci
from traci._trafficlight import Logic, Phase


class InterPara:
    # 方向是 北，东，南，西（以北开始顺时针转动）
    InterPara = {
        'j_1': ['z_1', 'z_39', 'z_15', 'z_25'],
        'j_2': ['z_5', 'z_38', 'z_19', 'z_26'],
        'j_3': ['z_9', 'z_37', 'z_23', 'z_27'],
        'j_4': ['z_2', 'z_43', 'z_14', 'z_29'],
        'j_5': ['z_6', 'z_42', 'z_18', 'z_30'],
        'j_6': ['z_10', 'z_41', 'z_22', 'z_31'],
        'j_7': ['z_3', 'z_47', 'z_13', 'z_33'],
        'j_8': ['z_7', 'z_46', 'z_17', 'z_34'],
        'j_9': ['z_11', 'z_45', 'z_21', 'z_35']
    }

    @staticmethod
    def getRoadIDList(InterID):
        return InterPara.InterPara[InterID]


class NetworkControl:
    # 由于每个交叉口的相位差是固定的
    # 所以信号控制可以以交叉口为单位进行更新
    @staticmethod
    def signalControl(junctionID, controlPara):
        for i in range(len(controlPara)):
            if controlPara[i] <= 0:
                controlPara[i] = 5
            if not isinstance(controlPara[i], int):
                controlPara[i] = int(controlPara[i])
        logicChange = Logic(
            programID='0',
            type=0,
            currentPhaseIndex=0,
            phases=(
                Phase(duration=controlPara[0], state='GGgGrrGrrGrr'),
                Phase(duration=2.0, state='GyyGrrGrrGrr'),
                Phase(duration=1.0, state='GrrGrrGrrGrr'),
                Phase(duration=controlPara[1], state='GrrGGgGrrGrr'),
                Phase(duration=2.0, state='GrrGyyGrrGrr'),
                Phase(duration=1.0, state='GrrGrrGrrGrr'),
                Phase(duration=controlPara[2], state='GrrGrrGGgGrr'),
                Phase(duration=2.0, state='GrrGrrGyyGrr'),
                Phase(duration=1.0, state='GrrGrrGrrGrr'),
                Phase(duration=controlPara[3], state='GrrGrrGrrGGg'),
                Phase(duration=2.0, state='GrrGrrGrrGyy'),
                Phase(duration=1.0, state='GrrGrrGrrGrr')
            ),
            subParameter={}
        )

        traci.trafficlight.setProgramLogic(junctionID, logicChange)

    # using Q = KV
    @staticmethod
    def getDemand(InterID):
        edges = InterPara.getRoadIDList(InterID)
        demandList = []
        for ed in edges:
            meanSpeed = traci.edge.getLastStepMeanSpeed(ed)
            meanDensity = traci.edge.getLastStepVehicleNumber(ed) / 500
            demandList.append(meanSpeed * meanDensity)

        return demandList

    @staticmethod
    def getMeanVelocity(InterID):
        edges = InterPara.getRoadIDList(InterID)
        MSList = []
        for ed in edges:
            meanSpeed = traci.edge.getLastStepMeanSpeed(ed)
            MSList.append(meanSpeed)

        return MSList

    @staticmethod
    def getVehicleNum(InterID):
        edges = InterPara.getRoadIDList(InterID)
        VNList = []
        for ed in edges:
            vehNum = traci.edge.getLastStepVehicleNumber(ed)
            VNList.append(vehNum)

        return VNList


if __name__ == '__main__':
    traci.start(
        [
            'sumo', '-n', 'GridNetwork.net.xml',
            '-r', 'GridNetwork.rou.xml',
        ]
    )

    cnt = 0
    while cnt < 20:
        print(cnt)
        traci.simulationStep()
        print(NetworkControl.getDemand('j_1'))
        print(traci.trafficlight.getAllProgramLogics('j_1'))
        if cnt == 10:
            NetworkControl.signalControl('j_1', [13, 25, 27, 15])

        print('=' * 20)
        cnt += 1
