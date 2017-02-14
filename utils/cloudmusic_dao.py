# coding=utf-8

"""
负责进行云音乐的数据库相关操作

Created by jayvee on 16/12/24.
"""
from utils.db_utils import get_db_inst
from utils.logger_utils import data_process_logger


class CloudMusicDAO:
    def __init__(self, db_name, collection_name):
        self.db_name = db_name
        self.collection_name = collection_name
        self.db_inst = get_db_inst(self.db_name, self.collection_name)

    def save_unique_item(self, data_obj, primary_key='userId', is_overwrite=False, is_inform=False):
        """
        存储数据对象,并避免重复存储
        Args:
            data_obj:
            primary_key:
            is_overwrite:

        Returns:

        """
        find_result = self.db_inst.find_one({primary_key: data_obj[primary_key]}, {primary_key: 1})
        # is_exist = user_dbinst.find({'userId': userinfo['userId']}).count() != 0
        # print find_result.count()

        if not find_result:
            self.db_inst.insert(data_obj)
        elif is_overwrite:
            self.db_inst.update({primary_key: data_obj[primary_key]}, data_obj)
            if is_inform:
                data_process_logger.warn(
                    'overwrite item %s in %s' % (data_obj[primary_key], self.collection_name))
        else:
            if is_inform:
                data_process_logger.warn(
                    'Item %s exist! in %s' % (data_obj[primary_key], self.collection_name))
