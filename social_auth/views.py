from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response


from .serializers import GoogleSocialAuthSerialiazer

# Create your views here.


class GoogleSocialAuthView(generics.GenericAPIView):
    serializer_class = GoogleSocialAuthSerialiazer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data["auth_token"]
        return Response(data, status.HTTP_200_OK)
