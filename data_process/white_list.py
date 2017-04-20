# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: white_list.py
@time: 2017/2/15 14:36
@contact: ustb_liubo@qq.com
@annotation: white_list
"""
import sys
import logging
from logging.config import fileConfig
import os
from pinyin import PinYin

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


# 在名单中的不用关心,直接过滤调(包含这些词就可以过滤调) ---只有一个词才能过滤

white_list = {
    u"天气预报",
    u"京东",
    u"淘宝",
    u"百度",
    u"微信",
    u"斗鱼",
    u"爱奇艺",
    u"腾讯视频",
    u"qq",
    u"熊猫tv",
    u"快递",
    u'4399',
}


word2pinyin = PinYin()
word2pinyin.load_word()
alphabet = {'a':1, 'b':1, 'c':1, 'd':1, 'e':1, 'f':1, 'g':1,
            'h':1, 'i':1, 'j':1, 'k':1, 'l':1, 'm':1, 'n':1,
            'o':1, 'p':1, 'q':1, 'r':1, 's':1, 't':1,
            'u':1, 'v':1, 'w':1, 'x':1, 'y':1, 'z':1}


def hanzi2pinyi(word):
    result = []
    for hanzi in word:
        if hanzi.lower() in alphabet:
            result.append(hanzi.lower())
        else:
            result.append(word2pinyin.hanzi2pinyin(hanzi))
    return ''.join(result)


if __name__ == '__main__':
    for word in white_list:
        print word2pinyin.hanzi2pinyin_split(word)
