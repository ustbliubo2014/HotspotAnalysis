# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: gensim_word2vec_train.py
@time: 2017/2/13 9:59
@contact: ustb_liubo@qq.com
@annotation: gensim_word2vec_train
"""
import sys
import logging
from logging.config import fileConfig
import os
from gensim.models import word2vec
import logging
import pdb

# reload(sys)
# sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


if __name__ == '__main__':
    # corpus_file = u'/data/liubo/hotspot/query_list_20161130_new.txt'
    # model_path = u'/data/liubo/hotspot/query_list_20161130.gensim.model'

    # corpus_file = '/data/liubo/hotspot/test_query_uniq_utf8_wordcut.txt'
    # model_path = '/data/liubo/hotspot/test_query_uniq_beijing.gensim.model'

    # corpus_file = '/data/liubo/hotspot/test_query_uniq_utf8_wordcut.txt'
    # model_path = '/data/liubo/hotspot/test_query_uniq_beijing.gensim.model'

    # corpus_file = '/data/liubo/hotspot/query_list_20161110_country_wordcut.txt'
    # model_path = '/data/liubo/hotspot/query_list_20161110_country_wordcut.gensim.model'

    corpus_file = sys.argv[1]
    model_path = sys.argv[2]

    sentences = word2vec.Text8Corpus(corpus_file)
    # 用所有query_list训练太慢(将查询次数太少的过滤掉[小于window])
    model = word2vec.Word2Vec(sentences, size=200, window=5, min_count=5, workers=12)  # 训练skip-gram模型; 默认window=5
    # pdb.set_trace()
    # 保存模型，以便重用
    model.save(model_path)
    # 对应的加载方式
    # model_2 = word2vec.Word2Vec.load(model_path)


