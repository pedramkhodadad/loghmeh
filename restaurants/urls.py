
from django.urls import path
from . import views


app_name = 'restaurants'


urlpatterns = [

    path(
        '',
        views.restaurant_list,
        name='restaurant_list'
    ),

    path(
        'create/',
        views.restaurant_create,
        name='restaurant_create'
    ),

    path(
        '<int:pk>/',
        views.restaurant_detail,
        name='restaurant_detail'
    ),

    path(
        '<int:pk>/edit/',
        views.restaurant_update,
        name='restaurant_update'
    ),

    path(
        '<int:pk>/delete/',
        views.restaurant_delete,
        name='restaurant_delete'
    ),

]
