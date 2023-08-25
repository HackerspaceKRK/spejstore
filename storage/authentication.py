import ipaddress
from rest_framework import exceptions

from rest_framework.authentication import SessionAuthentication
from spejstore.settings import (
    LAN_ALLOWED_ADDRESS_SPACE,
    LAN_ALLOWED_HEADER,
    PROD,
    PROXY_TRUSTED_IPS,
)


headers_to_check_for_ip = [
    "HTTP_X_FORWARDED_FOR",
    "X_FORWARDED_FOR",
    "HTTP_CLIENT_IP",
    "HTTP_X_REAL_IP",
    "HTTP_X_FORWARDED",
    "HTTP_X_CLUSTER_CLIENT_IP",
    "HTTP_FORWARDED_FOR",
    "HTTP_FORWARDED",
    "HTTP_VIA",
]


def get_request_meta(request, key):
    value = request.META.get(key, "")
    if value == "":
        return None
    return value


def get_ip_from_request(request):
    for header in headers_to_check_for_ip:
        ip = get_request_meta(request, header)
        if not ip:
            ip = get_request_meta(request, header.replace("_", "-"))
        if ip:
            return ip
    return None


def has_permission(request):
    if PROD:
        client_ip = get_ip_from_request(request)
        if client_ip is None:
            # This should only happen on localhost env when fiddling with code.
            # It's technically impossible to get there with proper headers.
            raise exceptions.AuthenticationFailed("Unauthorized: no ip detected?")
        # Make sure that we need to check PROXY_TRUSTED_IPS here
        if len(PROXY_TRUSTED_IPS) > 0:
            if request.META["REMOTE_ADDR"] not in PROXY_TRUSTED_IPS:
                raise exceptions.AuthenticationFailed(
                    "Unauthorized: request is not coming from the PROXY_TRUSTED_IPS machine"
                )
        return ipaddress.IPv4Address(client_ip) in ipaddress.IPv4Network(
            LAN_ALLOWED_ADDRESS_SPACE
        )
    else:
        return True


class LanAuthentication(SessionAuthentication):
    def authenticate(self, request):
        is_session_authorized = super().authenticate(request)
        if is_session_authorized:
            return is_session_authorized
        is_authorized = self.has_permission(request)
        if is_authorized:
            user = getattr(request._request, "user", None)
            return (user, "authorized")
        else:
            raise exceptions.AuthenticationFailed(
                "Unauthorized: not in subnet of " + LAN_ALLOWED_ADDRESS_SPACE
            )

    def authenticate_header(self, request):
        return LAN_ALLOWED_HEADER
