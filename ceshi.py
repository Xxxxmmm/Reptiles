#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 野猪佩奇
# @contact : 2790279232@qq.com
# @File    : ceshi.py
# @Software: PyCharm
# @Time    : 2020-07-13-0013 16:51
for page in range(1, 100, 2):
    url = f"https://search.jd.com/Search?keyword=%E7%94%B5%E8%84%91&page={page}&s=151&click=0"
    print(url)