import logging
from oauthlib.oauth2 import WebApplicationClient, generate_token
from requests_oauthlib import OAuth2Session
from ulrparse import urlparse, parse_qs
# import requests

log = logging.getLogger(__name__)


class UserInfo:
    def __init__(self, user_email, account_type, authorization_service,
                 token_service, discovery_resource, discovery_service):
        self.user_email = user_email
        self.account_type = account_type
        self.authorization_service = authorization_service
        self.token_service = token_service
        self.discovery_resource = discovery_resource
        self.discovery_service = discovery_service


class O365Session(OAuth2Session):
    """
    Wrapper for requests_oauthlib.OAuth2Session that handles the special case
    of Microsoft(c) Office 365 cloud service discovery.

    See https://requests-oauthlib.readthedocs.org/en/latest/ for more details on
    requests_oauthlib
    """

    ResourceId = 'https://api.office.com/discovery/'
    ApiEndpointBase = 'https://api.office.com/discovery/v1.0/me/'
    FirstSignInFormat = 'FirstSignIn?redirect_uri={0}&scope={1}'

    # TODO: Need to review these parameters for any that are not applicable
    #       to the wrapper class and remove them from the signature and the
    #       accompanying documentation block below as well as intiialization
    #       in the constructor.
    def __init__(self, client_id=None, client=None, auto_refresh_url=None,
                 auto_refresh_kwargs=None, scope=None, redirect_uri=None,
                 token=None, state=None, token_updater=None, **kwargs):
        """Construct a new OAuth 2 client session.
        :param client_id: Client id obtained during registration
        :param client: :class:`oauthlib.oauth2.Client` to be used. Default is
                       WebApplicationClient which is useful for any
                       hosted application but not mobile or desktop.
        :param scope: List of scopes you wish to request access to
        :param redirect_uri: Redirect URI you registered as callback
        :param token: Token dictionary, must include access_token
                      and token_type.
        :param state: State string used to prevent CSRF. This will be given
                      when creating the authorization url and must be supplied
                      when parsing the authorization response.
                      Can be either a string or a no argument callable.
        :auto_refresh_url: Refresh token endpoint URL, must be HTTPS. Supply
                           this if you wish the client to automatically refresh
                           your access tokens.
        :auto_refresh_kwargs: Extra arguments to pass to the refresh token
                              endpoint.
        :token_updater: Method with one argument, token, to be used to update
                        your token databse on automatic token refresh. If not
                        set a TokenUpdated warning will be raised when a token
                        has been refreshed. This warning will carry the token
                        in its token argument.
        :param kwargs: Arguments to pass to the Session constructor.
        """
        super(O365Session, self).__init__(**kwargs)
        self.client_id = client_id or client.client_id
        self.scope = scope
        self.redirect_uri = redirect_uri
        self.token = token or {}
        self.state = state or generate_token
        self._state = state
        self.auto_refresh_url = auto_refresh_url
        self.auto_refresh_kwargs = auto_refresh_kwargs or {}
        self.token_updater = token_updater
        self._client = client or WebApplicationClient(client_id, token=token)
        self.auth._populate_attributes(token or {})
        self.user_info = None

    def get_discovery_url(self):
        return (self.ApiEndpointBase +
                self.FirstSignInFormat.format(self.redirect_uri, self.scope))

    def parse_discovery(self, callback_uri):
        parsed = urlparse(callback_uri)
        query = parse_qs(parsed.query)
        self.user_info = UserInfo(query['user_email'],
                                  query['account_type'],
                                  query['authorization_service'],
                                  query['token_service'],
                                  query['discovery_resource'],
                                  query['discovery_service'])

    def authorization_url(self, callback_uri, client_secret, resource_uri):
        super.authorization_url(self.user_info.authorization_service,
                                authorization_response=callback_uri,
                                client_secret=client_secret,
                                resource=resource_uri,
                                login_hint=self.user_info.user_email)
