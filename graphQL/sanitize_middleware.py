import json
import bleach
from graphql import parse
from django.http import HttpRequest
from io import BytesIO

class SanitizeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def sanitize_dict_values(self, request):
        for key, value in request.items():
            if isinstance(value, dict):
                self.sanitize_dict_values(value)
            elif isinstance(value, str):
                request[key] = bleach.clean(value)
            elif isinstance(value, list):
                for i in range(len(value)):
                    self.sanitize_dict_values(value[i])

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