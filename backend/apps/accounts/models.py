from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ("DEFENCE_PERSONNEL", "Defence Personnel"),
        ("FAMILY", "Family Member"),
        ("VETERAN", "Veteran"),
        ("CERT_OFFICER", "CERT Officer"),
        ("ADMIN", "Admin"),
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username