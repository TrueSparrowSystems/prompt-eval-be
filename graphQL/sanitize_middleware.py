import json
import bleach
from graphql import parse
from django.http import HttpRequest
from io import BytesIO

"""
sanitize middleware for sanitizing the request body and query parameters

@class SanitizeMiddleware
"""
class SanitizeMiddleware:
    """
    Initializes the middleware with the get_response callable.

    @param {Callable} get_response

    @returns {SanitizeMiddleware} SanitizeMiddleware object
    """
    def __init__(self, get_response):
        self.get_response = get_response

    """
    Recursively sanitizes dictionary values by applying cleaning operations.

    @param {Dict} request

    @returns {Dict} Sanitized request
    """
    def sanitize_dict_values(self, request):
        for key, value in request.items():
            if isinstance(value, dict):
                self.sanitize_dict_values(value)
            elif isinstance(value, str):
                request[key] = bleach.clean(value)
            elif isinstance(value, list):
                for i in range(len(value)):
                    self.sanitize_dict_values(value[i])

    """
    Processes the request and sanitizes the request body and query parameters.

    @param {HttpRequest} request

    @returns {HttpResponse} Response
    """
    def __call__(self, request: HttpRequest):
        try:
            if request.body:
                # Sanitize the request body
                body = json.loads(request.body)
                self.sanitize_dict_values(body)
                sanitized_body = json.dumps(body).encode('utf-8')
                request._stream = BytesIO(sanitized_body)
                request._body = sanitized_body
                request._content_length = len(sanitized_body)
                print('request.body', sanitized_body)
            # Sanitize query parameters
            query_params = request.GET.copy()
            self.sanitize_dict_values(query_params)
            request.GET = query_params

        except Exception as e:
            print('Error in middleware:', e)

        response = self.get_response(request)

        return response