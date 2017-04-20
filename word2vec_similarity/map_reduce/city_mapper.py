# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: city_mapper.py
@time: 2017/2/15 17:46
@contact: ustb_liubo@qq.com
@annotation: city_mapper
"""
import sys
import logging
from logging.config import fileConfig
import os
import traceback
from time import time
import hashlib

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


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


def wordQ2B(content):
    start = time()
    content = list(content)
    for index, c in enumerate(content):
        try:
            if not is_chinese_word(c):
                content[index] = charQ2B(c)
        except:
            continue
    end = time()
    # print (end - start)
    return ''.join(content)


def top_filter():
    # 过滤各个搜索引擎中,自动推荐的内容
    keywords = ['newtab_new_hot', 'baidutop10']
    pass


if __name__ == '__main__':
    md5 = hashlib.md5()
    for line in sys.stdin:
        try:
            tmp = line.rstrip().split('\t')
            if len(tmp) > 6:
                this_time = tmp[1][:10]
                ip = tmp[2]
                md5.update(ip)
                ip = md5.hexdigest()
                query = tmp[4]
                address = tmp[6]
                address = address.split(',')
                for k in range(len(address) - 1, 0, -1):
                    if len(address[k]) > 0:
                        address = address[k]
                        break
                # if address == '保定' or address == '保定市':
                if True:
                    if query.startswith('query'):
                        query = query[9:]
                        if len(query) < 40 and len(query) > 0:
                            query = wordQ2B(query)
                            print '\t'.join([ip, this_time, query])
        except:
            traceback.print_exc()
            continue

