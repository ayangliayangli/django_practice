# 功能概要

## web控制台

* 用户
    * 注册用户
    * 登录用户
* 主机管理
    * 显示当前用户所有的主机
        * 分页显示
        * 按照主机所属组过滤
    * 删除当前用户的一个主机
    * 为当前用户新建一个主机
* 日志
    * 查看当前用户日志
    * 清空当前用户日志

## terminal

* 使用web端新建的用户登录
* 选择一个主机登录
* 在模拟终端里面进行操作

# 技术亮点

## web控制台

* frontend
    * html
    * css
    * js
    * jquery
    * ajax -- FormData
    * bootstrap
    * echars[baidu open source]
* backend
    * django
        * Form 验证
        * private key 文件的处理
        * 用户头像的处理
    * python
        * 配置文件处理
        * 公共lib库的处理

## terminal


# 修复优化日志


## 11月5日

* 技术选型 django + bootstrap + echars3
* 新增---基本框架 实现

## 11月6日
* 新增 -- index 页面静态数据
* 新增 -- 注册页面

## 11月7日

* 新增 -- index页面动态数据
* 优化 -- 注册界面

## 11月8日

* 新增 -- 登录界面

## 11月9日

* 新增 -- 增加主机,界面 动态
* 新增 -- index页面分页显示


## 11月10日

* console 端调通,基于堡垒机修改,使用django的ORM模块


# todo

-[x] 新增主机
-[x] 注册
-[x] 登录
-[ ] index 按照主机组进行过滤
-[ ] 查看自己的操作日志


