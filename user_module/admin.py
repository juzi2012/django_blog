from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile
# Register your models here.

# 下面一系列操作就是将Profile字段添加到后台user的显示
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines=(ProfileInline,)
    list_display=('username', 'email', 'first_name', 'last_name','nickname', 'is_staff')
    def nickname(self,obj):
        return obj.profile.nickname;
    nickname.short_description="昵称"

admin.site.unregister(User)
admin.site.register(User,UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    display_list=('user','nickname')
