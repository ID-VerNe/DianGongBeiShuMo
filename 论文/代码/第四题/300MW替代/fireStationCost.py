# -*- coding: utf-8 -*-
# @Time ： 2022/5/27 17:13
# @File ： 火电运行成本.py
# @IDE ：  PyCharm

###############
# 煤用量
# 火电烧煤运行成本
def fireStationCoalCost(p, a, b, c):
    '''
    :param p: 功率
    :param a: 煤用量参数1
    :param b: 煤用量参数2
    :param c: 煤用量参数3
    :return:
    '''
    return p ** 2 * a + p * b + c


# 火电煤维护成本
def fireStationMaintenanceCost(p, a, b, c):
    '''
    :param p: 功率
    :param a: 煤用量参数1
    :param b: 煤用量参数2
    :param c: 煤用量参数3
    :return:
    '''
    coalCost = fireStationCoalCost(p, a, b, c)
    return coalCost * 0.5


# 单次火电煤运行成本
def fireStationRunCost(p, a, b, c):
    '''
    :param p: 功率
    :param a: 煤用量参数1
    :param b: 煤用量参数2
    :param c: 煤用量参数3
    :return:
    '''
    coalCost = fireStationCoalCost(p, a, b, c)
    maintenanceCost = fireStationMaintenanceCost(p, a, b, c)
    return coalCost + maintenanceCost


##############
# 碳费用
# 总发电量
def totalGeneration(powerPlan):
    '''
    :param powerPlan: 电力计划
    :return:
    '''
    return sum(powerPlan) * 0.25


# 碳排放量
def carbonEmission(powerPlan, carbonWeight):
    '''
    :param powerPlan: 电力计划
    :param carbonWeight: 碳排放参数
    :return:
    '''
    return totalGeneration(powerPlan) * carbonWeight
