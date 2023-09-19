import ipaddress
from rest_framework import exceptions

from rest_framework.authentication import SessionAuthentication
from spejstore.settings import (
    LAN_ALLOWED_ADDRESS_SPACE,
    LAN_ALLOWED_SINGLE_ADDRESS,
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


def has_address_space_permission(client_ip):
    return ipaddress.IPv4Address(client_ip) in ipaddress.IPv4Network(
        LAN_ALLOWED_ADDRESS_SPACE
    )

def has_single_address_permission(client_ip):
    return ipaddress.IPv4Address(client_ip) == LAN_ALLOWED_SINGLE_ADDRESS


def has_permission(request):
    # We don't care if address space is undefined
    if LAN_ALLOWED_ADDRESS_SPACE == '' and LAN_ALLOWED_SINGLE_ADDRESS == '':
        return (True, '')
    client_ip = get_ip_from_request(request)
    if client_ip is None:
        # This should only happen on localhost env when fiddling with code.
        # It's technically impossible to get there with proper headers.
        return (False, "Unauthorized: no ip detected?")

    if LAN_ALLOWED_ADDRESS_SPACE != '' and not has_address_space_permission(client_ip):
        return (False, "Unauthorized: " + client_ip + " not in subnet of " + LAN_ALLOWED_ADDRESS_SPACE)
    if LAN_ALLOWED_SINGLE_ADDRESS != '' and not has_single_address_permission(client_ip):
        return (False, "Unauthorized: " + client_ip + " is not " + LAN_ALLOWED_SINGLE_ADDRESS)
    return (True, '')

class LanAuthentication(SessionAuthentication):
    def authenticate(self, request):
        is_session_authorized = super().authenticate(request)
        if is_session_authorized:
            return is_session_authorized
        is_authorized, error_message = has_permission(request)
        if is_authorized:
            user = getattr(request._request, "user", None)
            return (user, "authorized")
        else:
            raise exceptions.AuthenticationFailed(
                error_message
            )

