import json
from rest_framework import renderers


class UserRenderer(renderers.JSONRenderer):

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # import pdb

        # pdb.set_trace()
        if "ErrorDetail" in str(data):
            response = json.dumps({"error": data})
        else:
            response = json.dumps({"data": data})

        return response
