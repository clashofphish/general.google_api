"""File to serve as base classes for authorizing API sessions."""
import os
import sys
base_path = os.path.abspath(os.path.join('..'))
if base_path not in sys.path:
    sys.path.append(base_path)

# Custom imports
from services.oauth2Flow_Services import Oauth2UsingFlow


class RequestSession:
    """Use the authorization object to generate a session for requests.

    :param authorizing_flow: obj: Oauth 2 authorization class

    Internally determined:
        :param session: obj: authorized session object for making requests
    """
    def __init__(
            self,
            authorizing_flow: Oauth2UsingFlow
    ):
        self.authorizing_flow = authorizing_flow
        # Internally determined parameters
        self._session = None

    @property
    def authorizing_flow(self):
        return self._authorizing_flow

    @authorizing_flow.setter
    def authorizing_flow(self, new):
        self._authorizing_flow = new

    # Internally determined parameters
    @property
    def session(self):
        return self._session

    def authorize_session(self):
        """Create authorized session."""
        self.authorizing_flow.initialize_flow()
        self.authorizing_flow.authorize_token()
        self._session = self.authorizing_flow.authorize_session()
