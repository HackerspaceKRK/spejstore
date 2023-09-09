from storage.authentication import has_permission
from django.http import HttpResponseRedirect


def is_authorized_or_in_lan_middleware(get_response):
    # One-time configuration and initialization.
    login_paths_to_ignore = [
        "/admin/login",
        "/static",
        "/admin/static",
        "/complete",
        "/favicon.ico",
        "/api",
    ]

    def middleware(request):
        if request.user.is_authenticated:
            return get_response(request)
        is_within_lan = has_permission(request)
        if is_within_lan:
            return get_response(request)
        else:
            for login_path in login_paths_to_ignore:
                if request.path.startswith(login_path):
                    return get_response(request)
            else:
                return HttpResponseRedirect("/admin/login")

    return middleware
