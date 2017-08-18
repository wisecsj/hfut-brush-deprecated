# -*- coding: utf-8 -*-
import requests
import urllib
import re

import sys

from .log import DevLogger as dlogger, UserLogger as ulogger
import getpass
from .utils import retry, scan_excel
from bs4 import BeautifulSoup

""" 
@author: W@I@S@E 
@contact: wisecsj@gmail.com 
@site: http://hfutoyj.cn/ 
@file: brush.py 
@time: 2017/8/18 16:41 
"""


class LoginMixin(object):
    def login(self):
        @retry(times=self._times)
        def single_login(self):
            """Sign in to tkkc.hfut.edu.cn
            """

            message = ''

            try:
                announce = self.get_login_form_data()
            except:
                dlogger.error('Func get_login_form_data failed')
            try:
                code = self.get_verify_code().text
            except:
                dlogger.error('Get verify code from Tencen Cloud Server failed')

            print("Trying " + ' ' + code)

            logForm = {
                announce: 'announce',
                'loginMethod': '{}button'.format(announce),
                "logname": self.sNum,
                "password": self.pwd,
                "randomCode": code
            }
            res = self.ses.post(self.login_url, data=logForm, headers=self.headers)

            if res.text.find("验证码错误") != -1:
                message = "Wrong verify code, Trying again ..."
                print(message)
            elif res.text.find("身份验证服务器未建立连接") != -1:
                message = "Wrong student number, Check and reinput please ..."
                print(message)
                self.sNum = input("请输入学号\n")
            elif res.text.find("密码不正确") != -1:
                message = "Wrong password, Check and reinput please ..."
                print(message)
                self.pwd = getpass.getpass("请输入密码\n")
            else:
                self.login_success = True
                message = 'Login Success !'
                return message

            return message

    def get_verify_code(self):
        """return verify code from self-build api
        """
        im = self.ses.get("http://tkkc.hfut.edu.cn/getRandomImage.do")
        tmp1 = urllib.parse.quote_from_bytes(im.content)
        code = self.ses.post('http://api.hfutoyj.cn/codeapi', data={'image': tmp1})
        return code

    def get_login_form_data(self):
        """As website add a new parameter 'announce'
        """
        r = self.ses.get(self.login_url).text
        announce = re.search(r'name="(.*?)" value="announce"', r)
        return announce


class SubmitMixin(object):
    def craw_question_title(self, url, retries=2):
        """craw the question text and return '' if failed """
        try:
            b = self.ses.post(url, headers=self.headers)
            b.encoding = 'utf-8'
            d = b.text
            title = re.search(r'&nbsp;(.*?)","', d, re.S)
            return title
        except Exception as e:
            print(e)
            if retries > 0:
                return self.craw(url, retries=retries - 1)
            else:
                dlogger.error("craw the {}th question failed".format(self.index))
                return ''

    def submit_for_full_test(self):
        start_url = input("请输入测试页面URL\n")

        body = self.ses.get(start_url, headers=self.headers)
        body.encoding = 'utf-8'
        wb_data = body.text

        urlId = re.search(r'do\?(.*?)&method', self.start_url, re.S)
        eval = re.search(r'eval(.*?)]\);', wb_data, re.S)

        bs = BeautifulSoup(wb_data, 'lxml')
        val = bs.form.input
        examReplyId = val['value']

        examId = re.search(r'<input type="hidden" name="examId" id="examId" value="(.*?)" />',
                           wb_data, re.S)

        exerciseId = re.findall(r'exerciseId":(.*?),', eval, re.S)

        examSEId = re.findall(r'examStudentExerciseId":(.*?),', eval, re.S)

        examStudentExerciseId = int(re.search(r'"examStudentExerciseId":(.*?),"exerciseId"',
                                              wb_data, re.S)
                                    )

        # id对应exerciseID,id2对应examStudetExerciseId
        for id in exerciseId:
            next_url = r"http://tkkc.hfut.edu.cn/student/exam/manageExam.do?%s&method=getExerciseInfo&examReplyId=%s&\
                    exerciseId=%s&examStudentExerciseId=%d" % (
                urlId, examReplyId, id, examStudentExerciseId)
            title = self.craw_question_title(next_url)
            ans = self.excel_dict.get[title, 'Not found']
            self.submit(ans, id, examStudentExerciseId, examReplyId, examId, self.index)
            # time.sleep(1)
            self.index += 1
            examStudentExerciseId = examStudentExerciseId + 1
        # input函数获取到的为字符串，所以进行Type conversion


    def submit_for_single_question(self, ans, id, id2, id3, id4, index, retries=2):
        """submit the answer of single question  to server"""
        dx = ["false"] * 4
        try:
            if ans.find('A') != -1:
                dx[0] = "true"
            if ans.find('B') != -1:
                dx[1] = "true"
            if ans.find('C') != -1:
                dx[2] = "true"
            if ans.find('D') != -1:
                dx[3] = "true"
            if ans.find('E') != -1:
                dx[4] = "true"
            if ans.find('正确') != -1:
                ans = "A"
            if ans.find('错误') != -1:
                ans = "B"
            data2 = {"examReplyId": id3,
                     "examStudentExerciseId": id2,
                     "exerciseId": id,
                     "examId": id4,
                     "DXanswer": ans,
                     "duoxAnswer": ans,
                     "PDanswer": ans,
                     "DuoXanswerA": dx[0],
                     "DuoXanswerB": dx[1],
                     "DuoXanswerC": dx[2],
                     "DuoXanswerD": dx[3],
                     "DuoXanswerE": dx[4],
                     "DuoXanswer": ans}  # 部分题库的多选是分成5个来提交，还有的是只用一个进行提交
            body = self.ses.post(self.save_url, data=data2, headers=self.headers)
            wb_data = body.text
            print(wb_data, index)
        except Exception as e:
            print(e)
            if retries > 0:
                return self.submit_for_single_question(ans, id, id2, id3, id4, index, retries=retries - 1)
            else:
                dlogger.error("submit_for_single_question() failed {}".format(self.index))
                return ''


class Brush(LoginMixin, SubmitMixin):
    save_url = "http://tkkc.hfut.edu.cn/student/exam/manageExam.do?1479131327464&method=saveAnswer"
    index = 1  # record probleme brushed count
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/41.0",
               "Host": "tkkc.hfut.edu.cn",
               "X-Requested-With": "XMLHttpRequest",
               }

    def __init__(self, sNum=None, pwd=None, excel_path='exercise.xls'):
        """

        :param flag:
            {
                0 : Go on after finish one test
                1 : Exit after brush all courses
                2 : re-login to another account
            }
        """
        self.ses = requests.session()
        self._sNum = sNum or input("请输入学号\n")
        self._pwd = pwd or getpass.getpass("请输入密码\n")
        self.excel_path = excel_path
        self.login_url = "http://tkkc.hfut.edu.cn/login.do?"
        self.login_success = False
        self._times = 3
        self.flag = 0

        self.excel_dict = scan_excel(self.excel_path)

    def start(self):

        while not self.login_success:
            self.login()
        while self.flag is 0:
            self.submit_for_full_test()
            self.flag = int(input("继续请输入0，退出请输入1,重新登录请输入2\n"))
        if self.flag is 1:
            sys.exit(0)
        if self.flag is 2:
            self.start()

