# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: topic_cluster.py
@time: 2017/2/13 14:38
@contact: ustb_liubo@qq.com
@annotation: topic_cluster : 测试几种主题聚类的效果
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
from sklearn.metrics.pairwise import cosine_similarity, cosine_distances
from time import time
import hcluster
import scipy.cluster.hierarchy as sch

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def query_list():
    # 用query_list训练word2vec模型, 每个query是一个word, 可以直接比较两个query的相似度, 也可以找出某query相似的top10
    # model_path = '/data/liubo/hotspot/query_list_baoding_20161130_utf-8.gensim.model'
    # query_vector_dic_file = 'query_list_baoding_vector.p'

    model_path = '/data/liubo/hotspot/query_list_beijing_20161101_utf8.gensim.model'
    query_vector_dic_file = 'query_list_vector.p'
    model = word2vec.Word2Vec.load(model_path)
    query_list = open('/data/liubo/hotspot/test_query_uniq_utf8.txt').read().split('\n')
    find_count = 0
    query_vector_dic = {}
    for query in query_list:
        try:
            query = query.decode('utf-8')[:]
            find = query in model
            if find:
                find_count += 1
                query_vector_dic[query] = model[query]
            else:
                print query, find
                # pdb.set_trace()
        except:
            print 'error :', query
            continue
    print 'find_count :', find_count
    return query_vector_dic
    # cPickle.dump(query_vector_dic, open(query_vector_dic_file, 'wb'))


def wiki_word2vec(model_path, query_file):
    # 用wiki训练word2vec模型, 一个query包含多个word, 最后query的向量由每个query相加
    # 也可以用搜素次训练word2vec模型, 一个query包含多个word, 最后query的向量由每个query相加
    # model_path = '/data/liubo/wiki/wiki.zh.gensim.model'
    # query_list = open('test_query.txt').read().split('\n')

    # model_path = '/data/liubo/hotspot/query_list_beijing_20161107_wordcut.gensim.model'
    # query_list = open('brw_query_date.1d.20161107.csv').read().split('\n')
    query_list = open(query_file).read().split('\n')
    model = word2vec.Word2Vec.load(model_path)
    query_vector_dic = {}
    line_count = 0
    start = time()
    # f_dst_vector = open('/data/liubo/hotspot/test_query_uniq_beijing_vector.txt', 'w')
    # f_dst_query = open('/data/liubo/hotspot/test_query_uniq_beijing_query.txt', 'w')
    query_useful_word_dic = {}  # 每个query产生向量时使用的word
    for query in query_list:
        try:
            query = query.decode('utf-8')[:]
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
                # f_dst_vector.write(' '.join(map(str, this_vector))+'\n')
                # f_dst_query.write(str(query)+'\n')
        except:
            print 'error query :', query, '\t', len(query_vector_dic)
            continue
        line_count += 1

        if line_count % 100000 == 0:
            print line_count, time() - start
            start = time()
    # f_dst_vector.close()
    # f_dst_query.close()
    print 'len(query_vector_dic) :', len(query_vector_dic)
    # cPickle.dump(query_vector_dic, open('query_wiki_vector.p', 'wb'))
    return query_vector_dic, query_useful_word_dic


def semantic_lexicon():
    pass


def all_query():
    # 整理出所有query
    query_file = '/data/liubo/hotspot/query_list_20161130_new.txt'
    query_dic = {}
    line_count = 1
    for line in open(query_file):
        tmp = line.rstrip().split('\t')
        for word in tmp:
            query_dic[word] = query_dic.get(word, 0) + 1
        if line_count % 100000 == 0:
            print 'line_count :', line_count, 'query_num :', len(query_dic)
        line_count += 1
    cPickle.dump(query_dic, open('/data/liubo/hotspot/all_query_dic.p', 'wb'))


