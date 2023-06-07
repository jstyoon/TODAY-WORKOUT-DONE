from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.


class User(AbstractBaseUser):

    email = models.EmailField(
        max_length=50, unique=True, null=False, blank=False)
    password = models.CharField(max_length=200)
    avatar = models.ImageField(blank=True)
    bio = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
