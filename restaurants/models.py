from django.conf import settings
from django.db import models


class Restaurant(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='restaurants',
        verbose_name='صاحب رستوران'
    )

    name = models.CharField(max_length=150, verbose_name='نام رستوران')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    address = models.TextField(verbose_name='آدرس')
    phone = models.CharField(max_length=20, verbose_name='شماره تماس')
    image = models.ImageField(
        upload_to='restaurants/',
        blank=True,
        null=True,
        verbose_name='تصویر رستوران'
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Food(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='foods',
        verbose_name='رستوران'
    )

    name = models.CharField(max_length=150, verbose_name='نام غذا')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='قیمت'
    )
    image = models.ImageField(
        upload_to='foods/',
        blank=True,
        null=True,
        verbose_name='تصویر غذا'
    )

    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name