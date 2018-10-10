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

    def get_user(self, user_id):
        """
        Return user with given ID from the User model used by this backend.
        This is called by django.contrib.auth.middleware.
        """
        return self.strategy.get_user(user_id)

    def pipeline(self, pipeline, pipeline_index=0, *args, **kwargs):
        out = self.run_pipeline(pipeline, pipeline_index, *args, **kwargs)
        if not isinstance(out, dict):
            return out
        user = out.get('user')
        if user:
            user.social_user = out.get('social')
            user.is_new = out.get('is_new')
        return user
