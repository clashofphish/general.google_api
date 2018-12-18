import os
import sys
base_path = os.path.abspath(os.path.join('..'))
if base_path not in sys.path:
    sys.path.append(base_path)

# Custom imports
from services.oauth2Refresh_Services import RefreshCredentialFile


class Oauth2UsingToken:
    """Initialize a flow object for Google Oauth2 verification.

    :param creds_service: obj: object for handling the operations for credentials
    :param auth_service: obj: dummy variable to facilitate code reuse

    Internally determined:
        :param session: google.auth.transport.requests.AuthorizedSession:
                    authorized session for pulling data from Google API
    """
    def __init__(
            self,
            creds_service: RefreshCredentialFile,
            auth_service=None
    ):
        self.creds_service = creds_service
        # Internally determined parameters
        self._session = None

    @property
    def creds_service(self):
        return self._creds_service

    @creds_service.setter
    def creds_service(self, new):
        self._creds_service = new

    # Internally determined parameters
    @property
    def session(self):
        return self._session

    def instantiate_creds(self):
        self.creds_service.initialize_saved_creds()

    def authorize_token(self):
        self.creds_service.refresh_creds()

    def save_updated_creds(self):
        self.creds_service.save_updated_creds()

    def authorize_session(self):
        self._session = self._creds_service.session
        return self._session
