
from django.urls import path
from . import views


app_name = 'restaurants'


urlpatterns = [
    path(
    'my/',
    views.restaurant_owner_list,
    name='restaurant_owner_list'
    ),

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

    path(
        '<int:restaurant_id>/foods/',
        views.food_list,
        name='food_list'
    ),

    path(
        '<int:restaurant_id>/foods/add/',
        views.food_create,
        name='food_create'
    ),

    path(
        '<int:restaurant_id>/foods/<int:food_id>/edit/',
        views.food_update,
        name='food_update'
    ),

    path(
        '<int:restaurant_id>/foods/<int:food_id>/delete/',
        views.food_delete,
        name='food_delete'
    ),

    path(
        '<int:restaurant_id>/foods/<int:food_id>/toggle/',
        views.food_toggle_availability,
        name='food_toggle_availability'
    ),

]

