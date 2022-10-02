from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Patient(AbstractUser):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    mobile = models.CharField(max_length=12)
    password = models.CharField(max_length=300)
    address = models.CharField(max_length=200)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []