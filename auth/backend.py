from social_core.backends.oauth import BaseOAuth2
from six.moves.urllib_parse import urlencode, unquote

class HSWawOAuth2(BaseOAuth2):
    """Hackerspace OAuth authentication backend"""
    name = 'hswro'
    ID_KEY = 'username'
    AUTHORIZATION_URL = 'http://sso.lokal.hswro.org/oauth/authorize'
    ACCESS_TOKEN_URL = 'http://sso.lokal.hswro.org/oauth/token'
    DEFAULT_SCOPE = ['profile:read']
    REDIRECT_STATE = False
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('expires', 'expires_in')
    ]

    def get_user_details(self, response):
        """Return user details from Hackerspace account"""
        personal_email = None
        if response.get('personal_email'):
            personal_email = response.get('personal_email')[0]

        return {'username': response.get('username'),
                'email': response.get('email'),
                'personal_email': personal_email,
                }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'http://sso.lokal.hswro.org/api/1/profile'
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
