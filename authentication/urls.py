from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, VerifyEmail, LoginAPIView

urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("email-verify", VerifyEmail.as_view(), name="email-verify"),
]
