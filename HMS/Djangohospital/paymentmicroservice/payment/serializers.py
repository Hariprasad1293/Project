from .models import PaymentStatus
from rest_framework import serializers

class PaymentSerializers(serializers.ModelSerializer):
    class Meta:
        model = PaymentStatus
        fields = '__all__'