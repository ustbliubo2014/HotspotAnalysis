# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: cluster_merge.py
@time: 2017/3/21 17:21
@contact: ustb_liubo@qq.com
@annotation: cluster_merge : 如果两个类中所有query的distance小于merge_threshold, 合并两个cluster
"""
import sys
import logging
from logging.config import fileConfig
import os
from cluster_split import load_cluster_result, get_query_pair_distance
import cPickle
from time import time
from copy import deepcopy

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


if __name__ == '__main__':
    start = time()
    merge_threshold = 21
    cluster_merge_threshold = 15
    day = sys.argv[1]
    all_query_pair_distance_dic = cPickle.load(
            open('/data/liubo/hotspot/query_search/beijing_query_dist_dic_{}.p'.format(day), 'rb'))
    split_result_file = '/data/liubo/hotspot/query_search/beijing_{}_cluster_result_1.1_average_split.txt'.format(day)
    merge_result_file = '/data/liubo/hotspot/query_search/beijing_{}_cluster_result_1.1_average_merge2.txt'.format(day)
    f_merge = open(merge_result_file, 'w')
    split_cluster_result_dic = load_cluster_result(split_result_file)
    current_cluster_id = max(split_cluster_result_dic.keys()) + 1
    merge_cluster_dic = {}
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
    for cluster in new_cluster_id_dic:
        result_list = new_cluster_id_dic.get(cluster)
        for query in result_list:
            f_merge.write(query+'\t'+str(cluster)+'\n')
    f_merge.close()
    end = time()
    print 'merge time :', (end - start)
