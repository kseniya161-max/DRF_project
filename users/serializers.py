from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Payments, User


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class UserAPIView(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


