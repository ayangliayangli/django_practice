# 项目概述

# 功能



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
    * 利用django.forms 在后端做基本的验证
        * errors_message
        * validators = []
        * widget=forms.Select(choices=c)
    * session
        * 使用session来保持用户的登录状态
        * 删除服务器端的session

# tudo

-[x] 注册数据验证
-[x] 注销
-[x] admin 界面定制
-[x] 优化注册的时候不能显示新加的用户类型
-[ ] 登录页面
-[ ] 优化注册页面的提示信息
-[ ] 新增手机号的验证,自定义一个validators


# 作者信息