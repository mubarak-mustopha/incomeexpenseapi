import random
import re
from decouple import config
from django.contrib.auth import get_user_model, authenticate


User = get_user_model()


class AuthProviderError(Exception):
    pass


def generate_username(username):
    username = re.sub(r"\s+", "", username)
    if not User.objects.filter(username=username).exists():
        return username
    return generate_username(username + str(random.randint(1, 1000)))


def register_social_user(name, email, provider):
    user = User.objects.filter(email=email).first()

    if user:
        if not user.auth_provider == provider:
            raise AuthProviderError(
                f"Pls log in with your auth provider: {user.auth_provider}"
            )
        else:
            auth_user = authenticate(email=email, password=config("SOCIAL_SECRET"))
    else:
        user = User.objects.create(
            username=generate_username(name),
            email=email,
            passowrd=config("SOCIAL_SECRET"),
        )
        user.auth_provider = provider
        user.is_verified = True
        user.save()
        auth_user = user

    return {
        "email": auth_user.email,
        "username": auth_user.username,
        "tokens": auth_user.tokens,
    }
