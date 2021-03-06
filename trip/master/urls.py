from django.urls import path

from master import views

urlpatterns = [
    # path('slider/list/', views.slider_list, name='slider_list'),
    path('test/', views.test, name='test'),
    path('', views.index, name='index'),
]
