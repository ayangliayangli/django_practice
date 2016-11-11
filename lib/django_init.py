#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
@version:
@author: leo Yang
@license: none
@contact: yangliw3@foxmail.com
@site:
@software:PyCharm
@file:django_init.py
@time(UTC+8):16/11/10-21:43
'''

import os

# 为了使用django的数据库模块
# 导入python 环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_practice.settings")
import django
django.setup()