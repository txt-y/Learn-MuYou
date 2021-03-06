from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.shortcuts import render

from django.utils.timezone import now

from accounts.models import Profile, User
from order.choices import OrderStatus
from order.models import Order
from sight.models import Sight, Comment


def test(request):
    return render(request, 'master/test.html')


def get_data_count(start=None, end=None):  # 今天，昨天数据统计
    query = Q()
    if start:
        query = query & Q(created_at__gte=start)  # get >=
    if end:
        query = query & Q(created_at__lte=end)  # lte <=
    order_list = Order.objects.filter(is_valid=True, status=OrderStatus.PAID).filter(query)
    user_list = Profile.objects.select_related('user').filter(user__is_active=True).filter(query)
    return {
        'order_amount': order_list.aggregate(amount=Sum('buy_amount'))['amount'],  # 销售额
        'order_count': order_list.count(),  # 支付订单数
        'user_add_count': user_list.count(),  # 新增用户数
        # 下单用户数   取用户字段，去重，统计
        'order_user_count': order_list.values('user').distinct().count()
    }


def get_latest_order_stats(days=7):  # 最近几天数据统计
    now_time = now()
    date_array, amount_array, count_array = [], [], []
    for i in range(days, 0, -1):
        # 日期
        calc_time = now_time - timedelta(days=i)
        date_array.append(f'{calc_time.day}号')
        queryset = Order.objects.filter(is_valid=True, status=OrderStatus.PAID, created_at__date=calc_time.date())
        # 订单金额
        result = queryset.aggregate(amount=Sum('buy_amount'))
        # result = queryset.aggregate(amount=Sum('buy_amount'),count=Sum('buy_count'))
        amount_array.append(result['amount'] or 0)
        # 订单数量
        count_array.append(queryset.count())
        # count_array.append(len(queryset))
    return {
        'date': date_array,
        'amount': amount_array,
        'count': count_array
    }


@login_required(login_url='/admin/login/')  # 登录验证 使用自带的登录
def index(request):
    # 数据统计
    total_stats = {
        'sight_count': Sight.objects.filter(is_valid=True).count(),  # 景点总数
        'comment_count': Comment.objects.filter(is_valid=True).count(),  # 评价总数
        'user_count': User.objects.filter(is_active=True).count(),  # 用户总量
        'order_count': Order.objects.filter(is_valid=True, status=OrderStatus.PAID).count(),  # 订单总量
    }
    # 今日数据
    now_time = now()
    # print(now_time.strftime('%Y-%m-%d'))
    now_stats = get_data_count(start=datetime(now_time.year, now_time.month, now_time.day))
    # 昨日数据
    yesterday = now_time - timedelta(days=1)  # 获取昨天=今天-1
    yesterday_stats = get_data_count(
        start=datetime(yesterday.year, yesterday.month, yesterday.day),
        end=datetime(now_time.year, now_time.month, now_time.day)
    )
    # 数据走势
    latest_stats = get_latest_order_stats()
    return render(request, 'master/index.html', locals())
