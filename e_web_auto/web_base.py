# -*- coding: utf-8 -*-
# @Time    :2021/1/18 21:30
# @Author  :robot_zsj
# @File    :web_base.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

driver = webdriver.Chrome()
WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable(By.TAG_NAME, "title"))

current_handle = driver.current_window_handle()
all_handle = driver.window_handles()
for i in all_handle:
    if i != current_handle:
        driver.switch_to.window(i)

driver = webdriver.PhantomJS()

driver.find_element(By.id,)
