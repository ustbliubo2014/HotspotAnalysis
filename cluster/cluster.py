# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: cluster.py
@time: 2017/3/14 12:35
@contact: ustb_liubo@qq.com
@annotation: cluster
"""
import sys
import logging
from logging.config import fileConfig
import os
from sklearn.cluster import DBSCAN, KMeans, AgglomerativeClustering
import msgpack_numpy
import pdb
from sklearn.metrics import euclidean_distances
from time import time

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


if __name__ == '__main__':
    pass

    (query_list, all_query_vector) = msgpack_numpy.load(open('query_list-all_query_vector.p', 'rb'))

    query_num = 50000
    start = time()
    kmean = KMeans(n_clusters=300, n_jobs=10)
    kmean.fit(all_query_vector[:query_num])
    predict = kmean.predict(all_query_vector[:query_num])
    end = time()
    print 'fit_predict_time :', (end - start)
    all_result = []
    for index in range(len(query_list[:query_num])):
        all_result.append((query_list[index][0], predict[index]))
    all_result.sort(key=lambda x:x[1])
    f_result = open('kmean_result.txt', 'w')
    for element in all_result:
        f_result.write(element[0]+'\t'+str(element[1])+'\n')


