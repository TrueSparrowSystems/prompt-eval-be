import json
import bleach
from graphql import parse
from django.http import HttpRequest
from io import BytesIO

class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def sanitize_dict_values(self, d):
        for k, v in d.items():
            if isinstance(v, dict):
                self.sanitize_dict_values(v)
            elif isinstance(v, str):
                d[k] = bleach.clean(v)
            elif isinstance(v, list):
                for i in range(len(v)):
                    self.sanitize_dict_values(v[i])

    def __call__(self, request: HttpRequest):
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                body = json.loads(request.body)
                self.sanitize_dict_values(body)
                sanitized_body = json.dumps(body).encode('utf-8')
                request._stream = BytesIO(sanitized_body)
                request._body = sanitized_body
                request._content_length = len(sanitized_body)
            except Exception as e:
                print('error in middleware',e)

        response = self.get_response(request)

        return response