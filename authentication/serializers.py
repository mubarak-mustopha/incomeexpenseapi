from rest_framework import serializers

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
