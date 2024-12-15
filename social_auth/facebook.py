import facebook


class Facebook:
    @staticmethod
    def validate(token):
        graph = facebook.GraphAPI(access_token=token)
        profile = graph.request("/me?fields=name,email")
        return profile
