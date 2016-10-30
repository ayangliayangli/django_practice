from django.db import models

# Create your models here.


class UserType(models.Model):
    caption = models.CharField(max_length=32)

    def __str__(self):
        s = self.caption
        return s


class Hobby(models.Model):
    title = models.CharField(max_length=64)
    desc = models.TextField()

    def __str__(self):
        s = self.title
        return s


class UserInfo(models.Model):
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=16)
    phone = models.IntegerField(null=True,blank=True)
    email = models.EmailField()
    ctime = models.DateField(auto_now_add=True)  # create time
    mtime = models.DateField(auto_now=True)  # modified time

    user_type_id = models.ForeignKey(UserType, null=True, blank=True)  # foreign key
    hobby = models.ManyToManyField(Hobby, null=True, blank=True)  # manytomany key

    def __str__(self):
        s = self.username + "---" + self.password
        return s


