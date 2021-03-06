import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


# 定义路网
# TODO:1.将路网数据以外部数据形式导入2.自动随机生成指定规模的路网

def road_networks():
    # 多重有向图
    g = nx.MultiDiGraph()

    # topology construction logic(见"示意图.pdf")
    # 需调控路口
    g.add_node(1, name='j_1')
    g.add_node(2, name='j_2')
    g.add_node(3, name='j_3')
    g.add_node(4, name='j_4')
    g.add_node(5, name='j_5')
    g.add_node(6, name='j_6')
    g.add_node(7, name='j_7')
    g.add_node(8, name='j_8')
    g.add_node(9, name='j_9')

    # 辅助路口(网络外部路口，只提供车流，不需要调控)
    g.add_node(10, name='j_01')
    g.add_node(11, name='j_02')
    g.add_node(12, name='j_03')
    g.add_node(13, name='j_04')
    g.add_node(14, name='j_05')
    g.add_node(15, name='j_06')
    g.add_node(16, name='j_07')
    g.add_node(17, name='j_08')
    g.add_node(18, name='j_09')
    g.add_node(19, name='j_010')
    g.add_node(20, name='j_011')
    g.add_node(21, name='j_012')

    # 路径(路口i和j之间有6个车道:i->j有lmr,j->i有lmr):假设左转l,中间直行m,右转r
    g.add_edge(10, 1, name='z_1_l')
    g.add_edge(1, 4, name='z_2_l')
    g.add_edge(4, 7, name='z_3_l')
    g.add_edge(7, 13, name='z_4_l')
    g.add_edge(11, 2, name='z_5_l')
    g.add_edge(2, 5, name='z_6_l')
    g.add_edge(5, 8, name='z_7_l')
    g.add_edge(8, 14, name='z_8_l')
    g.add_edge(12, 3, name='z_9_l')
    g.add_edge(3, 6, name='z_10_l')
    g.add_edge(6, 9, name='z_11_l')
    g.add_edge(9, 15, name='z_12_l')
    g.add_edge(13, 7, name='z_13_l')
    g.add_edge(7, 4, name='z_14_l')
    g.add_edge(4, 1, name='z_15_l')
    g.add_edge(1, 10, name='z_16_l')
    g.add_edge(14, 8, name='z_17_l')
    g.add_edge(8, 5, name='z_18_l')
    g.add_edge(5, 2, name='z_19_l')
    g.add_edge(2, 11, name='z_20_l')
    g.add_edge(15, 9, name='z_21_l')
    g.add_edge(9, 6, name='z_22_l')
    g.add_edge(6, 3, name='z_23_l')
    g.add_edge(3, 12, name='z_24_l')
    g.add_edge(16, 1, name='z_25_l')
    g.add_edge(1, 2, name='z_26_l')
    g.add_edge(2, 3, name='z_27_l')
    g.add_edge(3, 19, name='z_28_l')
    g.add_edge(17, 4, name='z_29_l')
    g.add_edge(4, 5, name='z_30_l')
    g.add_edge(5, 6, name='z_31_l')
    g.add_edge(6, 20, name='z_32_l')
    g.add_edge(18, 7, name='z_33_l')
    g.add_edge(7, 8, name='z_34_l')
    g.add_edge(8, 9, name='z_35_l')
    g.add_edge(9, 21, name='z_36_l')
    g.add_edge(19, 3, name='z_37_l')
    g.add_edge(3, 2, name='z_38_l')
    g.add_edge(2, 1, name='z_39_l')
    g.add_edge(1, 16, name='z_40_l')
    g.add_edge(20, 6, name='z_41_l')
    g.add_edge(6, 5, name='z_42_l')
    g.add_edge(5, 4, name='z_43_l')
    g.add_edge(4, 17, name='z_44_l')
    g.add_edge(21, 9, name='z_45_l')
    g.add_edge(9, 8, name='z_46_l')
    g.add_edge(8, 7, name='z_47_l')
    g.add_edge(7, 18, name='z_48_l')
    g.add_edge(10, 1, name='z_1_m')
    g.add_edge(1, 4, name='z_2_m')
    g.add_edge(4, 7, name='z_3_m')
    g.add_edge(7, 13, name='z_4_m')
    g.add_edge(11, 2, name='z_5_m')
    g.add_edge(2, 5, name='z_6_m')
    g.add_edge(5, 8, name='z_7_m')
    g.add_edge(8, 14, name='z_8_m')
    g.add_edge(12, 3, name='z_9_m')
    g.add_edge(3, 6, name='z_10_m')
    g.add_edge(6, 9, name='z_11_m')
    g.add_edge(9, 15, name='z_12_m')
    g.add_edge(13, 7, name='z_13_m')
    g.add_edge(7, 4, name='z_14_m')
    g.add_edge(4, 1, name='z_15_m')
    g.add_edge(1, 10, name='z_16_m')
    g.add_edge(14, 8, name='z_17_m')
    g.add_edge(8, 5, name='z_18_m')
    g.add_edge(5, 2, name='z_19_m')
    g.add_edge(2, 11, name='z_20_m')
    g.add_edge(15, 9, name='z_21_m')
    g.add_edge(9, 6, name='z_22_m')
    g.add_edge(6, 3, name='z_23_m')
    g.add_edge(3, 12, name='z_24_m')
    g.add_edge(16, 1, name='z_25_m')
    g.add_edge(1, 2, name='z_26_m')
    g.add_edge(2, 3, name='z_27_m')
    g.add_edge(3, 19, name='z_28_m')
    g.add_edge(17, 4, name='z_29_m')
    g.add_edge(4, 5, name='z_30_m')
    g.add_edge(5, 6, name='z_31_m')
    g.add_edge(6, 20, name='z_32_m')
    g.add_edge(18, 7, name='z_33_m')
    g.add_edge(7, 8, name='z_34_m')
    g.add_edge(8, 9, name='z_35_m')
    g.add_edge(9, 21, name='z_36_m')
    g.add_edge(19, 3, name='z_37_m')
    g.add_edge(3, 2, name='z_38_m')
    g.add_edge(2, 1, name='z_39_m')
    g.add_edge(1, 16, name='z_40_m')
    g.add_edge(20, 6, name='z_41_m')
    g.add_edge(6, 5, name='z_42_m')
    g.add_edge(5, 4, name='z_43_m')
    g.add_edge(4, 17, name='z_44_m')
    g.add_edge(21, 9, name='z_45_m')
    g.add_edge(9, 8, name='z_46_m')
    g.add_edge(8, 7, name='z_47_m')
    g.add_edge(7, 18, name='z_48_m')
    g.add_edge(10, 1, name='z_1_r')
    g.add_edge(1, 4, name='z_2_r')
    g.add_edge(4, 7, name='z_3_r')
    g.add_edge(7, 13, name='z_4_r')
    g.add_edge(11, 2, name='z_5_r')
    g.add_edge(2, 5, name='z_6_r')
    g.add_edge(5, 8, name='z_7_r')
    g.add_edge(8, 14, name='z_8_r')
    g.add_edge(12, 3, name='z_9_r')
    g.add_edge(3, 6, name='z_10_r')
    g.add_edge(6, 9, name='z_11_r')
    g.add_edge(9, 15, name='z_12_r')
    g.add_edge(13, 7, name='z_13_r')
    g.add_edge(7, 4, name='z_14_r')
    g.add_edge(4, 1, name='z_15_r')
    g.add_edge(1, 10, name='z_16_r')
    g.add_edge(14, 8, name='z_17_r')
    g.add_edge(8, 5, name='z_18_r')
    g.add_edge(5, 2, name='z_19_r')
    g.add_edge(2, 11, name='z_20_r')
    g.add_edge(15, 9, name='z_21_r')
    g.add_edge(9, 6, name='z_22_r')
    g.add_edge(6, 3, name='z_23_r')
    g.add_edge(3, 12, name='z_24_r')
    g.add_edge(16, 1, name='z_25_r')
    g.add_edge(1, 2, name='z_26_r')
    g.add_edge(2, 3, name='z_27_r')
    g.add_edge(3, 19, name='z_28_r')
    g.add_edge(17, 4, name='z_29_r')
    g.add_edge(4, 5, name='z_30_r')
    g.add_edge(5, 6, name='z_31_r')
    g.add_edge(6, 20, name='z_32_r')
    g.add_edge(18, 7, name='z_33_r')
    g.add_edge(7, 8, name='z_34_r')
    g.add_edge(8, 9, name='z_35_r')
    g.add_edge(9, 21, name='z_36_r')
    g.add_edge(19, 3, name='z_37_r')
    g.add_edge(3, 2, name='z_38_r')
    g.add_edge(2, 1, name='z_39_r')
    g.add_edge(1, 16, name='z_40_r')
    g.add_edge(20, 6, name='z_41_r')
    g.add_edge(6, 5, name='z_42_r')
    g.add_edge(5, 4, name='z_43_r')
    g.add_edge(4, 17, name='z_44_r')
    g.add_edge(21, 9, name='z_45_r')
    g.add_edge(9, 8, name='z_46_r')
    g.add_edge(8, 7, name='z_47_r')
    g.add_edge(7, 18, name='z_48_r')

    # draw graph with labels
    '''
    nx.draw(g)
    plt.show()
    '''
    return g
