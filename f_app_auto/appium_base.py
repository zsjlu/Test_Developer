# -*- coding: utf-8 -*-
# @Time    :2021/1/23 12:15
# @Author  :robot_zsj
# @File    :appium_base.py
from appium import webdriver
from selenium.webdriver.support import  expected_conditions
from hamcrest import *


caps={}

driver = webdriver.Remote("url", caps)

driver.find_element().tag_name

