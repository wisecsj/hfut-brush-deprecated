# -*- coding: utf-8 -*-

"""
test module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
As get_verify_code() uses service on my Tencent Cloud Server and
travis-ci can not access the api(timout exception),So the test
always failed.
"""

from hfut_brush.bru import Brush
import os

WRONG_CODE_MESSAGE = "Wrong verify code, Trying again ..."
WRONG_ID_MESSAGE = "Wrong student number, Check and reinput please ..."
WRONG_PWD_MESSAGE = "Wrong password, Check and reinput please ..."
LOGIN_SUCCESS_MESSAGE = 'Login Success !'
TIMES_FAILED_MESSAGE = "Login failed after tried the max_times"

ID = os.getenv('HFUT_ID') or 'ID'  # replace 'ID' with your real ID
PWD = os.getenv('HFUT_PWD') or 'PWD'  # replace 'PWD' with your real password


def test_login_success():
    brush = Brush(ID, PWD)
    if ID == 'ID' and PWD == 'PWD':
        return True

    message, if_login_success = brush.login_for_test()
    while message == WRONG_CODE_MESSAGE:
        test_login_success()

    assert message == LOGIN_SUCCESS_MESSAGE and if_login_success == True


def test_login_ID():
    brush = Brush('2014', PWD)
    message, if_login_success = brush.login_for_test()
    while message == WRONG_CODE_MESSAGE:
        test_login_ID()

    assert message == WRONG_ID_MESSAGE and if_login_success == False


def test_login_PWD():
    brush = Brush('2014211666', 'qwer')
    message, if_login_success = brush.login_for_test()
    # handle situation when the verify code is not right
    while message == WRONG_CODE_MESSAGE:
        test_login_PWD()

    assert message == WRONG_PWD_MESSAGE and if_login_success == False

# def test_login_max_times():
