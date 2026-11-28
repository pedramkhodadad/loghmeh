# discounts/admin.py
from django.contrib import admin
from .models import Discount


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'restaurant', 'percentage', 'is_active', 'start_date', 'end_date', 'used_count', 'max_uses')
    list_filter = ('is_active', 'restaurant')
    search_fields = ('code',)