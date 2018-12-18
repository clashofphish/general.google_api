from google_auth_oauthlib.flow import Flow

import os
import sys
base_path = os.path.abspath(os.path.join('..'))
if base_path not in sys.path:
    sys.path.append(base_path)


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


class GoogleCredentialHandling:
    """Use to interface google.oauth.credentials with token and client secrets json.
    """
    def __init__(
            self,
            client_handling: ClientSecretsGoogleHandling,
            token_handling: AuthTokenFileHandling,
            credentials: Credentials = None
    ):
        self.client_handling = client_handling
        self.token_handling = token_handling
        self.credentials = credentials

    def initialize_saved_creds(self):
        """Initialize credentials using saved credentials."""
        self.client_handling.load_dict_create()
        self.token_handling.load_dict_create()

        self.credentials = Credentials(
            token=self.token_handling.access_token,
            refresh_token=self.token_handling.refresh_token,
            id_token=self.token_handling.id_token,
            token_uri=self.token_handling.refresh_token,
            client_id=self.client_handling.client_id,
            client_secret=self.client_handling.client_secret,
            scopes=self.token_handling.scope
        )

        self.credentials.expiry = self.token_handling.expires_at

    def save_updated_creds(self):
        """Save the credentials from the credential object."""
        # Client secret creds update
        self.client_handling.client_id = self.credentials.client_id
        self.client_handling.client_secret = self.credentials.client_secret
        self.client_handling.token_uri = self.credentials.token_uri

        # Token creds update
        self.token_handling.expires_at = self.credentials.expiry
        self.token_handling.id_token = self.credentials.id
        self.token_handling.refresh_token = self.credentials.refresh_token
        self.token_handling.scope = self.credentials.scopes
        self.token_handling.access_token = self.credentials.token
        self.token_handling.valid = self.credentials.valid

        # Save credentials
        self.client_handling.create_dict_save()
        self.token_handling.create_dict_save()