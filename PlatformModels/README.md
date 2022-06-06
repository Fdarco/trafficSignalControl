**暂定，待修改**
#### TODO
- 确定合理的green_wave
- 调节参数

#### 参考论文
A Hybrid Strategy for Real-Time Traffic Signal Control of Urban Road Networks

#### 算法流程
* 以秒为单位从sumo采集各车道实时车流量(辆/时)和各车道车辆数量(辆)
* 根据信号控制模块的混合策略实时输出各路口绿灯时长
* sumo实时调整绿灯时长
* 根据sumo记录的各路口或各车辆的信息，评价信号控制的性能

先仿真一段时间，根据反馈的性能值自适应地调节信号控制系统中的超参数。
或者较优超参数后，固定超参数，继续仿真。

#### 文件说明

|     **名称**      |  **说明**   |  **进度**  |
|:---------------:|:---------:|:--------:|
|     main.py     |    主函数    |   done   |
|   strategy_py   |   控制策略    |   done   |
| db_strategy_py  |   DB策略    |   done   |
| lq_strategy_py  |   LQ策略    |   done   |
| hcs_strategy_py |   混合策略    |   done   |
|    README.md    |   说明文档    | progress |
|     LQ策略.md     | LQ策略的说明文档 |   done   |
|   junction.py   |   需调控路口   |   done   |
|     others      |   其他文件    |   done   |
|   param.json    |    参数     |   done   |
|   SUMOModels    |  sumo文件   | progress |







