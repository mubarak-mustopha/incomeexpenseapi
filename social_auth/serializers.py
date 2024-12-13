from decouple import config
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .facebook import Facebook
from .google import Google
from .register import register_social_user


class FacebookSocialAuthSerialiazer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Facebook.validate(auth_token)
        print(user_data)

        try:
            user_id = user_data["id"]
            email = user_data["email"]
            name = user_data["name"]
            provider = "facebook"

            return register_social_user(
                user_id=user_id, email=email, name=name, provider=provider
            )

        except Exception as e:
            print(e)
            raise serializers.ValidationError("Token is invalid or has expired.")


class GoogleSocialAuthSerialiazer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)
        # import pdb

        # pdb.set_trace()
        try:
            user_data["sub"]

        except:
            raise serializers.ValidationError(
                "Token is invalid or expired, pls login again"
            )

        g_client = config("GOOGLE_CLIENT_ID")
        if user_data["aud"] != g_client:
            raise AuthenticationFailed("Oops, unknown client. Access Denied!")

        user_id = user_data["sub"]
        email = user_data["email"]
        name = user_data["name"]
        provider = "google"

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name
        )
