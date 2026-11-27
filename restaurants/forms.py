
from django import forms
from .models import Restaurant
from .models import Food

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




class FoodForm(forms.ModelForm):

    class Meta:
        model = Food

        fields = [
            'name',
            'description',
            'price',
            'image',
            'is_available',
        ]

        labels = {
            'name': 'نام غذا',
            'description': 'توضیحات غذا',
            'price': 'قیمت',
            'image': 'تصویر غذا',
            'is_available': 'موجود بودن غذا',
        }