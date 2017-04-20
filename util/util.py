# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: util.py
@time: 2017/2/17 14:43
@contact: ustb_liubo@qq.com
@annotation: util
"""
import sys

import logging
from logging.config import fileConfig
import os
from time import time
import pdb
from zhtools.langconv import *
import traceback

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


stop_word_file = '/home/liubo-it/HotspotAnalysis/data/stop_word.dat'
stop_word_set = set([word.strip() for word in map(lambda x:x.decode('utf-8'), open(stop_word_file).read().split('\n'))])
filter_word_file = '/home/liubo-it/HotspotAnalysis/data/filter_words.txt'
filter_word_set = set([word.strip() for word in map(lambda x:x.decode('utf-8'), open(filter_word_file).read().split('\n'))])
stop_word_set = stop_word_set | filter_word_set


def is_chinese_word(uchar):
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False


def charQ2B(ustring):
    """把字符串全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code==0x3000:
            inside_code=0x0020
        else:
            inside_code-=0xfee0
        if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
            rstring += uchar
        rstring += unichr(inside_code)
    return rstring


def strQ2B(content):
    # start = time()
    content = list(content)
    for index, c in enumerate(content):
        try:
            if not is_chinese_word(c):
                content[index] = charQ2B(c)
        except:
            continue
    # end = time()
    # print (end - start)
    return ''.join(content)


def stop_word_filter(word_list):
    new_word_list = []
    for word in word_list:
        if word not in stop_word_set and word.encode('utf-8') not in stop_word_set:
            new_word_list.append(word)
    return new_word_list


def chinese_word_filter(content):
    # 将content中的非中文删掉
    new_content = []
    for char in content:
        if is_chinese_word(char):
            new_content.append(char)
    content = ''.join(new_content)
    return content


# 转换繁体到简体
def cht_to_chs(line):
    line = Converter('zh-hans').convert(line)
    line.encode('utf-8')
    return line


# 转换简体到繁体
def chs_to_cht(line):
    line = Converter('zh-hant').convert(line)
    line.encode('utf-8')
    return line


if __name__ == '__main__':
    pass
    src_file = '/data/liubo/hotspot/zhihu_corpus_1000000.txt'
    dst_file = '/data/liubo/hotspot/zhihu_corpus_1000000_chs.txt'
    f_dst = open(dst_file, 'w')
    count = 0
    start = time()
    for line in open(src_file):
        try:
            line = line.decode('utf-8')
            chs_line = cht_to_chs(line)
            f_dst.write(line)
            count += 1
        except:
            traceback.print_exc()
            continue
        if count % 1000 == 0:
            end = time()
            print count, (end - start)
            start = time()
