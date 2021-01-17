# -*- coding: utf-8 -*-
# @Time    :2021/1/16 22:29
# @Author  :robot_zsj
# @File    :test_case01.py
def add(x, y):
    return x + y


def test_add():
    assert add(1, 99) == 100
    # assert add(1, 99) == 1
