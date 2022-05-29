# -*- coding: utf-8 -*-
# @Time ： 2022/5/28 14:48
# @File ： 第二题：功率平衡绘图.py
# @IDE ：  PyCharm

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator

# 读取数据
df = pd.read_csv('第二题：目标、机组1、2、风电、差值、弃风量.csv')
data = df['差值']
time = df['时间']
print(time)

# 每隔16个数取出time
time_new = []
for i in range(0, len(time), 16):
    time_new.append(time[i])

time_new.append('24:00:00')
# print(time_new)
# 生成0-96的数据
data_new = []
for i in range(0, 96, 16):
    data_new.append(i)
    
data_new.append(96)
# print(data_new)

# 绘图
plt.figure(figsize=(7, 3), dpi=800)
ax = plt.subplot(111)

plt.plot(data, color='blue', linewidth=1.5, linestyle='-')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.title('功率平衡图')
plt.xlabel('时间')
plt.ylabel('功率/MW')
plt.tight_layout()
plt.grid(True)
xmajorLocator = MultipleLocator(16)
ax.xaxis.set_major_locator(xmajorLocator)
plt.xticks(data_new,time_new)
plt.savefig('第二题：功率平衡图.png')

plt.show()
