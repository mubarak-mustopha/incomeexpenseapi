from decouple import config
from google.oauth2 import id_token
from google.auth.transport import requests

GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID")


class Google:
    @staticmethod
    def validate(token):
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), GOOGLE_CLIENT_ID
        )

        return idinfo
