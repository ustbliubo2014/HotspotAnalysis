# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: word_sim.py
@time: 2017/4/6 19:02
@contact: ustb_liubo@qq.com
@annotation: word_sim
"""
import sys
import logging
from logging.config import fileConfig
import os
from keyword_distance import load_word2vec_model
import pdb
from sklearn.metrics import euclidean_distances

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


if __name__ == '__main__':
    word2vec_model_path = '/data/liubo/hotspot/zhihu_corpus_1000000.model'
    word2vec_model = load_word2vec_model(word2vec_model_path)
    pdb.set_trace()
