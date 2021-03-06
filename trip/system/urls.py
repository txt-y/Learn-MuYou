from django.urls import path

from system import views

urlpatterns = [
    path('slider/list/', views.slider_list, name='slider_list'),
    path('send/sms/', views.send_sms.as_view(), name='send_sms'),
]
