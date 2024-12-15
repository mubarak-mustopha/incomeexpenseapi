from google.auth.exceptions import GoogleAuthError
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed


from .facebook import Facebook
from .google import Google
from .register import register_social_user, AuthProviderError


class FacebookSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField(min_length=8)

    def validate_auth_token(self, auth_token):
        try:
            user_info = Facebook.validate(auth_token)

            name = user_info["name"]
            email = user_info["email"]
            provider = "facebook"
            return register_social_user(name=name, email=email, provider=provider)

        except Exception:
            raise AuthenticationFailed("Token expired or invalid.")


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField(min_length=8)

    def validate_auth_token(self, auth_token):
        try:
            user_info = Google.validate(auth_token)

            name = user_info["name"]
            email = user_info["email"]
            provider = "google"
            return register_social_user(name=name, email=email, provider=provider)

        except ValueError:
            raise AuthenticationFailed("Token expired or invalid.")
        except GoogleAuthError:
            raise AuthenticationFailed("Email issuer must be google.")
        except AuthProviderError as e:
            raise AuthenticationFailed(str(e))
