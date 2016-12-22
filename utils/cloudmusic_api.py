# coding=utf-8
import hashlib
import json
from urllib import urlencode

import requests

from utils.config_utils import get_config
from utils.encrypt_utils import encrypted_request
from utils.logger_utils import data_process_logger

"""
Created by jayvee on 16/12/14.
"""

config_infos = get_config()
csrf_token = config_infos['csrf_token']

header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'music.163.com',
    'Referer': 'http://music.163.com/',
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
}
cookies = {'appver': '1.5.2'}


def user_login(username, password):
    """
    用户登录api
    :param username:
    :param password:
    :return:
    """
    base_url = 'https://music.163.com/weapi/login/cellphone'
    login_url = 'https://music.163.com/weapi/login/'
    password = hashlib.md5(password).hexdigest()
    text = {
        'phone': username,
        'password': password,
        'rememberLogin': 'true'
    }
    data = encrypted_request(text)
    # s = requests.session()
    # s.headers = header
    res = requests.post(base_url, data=data, headers=header).content
    print res


def playlist_detail(playlist_id):
    """
    根据歌单id获取歌单的详情
    :param playlist_id:playlist id
    :return: playlist info json text
    """
    base_url = 'http://music.163.com/api/playlist/detail?id=%s' % playlist_id
    res = requests.get(base_url, headers=header).content
    # print res
    return json.loads(res)


def user_playlist(uid, offset=0, limit=100):
    """
    根据用户id获取用户歌单
    :param uid:
    :param offset:
    :param limit:
    :return:
    """
    base_url = 'http://music.163.com/api/user/playlist/?offset=%s&limit=%s&uid=%s' % (offset, limit, uid)
    # data = {'offset': offset, 'limit': limit, 'uid': uid}
    try:
        # data = urlencode(data)
        res = requests.get(base_url, headers=header).content
        data = json.loads(res)
        return data['playlist']
    except (requests.exceptions.RequestException, KeyError) as e:
        data_process_logger.error(e)
        return -1


def song_detail(song_ids, offset=0):
    """
    根据歌曲id列表批量获取歌曲详情
    :param song_ids:
    :return:
    """
    tmpids = song_ids[offset:]
    tmpids = tmpids[0:100]
    tmpids = list(map(str, tmpids))
    base_url = 'http://music.163.com/api/song/detail?ids=[%s]' % (  # NOQA
        ','.join(tmpids))
    try:
        data = json.loads(requests.get(base_url).content)
        # the order of data['songs'] is no longer the same as tmpids,
        # so just make the order back
        data['songs'].sort(key=lambda song: tmpids.index(str(song['id'])))
        return data['songs']
    except requests.exceptions.RequestException as e:
        data_process_logger.error(e)
        return []


def user_details(uid):
    """
    根据uid获取用户详情(通过歌单列表间接获取creator信息)
    :param uid:
    :return:
    """
    # upl = user_playlist(uid, limit=1)
    base_url = 'http://music.163.com/api/user/playlist/?offset=%s&limit=%s&uid=%s' % (0, 0, uid)
    # data = {'offset': offset, 'limit': limit, 'uid': uid}
    try:
        # data = urlencode(data)
        res = requests.get(base_url, headers=header).content
        data = json.loads(res)
        return data['playlist'][0]['creator']
    except (requests.exceptions.RequestException, KeyError) as e:
        data_process_logger.error(e)
        return -1


def search_web(s_name, type, limit=10):
    """
    网页搜索api
    :param s_name: 搜索词
    :param type: 搜索类型:1 单曲;10 专辑;100 歌手;1000 歌单;1002 用户
    :param limit:
    :return:
    """
    data = {"s": s_name, "type": type, "limit": limit}
    search_url = 'http://music.163.com/api/search/get/web'
    try:
        d = urlencode(data)
        res = requests.post(search_url, d, headers=header).content
        data = json.loads(res)
        return data
    except (requests.exceptions.RequestException, KeyError) as e:
        data_process_logger.error(e)
        return -1


if __name__ == '__main__':
    pass
    # a = playlist_detail('3659853')
    # print a
    # b = user_playlist('2886507')
    # print b
    # c = song_detail(['37239018', '23'])
    d = user_details('2886507')
    print search_web('jayvee he', '1002', 10)
