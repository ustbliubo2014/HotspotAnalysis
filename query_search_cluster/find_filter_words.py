# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: find_filter_words.py
@time: 2017/3/10 19:09
@contact: ustb_liubo@qq.com
@annotation: find_filter_words
"""
import sys
import logging
from logging.config import fileConfig
import os
import pdb

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def find_filter_word():
    f_result = open('/home/liubo-it/HotspotAnalysis/data/filter_words.txt', 'w')
    head_threshold = 300
    filter_percent = 0.8
    file_prefix = 'word_stat_'
    folder = '/data/liubo/hotspot/query_search/'
    file_list = os.listdir(folder)
    word_count_dic = {}
    file_num = 0
    for file_name in file_list:
        this_count = 0
        if file_prefix not in file_name:
            continue
        for line in open(os.path.join(folder, file_name)):
            tmp = line.rstrip().split('\t')
            if len(tmp) == 2:
                word, _ = tmp
                word_count_dic[word] = word_count_dic.get(word, 0) + 1
            this_count += 1
            if this_count > head_threshold:
                break
        file_num += 1
    for word in word_count_dic:
        count = word_count_dic.get(word)
        if count > file_num * filter_percent:
            f_result.write(word+'\n')
            print word
    print 'file_num :', file_num


if __name__ == '__main__':
    pass
    find_filter_word()
