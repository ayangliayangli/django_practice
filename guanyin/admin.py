from django.contrib import admin

# Register your models here.

from . import models


class HostGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", )
    list_editable = ("name", )
    list_filter = ("name", )
    search_fields = ("name", )


class HostAdmin(admin.ModelAdmin):
    list_display = ("id", "hostname", "ip", "port", "host_user_name", "host_password", "host_group", )
    list_editable = ("hostname", "host_group")
    list_filter = ("hostname", "host_group__name")
    search_fields = ("hostname", "host_group__name")


class UserGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    list_editable = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password", "user_group", "email", "phone", "avatar_path", )
    list_editable = ("user_group", )
    list_filter = ("username", "user_group")
    search_fields = ("username", "user_group__name", "hosts__hostname")

admin.site.register(models.HostGroup, HostGroupAdmin)
admin.site.register(models.Host, HostAdmin)
admin.site.register(models.UserGroup, UserGroupAdmin)
admin.site.register(models.User, UserAdmin)
