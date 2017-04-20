# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: show.py
@time: 2017/4/6 10:34
@contact: ustb_liubo@qq.com
@annotation: show
"""
import sys
import logging
from logging.config import fileConfig
import os
import requests
from bs4 import BeautifulSoup
import bs4
import cPickle
import traceback
import pdb

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def get_title(url):
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.content)
        tmp = (soup.select('.main_tit'))[0]
        title = [x for x in tmp.children][1].text
        return title
    except:
        traceback.print_exc()
        return ''


if __name__ == '__main__':
    pass

    # url_title_dic = cPickle.load(open('url_title_dic.p', 'rb'))
    # f = open('url_title.txt', 'w')
    # for url in url_title_dic:
    #     f.write(url+'\t'+url_title_dic.get(url)+'\n')
    # f.close()

    # distance_dic = cPickle.load(open('distance_dic.p', 'rb'))
    # items = distance_dic.items()
    # items.sort(key=lambda x:x[1])
    # f = open('result.txt', 'w')
    # f.write('\t'.join(['query', 'url', 'title', 'distance'])+'\n')
    # for index, item in enumerate(items[:100]):
    #     query_url, distance = item
    #     query, url = query_url
    #     print index
    #     f.write('\t'.join(map(lambda x:str(x).rstrip().replace('\r', '').replace('\n', ''), [query, url, url_title_dic.get(url), distance]))+'\n')

    for line in open('C:\Users\liubo\Desktop/query_string_label_outcome1'):
        tmp = line.rstrip().split('\t')
        print len(tmp)