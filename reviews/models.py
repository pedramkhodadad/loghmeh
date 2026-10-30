from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from restaurants.models import Food


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'food'],
                name='unique_review_per_user_food'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.food}'
    