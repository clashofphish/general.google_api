"""File to serve as base classes for authorizing API sessions."""
import os
import sys
base_path = os.path.abspath(os.path.join('..'))
if base_path not in sys.path:
    sys.path.append(base_path)

# Custom imports
from procedures.oauth2Flow_Procedures import Oauth2UsingFlow
from procedures.oauth2Refresh_Procedures import Oauth2UsingToken


class RequestSession:
    """Use the authorization object to generate a session for requests.

    :param authorizing_oauth: obj: Oauth 2 authorization class

    Internally determined:
        :param session: obj: authorized session object for making requests
    """
    def __init__(
            self,
            authorizing_oauth: [Oauth2UsingFlow, Oauth2UsingToken]
    ):
        self.authorizing_oauth = authorizing_oauth
        # Internally determined parameters
        self._session = None

    @property
    def authorizing_oauth(self):
        return self._authorizing_oauth

    @authorizing_oauth.setter
    def authorizing_oauth(self, new):
        self._authorizing_oauth = new

    # Internally determined parameters
    @property
    def session(self):
        return self._session

    def authorize_session(self, save_new=True):
        """Create authorized session."""
        self.authorizing_oauth.instantiate_creds()
        self.authorizing_oauth.authorize_token()

        if save_new:
            self.authorizing_oauth.save_updated_creds()

        self._session = self.authorizing_oauth.authorize_session()
