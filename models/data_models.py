# coding=utf-8
from utils.cloudmusic_api import user_playlist, user_details
from utils.logger_utils import data_process_logger

"""
Created by jayvee on 16/12/22.
"""


class User:
    """
    用户类

    """

    def __init__(self, uid):
        self.uid = uid
        self.playlist = []
        self.details = {}
        self.has_details = False
        # get user info

    def fill_user_playlist(self):
        # get user playlist
        pl = user_playlist(self.uid)
        if pl != -1:
            self.playlist = pl
        else:
            data_process_logger.error('cannot get the playlist of user %s' % self.uid)

    def fill_user_details(self):
        u_details = user_details(self.uid)
        if u_details != -1:
            self.details = u_details
            self.has_details = True
        else:
            data_process_logger.error('cannot get the details of user %s' % self.uid)


class Song:
    """
    歌曲类
    """

    def __init__(self, sid):
        self.sid = sid
        self.details = {}
        self.has_details = False

    def _fill_song_details(self):
        pass
