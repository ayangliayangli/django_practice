from django.db import models
from django.utils.html import format_html

# Create your models here.


# 模仿京东页面需要的类
# 模拟用户注册,登录,购物车

class User(models.Model):
    username = models.CharField(max_length=32, unique=True,null=False)
    password = models.CharField(max_length=32)
    phone = models.CharField(max_length=16)

