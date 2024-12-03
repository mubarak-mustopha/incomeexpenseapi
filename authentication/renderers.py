import json
from rest_framework.renderers import JSONRenderer


class UserRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):

        if "ErrorDetail" in str(data):
            response = json.dumps({"error": data})
        else:
            response = json.dumps({"data": data})
        return response
        # import pdb

        # pdb.set_trace()
        # return super().render(data, accepted_media_type, renderer_context)
