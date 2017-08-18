# -*- coding: utf-8 -*-


"""
    hfut-brush.user
    ~~~~~~~~~~~~~~~

    This module implements User interface

    ~~~~~~~~~~~~~~~
@author: W@I@S@E 
@contact: wisecsj@gmail.com 
@site: http://hfutoyj.cn/ 
@file: user.py 
@time: 2017/8/18 9:38 
"""


class User(object):
    """
        User Class
    """
    def __init__(self, sNum, pwd):
        """

        :param sNum: student number
        :param pwd: the password
        """
        self._sNum = sNum
        self._pwd = pwd

    @property
    def sNum(self):
        return self._sNum

    @property
    def pwd(self):
        return self._pwd


class Login(object):
    def __init__(self):
