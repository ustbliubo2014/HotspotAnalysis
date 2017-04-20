# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: gensim_lda.py
@time: 2017/2/17 16:26
@contact: ustb_liubo@qq.com
@annotation: gensim_lda
"""
import sys
import logging
from logging.config import fileConfig
import os
import jieba
from gensim import corpora, models
import pdb
import cPickle

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


def get_stop_words_set(file_name):
    with open(file_name, 'r') as file:
        return set([line.strip() for line in file])


def get_words_list(file_name, stop_word_file):
    stop_words_set = get_stop_words_set(stop_word_file)
    print "共计导入 %d 个停用词" % len(stop_words_set)
    word_list = []
    line_count = 0
    with open(file_name, 'r') as file:
        for line in file:
            tmp_list = list(jieba.cut(line.strip(), cut_all=False))
            # 注意这里term是unicode类型, 如果不转成str, 判断会为假
            word_list.append([term for term in tmp_list if str(term) not in stop_words_set]) #
            line_count += 1
            if line_count % 10000 == 0:
                print line_count
                break
    return word_list


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: %s <raw_msg_file> <stop_word_file> <output_file>" % sys.argv[0]
        sys.exit(1)

    raw_msg_file = sys.argv[1]
    stop_word_file = sys.argv[2]
    model_file = sys.argv[3]

    print 'load word'
    word_list = get_words_list(raw_msg_file, stop_word_file)    # 列表, 其中每个元素也是一个列表, 即每行文字分词后形成的词语列表
    word_dict = corpora.Dictionary(word_list)   # 生成文档的词典, 每个词与一个整型索引值对应
    print 'word corpus'
    corpus_list = [word_dict.doc2bow(text) for text in word_list]   # 词频统计, 转化成空间向量格式
    print 'train lda'
    lda = models.ldamodel.LdaModel(corpus=corpus_list, id2word=word_dict, num_topics=100, alpha='symmetric', distributed=False)
    cPickle.dump(lda, open(model_file, 'wb'))

    # pdb.set_trace()
    # topics = lda.show_topics()
    # lda.print_topic()
    lda.get_document_topics()
    for pattern in lda.show_topics():
        print"%s" % str(pattern)