from django.db import models

# Create your models here.
class PaymentStatus(models.Model):
    email = models.CharField(max_length=50)
    demail = models.CharField(max_length=50)
    speciality = models.CharField(max_length=50)
    appointment_date = models.CharField(max_length=200)
    appointment_time = models.CharField(max_length=200)
    mode_of_payment = models.CharField(max_length=50)
    mobile = models.CharField(max_length=12)
    status = models.CharField(max_length=15)