def topic_cluster(query_vector_dic, query_useful_word_dic, cluster_result_file):
    # 聚类之后, 还要提取每个类的主题
    # result_file = 'brw_query_date.1d.20161107_cluster.txt'
    result_file = cluster_result_file

    # result_file = 'query_wiki_cluster.txt'
    # query_vector_dic_file = 'query_wiki_vector.p'


    # query_vector_dic = cPickle.load(open(query_vector_dic_file, 'rb'))

    data = np.array(query_vector_dic.values())
    all_query_list = query_vector_dic.keys()


    all_dist = ['braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine',
                'euclidean', 'minkowski', 'seuclidean', 'sqeuclidean']
    all_method = ['single', 'complete', 'average', 'weighted']


    for dist in all_dist:
        for method in all_method:
            cluster_result = sch.fcluster(sch.linkage(sch.distance.pdist(data, dist), method=method), t=1.0)
            print 'dist :', dist, 'method :', method, np.max(cluster_result)
            f_result = open(result_file+'_'+dist+'_'+method, 'w')
            query_cluster_result = []
            for index in range(len(all_query_list)):
                try:
                    query = all_query_list[index]
                    # this_query_vector = np.reshape(query_vector_dic.get(query), (1, 200))
                    # this_cluster_id = cluster.labels_[index]
                    this_cluster_id = cluster_result[index]
                    query_cluster_result.append((query.rstrip(), this_cluster_id))
                    # f_result.write(query.rstrip() + '\t' + str(this_cluster_id) + '\n')
                    # f_result.write(query+'\t'+str(kmeans.predict(this_query_vector)[0])+'\n')
                except:
                    traceback.print_exc()
                    continue
            query_cluster_result.sort(key=lambda x:x[1])
            for element in query_cluster_result:
                query, this_cluster_id = element
                f_result.write(query.rstrip() + '\t' + str(this_cluster_id) + '\n')
            f_result.close()


    # kmeans = KMeans(init='k-means++', n_clusters=500)
    # kmeans.fit(data)
    # cluster_center = kmeans.cluster_centers_
    # to_all_cluster_distances = {} # {cluster_id:[(query, distance[和中心点的距离])]}
    # for query in query_vector_dic:
    #     try:
    #         this_query_vector = np.reshape(query_vector_dic.get(query), (1, 200))
    #         all_center_sims = cosine_distances(cluster_center, this_query_vector)
    #         this_cluster_id = np.argmin(all_center_sims)
    #         to_cluster_sim = np.min(all_center_sims)
    #         this_query_list = to_all_cluster_distances.get(this_cluster_id, [])
    #         this_query_list.append((query, to_cluster_sim))
    #         to_all_cluster_distances[this_cluster_id] = this_query_list
    #         # f_result.write(query+'\t'+str(kmeans.predict(this_query_vector)[0])+'\n')
    #     except:
    #         traceback.print_exc()
    #         continue
    # print_info = {}
    # for cluster_id in to_all_cluster_distances:
    #     this_query_list = to_all_cluster_distances.get(cluster_id)
    #     this_query_list.sort(key=lambda x:x[1])
    #     topic = '\t'.join([x[0] for x in this_query_list[:min(5, len(this_query_list))]])
    #     for element in this_query_list:
    #         query, to_cluster_sim = element
    #         # f_result.write(query+'\t'+str(cluster_id)+'\t'+topic+'\n')
    #         f_result.write(query.rstrip() + '\t' + str(cluster_id) + '\t' + '\t'.join(query_useful_word_dic.get(query)) + '\n')
    #     print_info[cluster_id] = len(this_query_list)
    # f_result.close()
    # print print_info


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
    # pdb.set_trace()


if __name__ == '__main__':
    pass
    # all_query()
    # query_vector_dic = query_list()

    day = sys.argv[1]
    model_path = '/data/liubo/hotspot/query_list_beijing_{}_wordcut.gensim.model'.format(day)
    query_file = 'brw_query_date.1d.{}.csv'.format(day)
    cluster_result_file = 'cluster_result/brw_query_date.1d.{}_cluster_hcluster.txt'.format(day)
    # query_file = '/data/liubo/hotspot/beijing_query_top10000_{}.txt'.format(day)
    # cluster_result_file = '/data/liubo/hotspot/beijing_query_top10000_{}_cluster_result.txt'.format(day)
    query_vector_dic, query_useful_word_dic = wiki_word2vec(model_path,query_file)
    topic_cluster(query_vector_dic, query_useful_word_dic, cluster_result_file)
