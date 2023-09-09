from storage.authentication import has_permission
from django.http import HttpResponseRedirect
from spejstore.settings import STATIC_URL, MEDIA_URL, LOGIN_URL
from django.core.exceptions import PermissionDenied

def is_authorized_or_in_lan_middleware(get_response):
    # One-time configuration and initialization.
    login_paths_to_ignore = [
        "/login",
        LOGIN_URL[:-1],
        STATIC_URL[:-1],
        MEDIA_URL[:-1],
        "/admin/static",
        "/complete",
        "/favicon.ico",
        "/api/1",
    ]

    def middleware(request):
        if request.user.is_authenticated:
            return get_response(request)
        is_within_lan, error_message = has_permission(request)
        if is_within_lan:
            return get_response(request)
        else:
            for login_path in login_paths_to_ignore:
                if request.path.startswith(login_path):
                    return get_response(request)
            else:
                raise PermissionDenied()

    return middleware
