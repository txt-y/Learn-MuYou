from django.urls import path

from accounts import views

urlpatterns = [
    # path('user/login/', views.user_login, name='login'),
    # path('user/logout/', views.user_logout, name='logout'),

    path('user/api/login/', views.user_api_login.as_view(), name='user_api_login'),
    path('user/api/logout/', views.user_api_logout.as_view(), name='user_api_logout'),
    path('user/api/register/', views.user_api_register.as_view(), name='user_api_register'),
    path('user/api/info/', views.user_api_info.as_view(), name='user_api_info'),
]
