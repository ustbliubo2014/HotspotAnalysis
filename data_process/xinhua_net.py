# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: xinhua_net.py
@time: 2017/4/1 16:30
@contact: ustb_liubo@qq.com
@annotation: xinhua_net
"""
import sys
sys.path.append('/home/liubo-it/HotspotAnalysis/')
import json
import jieba.analyse as al
import jieba
import pdb
from util.util import stop_word_filter, strQ2B, chinese_word_filter
from bs4 import BeautifulSoup
import traceback
import requests
import os
import cPickle
import nltk

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


if __name__ == '__main__':
    file_name = '/data/xinhuanet_all.txt'
    url_keywords_dic = {}
    count = 0
    dst_file = '/data/yuqing.txt'
    f_dst = open(dst_file, 'w')
    top_num = 20

    for line in open(file_name):
        tmp = line.strip().split('\t')
        if len(tmp) == 2:
            url = tmp[0]
            dic = json.loads(tmp[1])
            if 'yuqing' not in url:
                continue
            if len(os.path.split(url)[-1].split('_')) == 3:
                continue
            if 'content' in dic:
                content = dic['content']
                key_words = al.extract_tags(content, top_num)
                fd = nltk.FreqDist(jieba.cut(content))
                f_dst.write(url + '\n' + '\t'.join(key_words) + '\n')
                count += 1
                for index in range(len(key_words)):
                    key_words[index] = (key_words[index], fd[key_words[index]])
                url_keywords_dic[url] = key_words
        if count % 100 ==0:
            print count
    cPickle.dump(url_keywords_dic, open('url_keywords_dic.p', 'wb'))
