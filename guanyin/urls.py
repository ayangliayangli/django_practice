#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
@version:
@author: leo Yang
@license: none
@contact: yangliw3@foxmail.com
@site:
@software:PyCharm
@file:urls.py
@time(UTC+8):16/7/29-12:28
'''

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"index/", views.index, name="index"),
    url(r"session_register/", views.session_register, name="session_register"),
    url(r"session_login/", views.session_login, name="session_login"),
    url(r"logout/", views.logout, name="logout"),
    url(r"get_check_code/", views.get_check_code, name="get_check_code"),
    url(r"del_host_relationship_via_hostid/", views.del_host_relationship_via_hostid, name="del_host_relationship_via_hostid"),
    url(r"add_host/", views.add_host, name="add_host"),
    url(r"show_mylog/", views.show_mylog, name="show_mylog"),
    url(r"resume_yangli/", views.resume_yangli, name="resume_yangli"),
    url(r"my_center/", views.my_center, name="my_center"),
    # url(r"main/", views.main, name="main"),

]
