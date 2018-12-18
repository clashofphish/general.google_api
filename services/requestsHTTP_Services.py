"""File to serve as base classes for making HTTP requests through the Requests
library"""
from google.auth.transport.requests import AuthorizedSession

import os
import sys
base_path = os.path.abspath(os.path.join('.'))
if base_path not in sys.path:
    sys.path.append(base_path)

# Custom imports
from services.gsheetsAPI_Services import GSheetsFormatRequests


class SessionRequests:
    """Class for holding request actions to interact with API.

    :param session: obj: session object for making requests
    """
    def __init__(
            self,
            session=None
    ):
        self.session = session

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, new):
        self._session = new

    def fetch_test(self):
        print(self.session.get('https://www.googleapis.com/userinfo/v2/me').json())
