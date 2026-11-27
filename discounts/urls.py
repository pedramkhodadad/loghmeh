
from django.urls import path
from . import views

app_name = 'discounts'

urlpatterns = [
    path('', views.discount_list, name='discount_list'),
    path('create/', views.discount_create, name='discount_create'),
    path('<int:pk>/edit/', views.discount_update, name='discount_update'),
    path('<int:pk>/toggle/', views.discount_toggle, name='discount_toggle'),
]
