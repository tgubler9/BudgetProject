import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1L4yjLKLaMQQokcvFhDzepPWEyGQhhnxnpq7VgPZB0bc"

credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
service = build("sheets", "v4", credentials=credentials)
sheets = service.spreadsheets()

result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="Sheet1!A1:A38").execute()
