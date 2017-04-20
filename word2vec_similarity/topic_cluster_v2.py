# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: topic_cluster_v2.py
@time: 2017/2/23 17:39
@contact: ustb_liubo@qq.com
@annotation: topic_cluster_v2
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


def wiki_word2vec(model_path, query_file):
    query_list = map(lambda x:x.decode('utf-8')[:], open(query_file).read().rstrip().split('\n'))
    model = word2vec.Word2Vec.load(model_path)
    query_vector_dic = {}
    line_count = 0
    start = time()
    query_useful_word_dic = {}  # 每个query产生向量时使用的word
    all_query_dic = {}
    for query in query_list:
        try:
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
            all_query_dic[query] = 1
        except:
            print 'error query :', query, '\t', len(query_vector_dic)
            continue
        line_count += 1
        if line_count % 100000 == 0:
            print line_count, time() - start
            start = time()
    print 'len(query_vector_dic) :', len(query_vector_dic)
    return query_vector_dic, query_useful_word_dic, all_query_dic


def topic_cluster(query_vector_dic, query_useful_word_dic, all_query_dic, cluster_result_file):
    # 聚类之后, 还要提取每个类的主题
    result_file = cluster_result_file
    data = np.array(query_vector_dic.values())
    all_query_list = query_vector_dic.keys()

    # all_dist = ['braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine',
    #             'euclidean', 'minkowski', 'seuclidean', 'sqeuclidean']
    # all_method = ['single', 'complete', 'average', 'weighted']

    all_dist = ['euclidean']
    all_method = ['average']
    cluster_center_dic = {}  # {cluster_id:[vector,...,vector]}
    for dist in all_dist:
        for method in all_method:
            cluster_result = sch.fcluster(sch.linkage(sch.distance.pdist(data, dist), method=method), t=1.1)
            max_cluster_id = np.max(cluster_result)
            print 'dist :', dist, 'method :', method, 'max_cluster_id :', max_cluster_id
            # f_result = open(result_file+'_'+dist+'_'+method, 'w')
            f_result = open(result_file, 'w')
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
                f_result.write(query.rstrip() + '\t' + str(this_cluster_id) + '\t' + cluster_center_dic.get(this_cluster_id) +'\n')
            current_cluster_id = max_cluster_id + 1
            for query in all_query_dic:
                f_result.write(query.rstrip() + '\t' + str(current_cluster_id) + '\t' + query.rstrip() + '\n')
                current_cluster_id += 1
            f_result.close()


def cal_two_sentence_similarity(model, sentence1, sentence2):
    sentence1_word_list = [word for word in jieba.cut(sentence1, cut_all=False)]
    sentence2_word_list = [word for word in jieba.cut(sentence2, cut_all=False)]
    sentence1_useful_word = []
    sentence2_useful_word = []
    sentence1_has_find = False
    sentence2_has_find = False
    sentence1_vector = [0] * 200
    sentence2_vector = [0] * 200
    for word in sentence1_word_list:
        if word in model:
            sentence1_vector = sentence1_vector + model[word]
            sentence1_has_find = True
            sentence1_useful_word.append(word)
    for word in sentence2_word_list:
        if word in model:
            sentence2_vector = sentence2_vector + model[word]
            sentence2_has_find = True
            sentence2_useful_word.append(word)

    if sentence1_has_find and sentence2_has_find:
        print len(sentence1_useful_word), len(sentence2_useful_word)
        sentence1_vector = np.array(sentence1_vector) / len(sentence1_useful_word)
        sentence2_vector = np.array(sentence2_vector) / len(sentence2_useful_word)
        print cosine_similarity(sentence1_vector, sentence2_vector)
        for word in sentence1_useful_word:
            print word,
        print
        for word in sentence2_useful_word:
            print word,
        print


if __name__ == '__main__':
    pass
    day = sys.argv[1]
    model_path = '/data/liubo/hotspot/query_list_beijing_{}_wordcut.gensim.model'.format(day)
    query_file = 'brw_query_date.1d.{}.csv'.format(day)
    cluster_result_file = 'cluster_result/brw_query_date.1d.{}_cluster_hcluster.txt'.format(day)
    # query_file = '/data/liubo/hotspot/beijing_query_top10000_{}.txt'.format(day)
    # cluster_result_file = '/data/liubo/hotspot/beijing_query_top10000_{}_cluster_result.txt'.format(day)
    query_vector_dic, query_useful_word_dic, all_query_dic = wiki_word2vec(model_path,query_file)
    topic_cluster(query_vector_dic, query_useful_word_dic, all_query_dic, cluster_result_file)
