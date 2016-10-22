# 概述

        使用django提供的友好强大的web框架,开发的一个模拟京东用户登录和注册的过程,整个系统是和数据库联动的
        该项目尽可能多的包含了框架当中的知识点,详见 【功能亮点】 小结

# 实现功能
        用户登录
        用户注册
        用户展示
        定制admin提供的后台管理

# 功能亮点

* 使用`sqlite数据库`存储用户数据
* 使用模板技术,使用`母版继承`,简化前段页面开发
* 路由系统使用了`路由分发`技术,让每个APP相对独立
* 前端使用自己写的`jquery扩展`实现前端验证
* 使用`ajax技术`后台验证数据正确性, location.href 跳转
* jd主页沿用了之前写的

# 难点

* 前端验证和后端验证的顺序问题
        
        因为之前前端验证是写在jquery的,切绑定的是submit的按钮,导致前段验证通过后,即使后段验证失败,也会跳转到一个新的页面
        解决办法：把submit换成button,那么form将永远不会跳转,知道前段后段都验证通过后,ajax函数里面触发 location.href 跳转
* 其他

# todu

* 主页可以直接访问（绕过登录）,因为还在研究session 和 cookie , 暂时不能记住用户登录状态