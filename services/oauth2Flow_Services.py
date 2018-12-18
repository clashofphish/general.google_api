"""File to serve as the base classes for implementing Google OAuth2 through the
google_auth_oauthlib.flow Flow object."""
from google_auth_oauthlib.flow import Flow

import os
import sys
base_path = os.path.abspath(os.path.join('..'))
if base_path not in sys.path:
    sys.path.append(base_path)


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
