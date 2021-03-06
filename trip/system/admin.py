from django.contrib import admin

# Register your models here.
from system import models
from utils import actions


@admin.register(models.Slider)
class sliderAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'desc', 'typrs', 'img', 'reorder', 'start_time', 'end_time', 'target_url', 'is_valid')  # 显示字段
    list_per_page = 15  # 分页大小，默认100

    actions = (actions.set_invalid, actions.set_valid)


@admin.register(models.ImageRelated)
class imageRelatedAdmin(admin.ModelAdmin):
    list_display = (
        'format_user', 'img', 'summary', 'content_type', 'object_id', 'created_at', 'updated_at', 'is_valid')  # 显示字段
    list_per_page = 15  # 分页大小，默认100

    actions = (actions.set_invalid, actions.set_valid)

    def format_user(self, obj):  # 格式化字段内容
        if not obj.user:
            return '景点图片'
        return obj.user

    format_user.short_description = '上传用户'
