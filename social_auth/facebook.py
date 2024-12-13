import facebook


class Facebook:
    @staticmethod
    def validate(token):
        try:
            graph = facebook.GraphAPI(access_token=token)
            profile = graph.request("/me?fields=name,email")
            return profile
        except:
            return "The token is invalid or has expired."
