from decouple import config
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .google import Google
from .register import register_social_user


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
