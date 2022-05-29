# -*- coding: utf-8 -*-
# @Time ： 2022/5/27 10:33
# @File ： 第二题：弃风.py
# @IDE ：  PyCharm
import numpy as np
import pandas as pd

import fireStationCost


def write_file(pd):
    with open('第五题：失负荷量.csv', 'a') as f:
        pd = round(pd, 3)
        pd = str(pd)
        f.write('{}\n'.format(pd))
        f.close()


# 计算弃风量
def get_wind_loss(**kwargs):
    wind_loss = []
    for i in range(len(kwargs['data_wind_300'])):
        wind_loss_num = -kwargs['target_fire'][i] + kwargs['fireStation1'][i] + kwargs['data_wind_300'][i]
        wind_loss.append(round(wind_loss_num, 3))
    return wind_loss


# 计算总失负荷量
def get_loss_load(load_loss):
    loss_load_sum = 0
    for i in range(len(load_loss)):
        if load_loss[i] < 0:
            loss_load_sum += load_loss[i]
    return -loss_load_sum


# 判断是否超出范围
def judge(p, up, down):
    if p > up:
        return up, 'up'
    elif p < down:
        return down, 'down'
    else:
        return p, 'ok'


def get_wind_load(load_loss):
    loss_wind_sum = 0
    for i in range(len(load_loss)):
        if load_loss[i] > 0:
            loss_wind_sum += load_loss[i]
    return loss_wind_sum


# 煤费用
def coalCost(data_group_1):
    # 计算煤用量
    cost_1 = []
    for i in range(len(data_group_1)):
        cost_1.append(fireStationCost.fireStationRunCost(data_group_1[i], 0.226, 30.42, 786.80))
    # 将结果转化为array数组
    cost_1 = np.array(cost_1)
    # 计算15min内的用煤量
    cost_1 = cost_1 * 0.25
    # 计算15min内的用煤费用（700元/吨）
    cost_1 = cost_1 * 0.7
    return cost_1


# 碳费用
def carbonCost(data_group_1, carbon_price):
    cost_1 = fireStationCost.carbonEmission(data_group_1, 0.72) * carbon_price
    return cost_1


if __name__ == '__main__':
    # 读取风电场数据
    data_wind = pd.read_excel('附件1.xlsx')
    data_wind = data_wind.dropna()
    data_wind_900 = data_wind['w900']
    data_target = data_wind['l900']
    
    # 转换为array
    data_wind_900, data_target = np.array(data_wind_900), np.array(data_target)
    # 计算机组1功率
    fireStation = data_target - data_wind_900
    # 判断机组1功率是否超出范围
    fireStation1 = []
    for i in range(len(fireStation)):
        p, judge_result = judge(fireStation[i], 600, 180)
        fireStation1.append(p)
    
    # 计算弃风量
    load_loss = get_wind_loss(data_wind_300=data_wind_900, fireStation1=fireStation1,
                              target_fire=data_target)
    # print(load_loss)
    
    # 计算总失负荷量
    loss_load_sum = get_loss_load(load_loss) * 0.25
    # 计算丢负荷损失
    loss_load_cost = loss_load_sum * 8 * 1000
    # print(loss_load_sum)
    
    #####计算储能成本
    # 计算单次最大丢负荷量
    loss_load_max = min(load_loss)
    # 取绝对值
    loss_load_max = abs(loss_load_max)
    # 所需储能容量
    storage_capacity = loss_load_max / 0.9
    ## 储能投资成本
    # 单位功率成本
    unit_cost = storage_capacity * 3000 * 1000
    # 单位能量成本
    unit_energy_cost = storage_capacity * 0.25 * 3000 * 1000
    ## 储能运维成本
    storage_capacity_cost = loss_load_sum * 0.05 * 1000
    # 总储能成本
    storage_cost = (unit_cost + unit_energy_cost) / 10 / 365 + storage_capacity_cost
    
    # 计算弃风量
    loss_wind_sum = get_wind_load(load_loss) * 0.25
    # 计算弃风损失
    loss_wind_cost = loss_wind_sum * 0.3 * 1000
    
    # 煤费用
    cost_coal = coalCost(data_group_1=fireStation1)
    coalSum = sum(cost_coal)
    
    # 碳排放费用
    carbon_price = 60
    cost_carbon = carbonCost(data_group_1=fireStation1, carbon_price=carbon_price)
    
    # 总成本
    total_cost = loss_wind_cost + coalSum + cost_carbon + storage_cost
    loadSum = sum(data_target) * 0.25
    
    print('风电装机900MW、替代机组2、3时，丢负荷电量{}MWh，最大失负荷功率为{}MW，需要配备最小储能容量为{}MWh。考虑碳捕集成本60元/吨，此时单位供电成本为{}元/KWh'.format(
        round(loss_load_sum, 3),
        round(loss_load_max, 3),
        round(storage_capacity, 3),
        round(total_cost / loadSum / 1000, 3)))
