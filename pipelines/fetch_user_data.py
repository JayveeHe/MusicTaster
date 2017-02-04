# coding=utf-8
"""
Created by jayvee on 16/12/22.
"""
from utils.cloudmusic_api import *


def test():
    # u = User('2886507')
    # u.fill_details()
    # print u
    uname = ''  # 填入用户名,手机登录
    pwd = ''
    fetch_login_userdata(username=uname, password=pwd)


def fetch_login_userdata(username, password):
    """
    以当前登录用户为起点,获取各类信息
    :return:
    """
    user_info = user_login(username=username, password=password)
    if user_info != -1:
        user_profile = user_info['profile']
        uid = user_profile['userId']
        upl = user_playlist(uid)
        print len(upl)
    else:
        data_process_logger.warn('fetch login userdata failed')


def fetch_user_networks(start_id):
    """
    启动用户信息爬取的函数
    Args:
        start_id: 入口id

    Returns:

    """
    user_details()


# def get_user_info(uid):

if __name__ == '__main__':
    test()
