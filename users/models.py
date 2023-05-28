from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDERS = [
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'I am not a human'),
    ]
    image = models.ImageField(upload_to='users_image', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDERS, default='m')
    birthday = models.DateField(default='1900-01-01')
