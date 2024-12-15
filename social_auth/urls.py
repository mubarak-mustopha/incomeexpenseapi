from django.urls import path

from .views import GoogleSocialAuthView, FacebookSocialAuthView


urlpatterns = [
    path("facebook/", FacebookSocialAuthView.as_view()),
    path("google/", GoogleSocialAuthView.as_view()),
]
