"""File to serve as the base classes for implementing Google OAuth2 through the
google_auth_oauthlib.flow Flow object."""
from google_auth_oauthlib.flow import Flow

import os
import sys
base_path = os.path.abspath(os.path.join('..'))
if base_path not in sys.path:
    sys.path.append(base_path)

# Custom imports
from services.oauth2FileHandling_Services \
    import ClientSecretsGoogleHandling, AuthTokenFileHandling


class ManualAuthFlow:
    """Use flow object to manually to create an authorization token.

    :param flow: google_auth_oauthlib.flow: initialized object

    Internally determined:
        :param token: json obj: created authorization token
    """
    def __init__(
            self,
            flow: Flow = None
    ):
        self.flow = flow
        # Internally determined parameters
        self._token = None

    @property
    def flow(self):
        return self._flow

    @flow.setter
    def flow(self, new):
        self._flow = new

    # Internally determined parameters
    @property
    def token(self):
        return self._token

    def load_token(self):
        """Manual generation of authorization token.
        Note:
            Outputs authorization URL to command line.
            Requires input of authorization code from web page.

        :return flow: google_auth_oauthlib.flow: authorization token fetched
        """
        auth_url, _ = self.flow.authorization_url(prompt='consent')
        print('Please go to this URL: {}'.format(auth_url))

        code = input('Enter the authorization code:')
        self._token = self.flow.fetch_token(code=code)

        return self.flow


class FlowCredentialFile:
    """Use to interface google.oauth.credentials with token and client secrets json.
    """
    def __init__(
            self,
            client_handling: ClientSecretsGoogleHandling,
            token_handling: AuthTokenFileHandling,
            flow: Flow = None
    ):
        self.client_handling = client_handling
        self.token_handling = token_handling
        self.flow = flow

    @property
    def flow(self):
        return self._flow

    @flow.setter
    def flow(self, new):
        self._flow = new

    def save_updated_creds(self):
        """Save the credentials from the credential object."""
        # Client secret creds update
        self.client_handling.client_id = self.flow.credentials.client_id
        self.client_handling.client_secret = self.flow.credentials.client_secret
        self.client_handling.token_uri = self.flow.credentials.token_uri
        self.client_handling.project_id = self.flow.client_config['project_id']
        self.client_handling.auth_uri = self.flow.client_config['auth_uri']
        self.client_handling.redirect_uri = self.flow.client_config['redirect_uris']

        # Token creds update
        self.token_handling.expires_at = self.flow.credentials.expiry
        self.token_handling.id_token = self.flow.credentials.id_token
        self.token_handling.refresh_token = self.flow.credentials.refresh_token
        self.token_handling.scope = self.flow.credentials.scopes
        self.token_handling.access_token = self.flow.credentials.token

        # Save credentials
        self.client_handling.create_json_save()
        self.token_handling.create_json_save()
