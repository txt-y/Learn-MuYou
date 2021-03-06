from django import http
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator

from django.views.generic import ListView, DetailView
from django.core.cache import cache

from sight.models import Sight, Comment, Ticket, Info
from sight import serializers
from utils import constants
from utils.response import NotFoundJsonResponse
from utils.views import login_required


class SightListView(ListView):
    paginate_by = 5  # 每页5条数据

    def get_queryset(self):  # 重写查询方法
        query = Q(is_valid=True)
        is_hot = self.request.GET.get('is_hot', None)
        is_top = self.request.GET.get('is_top', None)
        name = self.request.GET.get('name', None)
        if is_hot:
            queryset = cache.get(constants.INDEX_SIGHT_HOT_KEY, None)
            if queryset:
                return queryset
            else:
                query = query & Q(is_hot=True)
                queryset = Sight.objects.filter(query)
                cache.set(constants.INDEX_SIGHT_HOT_KEY, queryset, timeout=constants.INDEX_SIGHT_TIMEOUT)
                return queryset
        if is_top:
            queryset = cache.get(constants.INDEX_SIGHT_TOP_KEY, None)
            if queryset:
                return queryset
            else:
                query = query & Q(is_top=True)
                queryset = Sight.objects.filter(query).order_by('-score')
                cache.set(constants.INDEX_SIGHT_TOP_KEY, queryset, timeout=constants.INDEX_SIGHT_TIMEOUT)
                return queryset
        if name:
            query = query & Q(name__icontains=name)
        queryset = Sight.objects.filter(query)
        return queryset

    def get_paginate_by(self, queryset):
        page_size = self.request.GET.get('limit', self.paginate_by)
        return page_size

    # 因返回不是JS数据，重写返回方法
    def render_to_response(self, context, **response_kwargs):
        page_obj = context['page_obj']  # 获取分页数据
        if page_obj is not None:
            data = serializers.SightListSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()
        # data = {
        #     'meta': {
        #         'total_count': page_obj.paginator.count,
        #         'page_count': page_obj.paginator.num_pages,
        #         'current_count': page_obj.number
        #     },
        #     'objects': []
        # }
        # # object_list里的数据不能直接JS返回,要处理过
        # for item in page_obj.object_list:
        #     data['objects'].append({
        #         'id': item.id,
        #         'name': item.name,
        #         'min_price': item.min_price,
        #         'main_img': item.main_img.url,
        #         'score': item.score,
        #         'province': item.province,
        #         'city': item.city,
        #         'comment_count': 1
        #     })
        # return http.JsonResponse(data)


class SightDetailView(DetailView):
    model = Sight

    # def get_queryset(self):
    #     return Sight.objects.all()

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['object']
        if page_obj is not None:
            if page_obj.is_valid == False:
                return NotFoundJsonResponse()
            data = serializers.SightDetailSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()


class SightCommentListView(ListView):
    paginate_by = 10

    def get_queryset(self):
        sight_id = self.kwargs.get('pk', None)
        return Comment.objects.filter(is_valid=True, sight__id=sight_id)

    def get_paginate_by(self, queryset):
        page_size = self.request.GET.get('limit', self.paginate_by)
        return page_size

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['page_obj']
        if page_obj is not None:
            data = serializers.SightCommentListSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()


class SightTicketListView(ListView):
    paginate_by = 10

    def get_queryset(self):
        sight_id = self.kwargs.get('pk', None)
        return Ticket.objects.filter(is_valid=True, sight__id=sight_id)

    def get_paginate_by(self, queryset):
        page_size = self.request.GET.get('limit', self.paginate_by)
        return page_size

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['page_obj']
        if page_obj is not None:
            data = serializers.SightTicketListSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()


class SightInfoDetailView(DetailView):
    model = Info
    slug_field = 'sight__id'

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['object']
        if page_obj is not None:
            if page_obj.is_valid == False:
                return NotFoundJsonResponse()
            data = serializers.SightInfoSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()


class SightImageListView(ListView):
    paginate_by = 10

    def get_queryset(self):
        sight_id = self.kwargs.get('pk', None)
        return Sight.objects.filter(is_valid=True, id=sight_id).first().images.filter(is_valid=True)

    def get_paginate_by(self, queryset):
        page_size = self.request.GET.get('limit', self.paginate_by)
        return page_size

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['page_obj']
        if page_obj is not None:
            data = serializers.SightImageListSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()


@method_decorator(login_required, name='dispatch')  # 类装饰器 登录验证
class TicketDetailView(DetailView):
    slug_url_kwarg = 'pk'
    model = Ticket

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['object']
        if page_obj is not None and page_obj.is_valid:
            data = serializers.TicketDetailSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()
