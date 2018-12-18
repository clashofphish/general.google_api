"""File to serve as the base classes for implementing file handling base services 
for Google OAuth2 authorization credentials."""
from google.oauth2.credentials import Credentials
from datetime import datetime

import os
import sys
base_path = os.path.abspath(os.path.join('..'))
if base_path not in sys.path:
    sys.path.append(base_path)

# Custom imports
from services.fileHandling_Service import FileHandling


class LocalCredHandling:
    """Use to control credentials from Google API project credential file.
    For use with credential file that is saved to disk locally.

    :param load_save: obj: file handling object; assumes
                            'read_json' & 'write_json' methods
    :param filename: str: file name & loc for credentials from google cloud project

    Internally determined
        :param credentials_dict: json/dict: dictionary from credentials json file
    """
    def __init__(
            self,
            load_save: FileHandling,
            filename=None
    ):
        self.load_save = load_save
        self.filename = filename
        # Internally determined parameters
        self.credentials_dict = None

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
    def credentials_dict(self):
        return self._credentials_dict

    @credentials_dict.setter
    def credentials_dict(self, new):
        self._credentials_dict = new

    def load_creds(self):
        """Load the credentials from saved file."""
        self.credentials_dict = self.load_save.read_json(filename=self.filename)
        return self.credentials_dict

    def save_creds(self):
        """Save the credentials to a json file."""
        self.load_save.write_json(
            filename=self.filename,
            json_obj=self.credentials_dict
        )


class ClientSecretsGoogleHandling:
    """Load and save for the client secrets part of credentials.

    :param file_service: obj: class for handling how credentials are loaded and saved;
                    assumes - 'load_creds', 'save_creds' methods
    :param filename: str: location and name of location storing client secrets
    """
    def __init__(
            self,
            file_service: LocalCredHandling,
            filename
    ):
        self.file_service = file_service
        self.filename = filename
        self.client_id = None
        self.project_id = None
        self.auth_uri = None
        self.client_secret = None
        self.token_uri = None
        self.redirect_uris = None

    @property
    def file_service(self):
        return self._file_service

    @file_service.setter
    def file_service(self, new):
        self._file_service = new

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, new):
        self._filename = new

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, new):
        self._client_id = new

    @property
    def project_id(self):
        return self._project_id

    @project_id.setter
    def project_id(self, new):
        self._project_id = new

    @property
    def auth_uri(self):
        return self._auth_uri

    @auth_uri.setter
    def auth_uri(self, new):
        self._auth_uri = new

    @property
    def client_secret(self):
        return self._client_secret

    @client_secret.setter
    def client_secret(self, new):
        self._client_secret = new

    @property
    def token_uri(self):
        return self._token_uri

    @token_uri.setter
    def token_uri(self, new):
        self._token_uri = new

        if self._token_uri is not None:
            self._refresh_uri = self._token_uri

    @property
    def redirect_uris(self):
        return self._redirect_uris

    @redirect_uris.setter
    def redirect_uris(self, new):
        self._redirect_uris = new
        # Google adds "localhost" to redirect_uri - accounting for that
        if self._redirect_uris is not None:
            self._redirect = self._redirect_uris[0]

    # Internally determined parameters
    @property
    def refresh_uri(self):
        return self._refresh_uri

    @property
    def redirect(self):
        return self._redirect

    def create_json_save(self):
        """Create dictionary from client secret parameters and save as json."""
        secrets_dict = {
            'installed': {
                'client_id': self.client_id,
                'project_id': self.project_id,
                'auth_uri': self.auth_uri,
                'token_uri': self.token_uri,
                'client_secret': self.client_secret,
                'redirect_uris': self._redirect_uris
            }
        }

        self.file_service.filename = self.filename
        self.file_service.credentials_dict = secrets_dict
        self.file_service.save_creds()

    def load_json_create(self):
        """Load client secrets from json file and set parameters."""
        self.file_service.filename = self.filename
        secrets_dict = self.file_service.load_creds()

        self.client_id = secrets_dict['installed']['client_id']
        self.project_id = secrets_dict['installed']['project_id']
        self.auth_uri = secrets_dict['installed']['auth_uri']
        self.token_uri = secrets_dict['installed']['token_uri']
        self.client_secret = secrets_dict['installed']['client_secret']
        self.redirect_uris = secrets_dict['installed']['redirect_uris']


class AuthTokenFileHandling:
    """Load and save for the authentication token part of credentials.

    :param file_service: obj: class for handling how credentials are loaded and saved;
                    assumes - 'load_creds', 'save_creds' methods
    :param filename: str: location and name of location storing token
    :param scope: list(str): list of scope URIs
    """
    def __init__(
            self,
            file_service: LocalCredHandling,
            filename,
            scope
    ):
        self.file_service = file_service
        self.filename = filename
        self.scope = scope
        self.access_token = None
        self.expires_in = 3600
        self.refresh_token = None
        self.token_type = 'Bearer'
        self.id_token = None
        self.expires_at = None
        self.valid = None

    @property
    def file_service(self):
        return self._file_service

    @file_service.setter
    def file_service(self, new):
        self._file_service = new

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, new):
        self._filename = new

    @property
    def scope(self):
        return self._scope

    @scope.setter
    def scope(self, new):
        self._scope = new

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, new):
        self._access_token = new

    @property
    def expires_in(self):
        return self._expires_in

    @expires_in.setter
    def expires_in(self, new):
        self._expires_in = new

    @property
    def refresh_token(self):
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, new):
        self._refresh_token = new

    @property
    def token_type(self):
        return self._token_type

    @token_type.setter
    def token_type(self, new):
        self._token_type = new

    @property
    def id_token(self):
        return self._id_token

    @id_token.setter
    def id_token(self, new):
        self._id_token = new

    @property
    def expires_at(self):
        return self._expires_at

    @expires_at.setter
    def expires_at(self, new):
        self._expires_at = new

    @property
    def valid(self):
        return self._valid

    @valid.setter
    def valid(self, new):
        self._valid = new

    def create_json_save(self):
        """Create dictionary from token parameters and save as json."""
        token_dict = {
            'access_token': self.access_token,
            'expires_in': self.expires_in,
            'refresh_token': self.refresh_token,
            'scope': self.scope,
            'toke_type': self.token_type,
            'id_token': self.id_token,
            'expires_at': str(self.expires_at.timestamp())
        }

        if self.valid:
            token_dict['valid'] = self.valid

        self.file_service.filename = self.filename
        self.file_service.credentials_dict = token_dict
        self.file_service.save_creds()

    def load_json_create(self):
        """Load token from json file and set parameters."""
        self.file_service.filename = self.filename
        token_dict = self.file_service.load_creds()

        self.access_token = token_dict['access_token']
        self.expires_in = token_dict['expires_in']
        self.refresh_token = token_dict['refresh_token']
        self.scope = token_dict['scope']
        self.token_type = token_dict['toke_type']
        self.id_token = token_dict['id_token']
        self.expires_at = datetime.fromtimestamp(float(token_dict['expires_at']))

        if 'valid' in token_dict:
            self.valid = token_dict['valid']
