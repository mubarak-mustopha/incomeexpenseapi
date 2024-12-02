from django.urls import path

from .views import RegisterView, VerifyUserView, LoginAPIView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("verify_user/", VerifyUserView.as_view(), name="verify_user"),
]
