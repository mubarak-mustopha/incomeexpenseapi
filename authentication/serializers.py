from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        email = attrs["email"]
        username = attrs["username"]

        if not username.isalnum():
            raise serializers.ValidationError(
                "The username should only contain alphanumeric characters."
            )

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerficationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ["token"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=8)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        user = auth.authenticate(email=email, password=password)
        # import pdb

        # pdb.set_trace()

        if not user:
            raise AuthenticationFailed("Invalid credentials, try again.")
        if not user.is_active:
            raise AuthenticationFailed("Account disabled, pls contact admin.")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified.")

        return {
            "email": user.email,
            "username": user.username,
            "token": user.tokens(),
        }
