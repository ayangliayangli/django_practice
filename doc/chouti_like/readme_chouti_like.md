# 项目概述

# 功能

* 注册用户 带验证
* 登录 带验证 验证码 头像 等信息
* 分页
* 显示所有的用户类型
* 显示所有的用户,并且对用户做 增删改 的操作


# 知识点

* 前端
    * jquery
    * 延迟绑定事件 $().delegate(sub, type, func)
    * possition:fixed
    * float:right
    
* 后端
    * 路由系统
        * 一般路由
        * 动态路由
        * 路由分发,该project有多个APP
    * 模板
        * 模板继承
        * 模板include
        * 模板流程控制 for if 
        * 模板取值
    * models
        * models.ForeignKey
    * views
        * url复用,通过post get 区分
    * 登录利用django.forms 在后端做基本的验证
        * errors_message
        * validators = []
        * widget=forms.Select(choices=c)
    * 注册界面使用ajax(jquery版本)做后端基本验证
    * 登录界面使用Form自动生成的前端代码
    * session
        * 使用session来保持用户的登录状态
        * 删除服务器端的session
        * 验证码功能
        
    * 文件操作
        * 上传大头贴,上传之后同时显示到当前页面 ajax

# TODO

-[x] 注册数据验证
-[x] 注销
-[x] admin 界面定制
-[x] 优化注册的时候不能显示新加的用户类型
-[x] 登录页面
-[x] 优化【注册|登录】页面的提示信息, 故意只优化了一部分
-[x] 新增手机号的验证,自定义一个validators
-[x] 注册,验证码后端逻辑
-[x] 新增一个个人中心页面,展示自己的个人数据
-[x] 增加一个用户管理界面,对所有用户进行增删改查

# 调试优化信息
* 20161028 【修复】 不上传大头贴的时候,服务器内部错误
* 20161028 【修复】 手机号验证逻辑错误
* ... 



# 作者信息

* [github](https://github.com/yangllsdev/)
* [cnblogs](http://www.cnblogs.com/onemore/)
* name:  杨力（ Tim Yang ）
* phone: 185 658 66568
* email: yangliw3@foxmail.com