from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.openapi import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.conf import settings

from courses.models import Course
from users.models import Payments, User
from rest_framework.response import Response

from users.serializers import PaymentsSerializer, UserAPIView, PaymentsRequestSerializer
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY



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


class CreatePaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=PaymentsRequestSerializer)
    def post(self, request):
        serializer = PaymentsRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            course_id = serializer.validated_data['course_id']
            amount = serializer.validated_data['amount']
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)


            product = stripe.Product.create(name=course.name)

            price = stripe.Price.create(
                unit_amount=int(amount * 100),
                currency='usd',
                product=product.id,
            )

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price.id,
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://127.0.0.1:8000/users/payment/success/',
                cancel_url='http://127.0.0.1:8000/payment/failed/',
            )

            payment = Payments.objects.create(
                username=user,
                paid_course=course,
                sum=amount,
                payment_detail='Stripe Payment',
            )

            return Response({'url': session.url}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PaymentSuccessAPIView(APIView):
    """Успешный платеж"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Payment was successful!"})


class PaymentFailedAPIView(APIView):
    """Неуспешный платеж"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Failed"})

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
