from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
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

    @swagger_auto_schema(
        operation_description="Retrieve a list of payments",
        responses={200: PaymentsSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserListAPIView(ListAPIView):
    serializer_class = UserAPIView
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of users",
        responses={200: UserAPIView(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserAPIView
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve specific user",
        responses={200: UserAPIView}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserDestroyAPIView(DestroyAPIView):
    serializer_class = UserAPIView
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Destroy a list of users",
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserAPIView
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update a specific user",
        request_body=UserAPIView,
        responses={200: UserAPIView}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserAPIView
    queryset = User.objects.all()

    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=UserAPIView,
        responses={201: UserAPIView}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
