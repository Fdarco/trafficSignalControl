### 信号控制模块
#### 参考论文
A Hybrid Strategy for Real-Time Traffic Signal Control of Urban Road Networks

#### 算法流程
* 以秒为单位从sumo采集各车道实时车流量(辆/时)和各车道车辆数量(辆)
* 根据信号控制模块的混合策略实时输出各路口绿灯时长
* sumo实时调整绿灯时长
* 根据sumo记录的各路口或各车辆的信息，评价信号控制的性能

先仿真一段时间，根据反馈的性能值自适应地调节信号控制系统中的超参数。
或者较优超参数后，固定超参数，继续仿真。

在python终端，切换目录至traffic-signal-control\SUMOModels\gridNetwork，分别运行以下语句，可在sumo中产生不同流量的车流

    python randomTrips.py -n GridNetwork.net.xml -b 0 -e 3600 -p 0.75 -r GridNetwork_high.rou.xml
    python randomTrips.py -n GridNetwork.net.xml -b 0 -e 3600 -p 1 -r GridNetwork_middle.rou.xml
    python randomTrips.py -n GridNetwork.net.xml -b 0 -e 3600 -p 2 -r GridNetwork_low.rou.xml
找到代码中所有的traci.start模块，修改为对应的'GridNetwork_high.rou.xml'、'GridNetwork_middle.rou.xml'、'GridNetwork_low.rou.xml'名称

    traci.start(
            [
                # 'sumo-gui', '-n', 'GridNetwork.net.xml',  # 显示sumo-gui界面
                'sumo', '-n', 'GridNetwork.net.xml',
                '-r', 'GridNetwork_middle.rou.xml',
                '--tripinfo-output', 'GridNetwork.tripinfo.xml',
                '--emission-output', 'GridNetwork.emission.xml',
            ]
        )
#### 文件说明
代码整合进度

|               **名称**               |  **说明**   |  **进度**  |
|:----------------------------------:|:---------:|:--------:|
|              main.py               |    主函数    | progress |
|            strategy_py             |   控制策略    |   done   |
|           db_strategy_py           |   DB策略    |   done   |
|           lq_strategy_py           |   LQ策略    | progress |
|          hcs_strategy_py           |   混合策略    | progress |
|             README.md              |   说明文档    | progress |
|              LQ策略.md               | LQ策略的说明文档 | progress |
|            junction.py             |    路口     |   done   |
|               others               |   其他文件    | progress |
|             param.json             |    参数     | progress |
|             SUMOModels             |  sumo文件   | progress |
|        modify_green_time.py        |  修正绿灯时长   |   done   |


#### 问题
PSO  BO  　







