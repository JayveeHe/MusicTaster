# coding=utf-8
"""
Created by jayvee on 16/12/22.
"""
import time

from utils.cloudmusic_api import *
from utils.cloudmusic_dao import CloudMusicDAO
from utils.db_utils import get_db_inst


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
    if user_info != -1 and user_info['code'] == 200:
        # user_profile = user_info['profile']
        # uid = user_profile['userId']
        # upl = user_playlist(uid)
        # print len(upl)
        return user_info
    else:
        data_process_logger.warn('fetch login userdata failed')


def fetch_user_networks(start_id=None, max_user_count=5000):
    """
    启动用户信息爬取的函数
    Args:
        max_user_count: 本次最大爬取的用户数
        start_id: 入口id,如果没有则在数据库中任取一个

    Returns:

    """
    db_userinfo = get_db_inst('MusicTaster', 'UserInfos')
    DAO_inst = CloudMusicDAO('MusicTaster', 'UserInfos')
    # start_info = user_login('13717951224', 'hejiawei')
    # u_profile = user_profile(start_id)
    if not start_id:
        start_id = db_userinfo.find_one()['userId']
    idlist = set()
    idlist.add(start_id)
    # save start user info
    cur_id = start_id
    followlist = user_follows(cur_id)
    for i in followlist:
        idlist.add(i['userId'])
    # result_count = find_result.count()
    user_count = 0
    while len(idlist) > 0 and user_count < max_user_count and cur_id:
        if db_userinfo.find({'userId': cur_id}).count() != 0:
            # slp = random.random() * 1 + 0.5
            data_process_logger.info('[SKIP] No.%s User %s skip!' % (user_count, cur_id))
            # data_process_logger.info('sleep %s sec' % slp)
            user_count += 1
            cur_id = idlist.pop()
            continue
        u_profile = user_profile(cur_id)
        # db_userinfo.insert(u_profile)
        followlist = user_follows(cur_id)
        fanlist = user_fans(cur_id)
        u_profile['follows'] = followlist
        u_profile['fans'] = fanlist
        followids = []
        fanids = []
        for userinfo in followlist:
            int_id = userinfo['userId']
            followids.append(int_id)
            idlist.add(int_id)
        for userinfo in fanlist:
            int_id = userinfo['userId']
            fanids.append(int_id)
            idlist.add(int_id)
        u_profile['follow_ids'] = followids
        u_profile['follow_count'] = len(followids)
        u_profile['fan_ids'] = fanids
        u_profile['fan_count'] = len(fanids)
        DAO_inst.save_unique_item(u_profile)
        data_process_logger.info('[OK] No.%s User %s, nickname = %s ok! %s users left' % (
            user_count, cur_id, u_profile['nickname'], len(idlist)))
        slp = random.random() * 2 + 1
        data_process_logger.info('sleep %s sec' % slp)
        time.sleep(slp)
        cur_id = idlist.pop()
        user_count += 1
        # result_count = db_userinfo.find({'userId': cur_id}).count()
    print 'done'


def fetch_playlist(max_user_count=100):
    """
    进行用户歌单的抓取,同时更新UserInfos、SongInfos和Plyalists三个数据库的信息
    Args:
        max_user_count: 最大抓取的用户数

    Returns:
        无
    """
    user_dao_inst = CloudMusicDAO('MusicTaster', 'UserInfos')
    playlist_dao_inst = CloudMusicDAO('MusicTaster', 'Playlists')
    song_dao_inst = CloudMusicDAO('MusicTaster', 'SongInfos')
    userid_list = user_dao_inst.db_inst.find({"playlists": {'$exists': False}}).distinct('userId')
    # random.shuffle(userid_list)
    count = 0
    for uid in userid_list[:max_user_count]:
        # count = 0
        userinfo = user_dao_inst.db_inst.find_one({"userId": uid})
        # fetch playlist ids
        user_playlists = user_playlist(uid, limit=2000)
        data_process_logger.info(
            'processing the playlist of %s\nTotal playlist = %s' % (userinfo['nickname'], len(user_playlists)))
        if len(user_playlists):
            for i in range(len(user_playlists)):
                pl_info = user_playlists[i]
                data_process_logger.info(
                    'processing %s No.%s playlist: %s, total song: %s' % (
                        userinfo['nickname'], i, pl_info['name'], pl_info['trackCount']))
                # fetch playlist details
                # 首先查看是否在数据库中有
                pl_obj = playlist_dao_inst.db_inst.find_one({'id': pl_info['id']})
                if not pl_obj:
                    try:
                        pl_obj = playlist_detail(pl_info['id'])
                        pl_song_ids = []
                        if pl_obj != -1:
                            for song in pl_obj['tracks']:
                                song_dao_inst.save_unique_item(song, primary_key='id')
                                pl_song_ids.append(song['id'])
                            # 在playlist中保存track信息,只保存编号
                            user_playlists[i]['tracks_ids'] = pl_song_ids
                            pl_obj['tracks_ids'] = pl_song_ids
                            playlist_dao_inst.save_unique_item(pl_obj, primary_key='id', is_inform=True)
                            slp = random.random() * 2 + 1
                            # data_process_logger.info('sleep %s sec' % slp)
                            time.sleep(slp)
                        else:
                            data_process_logger.error('cannot fetch %s %s' % (pl_info['id'], pl_info['name']))
                    except Exception, e:
                        print e
                else:
                    user_playlists[i]['tracks_ids'] = pl_obj['tracks_ids']

        # 在userinfo中保存playlist信息
        userinfo['playlists'] = user_playlists
        user_dao_inst.save_unique_item(userinfo, primary_key='userId', is_overwrite=True, is_inform=True)
        data_process_logger.info('No.%s %s playlist handled!' % (count, userinfo['nickname']))
        slp = random.random() * 2 + 1
        data_process_logger.info('sleep %s sec' % slp)
        time.sleep(slp)
        count += 1
    print 'done'


if __name__ == '__main__':
    # login_user_info = fetch_login_userdata('', '')
    # start_id = login_user_info['profile']['userId']
    # tmp_id = 2886507
    # fill_song_comments()
    # fetch_user_networks()
    fetch_playlist(max_user_count=1000)
    # update_userinfo()
    # test()
