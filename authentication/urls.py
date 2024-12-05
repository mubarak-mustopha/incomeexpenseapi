from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import (
    RegisterView,
    VerifyUserView,
    LoginAPIView,
    PaswordResetAPIView,
    PasswordResetConfirmAPIView,
    PasswordResetCompleteAPIView,
)

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("password_reset/", PaswordResetAPIView.as_view(), name="password_reset"),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        PasswordResetConfirmAPIView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        PasswordResetCompleteAPIView.as_view(),
        name="password_reset_complete",
    ),
    path("register/", RegisterView.as_view(), name="register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify_user/", VerifyUserView.as_view(), name="verify_user"),
]
