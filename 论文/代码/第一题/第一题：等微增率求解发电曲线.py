# -*- coding: utf-8 -*-
# @Time ： 2022/5/27 9:14
# @File ： 第一题：等微增率求解发点曲线.py
# @IDE ：  PyCharm

import pandas as pd
import sympy as sp
from matplotlib import pyplot as plt


# 三机组等微增率计算
def equalIR_algorithm_3(pd):
    # 初始化功率参数
    p1, p2, p3 = sp.symbols('p_1 p_2 p_3')
    # 发电参数
    c1 = 0.226 * p1 ** 2 + 30.42 * p1 + 786.80
    c2 = 0.588 * p2 ** 2 + 65.12 * p2 + 451.32
    c3 = 0.785 * p3 ** 2 + 139.6 * p3 + 1049.50
    # 求导
    dc1 = sp.diff(c1, p1)
    dc2 = sp.diff(c2, p2)
    dc3 = sp.diff(c3, p3)
    # 组建方程组
    f1 = dc1 - dc2
    f2 = dc2 - dc3
    f3 = dc3 - dc1
    f4 = p1 + p2 + p3 - pd
    f5 = f1 - f2
    f6 = f2 - f3
    f7 = f3 - f1
    # 求解
    res = sp.solve({f4, f5, f6, f7})
    p1 = res[p1]
    p2 = res[p2]
    p3 = res[p3]
    return p1, p2, p3


# 双机组等微增率计算
def equalIR_algorithm_2(pd):
    # 初始化功率参数
    p1, p2 = sp.symbols('p_1 p_2')
    # 发电参数
    c1 = 0.226 * p1 ** 2 + 30.42 * p1 + 786.80
    c2 = 0.588 * p2 ** 2 + 65.12 * p2 + 451.32
    # 求导
    dc1 = sp.diff(c1, p1)
    dc2 = sp.diff(c2, p2)
    # 组建方程组
    f1 = dc1 - dc2
    f4 = p1 + p2 - pd
    # 求解
    res = sp.solve({f4, f1})
    p1 = res[p1]
    p2 = res[p2]
    return p1, p2


# 判断是否超出范围
def judge(p, up, down):
    if p > up:
        return up, 'up'
    elif p < down:
        return down, 'down'
    else:
        return p, 'ok'


# 单次求解发电最优解
def single_algorithm(pd, up1=600, down1=180, up2=300, down2=90, up3=150, down3=45):
    p1, p2, p3 = equalIR_algorithm_3(pd)
    p1, flag1 = judge(p1, up1, down1)
    p2, flag2 = judge(p2, up2, down2)
    p3, flag3 = judge(p3, up3, down3)
    if flag3 == 'down':
        p1, p2 = equalIR_algorithm_2(pd - down3)
        p1, flag1 = judge(p1, up1, down1)
        p2, flag2 = judge(p2, up2, down2)
        if flag2 == 'down':
            p1 = pd - down3 - down2
            p1, flag1 = judge(p1, up1, down1)
    # print('p1:', p1, 'p2:', p2, 'p3:', p3)
    return p1, p2, p3


# 追加写入文件
def write_file(pd, p1, p2, p3):
    with open('第一题：目标、机组1、2、3、差值.csv', 'a', encoding='utf-8') as f:
        dp = p1 + p2 + p3 - pd
        pd, p1, p2, p3, dp = round(pd, 3), round(p1, 3), round(p2, 3), round(p3, 3), round(dp, 3)
        pd, p1, p2, p3, dp = str(pd), str(p1), str(p2), str(p3), str(dp)
        f.write('{},{},{},{},{}\n'.format(pd, p1, p2, p3, dp))
        f.close()


# 画图
def draw_pic(p1, p2, p3):
    from matplotlib.ticker import MultipleLocator
    
    plt.figure(figsize=(7, 3), dpi=800)
    ax = plt.subplot(111)
    data_wind = pd.read_excel('附件1.xlsx')
    data_wind = data_wind.dropna()
    time = data_wind['时间']
    
    time_new = []
    for i in range(0, len(time), 16):
        time_new.append(time[i])
    
    time_new.append('24:00:00')
    
    data_new = []
    for i in range(0, 96, 16):
        data_new.append(i)
    data_new.append(96)
    
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.plot(p1, 'r-', label='机组1')
    plt.plot(p2, 'b-', label='机组2')
    plt.plot(p3, 'g-', label='机组3')
    plt.title('发电计划曲线')
    plt.xlabel('时间')
    plt.ylabel('发电量/MW')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    xmajorLocator = MultipleLocator(16)
    ax.xaxis.set_major_locator(xmajorLocator)
    plt.xticks(data_new, time_new)
    
    plt.savefig('三台火电机组最优发电曲线.png')
    plt.show()


if __name__ == '__main__':
    # 删除文件
    import os
    
    if os.path.exists('第一题：目标、机组1、2、3、差值.csv'):
        os.remove('第一题：目标、机组1、2、3、差值.csv')
    f = open('第一题：目标、机组1、2、3、差值.csv', 'a', encoding='utf-8')
    f.write('目标功率,机组1,机组2,机组3,差值\n')
    f.close()
    
    data = pd.read_excel('附件1.xlsx')
    data = data.dropna()
    p1_list, p2_list, p3_list = [], [], []
    for i in data['l900']:
        p1, p2, p3 = single_algorithm(i)
        # write_file(i, p1, p2, p3)
        p1_list.append(p1)
        p2_list.append(p2)
        p3_list.append(p3)
    draw_pic(p1_list, p2_list, p3_list)
    
    for i in range(len(p1_list)):
        write_file(data['l900'][i], p1_list[i], p2_list[i], p3_list[i])
