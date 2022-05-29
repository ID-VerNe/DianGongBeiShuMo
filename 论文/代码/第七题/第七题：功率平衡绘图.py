# -*- coding: utf-8 -*-
# @Time ： 2022/5/27 21:35
# @File ： 第七题：弃风量和失负荷量.py
# @IDE ：  PyCharm

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

##################################
# 读取数据并处理
# 将数组转换为列表
def list_data(data):
    data_list = data.tolist()
    return data_list


# 数据按96个时间点分组
def group_data(data_load_list, data_wind_list, data_time_list):
    data_load_group = []
    data_wind_group = []
    data_time_group = []
    for i in range(0, len(data_load_list), 96):
        data_load_group.append(data_load_list[i:i + 96])
        data_wind_group.append(data_wind_list[i:i + 96])
        data_time_group.append(data_time_list[i:i + 96])
    return data_load_group, data_wind_group, data_time_group


# 将时间戳转换为字符串
def time_to_str(data_time_group):
    data_time_str = []
    for i in range(len(data_time_group)):
        data_time_str.append(str(data_time_group[i]))
    return data_time_str


# 读取数据
def read_data():
    data = pd.read_excel('附件2.xlsx')
    data_load = data['负荷功率(MW)']
    data_wind = data['风电功率(MW)']
    data_time = data['时间']
    
    data_load_list = list_data(data_load)
    data_wind_list = list_data(data_wind)
    data_time_list = list_data(data_time)
    
    data_time_list = time_to_str(data_time_list)
    
    data_load_group, data_wind_group, data_time_group = group_data(data_load_list,
                                                                   data_wind_list,
                                                                   data_time_list)
    data_load_group, data_wind_group, data_time_group = np.array(data_load_group), \
                                                        np.array(data_wind_group),\
                                                        np.array(
        data_time_group)
    return data_load_group, data_wind_group, data_time_group


##########################
##弃风总量和丢负荷总量

# 计算弃风量
def get_wind_load(load_loss):
    loss_wind_sum = 0
    for i in range(len(load_loss)):
        if load_loss[i] > 0:
            loss_wind_sum += load_loss[i]
    return loss_wind_sum


# 计算丢负荷量
def get_loss_load(load_loss):
    loss_load_sum = 0
    for i in range(len(load_loss)):
        if load_loss[i] < 0:
            loss_load_sum += load_loss[i]
    return loss_load_sum


##########################
## 计算弃风量

def get_wind_loss(**kwargs):
    wind_loss = []
    for i in range(len(kwargs['data_wind_300'])):
        wind_loss_num = -kwargs['target_fire'][i] + kwargs['fireStation1'][i]\
                        + kwargs['data_wind_300'][i]
        wind_loss.append(round(wind_loss_num, 3))
    return wind_loss


################################
## 判断范围
# 判断是否超出范围
def judge(p, up, down):
    if p > up:
        return up, 'up'
    elif p < down:
        return down, 'down'
    else:
        return p, 'ok'


if __name__ == '__main__':
    data_load, data_wind, data_time = read_data()
    
    # 计算火电功率
    data_fire_raw = data_load - data_wind
    data_fire = []
    # 判断火电功率范围
    for i in range(len(data_fire_raw)):
        data_fire.append([])
        for j in range(len(data_fire_raw[i])):
            data_fire_temp, flag = judge(data_fire_raw[i][j], 600, 180)
            data_fire[i].append(data_fire_temp)
            # print(data_fire[0])
    
    # 计算弃风量
    data_wind_loss = []
    for i in range(len(data_fire)):
        data_wind_loss.append(
            get_wind_loss(data_wind_300=data_wind[i],
                          target_fire=data_load[i], fireStation1=data_fire[i]))
    # print(data_wind_loss[0])
    
    ###取出最值
    # 每日最大值
    data_wind_loss_max_day = np.array(data_wind_loss).max(axis=1)
    # print(data_wind_loss_max_day)
    # 每日最小值
    data_wind_loss_min_day = np.array(data_wind_loss).min(axis=1)
    # print(data_wind_loss_min_day)
    # 总最大值
    data_wind_loss_max_sum = np.array(data_wind_loss).max()
    # print(data_wind_loss_max_sum)
    # 总最小值
    data_wind_loss_min_sum = np.array(data_wind_loss).min()
    # print(data_wind_loss_min_sum)
    
    ###计算弃风总量和丢负荷总量
    # 计算弃风总量和丢负荷总量
    loss_wind_sum, loss_load_sum = [], []
    for i in range(len(data_wind_loss)):
        loss_wind_sum.append(get_wind_load(data_wind_loss[i]))
        loss_load_sum.append(get_loss_load(data_wind_loss[i]))
    # print(loss_wind_sum)
    # print(loss_load_sum)

    data_wind_loss=np.array(data_wind_loss)
    #展开成一维
    data_wind_loss_1d=data_wind_loss.flatten()
    
    str_base='7.'
    time_new=[]
    for i in range(16):
        time_new.append(str_base+str(i+1))
    data_new = []
    for i in range(0, 96*16, 96):
        data_new.append(i)
    
    plt.figure(figsize=(7, 3), dpi=800)
    ax = plt.subplot(111)

    plt.plot(data_wind_loss_1d, color='blue', linewidth=1.5, linestyle='-')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.title('功率平衡图')
    plt.xlabel('时间')
    plt.ylabel('功率/MW')
    plt.grid(True)
    xmajorLocator = MultipleLocator(96)
    ax.xaxis.set_major_locator(xmajorLocator)
    plt.xticks(data_new, time_new)
    #旋转x轴刻度
    plt.xticks(rotation=90)

    plt.tight_layout()
    plt.savefig('第七题：功率平衡图.png')
    plt.show()