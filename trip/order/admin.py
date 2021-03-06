from django.contrib import admin

# Register your models here.
from order import models
from utils import actions


@admin.register(models.Order)
class profileAdmin(admin.ModelAdmin):
    list_display = (
        'sn', 'user', 'buy_count', 'buy_amount', 'to_user', 'to_phone', 'to_area', 'to_address', 'remark', 'express_no',
        'status', 'types', 'created_at', 'is_valid')  # 显示字段
    list_per_page = 15  # 分页大小，默认100
    search_fields = ('sn', 'user')
    list_filter = ('status', 'types')

    admin.site.disable_action('delete_selected')
