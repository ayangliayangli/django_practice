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
    url(r"session_login/", views.session_login, name="session_login"),
    url(r"session_logout/", views.session_logout, name="session_logout"),
    url(r"session_register/", views.session_register, name="session_register"),
    url(r"index/", views.index, name="index"),
    url(r"show_user_types/", views.show_user_types, name="show_user_types"),



    url(r"add_user_type/", views.add_user_type, name="add_user_type"),

    # default page
    # url(r"^$", views.index,),


]
