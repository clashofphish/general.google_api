"""File to serve as base classes for making HTTP requests through the Requests
library"""


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
