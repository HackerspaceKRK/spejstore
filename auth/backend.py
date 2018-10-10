from social_core.backends.oauth import BaseOAuth2
from six.moves.urllib_parse import urlencode, unquote

class HSWawOAuth2(BaseOAuth2):
    """Hackerspace OAuth authentication backend"""
    name = 'hswaw'
    ID_KEY = 'username'
    AUTHORIZATION_URL = 'https://sso.hackerspace.pl/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://sso.hackerspace.pl/oauth/token'
    DEFAULT_SCOPE = ['profile:read']
    REDIRECT_STATE = False
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('expires', 'expires_in')
    ]

    def get_user_details(self, response):
        """Return user details from GitHub account"""
        return {'username': response.get('username'),
                'email': response.get('email'),
                }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://sso.hackerspace.pl/api/1/profile'
        headers = {
        'Authorization': 'Bearer {}'.format(access_token)

        }
        return self.get_json(url, headers=headers)

    def auth_url(self):
        """Return redirect url"""
        state = self.get_or_create_state()
        params = self.auth_params(state)
        params.update(self.get_scope_argument())
        params.update(self.auth_extra_arguments())
        params = urlencode(params)
        return '{0}?{1}'.format(self.authorization_url(), params)
