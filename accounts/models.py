from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        CUSTOMER = 'customer', 'مشتری'
        OWNER = 'owner', 'صاحب رستوران'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER
    )

    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username