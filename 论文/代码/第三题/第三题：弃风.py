# -*- coding: utf-8 -*-
# @Time ： 2022/5/27 10:33
# @File ： 第二题：弃风.py
# @IDE ：  PyCharm


import os

import pandas as pd
import sympy as sp


def write_file(pd, p1, p2, pw, loss, time):
    with open('第三题：目标、机组1、3、风电、差值、弃风量.csv', 'a', encoding='utf-8') as f:
        # 清空文件内容
        f.truncate()
        dp = p1 + p2 + pw - pd
        pd, p1, p2, pw, loss = round(pd, 3), round(p1, 3), round(p2, 3), round(pw, 3), round(loss, 3)
        dp = round(dp, 3)
        pd, p1, p2, pw, dp = str(pd), str(p1), str(p2), str(pw), str(dp)
        f.write('{},{},{},{},{},{},{}\n'.format(time, pd, p1, p2, pw, dp, loss))
        f.close()


# 计算弃风量
def get_wind_loss(**kwargs):
    wind_loss = []
    for i in range(len(kwargs['data_wind_600'])):
        wind_loss_num = kwargs['data_wind_600'][i] + kwargs['p1'][i] + kwargs['p2'][i] - kwargs['data_load'][i]
        # print(i, ':', wind_loss_num)
        wind_loss.append(round(wind_loss_num, 3))
    return wind_loss


def get_wind_load(load_loss):
    loss_wind_sum = 0
    for i in range(len(load_loss)):
        if load_loss[i] > 0:
            loss_wind_sum += load_loss[i]
    return loss_wind_sum


# 双机组等微增率
def equalIR_algorithm_2(pd):
    # 初始化功率参数
    p1, p3 = sp.symbols('p_1 p_2')
    # 发电参数
    c1 = 0.226 * p1 ** 2 + 30.42 * p1 + 786.80
    c2 = 0.785 * p3 ** 2 + 139.6 * p3 + 1049.50
    # 求导
    dc1 = sp.diff(c1, p1)
    dc2 = sp.diff(c2, p3)
    # 组建方程组
    f1 = dc1 - dc2
    f4 = p1 + p3 - pd
    # 求解
    res = sp.solve({f4, f1})
    p1 = res[p1]
    p3 = res[p3]
    return p1, p3


# 判断是否超出范围
def judge(p, up, down):
    if p > up:
        return up, 'up'
    elif p < down:
        return down, 'down'
    else:
        return p, 'ok'


# 单次求解发电最优解
def single_algorithm(pd, up1=600, down1=180, up3=150, down3=45):
    p1, p2 = equalIR_algorithm_2(pd)
    p1, flag1 = judge(p1, up1, down1)
    p2, flag2 = judge(p2, up3, down3)
    if flag2 == 'down':
        p1 = pd - down3
        p1, flag1 = judge(p1, up1, down1)
        return p1, p2
    if flag1 == 'up':
        p2 = pd - up1
        p2, flag2 = judge(p2, up3, down3)
        return p1, p2
    return p1, p2


# 读取数据
def read_data():
    data_wind = pd.read_excel('附件1.xlsx')
    data_wind = data_wind.dropna()
    # print(data_wind)
    data_wind_600 = data_wind['w600 ']
    time = data_wind['时间']
    data_load = data_wind['l900']
    return data_wind_600, time, data_load


if __name__ == '__main__':
    data_wind_600, time, data_load = read_data()
    
    if os.path.exists('第三题：目标、机组1、3、风电、差值、弃风量.csv'):
        os.remove('第三题：目标、机组1、3、风电、差值、弃风量.csv')
    f = open('第三题：目标、机组1、3、风电、差值、弃风量.csv', 'a', encoding='utf-8')
    f.write('时间,目标,机组1,机组3,风电,差值,弃风量\n')
    f.close()
    
    p1_list, p2_list = [], []
    for i in range(len(data_load)):
        p1, p2 = single_algorithm(data_load[i] - data_wind_600[i])
        # print(p1, p2)
        # 写入文件
        # write_file(data_load[i], p1, p2, data_wind_300[i])
        p1_list.append(p1)
        p2_list.append(p2)
    
    # 计算弃风量
    wind_loss = get_wind_loss(data_wind_600=data_wind_600, p1=p1_list, p2=p2_list, data_load=data_load)
    # print(wind_loss)
    # 写入文件
    for i in range(len(wind_loss)):
        write_file(data_load[i], p1_list[i], p2_list[i], data_wind_600[i], wind_loss[i], time[i])
    
    # 取出弃风量的最大值
    min_wind_loss = min(wind_loss)
    # print(min_wind_loss)
    
    # 计算可以减少的风电装机容量
    wind_power_min = 600 - min_wind_loss
    print('缺额的风电装机容量为：{}MW，即需要增加接入容量为：{}MW'.format(abs(min_wind_loss), round(abs(min_wind_loss), 3)))
    
    # 计算弃风总量
    wind_loss_all = get_wind_load(wind_loss) * 0.25
    print('弃风电量为：{}MWh'.format(wind_loss_all))
