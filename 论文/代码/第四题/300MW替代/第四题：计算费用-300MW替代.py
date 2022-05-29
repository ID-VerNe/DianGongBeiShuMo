# -*- coding: utf-8 -*-
# @Time ： 2022/5/27 15:29
# @File ： 第四题：计算费用-300MW替代.py
# @IDE ：  PyCharm

import csv

import numpy as np
import pandas as pd

import fireStationCost


# 煤费用
def coalCost(data_group_1, data_group_2):
    # 计算煤用量
    cost_1, cost_2 = [], []
    for i in range(len(data_group_1)):
        cost_1.append(fireStationCost.fireStationRunCost(data_group_1[i],
                                                         0.226, 30.42, 786.80))
        cost_2.append(fireStationCost.fireStationRunCost(data_group_2[i],
                                                         0.588, 65.12, 451.32))
    # 将结果转化为array数组
    cost_1, cost_2 = np.array(cost_1), np.array(cost_2)
    # 计算15min内的用煤量
    cost_1, cost_2 = cost_1 * 0.25, cost_2 * 0.25
    # 计算15min内的用煤费用（700元/吨）
    cost_1, cost_2 = cost_1 * 0.7, cost_2 * 0.7
    return cost_1, cost_2


# 碳费用
def carbonCost(data_group_1, data_group_2, carbon_price):
    cost_1 = fireStationCost.carbonEmission(data_group_1, 0.72) * carbon_price
    cost_2 = fireStationCost.carbonEmission(data_group_2, 0.75) * carbon_price
    return cost_1, cost_2


# 计算弃风量
def get_wind_load(load_loss):
    loss_wind_sum = 0
    for i in range(len(load_loss)):
        if load_loss[i] > 0:
            loss_wind_sum += load_loss[i]
    return loss_wind_sum


# 主函数
def main(carbon_price):
    data = pd.read_csv('第二题：目标、机组1、2、风电、差值、弃风量.csv')
    data_group_1 = data['机组1']
    data_group_2 = data['机组2']
    data_wind_loss = data['弃风量']
    data_wind = data['风电']
    data_load = data['目标']
    
    # 计算弃风量
    loss_wind_sum = get_wind_load(data_wind_loss) * 0.25
    # 计算弃风量损失
    loss_wind_cost = loss_wind_sum * 0.3 * 1000
    
    # 计算风电运维成本
    wind_sum = sum(data_wind) * 0.25
    wind_sum = wind_sum * 0.045 * 1000
    # 煤费用
    # 火电运行成本
    coal_cost_1, coal_cost_2 = coalCost(data_group_1, data_group_2)
    coal_cost_1 = sum(coal_cost_1)
    coal_cost_2 = sum(coal_cost_2)
    coalSum = coal_cost_1 + coal_cost_2
    # 碳排放成本
    carbon_cost_1, carbon_cost_2 = carbonCost(data_group_1, data_group_2, carbon_price)
    carbonSum = carbon_cost_1 + carbon_cost_2
    # 总成本
    total_cost = coalSum + carbonSum + loss_wind_cost + wind_sum
    loadSum = sum(data_load) * 0.25
    # print(loadSum)
    print('当碳捕集成本为{}元/吨时，火电运行成本为{}万元，碳捕集成本为{}万元，风电运维成本为{}万元，'
          '弃风电量为{}MWh，弃风损失为{}万元，系统单位供电成本为{}元/KWh'.format(
        round(carbon_price, 3),
        round(coalSum / 10000, 3),
        round(carbonSum / 10000, 3),
        round(wind_sum / 10000, 3),
        round(loss_wind_sum, 3),
        round(loss_wind_cost / 10000, 3),
        round(total_cost / loadSum / 1000, 3),
        3))
    # 写入csv
    with open('第四题：计算费用-300MW替代.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([carbon_price, coalSum / 10000, carbonSum / 10000, wind_sum / 10000,
                         loss_wind_sum, loss_wind_cost / 10000, total_cost / loadSum / 1000])


if __name__ == '__main__':
    carbonPrice = [0, 60, 80, 100]
    for i in carbonPrice:
        main(i)
