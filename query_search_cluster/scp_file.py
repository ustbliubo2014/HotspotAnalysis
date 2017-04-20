# encoding: utf-8

"""
@author: liubo
@software: PyCharm
@file: scp_file.py
@time: 2017/3/31 12:29
@contact: ustb_liubo@qq.com
@annotation: scp_file
"""
import sys
import logging
from logging.config import fileConfig
import os
import paramiko
import os
import traceback
import pexpect

reload(sys)
sys.setdefaultencoding("utf-8")
# fileConfig('logger_config.ini')
# logger_error = logging.getLogger('errorhandler')


# hostname = 'dpl07.skyeyes.lycc.qihoo.net'
# port = 22
# username = 'liubo-it'
# password = 'qwer1234!@#$QWER'
# remote_folder = '/data/liubo/hotspot/hadoop_file/20161124'
# local_folder = '/home/liubo-it/hadoop_file/20161124'


def scp_local2remote(ip, user, passwd, dst_path, filename):
    passwd_key = '.*assword.*'
    if os.path.isdir(filename):
        cmdline = 'scp -r {} {}@{}:{}'.format(filename, user, ip, dst_path)
    else:
        cmdline = 'scp {} {}@{}:{}'.format(filename, user, ip, dst_path)
    try:
        child = pexpect.spawn(cmdline)
        child.expect(passwd_key)
        child.sendline(passwd)
        child.expect(pexpect.EOF, timeout=2000)
        print "uploading"
    except:
        traceback.print_exc()
        print "upload faild!"


def scp_remote2local(ip, user, passwd, local_path, remote_path, is_folder):
    password_key = '.*assword.*'
    if is_folder:
        cmdline = 'scp -r {}@{}:{} {}'.format(user, ip, remote_path, local_path)
    else:
        cmdline = 'scp {}@{}:{} {}'.format(user, ip, remote_path, local_path)
    print cmdline
    try:
        child = pexpect.spawn(cmdline)
        child.expect(password_key)
        child.sendline(passwd)
        child.expect(pexpect.EOF, timeout=2000)
        print "downloading"
    except:
        traceback.print_exc()
        print "download faild!"


# 在远端服务器执行命令
def exec_remote_command(ip, port, user, password, command):
    pass
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, user, password)
    stdin, stdout, stderr = ssh.exec_command(command)
    print stdout.readlines()
    ssh.close()


if __name__ == "__main__":
    scp_local2remote(ip='dpl07.skyeyes.lycc.qihoo.net', user='liubo-it', passwd='qwer1234!@#$QWER',
         dst_path='/tmp', filename='/home/hdp-skyeye-algorithm/liubo-it/learn/hotspot/time_filter_fd')

    scp_remote2local(ip='dpl07.skyeyes.lycc.qihoo.net', user='liubo-it', passwd='qwer1234!@#$QWER',
                            local_path='/home/hdp-skyeye-algorithm/liubo-it/learn/hotspot', remote_path='/tmp/tmp',
                     is_folder=True)
    scp_remote2local(ip='dpl07.skyeyes.lycc.qihoo.net', user='liubo-it', passwd='qwer1234!@#$QWER',
                     local_path='/home/hdp-skyeye-algorithm/liubo-it/learn/hotspot', remote_path='/tmp/tmp/jieba.cache',
                     is_folder=False)
