from .models import BookAppointment
from rest_framework import serializers

class AppointmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = BookAppointment
        fields = '__all__'