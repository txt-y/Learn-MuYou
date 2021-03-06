import json

from django import http
from django.db import transaction
from django.db.models import F, Q
from django.shortcuts import render

from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView
from django.views.generic.detail import BaseDetailView

from order import serializers
from order.choices import OrderStatus
from order.forms import SubmitTicketOrderForm
from order.models import Order
from sight.models import Ticket
from utils.response import BadRequestJsonResponse, NotFoundJsonResponse
from utils.views import login_required


@method_decorator(login_required, name='dispatch')  # 类装饰器 登录验证
class TicketOrderSubmitView(FormView):
    # 验证用户是否已登录
    # 数据验证(门票ID，库存)
    # 关联用户，生成订单号，计算价格，生成订单
    # 返回内容：订单ID
    form_class = SubmitTicketOrderForm
    http_method_names = ['post']

    def form_valid(self, form):
        obj = form.save(user=self.request.user)
        return http.JsonResponse({
            'sn': obj.sn
        }, status=201)

    def form_invalid(self, form):
        err = json.loads(form.errors.as_json())
        return BadRequestJsonResponse(err)


@method_decorator(login_required, name='dispatch')  # 类装饰器 登录验证
class OrderDetailView(BaseDetailView):
    slug_field = 'sn'
    slug_url_kwarg = 'sn'

    def get_queryset(self):  # 获取用户的订单列表
        user = self.request.user
        return Order.objects.filter(user=user, is_valid=True)

    def get(self, request, *args, **kwargs):
        """GET订单详情"""
        order_obj = self.get_object()  # get_object会从get_queryset中找到对应的sn返回
        data = serializers.OredeDetailSerializer(order_obj).to_dict()
        return http.JsonResponse(data)

    @transaction.atomic  # 事务控制
    def post(self, request, *args, **kwargs):
        """POST订单支付"""
        # TODO选择支付方式
        order_obj = self.get_object()
        # 数据验证，状态判断
        if order_obj.status == OrderStatus.SUBMIT:
            # TODO调用支付接口
            # 改变订单状态
            order_obj.status = OrderStatus.PAID
            order_obj.save()
            order_obj.order_items.update(status=OrderStatus.PAID)  # 批量更新
            return http.JsonResponse({'msg': '支付成功'}, status=201)
        return http.JsonResponse({'msg': '支付失败'}, status=200)

    @transaction.atomic  # 事务控制
    def put(self, request, *args, **kwargs):
        """PUT取消订单"""
        # 获取订单对象
        order_obj = self.get_object()
        # 数据验证，状态判断
        if order_obj.status == OrderStatus.SUBMIT:
            # 改变状态
            order_obj.status = OrderStatus.CANCELED
            order_obj.save()
            # 回退库存
            items = order_obj.order_items.filter(status=OrderStatus.SUBMIT)  # 查询订单中商品状态为未支付的
            for i in items:  # 循环商品，复合关联门票表，回退库存
                obj = i.content_object
                obj.remain_stock = F('remain_stock') + i.count
                obj.save()
            items.update(status=OrderStatus.CANCELED)  # 批量更新商品状态
            return http.JsonResponse({'msg': '取消成功'}, status=201)
        return http.JsonResponse({'msg': '取消失败'}, status=200)

    @transaction.atomic  # 事务控制
    def delete(self, request, *args, **kwargs):
        """DELETE订单删除"""
        # 获取订单对象
        order_obj = self.get_object()
        # 数据验证，状态判断
        if order_obj.status != OrderStatus.SUBMIT and order_obj.is_valid:
            order_obj.is_valid = False
            order_obj.save()
            order_obj.order_items.update(is_valid=False)  # 批量更新
            return http.JsonResponse({'msg': '删除成功'}, status=201)
        return http.JsonResponse({'msg': '删除失败'}, status=200)


@method_decorator(login_required, name='dispatch')  # 类装饰器 登录验证
class OrderListView(ListView):
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        query = Q(is_valid=True, user=user)
        status = self.request.GET.get('status', 0)
        if status and status != '0':
            query = query & Q(status=status)
        return Order.objects.filter(query)

    def get_paginate_by(self, queryset):
        return self.request.GET.get('limit', self.paginate_by)

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['page_obj']
        if page_obj is not None:
            data = serializers.OrderListSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()


@method_decorator(login_required, name='dispatch')  # 类装饰器 登录验证
class OrderProfileView(BaseDetailView):
    slug_field = 'sn'
    slug_url_kwarg = 'sn'

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(is_valid=True, user=user)

    def get(self, request, *args, **kwargs):
        order_obj = self.get_object()
        data = serializers.OredeProfileSerializer(order_obj).to_dict()
        return http.JsonResponse(data)
