from django.core.exceptions import PermissionDenied
from storage.authentication import has_permission


def is_authorized_or_in_lan_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)
        if request.user.is_authenticated:
            return response
        is_within_lan = has_permission(request)
        if is_within_lan:
            return response
        else:
            raise PermissionDenied()

        # Code to be executed for each request/response after
        # the view is called.

    return middleware
