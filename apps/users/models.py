from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the User model, providing methods to create
    superusers and regular users with specific roles.

    Methods:
        create_superuser(username, email, password, **extra_fields):
            Creates and returns a superuser with the specified credentials.

        create_user(username, email, password, **extra_fields):
            Creates and returns a regular user with the specified credentials.

        _create_user(username, email, password, **extra_fields):
            Helper method to create and save a user with the given credentials.
       """

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Creates and returns a superuser with the 'admin' role and appropriate flags.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self._create_user(username, email, password, **extra_fields)

    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Creates and returns a regular user with the 'user' role.
        """

        extra_fields.setdefault('role', 'user')
        return self._create_user(username, email, password, **extra_fields)

    def _create_user(self, username, email, password, **extra_fields):
        """
        Helper method to create and save a user with the given credentials.
        Validates the email and sets the password before saving the user to the database.

        Raises:
            ValueError: If the email is not provided.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    Custom user model extending AbstractUser to include additional fields
    for email and role, and to allow user management with a custom manager.

    Attributes:
        email (EmailField): The user's unique email address.
        role (CharField): The role of the user (admin or user).
    """

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

    objects = CustomUserManager()

    def __str__(self):
        return f"User: {self.username} (role: {self.role}) {self.email}"
