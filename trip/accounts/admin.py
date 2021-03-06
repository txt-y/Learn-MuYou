from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from utils import actions

from accounts.forms import ProfileEditForm
from accounts import models


@admin.register(models.User)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'nickname', 'is_active', 'is_staff', 'date_joined')  # 显示字段
    search_fields = ('username', 'nickname')  # 搜索字段
    # add_fieldsets = (  # 新增的表单
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'password1', 'password2', 'nickname'),
    #     }),
    # )
    add_fieldsets = UserAdmin.add_fieldsets + (  # 新增的表单
        (None, {'fields': ('nickname',)}),
    )
    # fieldsets = (  # 修改的表单
    #     (None, {'fields': ('username', 'password')}),
    #     (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
    #     (_('Permissions'), {
    #         'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
    #     }),
    #     (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    # )
    fieldsets = UserAdmin.fieldsets + (  # 修改的表单
        (None, {'fields': ('nickname', 'avatar')}),
    )

    actions = (actions.set_invalid, actions.set_valid)


@admin.register(models.Profile)
class profileAdmin(admin.ModelAdmin):
    list_display = ('format_username', 'sex', 'age', 'created_at')  # 显示字段
    list_per_page = 15  # 分页大小，默认100
    list_select_related = ('user',)  # 外键关联一并查出
    list_filter = ('sex',)  # 快捷搜索
    search_fields = ('username', 'user__nickname')  # 关联搜索 双下划线跨表关联搜索
    exclude = ('user',)  # 排除的字段
    form = ProfileEditForm  # 表单，可自定义表单验证

    def format_username(self, obj):  # 格式化字段内容
        return obj.username[:3] + '***' + obj.username[-4:]

    format_username.short_description = '用户名'  # 修改显示的字段名字
