__author__ = 'aragorn'

from authomatic.providers import oauth2, oauth1, openid #, gaeopenid

CONFIG = {

    'tw': { # Your internal provider name

        # Provider class
        'class_': oauth1.Twitter,

        # Twitter is an AuthorizationProvider so we need to set several other properties too:
        'consumer_key': '########################',
        'consumer_secret': '########################',
    },

    'fb': {

        'class_': oauth2.Facebook,

        # Facebook is an AuthorizationProvider too.
        'consumer_key': '1394399690887901',
        'consumer_secret': '25f333e60b4b79990c9db69cc1a08276',

        # But it is also an OAuth 2.0 provider and it needs scope.
        'scope': ['user_about_me', 'email'],
    },

    'oi': {

        # OpenID provider dependent on the python-openid package.
        'class_': openid.OpenID,
    }
}