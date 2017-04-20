# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: keyword_distance.py
@time: 2017/4/5 16:49
@contact: ustb_liubo@qq.com
@annotation: keyword_distance : query和网页分别提取关键词, 计算query和网页之间的相似度, 排序后, 分析
"""
import sys
sys.path.append('/home/liubo-it/HotspotAnalysis/')
import logging
from logging.config import fileConfig
import os
import pdb
import traceback
import cPickle
import numpy as np
from sklearn.metrics import euclidean_distances
from time import time

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def load_word2vec_model(model_path):
    word2vec_model = {}
    start = time()
    for line in open(model_path):
        try:
            tmp = line.rstrip().split()
            word = tmp[0].decode('utf-8')
            vector = map(float, tmp[1:])
            word2vec_model[word] = vector
        except:
            traceback.print_exc()
            print line
            continue
    end = time()
    print 'load_word2vec_model :', (end - start), len(word2vec_model)
    return word2vec_model


def trans_keywords_vector(word2vec_model, keyword_list, vector_length=200):
    '''
        将多个keyword的vector合成一个整体 : 根据权重求平均
    :param word2vec_model:
    :param keyword_list: [(word, freq/tfidf)]
    :param vector_length: 词向量长度
    :return:
    '''
    new_list = []
    for keyword in keyword_list:
        word, freq = keyword
        if word in word2vec_model:
            new_list.append(keyword)
    sum_freq = sum([x[1] for x in new_list]) * 1.0
    new_list = map(lambda x:(x[0], x[1]/sum_freq), new_list)
    this_keywords_vector = np.asarray([0.0] * vector_length)
    for keyword in new_list:
        this_keywords_vector += (np.asarray(word2vec_model[keyword[0]]) * keyword[1])
    return this_keywords_vector / len(new_list)


def create_query_url_vector():
    # 生成每个query和url对应的vector
    word2vec_model_path = '/data/liubo/hotspot/zhihu_corpus_1000000.model'
    word2vec_model = load_word2vec_model(word2vec_model_path)
    useful_url_title_keyword_dic = cPickle.load(open('/data/liubo/hotspot/yuqing/useful_url_title_keyword_dic.p', 'rb'))
    beijing_20161109_query_keyword_dic = \
        cPickle.load(open('/data/liubo/hotspot/yuqing/beijing_20161109_query_keyword_dic.p', 'rb'))
    query_vector_dic = {}
    url_vector_dic = {}
    for query in beijing_20161109_query_keyword_dic:
        keyword_list = beijing_20161109_query_keyword_dic.get(query)
        query_vector = trans_keywords_vector(word2vec_model, keyword_list)
        query_vector_dic[query] = query_vector
    for url in useful_url_title_keyword_dic:
        title, keyword_list = useful_url_title_keyword_dic.get(url)
        url_vector = trans_keywords_vector(word2vec_model, keyword_list)
        url_vector_dic[url] = url_vector
    cPickle.dump(url_vector_dic, open('/data/liubo/hotspot/yuqing/url_vector_dic.p', 'wb'))
    cPickle.dump(query_vector_dic, open('/data/liubo/hotspot/yuqing/query_vector_dic.p', 'wb'))


def cal_query_url_distance():
    # 计算query_vector和url_vector之间的距离
    url_vector_dic = cPickle.load(open('/data/liubo/hotspot/yuqing/url_vector_dic.p', 'rb'))
    query_vector_dic = cPickle.load(open('/data/liubo/hotspot/yuqing/query_vector_dic.p', 'rb'))
    query_all_distance_dic = {}  # {query:[distance_1, ..., distance_n]}
    for query in query_vector_dic:
        query_vector = query_vector_dic.get(query)
        all_distance = []
        for url in url_vector_dic:
            url_vector = url_vector_dic.get(url)
            this_distance = euclidean_distances(np.reshape(query_vector, (1, len(query_vector))),
                                np.reshape(url_vector, (1, len(url_vector))))[0][0]
            all_distance.append(this_distance)
        query_all_distance_dic[query] = all_distance
    cPickle.dump(query_all_distance_dic, open('/data/liubo/hotspot/yuqing/query_all_distance_dic.p', 'wb'))


def mean_distance():
    # 每个query的所有距离取平均作为最后的距离
    query_all_distance_dic = cPickle.load(open('/data/liubo/hotspot/yuqing/query_all_distance_dic.p', 'rb'))
    f_distance = open('/data/liubo/hotspot/yuqing/query_mean_distance.txt', 'w')
    all_query_distance = []
    for query in query_all_distance_dic:
        mean_distance = np.mean(query_all_distance_dic.get(query))
        all_query_distance.append((query, mean_distance))
    all_query_distance.sort(key=lambda x: x[1])
    f_distance.write('query' + '\t' + 'distance' + '\n')
    for query_distance in all_query_distance:
        f_distance.write(query_distance[0] + '\t' + str(query_distance[1]) + '\n')
    f_distance.close()


def min_distance():
    # 每个query找出和它距离最近的URL, 保存距离和URL, title
    url_vector_dic = cPickle.load(open('/data/liubo/hotspot/yuqing/url_vector_dic.p', 'rb'))
    url_list = url_vector_dic.keys()
    useful_url_title_keyword_dic = cPickle.load(open('/data/liubo/hotspot/yuqing/useful_url_title_keyword_dic.p', 'rb'))
    query_all_distance_dic = cPickle.load(open('/data/liubo/hotspot/yuqing/query_all_distance_dic.p', 'rb'))
    f_distance = open('/data/liubo/hotspot/yuqing/query_min_distance.txt', 'w')
    all_query_distance = []
    for query in query_all_distance_dic:
        this_distance_list = query_all_distance_dic.get(query)
        min_index = np.argmin(this_distance_list)
        url = url_list[min_index]
        title, keywords = useful_url_title_keyword_dic[url]
        all_query_distance.append((query, url, title, this_distance_list[min_index]))
    all_query_distance.sort(key=lambda x: x[3])
    f_distance.write('\t'.join(['query', 'url', 'title', 'distance']) + '\n')
    for query_distance in all_query_distance:
        f_distance.write('\t'.join(map(str, query_distance)) + '\n')
    f_distance.close()


if __name__ == '__main__':
    pass
    # create_query_url_vector()
    # cal_query_url_distance()
    mean_distance()
    min_distance()
