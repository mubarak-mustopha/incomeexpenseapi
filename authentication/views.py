import jwt
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .renderers import UserRenderer
from .serializers import (
    RegisterSerializer,
    EmailVerficationSerializer,
    LoginSerializer,
    RequestPasswordResetEmailSerializer,
    SetNewPasswordSerializer,
)
from .utils import Util


# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user = User.objects.get(email=user_data["email"])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request)
        relative_link = reverse("email-verify")
        absurl = (
            f"{request.scheme}://"
            + current_site.domain
            + relative_link
            + "?token="
            + str(token)
        )
        email_body = (
            f"Hi, {user.username}. Use the link below to verify your email\n{absurl}"
        )
        data = {
            "email_body": email_body,
            "email_subject": "Verify your email",
            "to_email": user.email,
        }
        print(current_site, current_site.domain, request.scheme)
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerficationSerializer
    token_param_config = openapi.Parameter(
        "token",
        in_=openapi.IN_QUERY,
        description="Description",
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
                    {"email": "Successfully activated"}, status=status.HTTP_200_OK
                )
        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {"error": "Activation expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as identifier:
            return Response({"error": "Invalid token"}, status=status.HTTP_200_OK)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer

    def post(self, request):
        # data = {"request": request, "data": request.data}
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request)
            relative_link = reverse(
                "password-reset-confirm", kwargs={"uidb64": uidb64, "token": token}
            )
            absurl = "http://" + current_site.domain + relative_link
            email_body = f"Hello\n Use the link below to reset your password\n{absurl}"
            data = {
                "email_body": email_body,
                "email_subject": "Reset your password",
                "to_email": user.email,
            }
            Util.send_email(data)

        return Response(
            {"success": "Password reset link succesfully sent."},
            status=status.HTTP_200_OK,
        )


class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"error": "Invalid token, please request a new one"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            return Response(
                {
                    "success": True,
                    "message": "Credentials valid",
                    "uidb64": uidb64,
                    "token": token,
                }
            )
        except (DjangoUnicodeDecodeError, User.DoesNotExist):
            return Response(
                {"error": "Invalid credentials provided, please request a new one"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": True, "message": "Password rest successsful"},
            status=status.HTTP_200_OK,
        )
