# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: yuqing.py
@time: 2017/4/7 10:48
@contact: ustb_liubo@qq.com
@annotation: yuqing
"""
import sys
sys.path.append('/home/liubo-it/HotspotAnalysis/')
import logging
from logging.config import fileConfig
import os
from bs4 import BeautifulSoup
import traceback
import requests
import bs4
import cPickle
import pdb
from time import sleep, time
import json
import jieba.analyse as al
import jieba
import nltk
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def get_title_content(url):
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.content)
        tmp = (soup.select('.h-title'))
        if len(tmp) > 0:
            title = tmp[0].text
            content = ([x for x in (soup.select('.p-right')[0]).children])[1].text
        else:
            title = soup.find('title').text
            content = (soup.select('.article'))[0].text
    except:
        print url
        return '', ''
    if title == None:
        title = ''
    if content == None:
        content = ''
    return title, content


def trans_yuqing():
    file_name = '/data/liubo/hotspot/yuqing/xinhuanet_yuqing.txt'
    url_dic_path = '/data/liubo/hotspot/yuqing/url_title_content_dic.p'
    f_url_title = open('/data/liubo/hotspot/yuqing/url_title.txt', 'w')
    if os.path.exists(url_dic_path):
        new_url_title_content_dic = cPickle.load(open(url_dic_path, 'rb'))
    else:
        new_url_title_content_dic = {}
    print 'len(new_url_title_content_dic) :', len(new_url_title_content_dic)
    for line in open(file_name):
        tmp = line.rstrip().split('\t')
        if len(tmp) > 1:
            url = tmp[0]
            dic = json.loads(tmp[1])
            if 'title' in dic:
                title = dic['title']
                f_url_title.write(url+'\n'+title+'\n'+'\n')
            new_url_title_content_dic[url] = dic
    cPickle.dump(new_url_title_content_dic, open(url_dic_path, 'wb'))
    f_url_title.close()

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


def extract_topic():
    # 提取每个文章topic
    word2vec_model_path = '/data/liubo/hotspot/zhihu_corpus_1000000.model'
    word2vec_model = load_word2vec_model(word2vec_model_path)

    top_num = 20
    lower_threshold = 10 # 在最大的20个中最少找出10个有用的

    url_title_content_dic = cPickle.load(open('/data/liubo/hotspot/yuqing/url_title_content_dic.p', 'rb'))
    f_dst = open('/data/liubo/hotspot/yuqing/url_title_keyword.txt', 'w')
    url_list = url_title_content_dic.keys()
    useful_url_title_content_dic = {}
    # 使用sklearn求tfidf
    all_content = []
    all_url = []
    all_title = []
    for url in url_list:
        dic = url_title_content_dic.get(url)
        if 'content' in dic and 'title' in dic:
            content = dic['content']
            title = dic['title']
            content_words = ' '.join([word for word in jieba.cut(content)])
            all_content.append(content_words)
            all_url.append(url)
            all_title.append(title)
    start = time()
    # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()
    # 该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()
    # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(all_content))
    # 获取词袋模型中的所有词语
    all_word = vectorizer.get_feature_names()
    # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    weight = tfidf.toarray()
    end = time()
    print 'cal tfidf time :', (end - start)
    for index in range(len(all_content)):
        this_weight = zip(weight[index], range(weight.shape[1]))
        this_weight.sort(key=lambda x:x[0], reverse=True)
        find_num = 0
        this_keywords = []
        for k in range(top_num):
            word_tfidf, word_index = this_weight[k]
            word = all_word[word_index]
            if word in word2vec_model:
                find_num += 1
                this_keywords.append((word, word_tfidf))
        # 对应len(this_keywords) == 0的情况, 后面删除
        if len(this_keywords) >= lower_threshold:
            useful_url_title_content_dic[all_url[index]] = \
                (all_title[index], this_keywords)
            f_dst.write(all_url[index] + '\n' + all_title[index] + '\n' +
                        '\t'.join(map(lambda x:str(x[0])+'\t'+str(x[1]), this_keywords))+'\n')
    f_dst.close()
    cPickle.dump(useful_url_title_content_dic, open('/data/liubo/hotspot/yuqing/useful_url_title_content_dic.p', 'wb'))


if __name__ == '__main__':
    pass
    # trans_yuqing()
    extract_topic()
