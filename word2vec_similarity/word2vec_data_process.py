# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: word2vec_data_process.py
@time: 2017/2/9 19:21
@contact: ustb_liubo@qq.com
@annotation: word2vec_data_process
"""
import sys
import logging
from logging.config import fileConfig
import os

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


import pdb
import numpy as np
import jieba
import os
import base64
import msgpack
import sys
from conf import *
reload(sys)
sys.setdefaultencoding('utf-8')


class Word2vecDataProcess():
    '''
    处理word2vec过程中涉及到的文件转换,包括提取content内容并分词,生成vector_content_label文件(将content,vector,label放在一个文件夹)
    '''

    def __init__(self):
        # 这里的content_label_file是更过预处理后的文件
        self.content_label_file = content_label_file
        self.content_word_cut_file = content_word_cut_file
        self.content_word_vector_file = content_word_vector_file
        self.word2vec_exe_path = word2vec_exe_path
        self.vector_length = vector_length
        self.content_vector_label_file = content_vector_label_file
        self.label_trans_file = label_trans_file
        self.contentIndex_urlType_dic_file = contentIndex_urlType_dic_file
        self.word_idf_file = word_idf_file
        self.content_weight_vector_label_file = content_weight_vector_label_file

    def extract_cut_content(self, content_label_file, content_word_cut_file):
        f_cut = open(content_word_cut_file,'w')
        for line in open(content_label_file):
            tmp = line.rstrip().split('\t')
            if len(tmp) == 2:
                f_cut.write('\t'.join([word for word in jieba.cut(tmp[1])])+'\n')
        f_cut.close()

    def execute_word2vec(self):
        # 将word2vec的命令用字符串生成后用system执行,这样避免了手动操作
        cmd = self.word2vec_exe_path + ' -train ' + self.content_word_cut_file + ' -output ' + \
                    self.content_word_vector_file + ' -cbow 0 -size '+ str(self.vector_length) + ' -window 5 ' \
                    '-negative 0 -hs 1 -sample 1e-3 -threads 12 -binary 0'
        print cmd
        os.system(cmd)

    def load_word_vector(self,word_vector_file):
        word2vec_dic = {}#{word:vec}
        for line in open(word_vector_file):
            tmp = line.rstrip().split()
            if len(tmp) != vector_length + 1:
                continue
            # 其它的已经做了处理,所以加载所有word
            word2vec_dic[tmp[0]] = map(float,tmp[1:])
        return word2vec_dic

    def word2vec_sentence(self, content_label_file, content_vector_label_file):
        '''
            将content_label 转换成 content_vector_label ; 同时进行label的转换(str变成int)
        '''
        f_vector = open(content_vector_label_file,'w')
        word2vec_dic = self.load_word_vector(self.content_word_vector_file)
        no_find_count = 0
        no_find_sentence = 0
        contentIndex_urlType_dic = msgpack.load(open(contentIndex_urlType_dic_file,'rb'))
        if os.path.exists(self.label_trans_file):
            label_trans_dic = msgpack.load(open(self.label_trans_file,'rb'))
            current_label_index = max(label_trans_dic.values()) + 1
        else:
            label_trans_dic = {} # {label:label_index}
            current_label_index = 0
        line_index = 0
        for line in open(content_label_file):
            tmp = line.rstrip().split('\t')
            if len(tmp) < 2:
                continue
            label = tmp[0]
            urlType = contentIndex_urlType_dic.get(line_index)
            if label in label_trans_dic:
                label_index = label_trans_dic.get(label)
            else:
                print 'no label',line
                label_index = current_label_index
                label_trans_dic[label] = label_index
                current_label_index += 1
            content = tmp[1]
            word_list = jieba.cut(content)
            sentence_vector = [0] * self.vector_length
            has_find = False
            for word in word_list:
                word = word.decode('utf-8').encode('utf-8')
                if word in word2vec_dic:
                    has_find = True
                    sentence_vector = np.add(sentence_vector,word2vec_dic.get(word))
                else:
                    no_find_count += 1
            if not has_find:
                no_find_sentence += 1
            sentence_vector = list(sentence_vector)
            sentence_vector.append(urlType)
            # pdb.set_trace()
            sentence_vector = base64.b64encode(msgpack.packb(sentence_vector))
            f_vector.write(str(label_index)+'\t'+content+'\t'+sentence_vector+'\n')
        f_vector.close()
        msgpack.dump(label_trans_dic,open(self.label_trans_file,'wb'))
        print 'no_find_count',no_find_count,'no_find_sentence',no_find_sentence


    def word2vec_sentence_weight(self, content_label_file, content_weight_vector_label_file, word_idf_file):
        '''
            将content_label 转换成 content_vector_label ; 同时进行label的转换(str变成int)
        '''
        f_vector = open(content_weight_vector_label_file,'w')
        word2vec_dic = self.load_word_vector(self.content_word_vector_file)
        no_find_count = 0
        no_find_sentence = 0
        contentIndex_urlType_dic = msgpack.load(open(contentIndex_urlType_dic_file,'rb'))
        if os.path.exists(self.label_trans_file):
            label_trans_dic = msgpack.load(open(self.label_trans_file,'rb'))
            current_label_index = max(label_trans_dic.values()) + 1
        else:
            label_trans_dic = {} # {label:label_index}
            current_label_index = 0
        line_index = 0
        word_idf_dic = msgpack.load(open(word_idf_file, 'rb'))
        for line in open(content_label_file):
            tmp = line.rstrip().split('\t')
            label = tmp[0]
            urlType = contentIndex_urlType_dic.get(line_index)
            if label in label_trans_dic:
                label_index = label_trans_dic.get(label)
            else:
                print 'no label',line
                label_index = current_label_index
                label_trans_dic[label] = label_index
                current_label_index += 1
            content = tmp[1]
            word_list = [word for word in jieba.cut(content)]
            for word_index in range(len(word_list)):
                word_list[word_index] = word_list[word_index].decode('utf-8').encode('utf-8')
            sentence_vector = [0] * self.vector_length
            has_find = False
            word_tf_dic = {}
            for word in word_list:
                word_tf_dic[word] = word_tf_dic.get(word,0) + 1
            for word in word_list:
                if word in word2vec_dic:
                    has_find = True
                    word_weight = word_idf_dic.get(word) * word_tf_dic.get(word)
                    sentence_vector = np.add(sentence_vector, np.multiply(word_weight, word2vec_dic.get(word)))
                else:
                    no_find_count += 1
            if not has_find:
                no_find_sentence += 1
            sentence_vector = list(sentence_vector)
            sentence_vector.append(urlType)
            sentence_vector = base64.b64encode(msgpack.packb(sentence_vector))
            f_vector.write(str(label_index)+'\t'+content+'\t'+sentence_vector+'\n')
        f_vector.close()
        msgpack.dump(label_trans_dic,open(self.label_trans_file,'wb'))
        print 'no_find_count',no_find_count,'no_find_sentence',no_find_sentence


if __name__ == '__main__':
    word2vecDataProcess = Word2vecDataProcess()
    word2vecDataProcess.word2vec_sentence(word2vecDataProcess.content_label_file,
                                          word2vecDataProcess.content_vector_label_file)
    word2vecDataProcess.word2vec_sentence_weight(word2vecDataProcess.content_label_file,
                                    word2vecDataProcess.content_weight_vector_label_file,word2vecDataProcess.word_idf_file)