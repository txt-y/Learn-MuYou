from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('ticket/submit/', views.TicketOrderSubmitView.as_view(), name="ticket_submit"),
    path('order/detail/<int:sn>', views.OrderDetailView.as_view(), name="order_detail"),
    path('order/list/', views.OrderListView.as_view(), name='order_list'),
    path('order/profile/<int:sn>', views.OrderProfileView.as_view(), name="order_profile"),
]
