# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: mapper_query_search.py
@time: 2017/3/8 11:42
@contact: ustb_liubo@qq.com
@annotation: mapper_query_search
"""
import sys
sys.path.append('/home/liubo-it/HotspotAnalysis/')
import logging
from logging.config import fileConfig
import os
import bs4
from bs4 import BeautifulSoup
import urllib2
import traceback
# from util import stop_word_filter, strQ2B, chinese_word_filter
from util.util import stop_word_filter, strQ2B, chinese_word_filter
import jieba
import pdb
from time import time
import requests
import multiprocessing
import base64
import msgpack

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


# 将一个城市的query排序后, 取前200个, 然后一个城市一个文件, 每个文件用一个map处理 (本地做)
# mapper : 获取360搜索的查询结果
# reducer : 统计变量, 获取每个query的关键词


pre_url = 'https://www.so.com/s?ie=utf-8&fr=none&src=360sou_newhome&q='
title_list = ['.res-title']
snapshot_list = ['.res-rich', 'res-desc']
all_query_result = []

def get_query_search(query):
    url = pre_url + query
    request = requests.get(url)
    soup = BeautifulSoup(request.content)
    query_result_list = soup.select('.res-list')
    all_title = []
    all_snapshot = []
    for query_result in query_result_list:
        try:
            for title_str in title_list:
                title = query_result.select(title_str)
                if len(title) > 0:
                    all_title.append(title[0].text.rstrip())
                    break
            for snapshot_str in snapshot_list:
                snapshot = query_result.select(snapshot_str)
                if len(snapshot) > 0:
                    all_snapshot.append(snapshot[0].text.rstrip())
                    break
        except:
            traceback.print_exc()
            continue
    for index in range(len(all_title)):
        all_title[index] = '\t'.join(stop_word_filter(
                [word for word in jieba.cut(chinese_word_filter(strQ2B(all_title[index])))]))
    for index in range(len(all_snapshot)):
        all_snapshot[index] = '\t'.join(stop_word_filter(
                [word for word in jieba.cut(chinese_word_filter(strQ2B(all_snapshot[index])))]))
    return repr((query, all_title, all_snapshot))


def get_query_recommend(query):
    recommend_list = []
    try:
        url = pre_url + query
        request = requests.get(url)
        soup = BeautifulSoup(request.content)
        query_recommend_list = soup.select('.so-pdr-bd')
        if len(query_recommend_list) == 0:
            return ''
        query_recommend_list = [x for x in soup.select('.so-pdr-bd')[0].children]
        for query_recommend in query_recommend_list:
            try:
                if type(query_recommend) == bs4.element.Tag:
                    recommend_list.append(query_recommend.string)
            except:
                continue
        return repr((query, recommend_list))
    except:
        return ''


def mapper(search_func, result_file):
    pool = multiprocessing.Pool(processes=30)
    start = time()
    f_result = open(result_file, 'w')
    all_query_list = open('/data/liubo/hotspot/query_search/unique_query_{}.txt'.format(day)).read().split('\n')[:]
    for line in all_query_list[:]:
        try:
            query = line.rstrip()
            all_query_result.append(pool.apply_async(search_func, (query,)))
        except:
            traceback.print_exc()
            continue
    pool.close()
    pool.join()

    for result in all_query_result:
        f_result.write(result.get() + '\n')
    print 'mapper time :', (time() - start)


if __name__ == '__main__':
    pass
    day = sys.argv[1]
    mapper(get_query_search, '/data/liubo/hotspot/query_search/search_result_{}.txt'.format(day))
    # mapper(get_query_recommend, '/data/liubo/hotspot/query_search/recommend_result_{}.txt'.format(day))
    # get_query_recommend('新疆布尔津地图')
