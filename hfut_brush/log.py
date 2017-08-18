# -*- coding: utf-8 -*-
import logging

""" 
@author: W@I@S@E 
@contact: wisecsj@gmail.com 
@site: http://hfutoyj.cn/ 
@file: log.py 
@time: 2017/8/18 20:04 
"""

import logging

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(message)s',
                    datefmt='%Y:%m:%d %H:%M:%S')

DevLogger = logging.getLogger('hfut_brush')
UserLogger = logging.getLogger()

formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
handler = logging.FileHandler('hfut_brush.log')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)  # the lowest level handler would handle
DevLogger.setLevel(logging.WARNING)
DevLogger.addHandler(handler)
DevLogger.propagate = 0  # prevent the LogRecord propagate to root logger(prevent console output)

# UserLogger.info('test')
# DevLogger.info('1')
