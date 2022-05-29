# -*- coding: utf-8 -*-
# @Time ： 2022/5/27 15:29
# @File ： 第一题：根据发电计划计算煤用量.py
# @IDE ：  PyCharm

import numpy as np
import pandas as pd

import fireStationCost


# 煤费用
def coalCost(data_group_1, data_group_2, data_group_3):
    # 计算煤用量
    cost_1, cost_2, cost_3 = [], [], []
    for i in range(len(data_group_1)):
        cost_1.append(fireStationCost.fireStationRunCost(data_group_1[i], 0.226, 30.42, 786.80))
        cost_2.append(fireStationCost.fireStationRunCost(data_group_2[i], 0.588, 65.12, 451.32))
        cost_3.append(fireStationCost.fireStationRunCost(data_group_3[i], 0.785, 139.6, 1049.50))
    # 将结果转化为array数组
    cost_1, cost_2, cost_3 = np.array(cost_1), np.array(cost_2), np.array(cost_3)
    # 计算15min内的用煤量
    cost_1, cost_2, cost_3 = cost_1 * 0.25, cost_2 * 0.25, cost_3 * 0.25
    # 计算15min内的用煤费用（700元/吨）
    cost_1, cost_2, cost_3 = cost_1 * 0.7, cost_2 * 0.7, cost_3 * 0.7
    return cost_1, cost_2, cost_3


# 碳费用
def carbonCost(data_group_1, data_group_2, data_group_3, carbon_price):
    cost_1 = fireStationCost.carbonEmission(data_group_1, 0.72) * carbon_price
    cost_2 = fireStationCost.carbonEmission(data_group_2, 0.75) * carbon_price
    cost_3 = fireStationCost.carbonEmission(data_group_3, 0.79) * carbon_price
    return cost_1, cost_2, cost_3


# 主函数
def main(carbon_price):
    data = pd.read_csv('第一题：目标、机组1、2、3、差值.csv')
    data_group_1 = data['机组1']
    data_group_2 = data['机组2']
    data_group_3 = data['机组3']
    data_load = data['目标功率']
    
    # 煤费用
    # 火电运行成本
    coal_cost_1, coal_cost_2, coal_cost_3 = coalCost(data_group_1, data_group_2, data_group_3)
    coal_cost_1 = sum(coal_cost_1)
    coal_cost_2 = sum(coal_cost_2)
    coal_cost_3 = sum(coal_cost_3)
    coalSum = coal_cost_1 + coal_cost_2 + coal_cost_3
    # 碳排放成本
    carbon_cost_1, carbon_cost_2, carbon_cost_3 = carbonCost(data_group_1, data_group_2, data_group_3, carbon_price)
    carbonSum = carbon_cost_1 + carbon_cost_2 + carbon_cost_3
    # 总成本
    total_cost = coalSum + carbonSum
    loadSum = sum(data_load) * 0.25
    # print(loadSum)
    print('当碳捕集成本为{}元/吨时，火电运行成本为{}万元，碳捕集成本为{}万元，'
          '总成本为{}万元，系统单位供电成本为{}元/KWh'.format(round(carbon_price, 3), round(coalSum / 10000, 3),
                                             round(carbonSum / 10000, 3),
                                             round(total_cost / 10000, 3),
                                             round(total_cost / loadSum / 1000, 3),
                                             3))


if __name__ == '__main__':
    carbonPrice = [0, 60, 80, 100]
    for i in carbonPrice:
        main(i)
