#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
@version:
@author: leo Yang
@license: none
@contact: yangliw3@foxmail.com
@site:
@software:PyCharm
@file:core.py
@time(UTC+8):16/10/2-08:35
'''

# 这里是把项目的目录导入
# 当把程序放到其他地方执行的时候, 项目目录不会默认加入 sys.path
# 此功能已经移动到  /bin/start.py
# import sys,os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from src import data_durable_via_django
from src import my_paramiko
from etc import setting
from guanyin import models

# global variable
logined_user = {"username":"", "password":""}


def cmd_help():
    s = """
    help information for you :
        conn : make a connection with specified host
        exit : exit blockhouse system
        help : help infomation
        more : want more , go to web console
        """
    print(s)


def login():
    if logined_user["username"]:
        print("{}, you have logined".format(logined_user["username"]))
    else:
        # 用户还没有登录
        print("you should login first")
        name = input("name:")
        password = input("password:")
        login_sussess_flag = data_durable_via_django.login(username=name,
                                                          password=password)
        if login_sussess_flag:
            logined_user["username"] = name
            logined_user["password"] = password
            print("[{}] welcome to blockhouse".format(logined_user["username"]))
            cmd_help()
        else:
            print("logined failure, check user and password")


def connect_host():

    user_id = models.User.objects.get(username=logined_user["username"]).id

    host_id = data_durable_via_django.select_host_with_user(logined_user["username"],)

    host = models.Host.objects.get(pk=host_id)
    ip = host.ip
    port = host.port
    username = host.host_user_name
    password = host.host_password
    print(type(ip), ip)
    print(type(port), port)
    print(type(username), username)
    print(type(password), password)

    # 这个方法天荒地老死循环,直到ctrl + c 退出那个tty
    my_paramiko.run(host=ip, port=port, username=username, password=password, blockhouseuser_id=user_id)


def main():
    login()
    # connect_host()
    while True:
        cmd = input("type ? for more >>").strip()
        if cmd == "help" or cmd == "?":
            cmd_help()
        elif cmd == "conn":
            connect_host()
        elif cmd == "exit":
            break
        elif cmd == "":
            continue
        else:
            cmd_help()


if __name__ == '__main__':
    main()