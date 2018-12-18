"""File for composing the flow process."""
from google_auth_oauthlib.flow import Flow

import os
import sys
base_path = os.path.abspath(os.path.join('..'))
if base_path not in sys.path:
    sys.path.append(base_path)

# Custom imports
from services.oauth2Flow_Services import ManualAuthFlow, FlowCredentialFile


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
