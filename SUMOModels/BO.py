import numpy as np
from bayes_opt import BayesianOptimization
from SUMOModels.tuningObjectFunction import fit_fun_BO_offset, fit_fun_BO_hyperparameters, update_json


def tuning_hyperparameters(init_points=10, n_iter=50):
    """
    参数空间：
        "green_wave": [0, 10, 20, 30, 40, 10, 20, 30, 40],
        "HCS_b1": 0.3,
        "HCS_b2": 0.5,
        "DB_b3": 0.75,
        "LQ_r": 0.5,
        "LQ_scale": 0.2
    """
    # Bounded region of parameter space
    pbounds = {'green_wave_1': (0, 90),
               'green_wave_2': (0, 90),
               'green_wave_3': (0, 90),
               'green_wave_4': (0, 90),
               'green_wave_5': (0, 90),
               'green_wave_6': (0, 90),
               'green_wave_7': (0, 90),
               'green_wave_8': (0, 90),
               'green_wave_9': (0, 90),
               'HCS_b1': (0.15, 0.40),
               'HCS_b2': (0.45, 0.65),
               'DB_b3': (0.6, 0.9),
               'LQ_r': (0.1, 1),
               'LQ_scale': (0.1, 0.5)
               }
    optimizer = BayesianOptimization(
        f=fit_fun_BO_hyperparameters,
        pbounds=pbounds,
        verbose=2,  # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
        random_state=1,
    )

    optimizer.maximize(
        init_points=init_points,
        n_iter=n_iter,
    )

    # 更新param.json文件
    opt_params = optimizer.max['params']
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

    return optimizer.max


def tuning_offset(init_points=10, n_iter=50):
    """参数空间："green_wave": [0, 10, 20, 30, 40, 10, 20, 30, 40]"""
    # Bounded region of parameter space
    pbounds = {'green_wave_1': (0, 90),
               'green_wave_2': (0, 90),
               'green_wave_3': (0, 90),
               'green_wave_4': (0, 90),
               'green_wave_5': (0, 90),
               'green_wave_6': (0, 90),
               'green_wave_7': (0, 90),
               'green_wave_8': (0, 90),
               'green_wave_9': (0, 90),
               }
    optimizer = BayesianOptimization(
        f=fit_fun_BO_offset,
        pbounds=pbounds,
        verbose=2,  # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
        random_state=1,
    )

    optimizer.maximize(
        init_points=init_points,
        n_iter=n_iter,
    )

    # 更新param.json文件
    opt_params = optimizer.max['params']
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

    return optimizer.max


if __name__ == '__main__':
    """
        单独运行Part1 调节超参数(offset+HCS中的参数)
        单独运行Part2 调节offset(注:需要先找到合适的tuningObjectFunction.fit_fun_BO中的controlParaList及"HCS_b1"等五个参数)
    """

    """
    Part1
        基于BO调节超参数
        Args:
            init_points:初始点个数 {int}
            n_iter:迭代次数 {int}
        Returns:
            result: {dict:2}
                target:最优适应度值 {float64()}
                params:最优参数 {dict:14}
    """
    init_points = 2
    n_iter = 3
    result = tuning_hyperparameters(init_points, n_iter)

    """
    Part2
        基于BO调节offset
        Args:
            init_points:初始点个数 {int}
            n_iter:迭代次数 {int}
        Returns:
            result: {dict:2}
                target:最优适应度值 {float64()}
                params:最优offsetList参数 {dict:9}
    """
    # init_points = 2
    # n_iter = 3
    # result = tuning_offset(init_points, n_iter)
