from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Payments


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'

