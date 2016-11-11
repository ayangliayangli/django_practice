#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
@version:
@author: leo Yang
@license: none
@contact: yangliw3@foxmail.com
@site:
@software:PyCharm
@file:start.py
@time(UTC+8):16/10/2-21:24
'''


import os, sys

# append project path to sys.path
PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(PROJECT_PATH)

# append project path to sys.path
PROJECT_PATH_PAR = os.path.dirname(PROJECT_PATH)
sys.path.append(PROJECT_PATH_PAR)

# 为了使用django的数据库模块
# 导入python 环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_practice.settings")
import django
django.setup()


from src import core
core.main()