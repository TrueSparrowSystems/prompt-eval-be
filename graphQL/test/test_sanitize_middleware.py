from django.test import TestCase, Client
from django.http import HttpRequest, JsonResponse
import json
from graphQL.sanitize_middleware import SanitizeMiddleware

#to run this test case: python manage.py test graphQL.test.test_sanitize_middleware

class SanitizeMiddlewareTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.middleware = SanitizeMiddleware(get_response=None)

    def get_response_for_test_middleware_sanitizes_string_values(self, request):
        data = {
            'name': '&lt;script&gt;alert("XSS")&lt;/script&gt;',
            'age': 20,
            'description': 'Lorem ipsum',
        }
        return JsonResponse(data)
    
    def get_response_for_test_middleware_sanitizes_nested_values(self, request):
        data = {
            'name': '&lt;script&gt;alert("XSS")&lt;/script&gt;',
            'age': 20,
            'profile': {
                'bio': 'Lorem ipsum',
                'address': {
                    'street': '&lt;script&gt;alert("XSS")&lt;/script&gt;',
                    'city': 'New York',
                },
            },
        }
        return JsonResponse(data)
    
    def get_response_for_test_middleware_sanitizes_string_values_query_params(self, request):
        data = {
            'name': '&lt;script&gt;alert("XSS")&lt;/script&gt;',
            'age': '20',
            'city': 'New York',
        }
        return JsonResponse(data)

    def test_middleware_sanitizes_string_values(self):
        request = HttpRequest()
        request.method = 'POST'
        request.content_type = 'application/json'
        data = {
            'name': '<script>alert("XSS")</script>',
            'age': 20,
            'description': 'Lorem ipsum',
        }
        request._body = json.dumps(data).encode('utf-8')

        self.middleware.get_response = self.get_response_for_test_middleware_sanitizes_string_values
        middleware_response = self.middleware(request)

        self.assertEqual(
            middleware_response.content.decode('utf-8'),
            json.dumps({
                'name': '&lt;script&gt;alert("XSS")&lt;/script&gt;',
                'age': 20,
                'description': 'Lorem ipsum',
            })
        )

    def test_middleware_sanitizes_nested_values(self):
        request = HttpRequest()
        request.method = 'POST'
        request.content_type = 'application/json'
        data = {
            'name': '<script>alert("XSS")</script>',
            'age': 20,
            'profile': {
                'bio': 'Lorem ipsum',
                'address': {
                    'street': '<script>alert("XSS")</script>',
                    'city': 'New York',
                },
            },
        }
        request._body = json.dumps(data).encode('utf-8')

        self.middleware.get_response = self.get_response_for_test_middleware_sanitizes_nested_values
        middleware_response = self.middleware(request)

        self.assertEqual(
            middleware_response.content.decode('utf-8'),
            json.dumps({
                'name': '&lt;script&gt;alert("XSS")&lt;/script&gt;',
                'age': 20,
                'profile': {
                    'bio': 'Lorem ipsum',
                    'address': {
                        'street': '&lt;script&gt;alert("XSS")&lt;/script&gt;',
                        'city': 'New York',
                    },
                },
            })
        )
    
    def test_middleware_sanitizes_query_params(self):
        request = HttpRequest()
        request.method = 'GET'
        request.GET = {
            'name': '<script>alert("XSS")</script>',
            'age': '20',
            'city': 'New York',
        }

        self.middleware.get_response = self.get_response_for_test_middleware_sanitizes_string_values_query_params
        middleware_response = self.middleware(request)

        self.assertEqual(
            middleware_response.content.decode('utf-8'),
            json.dumps({
                'name': '&lt;script&gt;alert("XSS")&lt;/script&gt;',
                'age': '20',
                'city': 'New York'
            })
        )
