# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: topic_cluster_country.py
@time: 2017/2/28 10:55
@contact: ustb_liubo@qq.com
@annotation: topic_cluster_country : 同时对全国所有地方聚类(增加一列地名)
"""
import sys
import logging
from logging.config import fileConfig
import os
import msgpack_numpy
import cPickle
from gensim.models import word2vec
import pdb
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
import numpy as np
import traceback
import jieba
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity
from time import time
import hcluster
import scipy.cluster.hierarchy as sch

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def wiki_word2vec(model, query_list, all_query_vector_dic, all_query_useful_word_dic):
    # 某一地方的搜索词(top 200)
    # query_list = map(lambda x:x.decode('utf-8')[:], open(query_file).read().rstrip().split('\n'))
    # model = word2vec.Word2Vec.load(model_path)
    query_vector_dic = {}
    line_count = 0
    start = time()
    query_useful_word_dic = {}  # 每个query产生向量时使用的word
    all_query_dic = {}
    for query in query_list:
        try:
            if query in all_query_vector_dic:
                query_vector_dic[query] = all_query_vector_dic.get(query)
                query_useful_word_dic[query] = all_query_useful_word_dic.get(query)
                continue
            this_vector = [0] * 200
            this_word_list = [word for word in jieba.cut(query, cut_all=False)]
            has_find = False
            useful_word_num = 0
            for word in this_word_list:
                if word in model:
                    this_vector = this_vector + model[word]
                    has_find = True
                    tmp_list = query_useful_word_dic.get(query, [])
                    tmp_list.append(word)
                    query_useful_word_dic[query] = tmp_list
                    useful_word_num += 1
            if has_find:
                this_vector = np.array(this_vector) / useful_word_num
                query_vector_dic[query] = this_vector
                all_query_useful_word_dic[query] = query_useful_word_dic[query]
                all_query_vector_dic[query] = this_vector
            all_query_dic[query] = 1
        except:
            print 'error query :', query, '\t', len(query_vector_dic)
            continue
        line_count += 1
        if line_count % 100000 == 0:
            print line_count, time() - start
            start = time()
    # print 'len(query_vector_dic) :', len(query_vector_dic)
    return query_vector_dic, query_useful_word_dic, all_query_dic


def topic_cluster(query_vector_dic, query_useful_word_dic, all_query_dic):
    # 聚类之后, 还要提取每个类的主题
    data = np.array(query_vector_dic.values())
    all_query_list = query_vector_dic.keys()
    result_list = []

    if len(all_query_list) == 1:
        result_list.append((all_query_list[0], 0, all_query_list[0]))
        return result_list

    all_dist = ['euclidean']
    all_method = ['average']
    cluster_center_dic = {}  # {cluster_id:[vector,...,vector]}
    for dist in all_dist:
        for method in all_method:
            cluster_result = sch.fcluster(sch.linkage(sch.distance.pdist(data, dist), method=method), t=1.1)
            max_cluster_id = np.max(cluster_result)
            query_cluster_result = []
            for index in range(len(all_query_list)):
                try:
                    query = all_query_list[index]
                    this_cluster_id = cluster_result[index]
                    vector_list = cluster_center_dic.get(this_cluster_id, [])
                    vector_list.append((query, query_vector_dic.get(query)))
                    cluster_center_dic[this_cluster_id] = vector_list
                    query_cluster_result.append((query, this_cluster_id))
                except:
                    traceback.print_exc()
                    continue
            for this_cluster_id in cluster_center_dic:
                tmp_list = cluster_center_dic.get(this_cluster_id)
                # 计算后保存{cluster_id:query}
                if len(tmp_list) == 1:
                    cluster_center_dic[this_cluster_id] = tmp_list[0][0]
                else:
                    this_vector_list = []
                    this_query_list = []
                    for element in tmp_list:
                        query, vector = element
                        this_vector_list.append(vector)
                        this_query_list.append(query)
                    this_vector_list = np.array(this_vector_list)
                    center_vector = np.reshape(np.mean(this_vector_list, axis=0), (1, 200))
                    this_distance_list = euclidean_distances(center_vector, this_vector_list)
                    cluster_center_dic[this_cluster_id] = this_query_list[np.argmin(this_distance_list)]
            query_cluster_result.sort(key=lambda x: x[1])
            for element in query_cluster_result:
                query, this_cluster_id = element
                if query in all_query_dic:
                    all_query_dic.pop(query)
                result_list.append((query, this_cluster_id, cluster_center_dic.get(this_cluster_id)))
            current_cluster_id = max_cluster_id + 1
            for query in all_query_dic:
                result_list.append((query, current_cluster_id, query))
                current_cluster_id += 1
    return result_list


def merge(all_query_score, cluster_result_list):
    all_query_score_cluster = []
    cluster_result_dic = {}
    for element in cluster_result_list:
        query, cluster_id, topic = element
        cluster_result_dic[query] = (cluster_id, topic)
    # print len(cluster_result_dic), len(cluster_result_list)
    for element in all_query_score:
        query, score, count = element
        if query in cluster_result_dic:
            cluster_id, topic = cluster_result_dic.get(query)
            all_query_score_cluster.append((query, score, count, cluster_id, topic))
        # else:
        #     print 'not find query :', query
    return all_query_score_cluster


def country_cluster():
    day = sys.argv[1]
    model_path = '/data/liubo/hotspot/model/query_list_{}_country_wordcut.gensim.model'.format(day)
    query_file = '/data/liubo/hotspot/time_filter_f/time_filter_f_{}.txt'.format(day)
    cluster_result_file = '/data/liubo/hotspot/query_cluster_result/time_filter_f_{}_cluster_result.txt'.format(day)
    f_result = open(cluster_result_file, 'w')
    model = word2vec.Word2Vec.load(model_path)
    all_query_vector_dic = {}
    all_query_useful_word_dic = {}
    address_count = 0
    start = time()
    for line in open(query_file):
        address, all_query_score = eval(line)
        all_query_score = all_query_score[:200]
        all_query = map(lambda x:x[0], all_query_score)
        query_vector_dic, query_useful_word_dic, all_query_dic = \
            wiki_word2vec(model, all_query, all_query_vector_dic, all_query_useful_word_dic)
        if len(query_vector_dic) == 0:
            continue
        cluster_result_list = topic_cluster(query_vector_dic, query_useful_word_dic, all_query_dic)
        all_query_score_cluster = merge(all_query_score, cluster_result_list)
        f_result.write(repr((address, all_query_score_cluster))+'\n')
        address_count += 1
        if address_count % 100 == 0:
            print address_count, (time() - start)


def show_address(cluster_file, address, show_file):
    result_line = []
    for line in open(cluster_file):
        this_address, query_cluster_result = eval(line)
        if address in this_address:
            f = open(show_file, 'w')
            for element in query_cluster_result:
                result_line.append((element[0], element[3]))
                # f.write('\t'.join(map(str, element))+'\n')
            result_line.sort(key=lambda x:x[1])
            for line in result_line:
                f.write('\t'.join(map(str, line))+'\n')
            f.close()
            break


if __name__ == '__main__':
    pass
    # country_cluster()
    show_address('/data/liubo/hotspot/query_cluster_result/time_filter_f_20161130_cluster_result.txt', '北京'.decode('utf-8'), 'beijing_result.txt')
