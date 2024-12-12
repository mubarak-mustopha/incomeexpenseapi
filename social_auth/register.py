import random
import re
from decouple import config
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


def generate_username(name):
    name = re.sub(r"\s+", "", name)
    if not User.objects.filter(username=name).exists():
        return name
    else:
        return generate_username(name + str(random.randint(1, 1000)))


def register_social_user(user_id, name, email, provider):
    user = User.objects.filter(email=email)

    if user.exists():

        if provider == user.first().auth_provider:
            auth_user = authenticate(email=email, password=config("SOCIAL_SECRET"))

            return {
                "username": auth_user.username,
                "email": auth_user.email,
                "tokens": auth_user.tokens(),
            }

        else:
            raise AuthenticationFailed(
                f"Please continue your login using {user.first().auth_provider}"
            )

    else:
        user = {
            "username": generate_username(name),
            "email": email,
            "password": config("SOCIAL_SECRET"),
        }
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        auth_user = authenticate(email=user.email, password=config("SOCIAL_SECRET"))

        return {
            "username": auth_user.username,
            "email": auth_user.email,
            "tokens": auth_user.tokens(),
        }
