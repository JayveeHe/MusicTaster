# coding=utf-8
from utils.cloudmusic_api import user_playlist, user_details, song_detail
from utils.logger_utils import data_process_logger

"""
Created by jayvee on 16/12/22.
"""


class InfoObj:
    """
    基础的信息类
    """

    def __init__(self):
        pass

    def fill_details(self):
        """
        填充信息类的信息
        :return:
        """
        pass


class User(InfoObj):
    """
    用户类

    """

    def __init__(self, uid):
        InfoObj.__init__(self)
        self.uid = uid
        self.playlist = []
        self.details = {}
        self.__has_details = False
        # get user info

    def __fill_user_playlist(self):
        """
        填充用户歌单信息
        :return: None
        """
        # get user playlist
        pl = user_playlist(self.uid)
        if pl != -1:
            self.playlist = pl
        else:
            data_process_logger.error('cannot get the playlist of user %s' % self.uid)

    def __fill_user_details(self):
        """
        填充用户信息
        :return: None
        """
        u_details = user_details(self.uid)
        if u_details != -1:
            self.details = u_details
            self.__has_details = True
        else:
            data_process_logger.error('cannot get the details of user %s' % self.uid)

    def fill_details(self):
        self.__fill_user_details()
        self.__fill_user_playlist()

    def __str__(self):
        return str(self.details)



class Song(InfoObj):
    """
    歌曲类
    """

    def __init__(self, sid):
        InfoObj.__init__(self)
        self.sid = sid
        self.details = {}
        self.__has_details = False

    def __fill_song_details(self):
        sd = song_detail(self.sid)
        if sd != -1:
            self.details = sd
            self.__has_details = True
        else:
            data_process_logger.error('cannot get the details of song %s' % self.sid)

    def fill_details(self):
        self.__fill_song_details()

    def __str__(self):
        return str(self.details)
