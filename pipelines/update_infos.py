# coding=utf-8

"""
Created by jayvee on 17/2/14.
"""
import random

import time

from utils.cloudmusic_api import song_comments
from utils.cloudmusic_dao import CloudMusicDAO
from utils.logger_utils import data_process_logger


def update_userinfo():
    """
    临时更新数据库的脚本
    Returns:

    """
    DAO_inst = CloudMusicDAO('MusicTaster', 'UserInfos')
    uids = DAO_inst.db_inst.distinct('userId')
    count = 0
    for uid in uids:
        userinfo = DAO_inst.db_inst.find_one({'userId': uid})
        userinfo['follow_count'] = len(userinfo['follow_ids'])
        userinfo['fan_count'] = len(userinfo['fan_ids'])
        DAO_inst.save_unique_item(userinfo, primary_key='userId', is_overwrite=True)
        data_process_logger.info('No.%s %s-%s' % (count, userinfo['userId'], userinfo['nickname']))
        count += 1
    print 'done'


def fill_song_comments():
    """
    填充歌曲的评论详情
    Returns:

    """
    dao_inst = CloudMusicDAO('MusicTaster', 'SongInfos')
    find_result = dao_inst.db_inst.find({'commentInfo': {'$exists': False}})
    count = 0
    for song_item in find_result:
        comm_data = song_comments(song_item['commentThreadId'], limit=10)
        if comm_data:  # 确保评论详情读取正确
            del comm_data['code']
            # del comm_data['userId']
            song_item['commentInfo'] = comm_data
            song_item['commentCount'] = comm_data['total']
        dao_inst.db_inst.save(song_item)
        data_process_logger.info(
            'No.%s %s, comments: %s done' % (count, song_item['name'], song_item['commentCount']))
        count += 1
        slp = random.random() * 2 + 1
        data_process_logger.info('sleep %s sec' % slp)
        time.sleep(slp)


if __name__ == '__main__':
    while 1:
        try:
            fill_song_comments()
        except Exception, e:
            print 'error %s' % e
            continue
