
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('owner/', views.restaurant_order_list, name='restaurant_order_list'),
    path('owner/<int:order_id>/', views.restaurant_order_detail, name='restaurant_order_detail'),
    path('owner/<int:order_id>/approve/', views.restaurant_order_approve, name='restaurant_order_approve'),
    path('owner/<int:order_id>/cancel/', views.restaurant_order_cancel, name='restaurant_order_cancel'),
    path('owner/<int:order_id>/send/', views.restaurant_order_send, name='restaurant_order_send'),
    path('owner/<int:order_id>/deliver/', views.restaurant_order_deliver, name='restaurant_order_deliver'),
]