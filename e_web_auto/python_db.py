# -*- coding: utf-8 -*-
# @Time    :2021/1/22 0:33
# @Author  :robot_zsj
# @File    :python_db.py
import shelve

db = shelve.open("db_data/test")

db['test'] = ['test']
db= shelve.open('db_data/test')
db['test'] = 'change'

db.close()