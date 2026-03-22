import secrets
import string

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class AuthProvider(models.TextChoices):
        APPLE = "apple", "Apple"
        EMAIL = "email", "Email"
        ADMIN = "admin", "Admin"

    class Gender(models.TextChoices):
        UNDISCLOSED = "undisclosed", "Undisclosed"
        FEMALE = "female", "Female"
        MALE = "male", "Male"
        NON_BINARY = "non_binary", "Non-binary"

    class AgeGroup(models.TextChoices):
        TEENS = "10s", "10s"
        TWENTIES = "20s", "20s"
        THIRTIES = "30s", "30s"
        FORTIES = "40s", "40s"
        FIFTIES = "50s", "50s"
        SIXTIES_PLUS = "60s", "60s+"

    email = models.EmailField(blank=True, null=True, unique=True)
    public_handle = models.CharField(max_length=24, unique=True, blank=True)
    auth_provider = models.CharField(max_length=16, choices=AuthProvider.choices, default=AuthProvider.EMAIL)
    provider_subject = models.CharField(max_length=255, blank=True, null=True, unique=True)
    gender = models.CharField(max_length=16, choices=Gender.choices, default=Gender.UNDISCLOSED)
    country_code = models.CharField(max_length=2, default="KR")
    age_group = models.CharField(max_length=8, choices=AgeGroup.choices, default=AgeGroup.TWENTIES)
    bio = models.CharField(max_length=280, blank=True)

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = None
        if not self.public_handle:
            alphabet = string.ascii_lowercase + string.digits
            self.public_handle = "creator-" + "".join(secrets.choice(alphabet) for _ in range(8))
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.public_handle or self.username

