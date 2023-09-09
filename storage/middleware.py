from django.core.exceptions import PermissionDenied
from storage.authentication import has_permission


def is_authorized_or_in_lan_middleware(get_response):
    # One-time configuration and initialization.
    login_paths_to_ignore = [
          '/admin/login/'
          '/complete/'
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
                raise PermissionDenied()

    return middleware
