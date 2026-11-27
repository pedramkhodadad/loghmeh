
from django import forms
from .models import Discount
from restaurants.models import Restaurant
from django.utils import timezone


class DiscountForm(forms.ModelForm):

    class Meta:
        model = Discount

        fields = [
            'restaurant',
            'code',
            'percentage',
            'start_date',
            'end_date',
            'min_order_amount',
            'max_uses',
        ]

        labels = {
            'restaurant': 'رستوران',
            'code': 'کد تخفیف',
            'percentage': 'درصد تخفیف',
            'start_date': 'تاریخ شروع',
            'end_date': 'تاریخ پایان',
            'min_order_amount': 'حداقل مبلغ سفارش',
            'max_uses': 'حداکثر تعداد استفاده',
        }

        widgets = {
            'start_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),

            'end_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'min_order_amount': forms.NumberInput(
                attrs={
                    'min': '0',
                    'step': '1000'
                }
            ),

            'max_uses': forms.NumberInput(
                attrs={
                    'min': '1',
                    'placeholder': 'خالی = نامحدود'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        super().__init__(*args, **kwargs)

        self.fields['restaurant'].queryset = Restaurant.objects.filter(
            owner=self.user
        )

        self.fields['start_date'].input_formats = [
            '%Y-%m-%dT%H:%M'
        ]

        self.fields['end_date'].input_formats = [
            '%Y-%m-%dT%H:%M'
        ]

    def clean_code(self):
        code = self.cleaned_data['code']
        return code.strip().upper()

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:

            if start_date >= end_date:
                raise forms.ValidationError(
                    'تاریخ پایان باید بعد از تاریخ شروع باشد.'
                )

        return cleaned_data
