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
    url(r"template/", views.template,),
    url(r"userinfo/", views.userinfo,),
    url(r"assets/", views.assets,),

    url(r"ajax_demo_register/", views.ajax_demo_register,),
    url(r"ajax_demo_login/", views.ajax_demo_login,),
    url(r"jd_main_page/", views.jd_main_page,),

    # default page
    url(r"^$", views.index,),


]
