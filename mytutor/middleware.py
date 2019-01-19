import re
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse

EXEPMT_URLS = [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]
for url in settings.LOGIN_EXEMPT_URLS:
    print(url)
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')

        url_is_exempt = any(url.match(path) for url in EXEPMT_URLS)

        
