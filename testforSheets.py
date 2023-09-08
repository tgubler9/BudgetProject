import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



def test_credentials(credentials):
    try:
        service = build("sheets", "v4", credentials=credentials)
        about = service.about().get().execute()

        # If the request is successful, it means the credentials are valid
        print("Credentials are valid and authenticated!")
        print(f"User: {about['user']['displayName']}")
        print(f"Email: {about['user']['emailAddress']}")
    except HttpError as e:
        print(f"Error occurred: {e}")
        print("Credentials are incorrect or missing necessary permissions.")

# Replace with your actual credentials
credentials = Credentials.from_authorized_user_file("token.json", SCOPES)

# Call the function to test the credentials
test_credentials(credentials)