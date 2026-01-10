from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    UserCreateAPIView,
    PaymentSuccessAPIView,
    PaymentFailedAPIView,
    CreatePaymentAPIView,
    UserListAPIView,
)

app_name = UsersConfig.name
urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("payment/create/", CreatePaymentAPIView.as_view(), name="create_payment"),
    path("payment/success/", PaymentSuccessAPIView.as_view(), name="payment_success"),
    path("payment/failed/", PaymentFailedAPIView.as_view(), name="payment_failed"),
    path("api/users/", UserListAPIView.as_view(), name="users_list"),
]
