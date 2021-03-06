import json

from django import http
from django.contrib.auth import logout
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import FormView

from accounts.forms import LoginForm, RegisterForm
from accounts import serializers
from utils.response import *


class user_api_login(View):
    http_method_names = ['post']

    def post(self, request):
        form = LoginForm(request.POST)
        # 如果通过验证，执行登录
        if form.is_valid():
            user = form.do_logon(request)
            # 返回用户信息
            profile = user.profile  # 外键反向引用
            data = {
                'user': serializers.UserSerializer(user).to_dict(),
                'profile': serializers.UserProfileSerializer(profile).to_dict()
            }
            return http.JsonResponse(data)
        else:
            # 没通过，返回表单错误信息
            err = json.loads(form.errors.as_json())
            return BadRequestJsonResponse(err)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return MethodNotAllowedJsonResponse()


class user_api_logout(View):
    http_method_names = ['get']

    def get(self, request):
        logout(request)
        return http.HttpResponse(status=201)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return MethodNotAllowedJsonResponse()


class user_api_info(View):
    http_method_names = ['get']

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            profile = user.profile  # 外键反向引用
            data = {
                'user': serializers.UserSerializer(user).to_dict(),
                'profile': serializers.UserProfileSerializer(profile).to_dict()
            }
            return http.JsonResponse(data)
        return UnauthorizedJsonResponse()

    def http_method_not_allowed(self, request, *args, **kwargs):
        return MethodNotAllowedJsonResponse()


class user_api_register(FormView):
    http_method_names = ['post']
    form_class = RegisterForm

    def form_valid(self, form):  # 通过的
        data = form.do_register(request=self.request)
        if data is not None:
            user, profile = data
            data = {
                'user': serializers.UserSerializer(user).to_dict(),
                'profile': serializers.UserProfileSerializer(profile).to_dict()
            }
            return http.JsonResponse(data, status=201)
        return ServerErrorJsonResponse()

    def form_invalid(self, form):  # 没通过的
        err_list = json.loads(form.errors.as_json())
        return BadRequestJsonResponse(err_list)
