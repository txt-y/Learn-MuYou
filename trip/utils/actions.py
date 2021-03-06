from django.contrib import messages


def set_invalid(modeladmin, request, queryset):
    queryset.update(is_valid=False)
    messages.success(request, '禁用操作成功')


set_invalid.short_description = '批量禁用操作'  # 显示中文名


def set_valid(modeladmin, request, queryset):
    queryset.update(is_valid=True)
    messages.success(request, '启用操作成功')


set_valid.short_description = '批量启用操作'  # 显示中文名
