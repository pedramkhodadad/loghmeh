
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [

    path(
        '<int:order_id>/',
        views.restaurant_order_detail,
        name='restaurant_order_detail'
    ),
    path(
        '',
        views.restaurant_order_list,
        name='restaurant_order_list'
    ),

]
