# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: hcluster.py
@time: 2017/3/14 14:29
@contact: ustb_liubo@qq.com
@annotation: cluster
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
from copy import deepcopy
from time import time

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def hierarchical_cluster(query_list, all_distance, method='average', threshold=1.1):
    linkage = sch.linkage(all_distance, method=method)
    cluster_result = sch.fcluster(linkage, t=threshold)
    cluster_result_dic = {}
    for index in range(len(cluster_result)):
        this_cluster_id = cluster_result[index]
        this_cluster_query_list = cluster_result_dic.get(this_cluster_id, [])
        this_cluster_query_list.append(query_list[index][0])
        cluster_result_dic[this_cluster_id] = this_cluster_query_list
    return cluster_result_dic


def get_query_pair_distance(query1, query2, distance_dic):
    query1 = query1.decode('utf-8')
    query2 = query2.decode('utf-8')
    if (query1, query2) in distance_dic:
        return distance_dic.get((query1, query2))
    else:
        return distance_dic.get((query2, query1))


def cluster_split(all_query_pair_distance_dic, cluster_result_dic, split_threshold=25.0):
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
    for cluster in add_cluster_dic:
        cluster_result_dic[cluster] = add_cluster_dic.get(cluster)
    return cluster_result_dic


def cluster_merge(split_cluster_result_dic, cluster_merge_threshold=15, merge_threshold=21):
    cluster_id_list = split_cluster_result_dic.keys()
    new_cluster_id_dic = {}
    for cluster_id1 in cluster_id_list:
        # 合并的过程中会删掉某些cluster
        if cluster_id1 in split_cluster_result_dic:
            query_list1 = split_cluster_result_dic.get(cluster_id1)
            for cluster_id2 in cluster_id_list:
                if cluster_id2 in split_cluster_result_dic:
                    query_list2 = split_cluster_result_dic.get(cluster_id2)
                    up_num = low_num = 0
                    if cluster_id1 != cluster_id2:
                        for query1 in query_list1:
                            for query2 in query_list2:
                                distance = get_query_pair_distance(query1, query2, all_query_pair_distance_dic)
                                if distance > merge_threshold:
                                    up_num += 1
                                else:
                                    low_num += 1
                        if low_num > up_num:
                            query_list1 = query_list1 + query_list2
                            split_cluster_result_dic.pop(cluster_id2)
            new_cluster_id_dic[cluster_id1] = query_list1
    split_cluster_result_dic = deepcopy(new_cluster_id_dic)
    cluster_id_list = split_cluster_result_dic.keys()
    new_cluster_id_dic = {}
    for cluster_id1 in cluster_id_list:
        if cluster_id1 in split_cluster_result_dic:
            query_list1 = split_cluster_result_dic.get(cluster_id1)
            for cluster_id2 in cluster_id_list:
                if cluster_id2 in split_cluster_result_dic:
                    query_list2 = split_cluster_result_dic.get(cluster_id2)
                    if cluster_id1 != cluster_id2:
                        has_merge = False
                        for query1 in query_list1:
                            for query2 in query_list2:
                                distance = get_query_pair_distance(query1, query2, all_query_pair_distance_dic)
                                if distance < cluster_merge_threshold:
                                    query_list1 = query_list1 + query_list2
                                    split_cluster_result_dic.pop(cluster_id2)
                                    has_merge = True
                                    break
                            if has_merge:
                                break
            new_cluster_id_dic[cluster_id1] = query_list1
    return new_cluster_id_dic


def cluster(query_list, all_distance, all_query_pair_distance_dic):
    cluster_result_dic = hierarchical_cluster(query_list, all_distance)
    split_cluster_result_dic = cluster_split(all_query_pair_distance_dic, deepcopy(cluster_result_dic))
    merge_cluster_result_dic = cluster_merge(split_cluster_result_dic)
    return merge_cluster_result_dic


if __name__ == '__main__':
    start = time()
    day = '20161130'
    (query_list, all_distance) = msgpack_numpy.load(
            open('/data/liubo/hotspot/query_search/all_query_dist_beijing_{}.p'.format(day), 'rb'))
    all_query_pair_distance_dic = cPickle.load(
            open('/data/liubo/hotspot/query_search/beijing_query_dist_dic_{}.p'.format(day), 'rb'))
    merge_cluster_result_dic = cluster(query_list, all_distance, all_query_pair_distance_dic)
    end = time()
    print 'time :', (end - start)
