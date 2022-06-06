import json
import numpy as np
from SUMOModels import hyperparametersRunModel, offsetRunModel
from SUMOModels.OffsetSet import OffsetSet


def read_json_data(json_path, x):
    dim = x.shape[0]
    with open(json_path, 'rb') as f:
        if dim == 14:
            x2params = {"green_wave": (x[0:9]).tolist(), "HCS_b1": x[9], "HCS_b2": x[10], "DB_b3": x[11], "LQ_r": x[12],
                        "LQ_scale": x[13], "Loss_j": 12, "green_time_g_N": [19, 19, 20, 20], "T": 40,
                        "S_z": [1500, 1500, 1500, 1500], "xz_max": 50, "g_ijmin": 10, "C": 90, "num_j_in": 9}
        elif dim == 9:
            x2params = {"green_wave": (x[0:9]).tolist(), "HCS_b1": 0.3, "HCS_b2": 0.5, "DB_b3": 0.75, "LQ_r": 0.5,
                        "LQ_scale": 0.2, "Loss_j": 12, "green_time_g_N": [19, 19, 20, 20], "T": 40,
                        "S_z": [1500, 1500, 1500, 1500], "xz_max": 50, "g_ijmin": 10, "C": 90, "num_j_in": 9}
        params = x2params
        dict = params
    f.close()
    return dict


def write_json_data(dict):
    json_path1 = './param.json'
    with open(json_path1, 'w') as r:
        json.dump(dict, r)
    r.close()


def update_json(x):
    json_path = './param.json'
    the_revised_dict = read_json_data(json_path, x)
    write_json_data(the_revised_dict)


def fit_fun_PSO(x):  # 适应函数
    dim = x.shape[1]
    x = x.reshape((dim,))
    # 取整offset
    with open('./param.json', 'r', encoding='utf8') as fp:
        param = json.load(fp)
    num_junction = param["num_j_in"]
    for i in range(num_junction):
        x[i] = round(x[i])
    if dim == 14:
        update_json(x)
        hyperparametersRunModel.PerformIndex.runModel(600, "HCS")
        waitingTimeSum, waitingCountSum, stopTimeSum, timeLossSum = hyperparametersRunModel.PerformIndex.getPI()
        fit = float(0.1 * waitingTimeSum + waitingCountSum + 10 * stopTimeSum + 0.1 * timeLossSum)
        return fit
    elif dim == 9:
        offsetList = x.reshape((9,)).tolist()
        controlParaList = [
            [13, 17, 15, 15],
            [12, 14, 18, 16],
            [14, 17, 13, 16],
            [13, 17, 15, 15],
            [12, 14, 18, 16],
            [14, 17, 13, 16],
            [13, 17, 15, 15],
            [12, 14, 18, 16],
            [14, 17, 13, 16]
        ]
        OC = OffsetSet(offsetList, controlParaList)
        OC.genAddFile()
        # 为了调节offset，sumo平台运行600s
        offsetRunModel.PerformIndex.runModel(600)
        waitingTimeSum, waitingCountSum, stopTimeSum, timeLossSum = offsetRunModel.PerformIndex.getPI()
        fit = float(0.1 * waitingTimeSum + waitingCountSum + 10 * stopTimeSum + 0.1 * timeLossSum)
        return fit



def fit_fun_BO_hyperparameters(green_wave_1, green_wave_2, green_wave_3, green_wave_4, green_wave_5,
               green_wave_6, green_wave_7, green_wave_8, green_wave_9, HCS_b1,
               HCS_b2, DB_b3, LQ_r, LQ_scale):  # 适应函数
    x = np.asarray([green_wave_1, green_wave_2, green_wave_3, green_wave_4, green_wave_5,
                    green_wave_6, green_wave_7, green_wave_8, green_wave_9, HCS_b1,
                    HCS_b2, DB_b3, LQ_r, LQ_scale]).reshape([1, 14])
    dim = x.shape[1]
    x = x.reshape((dim,))
    # 取整offset
    with open('./param.json', 'r', encoding='utf8') as fp:
        param = json.load(fp)
    num_junction = param["num_j_in"]
    for i in range(num_junction):
        x[i] = round(x[i])
    if dim == 14:
        update_json(x)
        hyperparametersRunModel.PerformIndex.runModel(600, "HCS")
        waitingTimeSum, waitingCountSum, stopTimeSum, timeLossSum = hyperparametersRunModel.PerformIndex.getPI()
        fit = float(0.1 * waitingTimeSum + waitingCountSum + 10 * stopTimeSum + 0.1 * timeLossSum)
        return -1 * fit
    elif dim == 9:
        offsetList = x.reshape((9,)).tolist()
        controlParaList = [
            [13, 17, 15, 15],
            [12, 14, 18, 16],
            [14, 17, 13, 16],
            [13, 17, 15, 15],
            [12, 14, 18, 16],
            [14, 17, 13, 16],
            [13, 17, 15, 15],
            [12, 14, 18, 16],
            [14, 17, 13, 16]
        ]
        OC = OffsetSet(offsetList, controlParaList)
        OC.genAddFile()
        # 为了调节offset，sumo平台运行600s
        offsetRunModel.PerformIndex.runModel(600)
        waitingTimeSum, waitingCountSum, stopTimeSum, timeLossSum = offsetRunModel.PerformIndex.getPI()
        fit = float(0.1 * waitingTimeSum + waitingCountSum + 10 * stopTimeSum + 0.1 * timeLossSum)
        return -1 * fit

def fit_fun_BO_offset(green_wave_1, green_wave_2, green_wave_3, green_wave_4, green_wave_5,
               green_wave_6, green_wave_7, green_wave_8, green_wave_9):  # 适应函数
    x = np.asarray([green_wave_1, green_wave_2, green_wave_3, green_wave_4, green_wave_5,
                    green_wave_6, green_wave_7, green_wave_8, green_wave_9]).reshape([1, 9])
    dim = x.shape[1]
    x = x.reshape((dim,))
    # 取整offset
    with open('./param.json', 'r', encoding='utf8') as fp:
        param = json.load(fp)
    num_junction = param["num_j_in"]
    for i in range(num_junction):
        x[i] = round(x[i])
    if dim == 14:
        update_json(x)
        hyperparametersRunModel.PerformIndex.runModel(600, "HCS")
        waitingTimeSum, waitingCountSum, stopTimeSum, timeLossSum = hyperparametersRunModel.PerformIndex.getPI()
        fit = float(0.1 * waitingTimeSum + waitingCountSum + 10 * stopTimeSum + 0.1 * timeLossSum)
        return -1 * fit
    elif dim == 9:
        offsetList = x.reshape((9,)).tolist()
        controlParaList = [
            [13, 17, 15, 15],
            [12, 14, 18, 16],
            [14, 17, 13, 16],
            [13, 17, 15, 15],
            [12, 14, 18, 16],
            [14, 17, 13, 16],
            [13, 17, 15, 15],
            [12, 14, 18, 16],
            [14, 17, 13, 16]
        ]
        OC = OffsetSet(offsetList, controlParaList)
        OC.genAddFile()
        # 为了调节offset，sumo平台运行600s
        offsetRunModel.PerformIndex.runModel(600)
        waitingTimeSum, waitingCountSum, stopTimeSum, timeLossSum = offsetRunModel.PerformIndex.getPI()
        fit = float(0.1 * waitingTimeSum + waitingCountSum + 10 * stopTimeSum + 0.1 * timeLossSum)
        return -1 * fit
