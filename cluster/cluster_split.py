# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: cluster_split.py
@time: 2017/3/21 16:04
@contact: ustb_liubo@qq.com
@annotation: cluster_split : 对于hie cluster的聚类结果, 将大于阈值的参数分割开来
                            如果某个样本和该类中所有样本的distance都大于一个阈值, 分开形成一个新的类
"""
import sys
import logging
from logging.config import fileConfig
import os
import cPickle
import pdb
from time import time

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def load_cluster_result(result_file):
    cluster_result_dic = {}
    for line in open(result_file):
        tmp = line.rstrip().split()
        if len(tmp) == 2:
            query, cluster_id = tmp
            result_list = cluster_result_dic.get(int(cluster_id), [])
            result_list.append(query)
            cluster_result_dic[int(cluster_id)] = result_list
    return cluster_result_dic


def get_query_pair_distance(query1, query2, distance_dic):
    query1 = query1.decode('utf-8')
    query2 = query2.decode('utf-8')
    if (query1, query2) in distance_dic:
        return distance_dic.get((query1, query2))
    else:
        return distance_dic.get((query2, query1))


if __name__ == '__main__':
    start = time()
    split_threshold = 25.0
    day = sys.argv[1]
    raw_result_file = '/data/liubo/hotspot/query_search/beijing_{}_cluster_result_1.1_average.txt'.format(day)
    all_query_pair_distance_dic = cPickle.load(
            open('/data/liubo/hotspot/query_search/beijing_query_dist_dic_{}.p'.format(day), 'rb'))
    split_result_file = '/data/liubo/hotspot/query_search/beijing_{}_cluster_result_1.1_average_split.txt'.format(day)
    f_split = open(split_result_file, 'w')
    cluster_result_dic = load_cluster_result(raw_result_file)
    current_cluster_id = max(cluster_result_dic.keys()) + 1
    add_cluster_dic = {}
    for cluster in cluster_result_dic:
        result_list = cluster_result_dic.get(cluster)
        split_query = []
        for index1 in range(len(result_list)):
            up_num = low_num = 0
            for index2 in range(len(result_list)):
                if index1 != index2:
                    distance = get_query_pair_distance(result_list[index1], result_list[index2], all_query_pair_distance_dic)
                    if distance > split_threshold:
                        up_num += 1
                    else:
                        low_num += 1
            if up_num > low_num:
                split_query.append(result_list[index1])
        for query in split_query:
            result_list.remove(query)
            add_cluster_dic[current_cluster_id] = [query]
            current_cluster_id += 1
        cluster_result_dic[cluster] = result_list
    for cluster in cluster_result_dic:
        result_list = cluster_result_dic.get(cluster)
        for query in result_list:
            f_split.write(query+'\t'+str(cluster)+'\n')
    for cluster in add_cluster_dic:
        result_list = add_cluster_dic.get(cluster)
        for query in result_list:
            f_split.write(query + '\t' + str(cluster) + '\n')
    f_split.close()
    end = time()
    print 'split time :', (end - start)