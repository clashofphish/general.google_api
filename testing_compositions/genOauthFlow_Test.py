import os
import sys
base_path = os.path.abspath(os.path.join('..'))
if base_path not in sys.path:
    sys.path.append(base_path)

# Custom imports
from services.fileHandling_Service import FileHandling
from services.oauth2Flow_Services import ManualAuthFlow
from services.oauth2FileHandling_Services \
    import LocalCredHandling, ClientSecretsGoogleHandling, AuthTokenFileHandling
from procedures.oauth2Flow_Procedures import FlowCredentialFile, Oauth2UsingFlow
from services.authorizeSession_Service import RequestSession
from services.requestsHTTP_Services import SessionRequests

# Scopes and file names for testing
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/userinfo.profile'
]
# Define credentials file
CREDS_FILE = 'client_secret.json'
CREDS_LOC = os.path.join(base_path, CREDS_FILE)
# Define token file
TOKEN_FILE = 'token.json'
TOKEN_LOC = os.path.join(base_path, TOKEN_FILE)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = ''
SAMPLE_RANGE_NAME = ''


def manual_auth():
    # Init classes
    file_handling = FileHandling()
    auth_meth = ManualAuthFlow()

    local_cred = LocalCredHandling(load_save=file_handling)
    secrets = ClientSecretsGoogleHandling(
        file_service=local_cred,
        filename=CREDS_LOC
    )
    token = AuthTokenFileHandling(
        file_service=local_cred,
        filename=TOKEN_LOC,
        scope=SCOPES
    )

    cred_files = FlowCredentialFile(
        client_handling=secrets,
        token_handling=token
    )
    oauth = Oauth2UsingFlow(creds_service=cred_files, auth_service=auth_meth)

    session = RequestSession(authorizing_oauth=oauth)
    reqs = SessionRequests()

    # Authorize session
    session.authorize_session()

    # Test request
    reqs.session = session.session
    reqs.fetch_test()


# def refresh_auth():
#     # Init classes
#     file_handling = FileHandling()
#     auth_meth = RefreshAuthFlow(load_save=file_handling, filename=TOKEN_LOC)
#     creds = GoogleCredHandling(
#         load_save=file_handling,
#         filename=CREDS_LOC,
#         scopes=SCOPES
#     )
#
#     oauth = Oauth2UsingFlow(handle_creds=creds, handle_token=auth_meth)
#     session = RequestSession(authorizing_flow=oauth)
#     reqs = SessionRequests()
#
#     # Authorize session
#     session.authorize_session()
#
#     # Test request
#     reqs.session = session.session
#     reqs.fetch_test()


if __name__ == '__main__':
    manual_auth()
