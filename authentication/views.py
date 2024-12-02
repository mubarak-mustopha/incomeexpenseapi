import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import RegisterSerializer, EmailVerifySerializer, LoginSerializer
from .utils import Util


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user_data.pop("password")
        user = User.objects.get(email=user_data["email"])
        token = RefreshToken.for_user(user).access_token

        domain = get_current_site(request)
        relative_url = reverse("verify_user")
        abs_url = f"{request.scheme}://{domain}{relative_url}?token={str(token)}"

        subject = "Activate your Account"
        body = (
            f"Hi, {user.email}\nClick the link below to verify your account\n{abs_url}"
        )
        Util.send_email(
            {"email_subject": subject, "email_body": body, "to_email": user.email}
        )

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyUserView(generics.GenericAPIView):
    serializer_class = EmailVerifySerializer

    token_param_config = openapi.Parameter(
        "token",
        in_=openapi.IN_QUERY,
        description="User token",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get("token")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response(
                {"message": "Activation successful"}, status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Expired token"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        return Response(data, status=status.HTTP_200_OK)
