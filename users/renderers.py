""" docstring """
import json
from rest_framework import renderers


class UserRenderer(renderers.JSONRenderer):
    """ 유저모델 JSON 렌더러 """
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''

        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps({'dmydata': data})
        return response
