from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("cart/", views.cart_detail, name="cart"),
    path("cart/add/<int:food_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:food_id>/", views.cart_remove, name="cart_remove"),
    path("cart/update/<int:food_id>/", views.cart_update, name="cart_update"),
    path("orders/checkout/", views.checkout, name="checkout"),
    path("orders/my-orders/", views.my_orders, name="my_orders"),
]