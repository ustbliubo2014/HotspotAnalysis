# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: lda_cluster.py
@time: 2017/2/16 17:59
@contact: ustb_liubo@qq.com
@annotation: lda_cluster
"""
import sys
import logging
from logging.config import fileConfig
import os
import jieba
import numpy as np
import lda
import cPickle
import pdb

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def load_data(file_name):
    # 返回numpy矩阵(每行是一个文档, 每列一个单词[词袋模型])
    word_index_dic = {}
    word_index = 0
    line_count = 0
    line_threshold = 10000
    for line in open(file_name):
        tmp = line.rstrip().split('\t')
        if len(tmp) < 3:
            continue
        query = tmp[2]
        all_word = [word for word in jieba.cut(query)]
        for word in all_word:
            if word not in word_index_dic:
                word_index_dic[word] = word_index
                word_index += 1
        line_count += 1
        if line_count > line_threshold:
            break
    word_num = len(word_index_dic)
    data = np.zeros(shape=(line_count, word_num), dtype=np.int)
    line_count = 0
    for line in open(file_name):
        tmp = line.rstrip().split('\t')
        if len(tmp) < 3:
            continue
        query = tmp[2]
        all_word = [word for word in jieba.cut(query)]
        for word in all_word:
            word_index = word_index_dic.get(word)
            data[line_count][word_index] = data[line_count][word_index] + 1
        line_count += 1
        if line_count > line_threshold:
            break
    return data, word_index_dic


if __name__ == '__main__':
    file_name = '/data/liubo/hotspot/query_city_baoding_20161125-20161130.txt'
    data, word_index_dic = load_data(file_name)
    index_word_dic = dict(map(lambda x: (x[1], x[0]), word_index_dic.items()))
    model = lda.LDA(n_topics=20, n_iter=500, random_state=1)
    model.fit(data)
    cPickle.dump(model, open('lda.model', 'wb'))
    cPickle.dump(index_word_dic, open('index_word_dic.p', 'wb'))
    topic_word = model.topic_word_
