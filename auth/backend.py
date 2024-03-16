from urllib.parse import urlencode
from social_core.backends.oauth import BaseOAuth2


class HSWawOAuth2(BaseOAuth2):
    """Hackerspace OAuth authentication backend"""

    name = "hswaw"
    ID_KEY = "username"
    AUTHORIZATION_URL = "https://auth.apps.hskrk.pl/application/o/authorize"
    ACCESS_TOKEN_URL = "http://authentik:9000/application/o/token"
    DEFAULT_SCOPE = ["profile:read"]
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False
    SCOPE_SEPARATOR = ","
    EXTRA_DATA = [("expires", "expires_in")]

    def get_user_details(self, response):
        """Return user details from Hackerspace account"""
        personal_email = None
        if response.get("personal_email"):
            personal_email = response.get("personal_email")[0]

        return {
            "username": response.get("username"),
            "email": response.get("email"),
            "personal_email": personal_email,
        }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = "http://authentik:9000/application/o/userinfo"
        headers = {"Authorization": "Bearer {}".format(access_token)}
        return self.get_json(url, headers=headers)
    def auth_url(self):
        """Return redirect url"""
        state = self.get_or_create_state()
        params = self.auth_params(state)
        params.update(self.get_scope_argument())
        params.update(self.auth_extra_arguments())
        params = urlencode(params)
        return "{0}?{1}".format(self.authorization_url(), params)
