# coding=utf-8

"""
负责进行云音乐的数据库相关操作

Created by jayvee on 16/12/24.
"""
from utils.db_utils import get_db_inst
from utils.logger_utils import data_process_logger


class CloudMusicDAO():
    def __init__(self, db_name='MusicTaster'):
        self.db_name = db_name

    def get_user_info_dbinst(self):
        """
        获取用户信息数据的数据库实例
        Returns:
            数据实例
        """
        try:
            user_dbinst = get_db_inst(self.db_name, 'UserInfos')
            return user_dbinst
        except Exception, e:
            data_process_logger.error('get_user_info_dbinst failed, details=%s' % e)
