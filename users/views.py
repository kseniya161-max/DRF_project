from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserAPIView


# Create your views here.
class PaymentsListAPIView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = (
        "payment_detail",
        "paid_course",
        "paid_lesson",
    )
    ordering_fields = ("payment_date",)
    permission_classes = [IsAuthenticated]


class UserListAPIView(ListAPIView):
    serializer_class = UserAPIView
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserAPIView
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(DestroyAPIView):
    serializer_class = UserAPIView
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserAPIView
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserAPIView
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
