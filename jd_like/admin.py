from django.contrib import admin
from . import models


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password", "phone")
    list_editable = ("username", "password", "phone")
    list_filter = ("username", "password", "phone")


admin.site.register(models.User, UserAdmin)
