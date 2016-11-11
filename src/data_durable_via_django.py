#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
@version:
@author: leo Yang
@license: none
@contact: yangliw3@foxmail.com
@site:
@software:PyCharm
@file:data_durable_via_mysql.py
@time(UTC+8):16/10/2-08:35
'''

import time
from lib import django_init  # init django environment in order to use django ORM
from guanyin import models


def select_host_with_user(username):
    hosts = models.Host.objects.filter(user__username=username)
    hosts_list = []
    for host in hosts:
        hosts_list.append(host)

    for index,item in enumerate(hosts_list, 1):
        print("[",index,"]", item)

    # 获取用户的输入
    while True:
        inp = input("which one do you want to connect:")
        if inp.isnumeric():
            break
        elif inp == "":
            continue
        else:
            print("just input index, is a number")
            continue

    sel_host_id = hosts_list[int(inp) - 1].id
    ret = sel_host_id
    return ret


def login(username,password):
    user_obj = models.User.objects.filter(username=username, password=password)
    if user_obj:
        # 登录成功
        return True
    else:
        return False


def make_record_via_mysql(content, blockhouseuser_id):

    user = models.User.objects.get(pk=blockhouseuser_id)
    models.Log.objects.create(user=user, content=content)
    print("----","start write record to mysql")




def main():
    # init_db()
    # drop_db()
    # add_host_group()
    # add_host_user()
    # add_host()
    # add_user()
    # print("return:", select_host_with_user("yangli","123456"))
    # show_record_via_username("yangli")
    pass

if __name__ == '__main__':
    main()