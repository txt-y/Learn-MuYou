import json

from django.shortcuts import render
from django import http

# Create your views here.
from django.views.generic import FormView

from system.forms import SendSmsCodeForm
from system.models import Slider
from utils.response import ServerErrorJsonResponse, BadRequestJsonResponse


def slider_list(request):
    data = {
        'meta': {},
        'objects': []
    }
    queryset = Slider.objects.filter(is_valid=True)
    # types = request.GET.get('typrs', None)
    # if types:
    #     queryset=queryset.filter(typrs=types)
    for item in queryset:
        data['objects'].append({
            'id': item.id,
            'name': item.name,
            'img_url': item.img.url,
            'target_url': item.target_url
        })
    return http.JsonResponse(data)


class send_sms(FormView):
    http_method_names = ['post']
    form_class = SendSmsCodeForm

    def form_valid(self, form):  # 通过的
        data = form.send_sms_code()
        if data is not None:
            return http.JsonResponse(data, status=201)
        return ServerErrorJsonResponse()

    def form_invalid(self, form):  # 没通过的
        err_list = json.loads(form.errors.as_json())
        return BadRequestJsonResponse(err_list)
