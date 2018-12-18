from google_auth_oauthlib.flow import Flow

import os
import sys
base_path = os.path.abspath(os.path.join('..'))
if base_path not in sys.path:
    sys.path.append(base_path)

# Custom imports
from services.oauth2FileHandling_Services \
    import ClientSecretsGoogleHandling, AuthTokenFileHandling
from services.oauth2Flow_Services import ManualAuthFlow


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


class Oauth2UsingFlow:
    """Initialize a flow object for Google Oauth2 verification.

    :param creds_service: obj: object for handling the operations for credentials
    :param auth_service: obj: object for handling the operation of authorizing a
                                token; assumes 'load_token' & 'save_token' methods

    Internally determined:
        :param flow: google_auth_oauthlib.flow: provides integration with
                        requests-oauthlib for running the OAuth 2.0 Authorization
                        Flow and acquiring user credentials
        :param session: google.auth.transport.requests.AuthorizedSession:
                    authorized session for pulling data from Google API
    """
    def __init__(
            self,
            creds_service: FlowCredentialFile,
            auth_service: ManualAuthFlow
    ):
        self.creds_service = creds_service
        self.auth_service = auth_service
        # Internally determined parameters
        self._flow = None
        self._session = None

    @property
    def creds_service(self):
        return self._creds_service

    @creds_service.setter
    def creds_service(self, new):
        self._creds_service = new

    @property
    def auth_service(self):
        return self._auth_service

    @auth_service.setter
    def auth_service(self, new):
        self._auth_service = new

    # Internally determined parameters
    @property
    def flow(self):
        return self._flow

    @property
    def session(self):
        return self._session

    def instantiate_creds(self):
        """Initialize the flow object."""
        self.creds_service.client_handling.load_json_create()

        self._flow = Flow.from_client_secrets_file(
            client_secrets_file=self.creds_service.client_handling.filename,
            scopes=self.creds_service.token_handling.scope,
            redirect_uri=self.creds_service.client_handling.redirect
        )

    def authorize_token(self):
        """Authorize the token using the flow object & save authorized token."""
        self.auth_service.flow = self._flow
        self._flow = self.auth_service.load_token()

        # ToDo: add error handling logic for when token authorization fails
        self.creds_service.token_handling.valid = True

    def save_updated_creds(self):
        """Save the authorized credentials"""
        self.creds_service.flow = self._flow
        self.creds_service.save_updated_creds()

    def authorize_session(self):
        """Authorize a requests session using the flow object.

        :return session: google.auth.transport.requests.AuthorizedSession:
                    authorized session for pulling data from Google API
        """
        self._session = self._flow.authorized_session()

        return self._session
