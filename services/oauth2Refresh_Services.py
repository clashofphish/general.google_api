"""File to serve as the base classes for implementing Google OAuth2 using previously
saved authentication token and client secrets credentials."""
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials

import os
import sys
base_path = os.path.abspath(os.path.join('..'))
if base_path not in sys.path:
    sys.path.append(base_path)

# Custom imports
from services.oauth2FileHandling_Services \
    import ClientSecretsGoogleHandling, AuthTokenFileHandling


class RefreshCredentialFile:
    """Use to interface google.oauth.credentials with token and client secrets json.
    """
    def __init__(
            self,
            client_handling: ClientSecretsGoogleHandling,
            token_handling: AuthTokenFileHandling
    ):
        self.client_handling = client_handling
        self.token_handling = token_handling
        # Internally determined parameters
        self._credentials = None
        self._session = None

    @property
    def client_handling(self):
        return self._client_handling

    @client_handling.setter
    def client_handling(self, new):
        self._client_handling = new

    @property
    def token_handling(self):
        return self._token_handling

    @token_handling.setter
    def token_handling(self, new):
        self._token_handling = new

    # Internally determined parameters
    @property
    def credentials(self):
        return self._credentials

    @property
    def session(self):
        return self._session

    def initialize_saved_creds(self):
        """Initialize credentials using saved credentials."""
        self.client_handling.load_json_create()
        self.token_handling.load_json_create()

        self._credentials = Credentials(
            token=self.token_handling.access_token,
            refresh_token=self.token_handling.refresh_token,
            id_token=self.token_handling.id_token,
            token_uri=self.client_handling.refresh_uri,
            client_id=self.client_handling.client_id,
            client_secret=self.client_handling.client_secret,
            scopes=self.token_handling.scope
        )

        self._credentials.expiry = self.token_handling.expires_at

    def refresh_creds(self):
        """Refresh the credentials with the refresh token."""
        # request = google_requests.Request()
        # self._credentials.refresh(request)

        self._session = AuthorizedSession(self._credentials)

    def save_updated_creds(self):
        """Save the refreshed credentials."""
        self.token_handling.expires_at = self._session.credentials.expiry
        self.token_handling.create_json_save()
