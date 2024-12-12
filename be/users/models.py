from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username