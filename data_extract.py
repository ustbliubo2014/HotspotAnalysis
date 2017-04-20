# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: data_extract.py
@time: 2017/2/9 12:29
@contact: ustb_liubo@qq.com
@annotation: data_extract
"""
import sys
import logging
from logging.config import fileConfig
import os
import json
import pdb
import gzip
import base64
import zlib
import traceback

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


if __name__ == '__main__':
    for line in open('data/weibo'):
        try:
            tmp = json.loads(line)
            url = tmp['durl']
            content = zlib.decompress(base64.b64decode(tmp['value'][0]['attrs']['content']))
            # print url
            if url == 'http://www.weibo.com/rosemary16':
                print content
        except:
            # traceback.print_exc()
            continue
