# -*- coding: utf-8 -*-
import functools
import xlrd
from .exceptions import (
    ExceedMaxTimes)

""" 
@author: W@I@S@E 
@contact: wisecsj@gmail.com 
@site: http://hfutoyj.cn/ 
@file: utils.py 
@time: 2017/8/18 10:19 
"""


class retry(object):
    """
    Basic Usage::
        @retry(times=3)
        def func():
            pass
    Then,the func would execute 3 times at most.

    """

    def __init__(self, times):
        if isinstance(times, int) and times > 0:
            self.times = times
        else:
            raise ValueError('`times` must be int and larger than 0')
        self.count = 0

    def __call__(self, f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            with self:
                return f(*args, **kwargs)

        return wrapped

    def __enter__(self):
        if self.count >= self.times:
            raise ExceedMaxTimes('超过最大执行次数')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.count += 1


def scan_excel(excel_path):
    """
    !!!
    Waiting for optimized (not finished)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    :param excel_path:
    :return: dict which key is title,value is corresponding answer
    """
    result_dict = dict()
    f = xlrd.open_workbook(excel_path)
    sheets_num = len(f.sheets())

    # 读取XLS中的题目和答案，存进字典
    for x in range(sheets_num):
        xls = f.sheets()[x]
        for i in range(1, xls.nrows):
            title = xls.cell(i, 0).value
            if x == 1 and sheets_num == 2:
                answer = xls.cell(i, 2).value
            elif x == 1 and sheets_num == 3:
                answer = xls.cell(i, 7).value
            elif x == 2 and sheets_num == 3:
                answer = xls.cell(i, 2).value
            else:
                answer = xls.cell(i, 7).value
            result_dict[title] = answer
            return result_dict
