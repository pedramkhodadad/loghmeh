from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from restaurants.models import Restaurant


class Discount(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='discounts'
    )

    code = models.CharField(max_length=50)
    percentage = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    # حداقل مبلغ سفارش برای استفاده از تخفیف
    min_order_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    # حداکثر تعداد دفعات استفاده از کد تخفیف
    max_uses = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)]
    )

    # تعداد دفعات استفاده‌شده از کد تخفیف
    used_count = models.PositiveIntegerField(default=0)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['restaurant', 'code'],
                name='unique_discount_code_per_restaurant'
            )
        ]

    def __str__(self):
        return self.code