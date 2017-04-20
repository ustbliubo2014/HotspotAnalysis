# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: hcluster.py
@time: 2017/3/14 14:29
@contact: ustb_liubo@qq.com
@annotation: hcluster
"""
import sys
import logging
from logging.config import fileConfig
import os
import scipy.cluster.hierarchy as sch
import msgpack_numpy
import pdb
import numpy as np
import cPickle

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


if __name__ == '__main__':
    threshold = float(sys.argv[1])
    method = sys.argv[2]
    day = sys.argv[3]

    (query_list, all_dist) = msgpack_numpy.load(
            open('/data/liubo/hotspot/query_search/all_query_dist_beijing_{}.p'.format(day), 'rb'))
    query_dist_dic = cPickle.load(open('/data/liubo/hotspot/query_search/beijing_query_dist_dic_{}.p'.format(day), 'rb'))

    linkage = sch.linkage(all_dist, method=method)
    cluster_result = sch.fcluster(linkage, t=threshold)
    cluster_result_dic = {}
    f_result = open('/data/liubo/hotspot/query_search/beijing_{}_cluster_result_{}_{}.txt'.format(day, threshold, method), 'w')
    for index in range(len(cluster_result)):
        this_cluster_id = cluster_result[index]
        this_cluster_query_list = cluster_result_dic.get(this_cluster_id, [])
        this_cluster_query_list.append(query_list[index])
        cluster_result_dic[this_cluster_id] = this_cluster_query_list
    f_cluster_dist = open('/data/liubo/hotspot/query_search/beijing_{}_cluster_result_dist_{}.txt'.format(day, threshold), 'w')
    for cluster_id in cluster_result_dic:
        this_cluster_query_list = cluster_result_dic.get(cluster_id)
        if len(this_cluster_query_list) > 1:
            for index1 in range(len(this_cluster_query_list)):
                for index2 in range(len(this_cluster_query_list)):
                    if index2 > index1:
                        word1 = this_cluster_query_list[index1][0]
                        word2 = this_cluster_query_list[index2][0]
                        if (word1, word2) in query_dist_dic:
                            f_cluster_dist.write(
                                    str(cluster_id) + '\t' + word1 + '\t' + word2 + '\t' +str(query_dist_dic[(word1, word2)]) + '\n')
                        else:
                            f_cluster_dist.write(
                                    str(cluster_id) + '\t' + word1 + '\t' + word2 + '\t' + str(query_dist_dic[(word2, word1)]) + '\n')
    for cluster_id in cluster_result_dic:
        this_cluster_query_list = cluster_result_dic.get(cluster_id)
        for query in this_cluster_query_list:
            f_result.write(query[0]+'\t'+str(cluster_id)+'\n')
    f_result.close()
