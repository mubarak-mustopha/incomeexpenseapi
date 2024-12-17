from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

from .models import User
from .utils import Util


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate(self, attrs):
        username = attrs["username"]
        email = attrs["email"]

        if not username.isalnum():
            raise serializers.ValidationError(
                "Username should contain only alphanumeric characters"
            )
        return attrs

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class EmailVerifySerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ["token"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=8)
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials")
        if not user.is_active:
            raise AuthenticationFailed("Account is disabled, pls contact admin")
        if not user.auth_provider == "email":
            raise AuthenticationFailed(
                f"Pls login with your auth provider: {user.auth_provider}"
            )
        if not user.is_verified:
            raise AuthenticationFailed("Email not verified")

        return {
            "email": user.email,
            "username": user.username,
            "tokens": user.tokens,
        }


class PaswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=8, max_length=255)

    def validate(self, attrs):
        email = attrs.get("email")
        request = self.context.get("request")
        user = User.objects.filter(email=email)
        if user.exists():
            user = user.first()
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            protocol = request.scheme
            domain = get_current_site(request).domain
            rel_url = reverse(
                "password_reset_confirm", kwargs={"uidb64": uidb64, "token": token}
            )

            abs_url = f"{protocol}://{domain}{rel_url}"
            subject = "Reset your password"
            body = f"Hi\nClick the link below to reset your password\n{abs_url}"

            Util.send_email(
                {"email_subject": subject, "email_body": body, "to_email": user.email}
            )

        return super().validate(attrs)


class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(min_length=2)
    token = serializers.CharField(min_length=6)

    def validate(self, attrs):
        uidb64 = attrs.get("uidb64")
        token = attrs.get("token")

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed(
                    "Invalid or expired link, pls request a new one", code=401
                )
            return {
                "email": user.email,
                "uidb64": uidb64,
                "token": token,
            }

        except Exception as e:
            if isinstance(e, AuthenticationFailed):
                raise (e)
            raise AuthenticationFailed("Invalid link, pls request a new one", code=401)


class PasswordResetCompleteSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=68, write_only=True)
    uidb64 = serializers.CharField(min_length=2, write_only=True)
    token = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        uidb64 = attrs.get("uidb64")
        token = attrs.get("token")
        password = attrs.get("password")

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed(
                    "Invalid or expired link, pls request a new one", code=401
                )
            user.set_password(password)
            user.save(update_fields=["password"])

        except Exception as e:
            if isinstance(e, AuthenticationFailed):
                raise (e)
            raise AuthenticationFailed("Invalid link, pls request a new one", code=401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate_refresh(self, value):
        try:
            self.token = RefreshToken(value)
            return value
        except:
            raise serializers.ValidationError("Token is invalid or expired.")

    def save(self, **kwargs):
        return self.token.blacklist()
