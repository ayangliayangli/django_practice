from django.db import models

# Create your models here.


class HostGroup(models.Model):
    name = models.CharField(max_length=128,verbose_name="主机组" )

    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    class Meta():
        verbose_name = "主机组"
        # unique_together = ()

    def __str__(self):
        s = self.name
        return s


class Host(models.Model):
    hostname = models.CharField(max_length=32)
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    host_user_name = models.CharField(max_length=32)
    host_password = models.CharField(max_length=32)
    host_key_path = models.CharField(max_length=128, null=True, blank=True, )
    host_group = models.ForeignKey(HostGroup, null=True, blank=True, )

    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)


    class Meta():
        verbose_name = "主机"
        # unique_together = ()

    def __str__(self):
        s = self.hostname
        return s


class UserGroup(models.Model):
    name = models.CharField(max_length=128)

    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    class Meta():
        verbose_name = "用户组"
        # unique_together = ()

    def __str__(self):
        s = self.name
        return s


class User(models.Model):
    username = models.CharField(max_length=32, unique=True, null=False, blank=False, verbose_name="用户名")
    password = models.CharField(max_length=32, verbose_name="密码")
    email = models.EmailField(null=True, blank=True, verbose_name="邮箱")
    phone = models.CharField(max_length=32, null=True, blank=True, verbose_name="电话")
    avatar_path = models.CharField(max_length=128, null=True, blank=True, unique=True, verbose_name="头像路径" )

    user_group = models.ForeignKey(UserGroup, null=True, blank=True, verbose_name="属组")
    hosts = models.ManyToManyField(Host, null=True, blank=True, verbose_name="我的主机",)

    class Meta():
        verbose_name = "用户"
        # unique_together = ()

    def __str__(self):
        s = self.username
        return s


class Log(models.Model):
    ctime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    content = models.CharField(max_length=128)

    class Meta():
        verbose_name = "操作日志"
        # unique_together = ()

    def __str__(self):
        s = "[{}] {}".format(self.user, self.content)
        return s