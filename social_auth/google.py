from google.oauth2 import id_token
from google.auth.transport import requests


class Google:
    @staticmethod
    def validate(auth_token):
        idinfo = None
        try:
            idinfo = id_token.verify_oauth2_token(auth_token, requests.Request())
            # import pdb

            # pdb.set_trace()

            if "accounts.google.com" in idinfo["iss"]:
                return idinfo
        except Exception as e:
            raise (e)

            # return "The token is either invalid or has expired"
