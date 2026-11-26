from django.contrib import admin
from .models import Restaurant, Food


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'address', 'phone')


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'is_available')
    list_filter = ('is_available', 'restaurant')
    search_fields = ('name', 'restaurant__name')
