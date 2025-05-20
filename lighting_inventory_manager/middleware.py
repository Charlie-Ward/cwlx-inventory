from django.shortcuts import redirect
from django.conf import settings

EXEMPT_URLS = [settings.LOGIN_URL, '/logout/', '/admin/login/']

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            if not any(path == url or path.startswith('/static/') for url in EXEMPT_URLS):
                return redirect(f"{settings.LOGIN_URL}?next={path}")
        return self.get_response(request)