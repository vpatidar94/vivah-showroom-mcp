import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheetClient:
    def __init__(self, credentials_file: str = 'credentials.json'):
        self._credentials_file = credentials_file
        self._client = self._authenticate()

    def _authenticate(self):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(self._credentials_file, scope)
        return gspread.authorize(creds)

    def get_client(self):
        return self._client
