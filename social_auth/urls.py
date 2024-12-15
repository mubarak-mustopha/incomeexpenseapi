from django.urls import path

from .views import GoogleSocialAuthView, FacebookSocialAuthView

urlpatterns = [
    path("google/", GoogleSocialAuthView.as_view(), name="google-login"),
    path("facebook/", FacebookSocialAuthView.as_view(), name="facebook-login"),
]
