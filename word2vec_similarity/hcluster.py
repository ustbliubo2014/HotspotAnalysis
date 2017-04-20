# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: hcluster.py
@time: 2017/2/23 10:15
@contact: ustb_liubo@qq.com
@annotation: hcluster
"""
import logging
import os
import sys
import scipy.cluster.hierarchy as sch
import numpy as np
import matplotlib.pylab as plt
import cPickle
import pdb

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def hcluster(data):

    return sch.fcluster(sch.linkage(sch.distance.pdist(data, 'chebyshev'), method='complete'), t=1.02)
    # # 生成距离矩阵
    # # disMat = sch.distance.pdist(data, 'euclidean')
    # disMat = sch.distance.pdist(data, 'chebyshev')
    #
    # # 层次聚类
    # Z = sch.linkage(disMat, method='average')
    # # 以树形保存层次聚类的结果
    # P = sch.dendrogram(Z)
    # plt.savefig('plot_dendrogram_1109.png')
    # # pdb.set_trace()
    # cluster_result = sch.fcluster(Z, t=1)
    # return cluster_result


if __name__ == '__main__':
    data = cPickle.load(open('data.p', 'rb'))
    hcluster(data)
    pass
