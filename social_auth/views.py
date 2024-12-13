from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response


from .serializers import GoogleSocialAuthSerialiazer, FacebookSocialAuthSerialiazer

# Create your views here.

class FacebookSocialAuthView(generics.GenericAPIView):
    serializer_class = FacebookSocialAuthSerialiazer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data["auth_token"]
        return Response(data, status.HTTP_200_OK)

class GoogleSocialAuthView(generics.GenericAPIView):
    serializer_class = GoogleSocialAuthSerialiazer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data["auth_token"]
        return Response(data, status.HTTP_200_OK)
