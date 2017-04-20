# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: reducer_query_search.py
@time: 2017/3/8 11:42
@contact: ustb_liubo@qq.com
@annotation: reducer_query_search
"""
import sys
sys.path.append('/home/liubo-it/HotspotAnalysis/')
import logging
from logging.config import fileConfig
import os
import jieba
import pdb
from time import time
from util.util import stop_word_filter, chinese_word_filter, strQ2B

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def word_stat():
    # 统计常出现的词,作为停用词
    day = sys.argv[1]
    stat_result_file = '/data/liubo/hotspot/query_search/word_stat_{}_filter.txt'.format(day)
    search_result_file = '/data/liubo/hotspot/query_search/search_result_{}.txt'.format(day)
    f_stat = open(stat_result_file, 'w')
    word_num_dic = {}
    count = 1
    start = time()
    for line in open(search_result_file):
        tmp = eval(line.rstrip())
        if len(tmp) == 3:
            word_list = []
            all_title = tmp[1]
            all_snapshot = tmp[2]
            for title in all_title:
                word_list.extend(title.split('\t'))
            for snapshot in all_snapshot:
                word_list.extend(snapshot.split('\t'))
            for word in word_list:
                word_num_dic[word] = word_num_dic.get(word, 0) + 1
        count += 1
    items = word_num_dic.items()
    items.sort(key=lambda x:x[1], reverse=True)
    for word, num in items:
        f_stat.write(str(word)+'\t'+str(num)+'\n')


def find_query_keywords():
    # 每个query找10个关键词来代表该query的语义
    keyword_num = 10
    last_query = ''
    last_query_keyword_num_dic = {}
    day = sys.argv[1]
    keywords_result_file = '/data/liubo/hotspot/query_search/keywords_{}_filter.txt'.format(day)
    search_result_file = '/data/liubo/hotspot/query_search/search_result_{}.txt'.format(day)
    f_keywords = open(keywords_result_file, 'w')

    for line in open(search_result_file):
        tmp = eval(line.rstrip())
        if len(tmp) == 3:
            this_query = tmp[0]
            word_list = []
            all_title = tmp[1]
            all_snapshot = tmp[2]
            for title in all_title:
                word_list.extend(title.split('\t'))
            for snapshot in all_snapshot:
                word_list.extend(snapshot.split('\t'))

            if this_query == last_query:
                for word in word_list:
                    last_query_keyword_num_dic[word] = last_query_keyword_num_dic.get(word, 0) + 1
            else:
                if len(last_query_keyword_num_dic) > 0:
                    items = last_query_keyword_num_dic.items()
                    items.sort(key=lambda x:x[1], reverse=True)
                    # keywords = stop_word_filter(map(lambda x:x[0], items))[:keyword_num]
                    keywords = map(lambda x:(x, last_query_keyword_num_dic.get(x)),
                                   stop_word_filter(map(lambda x:x[0], items))[:keyword_num])
                    f_keywords.write(last_query + '\t' + repr(keywords)+'\n')
                last_query = this_query
                last_query_keyword_num_dic = {}
                for word in word_list:
                    last_query_keyword_num_dic[word] = last_query_keyword_num_dic.get(word, 0) + 1
    if len(last_query_keyword_num_dic) > 0:
        items = last_query_keyword_num_dic.items()
        items.sort(key=lambda x: x[1], reverse=True)
        # keywords = stop_word_filter(map(lambda x: x[0], items))[:keyword_num]
        keywords = map(lambda x:(x, last_query_keyword_num_dic.get(x)),
                       stop_word_filter(map(lambda x: x[0], items))[:keyword_num])
        f_keywords.write(last_query + '\t' + repr(keywords) + '\n')


def recommend_result_process():
    keyword_num = 10
    day = sys.argv[1]
    recommend_result_file = '/data/liubo/hotspot/query_search/keywords_recommend_{}.txt'.format(day)
    search_recommend_file = '/data/liubo/hotspot/query_search/recommend_result_{}.txt'.format(day)
    f_keywords = open(recommend_result_file, 'w')
    for line in open(search_recommend_file):
        query, recommend_list = eval(line.rstrip())
        recommend_words_num_dic = {}
        for recommend in recommend_list:
            word_list = stop_word_filter([word for word in jieba.cut(chinese_word_filter(strQ2B(recommend)))])
            for word in word_list:
                recommend_words_num_dic[word] = recommend_words_num_dic.get(word, 0) + 1
        items = recommend_words_num_dic.items()
        items.sort(key=lambda x: x[1], reverse=True)
        f_keywords.write(query + '\t' + repr(items[:keyword_num]) + '\n')


if __name__ == '__main__':
    pass
    # word_stat()
    find_query_keywords()
    # recommend_result_process()