# coding=utf-8

"""
Created by jayvee on 16/12/22.
"""


class NonDataException(IOError):
    """
    无法获取到数据时的异常
    """

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message
