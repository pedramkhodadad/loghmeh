
from django import forms
from .models import Restaurant
from .models import Food
import re
from django.core.exceptions import ValidationError
class RestaurantForm(forms.ModelForm):

    class Meta:
        model = Restaurant

        fields = [
            'name',
            'description',
            'address',
            'phone',
            'image',
        ]

        labels = {
            'name': 'نام رستوران',
            'description': 'توضیحات',
            'address': 'آدرس',
            'phone': 'شماره تماس',
            'image': 'تصویر رستوران',
        }

        widgets = {
            'description': forms.Textarea(
                attrs={'rows': 4}
            ),

            'address': forms.Textarea(
                attrs={'rows': 3}
            ),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip().replace(' ', '').replace('-', '')
        if not re.fullmatch(r'(0\d{10}|\+98\d{10})', phone):
            raise ValidationError('شماره تماس معتبر نیست (مثال: 09123456789 یا 02112345678).')
        return phone



class FoodForm(forms.ModelForm):

    class Meta:
        model = Food

        fields = [
            'name',
            'description',
            'price',
            'image',
            'is_available',
            'is_active'
        ]

        labels = {
            'name': 'نام غذا',
            'description': 'توضیحات غذا',
            'price': 'قیمت',
            'image': 'تصویر غذا',
            'is_available': 'موجود بودن غذا',
        }