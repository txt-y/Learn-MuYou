from django.urls import path
from . import views

app_name = 'sight'

urlpatterns = [
    path('sight/list/', views.SightListView.as_view(), name='sight_list'),

    path('sight/detail/<int:pk>', views.SightDetailView.as_view(), name='sight_derail'),
    path('comment/list/<int:pk>', views.SightCommentListView.as_view(), name='sight_comment_list'),
    path('ticket/list/<int:pk>', views.SightTicketListView.as_view(), name='sight_ticket_list'),
    path('sight/info/<int:pk>', views.SightInfoDetailView.as_view(), name='sight_sight_info'),
    path('image/list/<int:pk>',views.SightImageListView.as_view(), name='sight_image_list'),
    path('ticket/detail/<int:pk>', views.TicketDetailView.as_view(), name='ticket_detail'),
]
