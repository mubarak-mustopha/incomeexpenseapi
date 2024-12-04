from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    VerifyEmail,
    LoginAPIView,
    RequestPasswordResetEmail,
    PasswordTokenCheckAPI,
    SetNewPasswordAPIView,
)

urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "request-reset-email/",
        RequestPasswordResetEmail.as_view(),
        name="request-reset-email",
    ),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordTokenCheckAPI.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset-complete/",
        SetNewPasswordAPIView.as_view(),
        name="password-reset-complete",
    ),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("email-verify", VerifyEmail.as_view(), name="email-verify"),
    path("", include("django.contrib.auth.urls")),
]


# from django.contrib.auth.views import PasswordResetConfirmView

# from django.contrib.auth import urls
