from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import User


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
        if not user.is_verified:
            raise AuthenticationFailed("Email not verified")

        return {
            "email": user.email,
            "username": user.username,
            "tokens": user.tokens,
        }
