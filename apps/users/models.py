from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]

    email = models.EmailField(unique=True, verbose_name='Email')
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Role',
    )

    def __str__(self):
        return f"User: {self.username} (role: {self.role}) {self.email}"
