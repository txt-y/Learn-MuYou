from django.contrib import admin

# Register your models here.
from sight import models
from utils import actions


@admin.register(models.Sight)
class SightAdmin(admin.ModelAdmin):
    list_per_page = 15  # 分页大小，默认100
    list_display = (
        'name', 'desc', 'score', 'province', 'city', 'area', 'town', 'min_price',
        'updated_at', 'created_at', 'is_valid')
    search_fields = ('name', 'desc')
    list_filter = ('is_top', 'is_hot')

    actions = (actions.set_invalid, actions.set_valid)

    def save_form(self, request, form, change):  # 重写保存方法，缓存景点
        obj = super().save_form(request, form, change)
        return obj


@admin.register(models.Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ('sight', 'entry_explain', 'play_way', 'tips', 'traffic')
    list_per_page = 15  # 分页大小，默认100
    search_fields = ('sight__name',)


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'sight', 'content', 'score', 'is_top', 'love_count', 'is_valid')
    list_per_page = 15  # 分页大小，默认100
    search_fields = ('user__username',)
    list_filter = ('sight',)

    actions = (actions.set_invalid, actions.set_valid)


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('sight', 'name', 'type', 'price', 'discount', 'total_stock', 'remain_stock', 'is_valid')
    list_per_page = 15  # 分页大小，默认100

    actions = (actions.set_invalid, actions.set_valid)
