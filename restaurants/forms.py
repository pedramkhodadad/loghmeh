
from django import forms
from .models import Restaurant


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
