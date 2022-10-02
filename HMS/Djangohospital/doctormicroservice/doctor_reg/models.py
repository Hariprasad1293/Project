from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Doctor(AbstractUser):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    speciality = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    mobile = models.CharField(max_length=12)
    address = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
