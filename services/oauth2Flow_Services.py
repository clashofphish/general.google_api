"""File to serve as the base classes for implementing Google OAuth2 through the
google_auth_oauthlib.flow Flow object."""
from google_auth_oauthlib.flow import Flow

import os
import sys
base_path = os.path.abspath(os.path.join('..'))
if base_path not in sys.path:
    sys.path.append(base_path)

# Custom imports
from services.fileHandling_Service import FileHandling


class GoogleCredHandling:
    """Use to control credentials from Google API project credential file.

    :param load_save: obj: file handling object; assumes
                            'read_json' & 'write_json' methods
    :param filename: str: file name & loc for credentials from google cloud project
    :param scopes: list[str]: list of Google scope strings

    Internally determined
        :param credentials: dict: dictionary from credentials json file
        :param redirect_uri: str: uri location for redirect_uri in flow init
    """
    def __init__(
            self,
            load_save: FileHandling,
            filename,
            scopes
    ):
        self.load_save = load_save
        self.filename = filename
        self.scopes = scopes
        # Internally determined parameters
        self.credentials = None

    @property
    def load_save(self):
        return self._load_save

    @load_save.setter
    def load_save(self, new):
        self._load_save = new

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, new):
        self._filename = new

    @property
    def scopes(self):
        return self._scopes

    @scopes.setter
    def scopes(self, new):
        self._scopes = new

    # Internally determined parameters
    @property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, new):
        self._credentials = new

        if self._credentials is not None:
            self._redirect_uri = self._credentials['installed']['redirect_uris'][0]

    @property
    def redirect_uri(self):
        return self._redirect_uri

    def load_creds(self):
        """Load the credentials from saved file."""
        self.credentials = self.load_save.read_json(filename=self.filename)


class ManualAuthFlow:
    """Use flow object to manually to create an authorization token.

    :param load_save: obj: file handling object with
                            'read_json' & 'write_json methods
    :param filename: str: file location and name as single string for token file

    Internally determined:
        :param token: json obj: created authorization token
    """
    def __init__(
            self,
            load_save: FileHandling,
            filename
    ):
        self.load_save = load_save
        self.filename = filename
        # Internally determined parameters
        self._token = None

    @property
    def load_save(self):
        return self._load_save

    @load_save.setter
    def load_save(self, new):
        self._load_save = new

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, new):
        self._filename = new

    # Internally determined parameters
    @property
    def token(self):
        return self._token

    def load_token(self, flow, creds=None):
        """Manual generation of authorization token.
        Note:
            Outputs authorization URL to command line.
            Requires input of authorization code from web page.

        :param flow: google_auth_oauthlib.flow: initialized object
        :return flow: google_auth_oauthlib.flow: authorization token fetched
        """
        auth_url, _ = flow.authorization_url(prompt='consent')
        print('Please go to this URL: {}'.format(auth_url))

        code = input('Enter the authorization code:')
        self._token = flow.fetch_token(code=code)

        return flow

    def save_token(self):
        """Save the token to file."""
        self.load_save.write_json(filename=self.filename, json_obj=self._token)


class RefreshAuthFlow:
    """Use flow object to load a previously saved token and use a flow object to
    refresh the token.

    :param load_save: obj: file handling object; assumes
                            'read_json' & 'write_json' methods
    :param filename: str: file location and name as single string for token file

    Internally determined:
        :param token: json obj: created authorization token
    """
    def __init__(
            self,
            load_save: FileHandling,
            filename
    ):
        self.load_save = load_save
        self.filename = filename
        # Internally determined parameters
        self.token = None

    @property
    def load_save(self):
        return self._load_save

    @load_save.setter
    def load_save(self, new):
        self._load_save = new

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, new):
        self._filename = new

    # Internally determined parameters
    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, new):
        self._token = new

        if self._token is not None:
            self._refresh_token = self._token['refresh_token']

    def load_token(self, flow, creds):
        """Load token from file and refresh it.

        :param flow: google_auth_oauthlib.flow: initialized object
        :param creds: dict: credentials dictionary
        :return flow: google_auth_oauthlib.flow: authorization token fetched
        """
        self.token = self.load_save.read_json(filename=self.filename)

        client_details = {
            'client_id': creds['installed']['client_id'],
            'client_secrets': creds['installed']['client_secret']
        }
        refresh_uri = creds['installed']['token_uri']

        # Sets the token parameter to the updated token.
        self.token = flow.oauth2session.refresh_token(
            token_url=refresh_uri,
            refresh_token=self._refresh_token,
            **client_details
        )
        # Tempory: test whether calling fetch_token after calling refresh_token works
        flow.fetch_token()

        return flow

    def save_token(self):
        """Save the token to file."""
        self.load_save.write_json(filename=self.filename, json_obj=self._token)


class Oauth2UsingFlow:
    """Initialize a flow object for Google Oauth2 verification.

    :param handle_creds: obj: object for handling the operation of credentials;
                                assumes ''
    :param handle_token: obj: object for handling the operation of authorizing a
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
            handle_creds: GoogleCredHandling,
            handle_token: [ManualAuthFlow, RefreshAuthFlow]
    ):
        self.handle_creds = handle_creds
        self.handle_token = handle_token
        # Internally determined parameters
        self._flow = None
        self._session = None

    @property
    def handle_creds(self):
        return self._handle_creds

    @handle_creds.setter
    def handle_creds(self, new):
        self._handle_creds = new

    @property
    def handle_token(self):
        return self._handle_token

    @handle_token.setter
    def handle_token(self, new):
        self._handle_token = new

    # Internally determined parameters
    @property
    def flow(self):
        return self._flow

    @property
    def session(self):
        return self._session

    def initialize_flow(self):
        """Initialize the flow object."""
        self.handle_creds.load_creds()

        self._flow = Flow.from_client_secrets_file(
            client_secrets_file=self.handle_creds.filename,
            scopes=self.handle_creds.scopes,
            redirect_uri=self.handle_creds.redirect_uri
        )

    def authorize_token(self):
        """Authorize the token using the flow object & save authorized token."""
        self._flow = self.handle_token.load_token(
            flow=self._flow,
            creds=self.handle_creds.credentials
        )
        self.handle_token.save_token()

    def authorize_session(self):
        """Authorize a requests session using the flow object.

        :return session: google.auth.transport.requests.AuthorizedSession:
                    authorized session for pulling data from Google API
        """
        self._session = self._flow.authorized_session()

        return self._session
