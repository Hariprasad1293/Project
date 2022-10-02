from random import choices
from django.db import models

# Create your models here.
class BookAppointment(models.Model):
    class Meta:
        unique_together = ('d_email', 'appointment_date', 'appointment_time')
    TIMESLOT_LIST = (
        (0, '09:00 - 09:30'),
        (1, '10:00 - 10:30'),
        (2, '11:00 - 11:30'),
        (3, '12:00 - 12:30'),
        (4, '13:00 - 13:30'),
        (5, '14:00 - 14:30'),
        (6, '15:00 - 15:30'),
        (7, '16:00 - 16:30'),
        (8, '17:00 - 17:30'),
    )
    TIMESLOT_LISTS = (
        ('9am', '9am'),
        ('10am', '10am'),
        ('11am', '11am'),
        ('12am', '12am'),
        ('5pm', '5pm'),
    )

    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    mobile = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    #doctor_fname = models.CharField(max_length=50)
    #doctor_lname = models.CharField(max_length=50)
    speciality = models.CharField(max_length=50)
    d_email = models.CharField(max_length=50)
    appointment_date = models.DateField(max_length=200)
    appointment_time = models.CharField(choices=TIMESLOT_LISTS, max_length=200)
    payment_status = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=20)
    appointment_status = models.CharField(max_length=50)

    def __str__(self):
        return '%s'%(self.id)
