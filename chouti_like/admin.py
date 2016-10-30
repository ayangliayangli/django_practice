from django.contrib import admin
from chouti_like import models

# Register your models here.


class UserTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "caption")
    list_filter = ("caption",)
    search_fields = ("caption",)


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password", "email", "phone", "user_type_id", "ctime", "mtime", )
    list_filter = ("username", "password", "email", "phone", "user_type_id", )
    search_fields = ("username", "phone", "user_type_id__caption")

class HobbyAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "desc", )
    list_filter = ("title", "desc", )
    search_fields = ("title", )

admin.site.register(models.UserType, UserTypeAdmin)
admin.site.register(models.UserInfo, UserInfoAdmin)
admin.site.register(models.Hobby, HobbyAdmin)
